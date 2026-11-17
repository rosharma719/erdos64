#!/usr/bin/env python3
"""Audit supplied pole-census manifests without claiming regenerated geng streams."""
import hashlib, json, pathlib, sys
if len(sys.argv)!=2:
    raise SystemExit('usage: python audit_prior_manifests.py <bundle/repo>')
repo=pathlib.Path(sys.argv[1]); r=repo/'tracks/2026-11-halving'
manifests=sorted((r/'census').glob('*.json'))
a=(r/'scripts/cycle_check.c').read_bytes(); b=(repo/'verifier/check_power_masks.c').read_bytes()
flags={"manifest_count":len(manifests),"counts_reconcile":True,"source_checksums_match":True,
       "both_checker_exits_recorded":True,"geng_version_recorded":True,"failures":[]}
for p in manifests:
    j=json.loads(p.read_text()); name=p.name
    if not (j['result']=='PASS' and j['geng_exit']==j['tee_exit']==j['checker_A_exit']==0 and j['raw_count']==j['checker_A_count']==j['checker_B_count'] and j['clean_A']==j['clean_B'] and j['degree2_vertices']==3*j['n']-2*j['e']):
        flags['counts_reconcile']=False;flags['failures'].append(name+':counts')
    if j['checker_A_sha256']!=hashlib.sha256(a).hexdigest() or j['checker_B_sha256']!=hashlib.sha256(b).hexdigest():
        flags['source_checksums_match']=False;flags['failures'].append(name+':sources')
    if 'checker_B_exit' not in j:
        flags['both_checker_exits_recorded']=False
    if 'Usage:' in j.get('nauty_geng',''):
        flags['geng_version_recorded']=False
print(json.dumps(flags,indent=2))
# Exit 1 reflects missing strict certification fields, while counts can still reconcile.
sys.exit(0 if all(flags[k] for k in ['counts_reconcile','source_checksums_match','both_checker_exits_recorded','geng_version_recorded']) else 1)
