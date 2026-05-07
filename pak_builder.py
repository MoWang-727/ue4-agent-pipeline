#!/usr/bin/env python3
"""UE4 替换 PAK 构建器 — Version 11 Fnv64BugFix"""

import struct, hashlib, os, argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List

PAK_MAGIC = 0x5A6F12E1

@dataclass
class FileEntry:
    path: str; data: bytes; offset: int=0; size: int=0
    compressed_size: int=0; compression_method: int=0

class PakBuilder:
    def __init__(self, mount_point: str="../../../"):
        self.mount_point = mount_point; self.entries: List[FileEntry] = []

    def add_file(self, path: str, data: bytes):
        e = FileEntry(path=path, data=data, size=len(data), compressed_size=len(data))
        self.entries.append(e)

    def add_directory(self, dir_path: str, base_path: str=""):
        for fp in Path(dir_path).rglob('*'):
            if fp.is_file():
                rp = str(fp.relative_to(dir_path))
                if base_path: rp = f"{base_path}/{rp}"
                self.add_file(rp, fp.read_bytes())

    def _build_index(self) -> bytes:
        idx = bytearray()
        m = self.mount_point.encode('utf-8')+b'\x00'; idx.extend(struct.pack('<I', len(m))); idx.extend(m)
        idx.extend(struct.pack('<I', len(self.entries)))
        for e in self.entries:
            fn = e.path.encode('utf-8')+b'\x00'; idx.extend(struct.pack('<I', len(fn))); idx.extend(fn)
            idx.extend(struct.pack('<Q', e.offset)); idx.extend(struct.pack('<Q', e.compressed_size))
            idx.extend(struct.pack('<Q', e.size)); idx.extend(struct.pack('<B', e.compression_method))
            idx.extend(struct.pack('<Q', int(datetime.now().timestamp())))
            idx.extend(hashlib.sha1(e.data).digest())
            idx.extend(struct.pack('<I', 0)); idx.extend(struct.pack('<B', 0)); idx.extend(struct.pack('<I', 0))
        return bytes(idx)

    def build(self, output_path: str) -> int:
        off = 0
        for e in self.entries: e.offset = off; off += e.compressed_size
        idx = self._build_index(); idx_off = off
        footer = struct.pack('<I', PAK_MAGIC) + struct.pack('<I', 11) + struct.pack('<Q', idx_off) + struct.pack('<Q', len(idx)) + hashlib.sha1(idx).digest()
        with open(output_path, 'wb') as f:
            for e in self.entries: f.write(e.data)
            f.write(idx); f.write(footer)
        return off + len(idx) + len(footer)

def main():
    p = argparse.ArgumentParser(description='UE4 PAK 构建器')
    p.add_argument('input'); p.add_argument('-o','--output', default='output.pak'); p.add_argument('--mount', default='../../../')
    args = p.parse_args()
    b = PakBuilder(mount_point=args.mount)
    ip = Path(args.input)
    if not ip.exists(): print(f"❌ 目录不存在: {args.input}"); return 1
    b.add_directory(args.input)
    print(f"📁 {len(b.entries)} 个文件")
    sz = b.build(args.output)
    print(f"✅ {args.output} | 💾 {sz/1024/1024:.1f}MB")
    with open(args.output,'rb') as f:
        f.seek(-4,2); magic=struct.unpack('<I',f.read(4))[0]
        print(f"🔐 魔数: {'✓' if magic==PAK_MAGIC else '✗'} 0x{magic:08X}")

if __name__=='__main__': main()
