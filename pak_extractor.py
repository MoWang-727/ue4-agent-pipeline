#!/usr/bin/env python3
"""
UE4 自定义 PAK 格式提取器
Version 11 / PakFile_Version_Fnv64BugFix / zlib 块压缩
"""

import struct, zlib, os, argparse, glob
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

PAK_MAGIC = 0x5A6F12E1

@dataclass
class PakFooter:
    version: int; index_offset: int; index_size: int; index_hash: bytes; encrypted: bool

@dataclass  
class PakEntry:
    filename: str; offset: int; size: int; uncompressed_size: int
    compression_method: int; compressed_blocks: List[Tuple[int, int]]
    hash: bytes; is_encrypted: bool; is_deleted: bool

class PakExtractor:
    def __init__(self, pak_path: str, output_dir: str = "./extracted/"):
        self.pak_path = Path(pak_path); self.output_dir = Path(output_dir)
        self.footer: Optional[PakFooter] = None; self.entries: List[PakEntry] = []
        self._file = None

    def open(self): self._file = open(self.pak_path, 'rb'); return self
    def close(self):
        if self._file: self._file.close()
    def __enter__(self): return self.open()
    def __exit__(self, *a): self.close()

    def parse_footer(self) -> PakFooter:
        self._file.seek(-44, os.SEEK_END); d = self._file.read(44)
        magic = struct.unpack_from('<I', d, 0)[0]
        if magic != PAK_MAGIC: raise ValueError(f"无效 PAK 魔数: 0x{magic:08X}")
        self.footer = PakFooter(
            version=struct.unpack_from('<I', d, 8)[0],
            index_offset=struct.unpack_from('<Q', d, 16)[0],
            index_size=struct.unpack_from('<Q', d, 24)[0],
            index_hash=d[32:52], encrypted=bool(d[4]))
        return self.footer

    def parse_index(self) -> List[PakEntry]:
        if not self.footer: self.parse_footer()
        self._file.seek(self.footer.index_offset); d = self._file.read(self.footer.index_size)
        pos = 0; pos += 4 + struct.unpack_from('<I', d, pos)[0]
        count = struct.unpack_from('<I', d, pos)[0]; pos += 4
        self.entries = []
        for _ in range(count):
            flen = struct.unpack_from('<I', d, pos)[0]; pos += 4
            fname = d[pos:pos+flen].rstrip(b'\x00').decode('utf-8', errors='replace'); pos += flen
            eoff = struct.unpack_from('<Q', d, pos)[0]; pos += 8
            esize = struct.unpack_from('<Q', d, pos)[0]; pos += 8
            usize = struct.unpack_from('<Q', d, pos)[0]; pos += 8
            cmeth = struct.unpack_from('<B', d, pos)[0]; pos += 1; pos += 8
            ehash = d[pos:pos+20]; pos += 20
            blocks = []
            if cmeth: nb = struct.unpack_from('<I', d, pos)[0]; pos += 4
            else: nb = 0
            for _ in range(nb):
                blocks.append((struct.unpack_from('<Q', d, pos)[0], struct.unpack_from('<Q', d, pos+8)[0])); pos += 16
            flags = struct.unpack_from('<B', d, pos)[0]; pos += 1; pos += 4
            self.entries.append(PakEntry(filename=fname, offset=eoff, size=esize, uncompressed_size=usize,
                compression_method=cmeth, compressed_blocks=blocks, hash=ehash,
                is_encrypted=bool(flags&1), is_deleted=bool(flags&2)))
        return self.entries

    def extract_entry(self, entry: PakEntry) -> bytes:
        self._file.seek(entry.offset)
        if entry.compression_method == 0: return self._file.read(entry.size)
        if entry.compressed_blocks:
            out = bytearray()
            for bs, be in entry.compressed_blocks:
                self._file.seek(entry.offset+bs); c = self._file.read(be-bs)
                try: out.extend(zlib.decompress(c))
                except: out.extend(zlib.decompress(c, -15))
            return bytes(out)
        c = self._file.read(entry.size)
        try: return zlib.decompress(c)
        except: return zlib.decompress(c, -15)

    def extract_all(self, verbose: bool = True):
        if not self.entries: self.parse_index()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        stats = {'success':0, 'skipped':0, 'failed':0, 'bytes':0}
        for i, e in enumerate(self.entries):
            if e.is_deleted: stats['skipped']+=1; continue
            try:
                data = self.extract_entry(e); p = self.output_dir/e.filename
                p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
                stats['success']+=1; stats['bytes']+=len(data)
                if verbose and i%50==0: print(f"\r  [{i+1}/{len(self.entries)}]", end='')
            except Exception as ex: stats['failed']+=1
        if verbose: print()
        return stats

def main():
    p = argparse.ArgumentParser(description='UE4 PAK 提取器')
    p.add_argument('input', nargs='+', help='PAK 文件'); p.add_argument('-o','--output', default='./extracted/')
    p.add_argument('-q','--quiet', action='store_true')
    args = p.parse_args()
    files=[]; [files.extend(glob.glob(x)) for x in args.input]
    if not files: files=args.input
    total={'success':0,'skipped':0,'failed':0,'bytes':0}
    for f in files:
        if not os.path.exists(f): print(f"⚠ 不存在: {f}"); continue
        print(f"\n🦐 解析: {f}")
        with PakExtractor(f, args.output) as ex:
            ex.parse_footer(); s=ex.extract_all(verbose=not args.quiet)
            for k in total: total[k]+=s[k]
            if not args.quiet: print(f"  ✅ {s['success']} | ⏭ {s['skipped']} | ❌ {s['failed']}")
    print(f"\n🎉 总计: {total['success']} 文件 / {total['bytes']/1024/1024/1024:.2f}GB")

if __name__=='__main__': main()
