#!/usr/bin/env python3
"""UE4 骨骼结构分析器 — SkeletalMesh 命名规律推断"""

import re, json, argparse
from pathlib import Path

KNOWN_CHARS = ['May','Cody','FearBoss','FearFather','FearMother','FearSister','FearBrother',
    'Hakim','Cutie','Rose','Doctor','MoonBaboon','Squirrel','Vacuum','Toolbox','Book','Microphone',
    'AICore','King','Queen','Bull','MechanicalBull','Wasp','Spider','Mole','Snail','Beetle',
    'Dragonfly','Caterpillar']

KNOWN_BONES = ['Root','Pelvis','Spine','Spine1','Spine2','Neck','Head','Jaw',
    'Clavicle_L','Clavicle_R','UpperArm_L','UpperArm_R','LowerArm_L','LowerArm_R',
    'Hand_L','Hand_R','Thigh_L','Thigh_R','Calf_L','Calf_R','Foot_L','Foot_R',
    'Toe_L','Toe_R','Thumb_L','Thumb_R','Index_L','Index_R','Middle_L','Middle_R',
    'Ring_L','Ring_R','Pinky_L','Pinky_R','IK_Foot_L','IK_Foot_R','IK_Hand_L','IK_Hand_R',
    'Weapon','WeaponSocket','Hair','Skirt','Cape','Eye_L','Eye_R','Mouth','Tongue',
    'Breast_L','Breast_R','Eyelid_L','Eyelid_R','Eyebrow_L','Eyebrow_R']

class SkeletonAnalyzer:
    def __init__(self, asset_dir: str):
        self.asset_dir = Path(asset_dir); self.characters = {}

    def _infer_char(self, name: str):
        nl = name.lower().replace('_','').replace(' ','')
        for c in KNOWN_CHARS:
            if c.lower().replace(' ','') in nl: return c
        w = re.findall(r'[A-Z][a-z]+', name); return w[0] if w else None

    def scan(self):
        for f in list(self.asset_dir.rglob('*.uasset')) + list(self.asset_dir.rglob('*.uexp')):
            c = self._infer_char(f.stem)
            if not c: continue
            if c not in self.characters:
                self.characters[c] = {'name':c,'files':[],'has_skel':False,'has_mesh':False,'has_abp':False,'has_phys':False,'variants':set()}
            self.characters[c]['files'].append(str(f.relative_to(self.asset_dir)))
            nl = f.stem.lower()
            if 'skeleton' in nl: self.characters[c]['has_skel'] = True
            elif 'skeletal' in nl or f.stem == c: self.characters[c]['has_mesh'] = True
            elif 'animblueprint' in nl or nl.startswith('abp_'): self.characters[c]['has_abp'] = True
            elif 'physics' in nl: self.characters[c]['has_phys'] = True
        return self.characters

    def analyze(self, character: str):
        if character not in self.characters: self.scan()
        if character not in self.characters: return {'error': f'角色 {character} 未找到'}
        info = self.characters[character]
        skel_file = None
        for f in self.asset_dir.rglob('*.uasset'):
            if 'skeleton' in f.stem.lower() and character.lower() in f.stem.lower():
                skel_file = f; break
        bones = []
        if skel_file:
            try:
                data = skel_file.read_bytes()
                text = data.decode('latin-1', errors='ignore')
                for b in KNOWN_BONES:
                    if b in text: bones.append(b)
            except: pass
        return {'character':character, 'skeleton':str(skel_file.relative_to(self.asset_dir)) if skel_file else None,
            'bone_count':len(bones), 'bones':bones, 'has_skel':info['has_skel'],
            'has_mesh':info['has_mesh'], 'has_abp':info['has_abp'], 'has_phys':info['has_phys'],
            'variants':list(info['variants']), 'file_count':len(info['files'])}

def main():
    p = argparse.ArgumentParser(description='UE4 骨骼分析器')
    p.add_argument('assets'); p.add_argument('-c','--character'); p.add_argument('-r','--report', action='store_true'); p.add_argument('-o','--output')
    args = p.parse_args()
    a = SkeletonAnalyzer(args.assets)
    if args.character:
        print(json.dumps(a.analyze(args.character), indent=2, ensure_ascii=False)); return
    if args.report:
        a.scan()
        lines=["# 骨骼资源分析报告\n",f"扫描: {args.assets} | 角色: {len(a.characters)}\n",
            "| 角色 | 文件 | 骨骼 | 网格 | ABP | 物理 | 完整度 |",
            "|------|------|------|------|-----|------|--------|"]
        for c,i in sorted(a.characters.items()):
            s=sum([i['has_skel'],i['has_mesh'],i['has_abp'],i['has_phys']]); pct=s*25
            lines.append(f"| {c} | {len(i['files'])} | {'✓' if i['has_skel'] else '✗'} | {'✓' if i['has_mesh'] else '✗'} | {'✓' if i['has_abp'] else '✗'} | {'✓' if i['has_phys'] else '✗'} | {'█'*(pct//20)+'░'*(5-pct//20)} {pct}% |")
        r='\n'.join(lines)
        if args.output: Path(args.output).write_text(r,encoding='utf-8'); print(f"✅ {args.output}")
        else: print(r)
        return
    chars=a.scan()
    print(f"\n🦴 {len(chars)} 个角色:\n")
    for n,i in sorted(chars.items()):
        d=[]; [d.append(x) for x,c in [('骨骼',i['has_skel']),('网格',i['has_mesh']),('ABP',i['has_abp'])] if c]
        print(f"  {n:20s} → {len(i['files']):3d} 文件 | {', '.join(d) if d else '无关键资源'}")

if __name__=='__main__': main()
