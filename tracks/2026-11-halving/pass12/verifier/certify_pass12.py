#!/usr/bin/env python3
"""Rebuild every available Pass XII stream and preserve exit codes/checksums.

This certifies *only* computations actually run. It does not claim to run
GENG or to verify the GitHub PR/branch or catalog completeness.
"""
from pathlib import Path
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
records=[]

def sha(path):
 p=Path(path)
 return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

def run(name,cmd,stdout_file=None):
 p=subprocess.run(cmd,cwd=HERE,text=True,capture_output=True)
 if stdout_file is not None:(HERE/stdout_file).write_text(p.stdout)
 records.append({'name':name,'argv':cmd,'exit_code':p.returncode,
                'stderr_excerpt':p.stderr[-800:],'stdout_file':stdout_file,
                'stdout_sha256':sha(HERE/stdout_file) if stdout_file else hashlib.sha256(p.stdout.encode()).hexdigest()})
 if p.returncode!=0:raise RuntimeError(f'{name}: exit {p.returncode}: {p.stderr[-600:]}')
 return p

run('build_graph_input',[sys.executable,'tower_reference.py','--generate','graph_examples.txt','--output','python_stream.txt'])
records[-1]['input_sha256']=sha(HERE/'graph_examples.txt')
run('compile_tower_c',['gcc','-O2','-std=c11','tower_independent.c','-o','tower_independent'])
run('tower_c',['./tower_independent','graph_examples.txt'],'c_stream.txt')
assert (HERE/'python_stream.txt').read_bytes()==(HERE/'c_stream.txt').read_bytes()
records.append({'name':'tower_stream_compare','exit_code':0,
                'python_sha256':sha(HERE/'python_stream.txt'),'c_sha256':sha(HERE/'c_stream.txt')})
run('two_pole_python',[sys.executable,'two_pole_small.py'],'python_2pole_stream.txt')
run('compile_two_pole_c',['gcc','-O2','-std=c11','two_pole_small.c','-o','two_pole_small'])
run('two_pole_c',['./two_pole_small'],'c_2pole_stream.txt')
assert (HERE/'python_2pole_stream.txt').read_bytes()==(HERE/'c_2pole_stream.txt').read_bytes()
records.append({'name':'two_pole_stream_compare','exit_code':0,
                'python_sha256':sha(HERE/'python_2pole_stream.txt'),'c_sha256':sha(HERE/'c_2pole_stream.txt')})
run('small_pole_input_and_python',[sys.executable,'small_pole_census.py','--generate','small_poles_input.txt','--verify','python_small_poles_stream.txt','--summary'],'small_poles_summary.txt')
records[-1]['input_sha256']=sha(HERE/'small_poles_input.txt')
records[-1]['verified_stream_sha256']=sha(HERE/'python_small_poles_stream.txt')
run('compile_small_pole_c',['gcc','-O2','-std=c11','small_pole_independent.c','-o','small_pole_independent'])
run('small_pole_c',['./small_pole_independent','small_poles_input.txt'],'c_small_poles_stream.txt')
assert (HERE/'python_small_poles_stream.txt').read_bytes()==(HERE/'c_small_poles_stream.txt').read_bytes()
records.append({'name':'small_pole_stream_compare','exit_code':0,
                'python_sha256':sha(HERE/'python_small_poles_stream.txt'),'c_sha256':sha(HERE/'c_small_poles_stream.txt')})
run('h15_explicit_isomorphism',[sys.executable,'verify_h15_isomorphism.py'],'h15_isomorphism_stream.txt')

# Existing fixture-suite test run: this runs only tests from the accessible pass XI package.
run('existing_research_suite',[sys.executable,'-m','pytest','-q',str(ROOT/'tracks/2026-11-halving/scripts')],'pass11_pytest_stream.txt')
run('pass12_tests',[sys.executable,'-m','pytest','-q',str(HERE.parent/'test_pass12.py')],'pass12_pytest_stream.txt')

codes={r['name']:r['exit_code'] for r in records}
report={'status':'COMPUTED on accessible local fixtures; requested higher-order geng runs NOT PERFORMED',
        'base':'Pass XI archive, NOT the specified GitHub branch',
        'requested_geng_orders_3pole':[13,15,17,19,21,23],
        'geng_status':'UNRUN (geng unavailable; actual branch/shards unavailable)',
        'requested_geng_orders_2pole':[8,10,12,14,16,18,20,22],
        'two_pole_geng_status':'UNRUN',
        'sources_sha256':{p.name:sha(p) for p in sorted(HERE.glob('*.py'))+sorted(HERE.glob('*.c'))},
        'checks':records}
(HERE/'certification_manifest.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'all_exit_codes_zero':all(x==0 for x in codes.values()),
    'tower_sha256':sha(HERE/'python_stream.txt'),
    'two_pole_sha256':sha(HERE/'python_2pole_stream.txt'),
    'small_pole_sha256':sha(HERE/'python_small_poles_stream.txt'),
    'steps':len(records)},indent=2))
