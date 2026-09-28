"""Build a deterministic Prism-compatible .mrpack; no dependency jars are bundled."""
from pathlib import Path
import hashlib, json, zipfile
from validate import ROOT, validate

validate()
lock=json.loads((ROOT/'pack.lock.json').read_text())
index={
    'formatVersion':1, 'game':'minecraft', 'versionId':'0.1.0',
    'name':'Blocklabor', 'summary':'A German programming workshop in Minecraft: quests, handbook and Lua/JavaScript exercises.',
    'dependencies':{'minecraft':lock['minecraft'],'neoforge':lock['neoforge']},
    'files':[{'path':'mods/'+m['file'],'hashes':{'sha1':m['sha1'],'sha512':m['sha512']},'downloads':[m['url']],'fileSize':m['size']} for m in lock['mods']],
}
out=ROOT/'dist';out.mkdir(exist_ok=True)
path=out/'blocklabor-0.1.0.mrpack'
def add(z,name,data):
    info=zipfile.ZipInfo(name,date_time=(2026,9,28,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o100644 << 16
    z.writestr(info,data)
with zipfile.ZipFile(path,'w') as z:
    add(z,'modrinth.index.json',(json.dumps(index,indent=2)+'\n').encode())
    for root,prefix in [(ROOT/'overrides','overrides'),(ROOT/'world-template/Blocklabor','overrides/saves/Blocklabor')]:
        for p in sorted(root.rglob('*')):
            if p.is_file():add(z,prefix+'/'+p.relative_to(root).as_posix(),p.read_bytes())
    add(z,'overrides/BLOCKLABOR-LICENSE.txt',(ROOT/'LICENSE').read_bytes())
sha=hashlib.sha256(path.read_bytes()).hexdigest()
(out/'SHA256SUMS.txt').write_text(f'{sha}  {path.name}\n')
print(f'Created {path.name} ({path.stat().st_size} bytes); SHA256 {sha}')
