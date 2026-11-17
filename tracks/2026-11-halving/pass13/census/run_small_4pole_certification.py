#!/usr/bin/env python3
"""Reproduce two independent n=6 clean four-pole enumerations; log exit codes and SHA256."""
import hashlib, json, pathlib, subprocess, sys, platform
p=pathlib.Path(__file__).resolve().parent
csrc=p/'four_poles_masks.c'
binary=p/'four_poles_masks'
compiled=subprocess.run(['cc','-O2','-Wall','-Wextra','-o',str(binary),str(csrc)],capture_output=True,text=True)
if compiled.returncode:
    print(compiled.stderr, file=sys.stderr)
    sys.exit(compiled.returncode)
commands=[('python_atlas',[sys.executable,str(p/'four_poles_atlas.py')]),('c_masks',[str(binary)])]
manifest={'scope':'All simple connected six-vertex graphs with four degree-2 vertices, two degree-3 vertices, and no power-of-two cycle',
 'python_version':platform.python_version(), 'commands':{},
 'checker_source_sha256': {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [p/'four_poles_atlas.py',csrc]},
 'compile_command':'cc -O2 -Wall -Wextra -o four_poles_masks four_poles_masks.c',
 'compile_exit_code':compiled.returncode}
for name,cmd in commands:
    r=subprocess.run(cmd,capture_output=True)
    (p/(name+'.tsv')).write_bytes(r.stdout)
    manifest['commands'][name]={'argv':cmd,'exit_code':r.returncode,'sha256':hashlib.sha256(r.stdout).hexdigest(),'stream_bytes':len(r.stdout),'stderr':r.stderr.decode('utf8',errors='replace')[:1000]}
if any(v['exit_code']!=0 for v in manifest['commands'].values()):
    manifest['checks_agree']=False
    (p/'four_pole_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');sys.exit(2)
manifest['checks_agree']=(p/'python_atlas.tsv').read_bytes()==(p/'c_masks.tsv').read_bytes()
manifest['certified_classes']=2 if manifest['checks_agree'] else None
manifest['total_labeled_graphs']=450 if manifest['checks_agree'] else None
(p/'four_pole_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('classes',manifest['certified_classes'],'labeled',manifest['total_labeled_graphs'],'same_stream',manifest['checks_agree'])
print('python_sha256',manifest['commands']['python_atlas']['sha256'])
print('c_sha256',manifest['commands']['c_masks']['sha256'])
sys.exit(0 if manifest['checks_agree'] else 1)
