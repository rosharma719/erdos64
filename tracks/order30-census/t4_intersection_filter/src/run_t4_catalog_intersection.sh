#!/usr/bin/env bash
# Exact resumable t=4 quotient census using the specialized high-throughput filter.
# Usage: run_t4_catalog_intersection.sh INPUT.g6 OUTDIR [CHUNK_LINES=100000] [JOBS=4]
set -euo pipefail
INPUT=${1:?input graph6 catalog}; OUT=${2:?output directory}; CHUNK=${3:-100000}; JOBS=${4:-4}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
FILTER=${T4_FILTER:-$ROOT/bin/t4_intersection_filter}
[[ -x "$FILTER" ]] || { echo "missing executable: $FILTER" >&2; exit 2; }
mkdir -p "$OUT/chunks" "$OUT/results" "$OUT/logs" "$OUT/candidates"
sha256sum "$INPUT" > "$OUT/input.sha256"
wc -l < "$INPUT" > "$OUT/input.lines"
if ! compgen -G "$OUT/chunks/chunk_*" >/dev/null; then split -l "$CHUNK" -d -a 4 "$INPUT" "$OUT/chunks/chunk_"; fi
run_one(){
  local f=$1
  local id=${f##*_}
  local j="$OUT/results/$id.json" l="$OUT/logs/$id.log" t="$OUT/logs/$id.time" d="$OUT/candidates/$id"
  [[ -s "$j" ]] && return 0
  mkdir -p "$d"; sha256sum "$f" > "$OUT/chunks/$id.sha256"
  /usr/bin/time -f '{"wall_seconds":%e,"user_seconds":%U,"sys_seconds":%S,"max_rss_kb":%M}' -o "$t" \
    "$FILTER" --outdir "$d" < "$f" > "$j.tmp" 2> "$l"
  mv "$j.tmp" "$j"
}
export -f run_one; export OUT FILTER
find "$OUT/chunks" -maxdepth 1 -type f -name 'chunk_[0-9][0-9][0-9][0-9]' -print0 | sort -z | xargs -0 -n1 -P "$JOBS" bash -c 'run_one "$0"'
python3 - "$OUT" "$FILTER" "$CHUNK" "$JOBS" <<'PY'
import glob,hashlib,json,os,sys,time
out,flt,chunk,jobs=sys.argv[1:]
rows=[]
for p in sorted(glob.glob(out+'/results/*.json')):
    with open(p) as f: rows.append((os.path.basename(p),json.load(f)))
keys=['lines','parsed','cubic22','connected','initial_markings','candidate_intersection_tests','graphs_with_candidates','final_markings','literal_checked','literal_mismatch','counterexamples','seconds']
agg={k:sum(d.get(k,0) for _,d in rows) for k in keys}
cy={}
for _,d in rows:
    for k,v in d.get('cycles_seen_by_length',{}).items():cy[k]=cy.get(k,0)+v
input_lines=int(open(out+'/input.lines').read())
agg.update({'marks':4,'quotient_order':22,'cycles_seen_by_length':dict(sorted(cy.items(),key=lambda z:int(z[0]))),'chunks_completed':len(rows),'input_path':os.path.abspath(open(out+'/input.sha256').read().strip().split(maxsplit=1)[1]),'input_sha256':open(out+'/input.sha256').read().split()[0],'input_lines':input_lines,'chunk_lines':int(chunk),'parallel_jobs':int(jobs),'filter_path':os.path.abspath(flt),'filter_sha256':hashlib.sha256(open(flt,'rb').read()).hexdigest(),'complete':agg['lines']==input_lines and agg['literal_mismatch']==0,'generated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
with open(out+'/aggregate.json','w') as f:json.dump(agg,f,indent=2,sort_keys=True)
if not agg['complete']: raise SystemExit('incomplete aggregation')
print(json.dumps(agg,indent=2,sort_keys=True))
PY
