#!/usr/bin/env bash
# certify_pole_shard.sh N E RES MOD OUTDIR LABEL
# One certified shard of the clean k-pole census:
#   geng -c -f -d2 -D3 N E:E RES/MOD   (connected, no C4, degrees 2..3, E edges)
# With E edges the degree sum fixes the number of degree-2 vertices: 3N - 2E.
# The stream is checksummed and fed to TWO independent checkers:
#   A = scripts/cycle_check.c          (DFS; reports graphs with no power-of-two cycle <= N)
#   B = verifier/check_power_masks.c   (repo checker; C4/C8/C16 presence masks; valid for N <= 31)
# Optional: GENG_EXTRA="-C" adds extra geng flags (here: biconnected only); recorded in the manifest.
# The shard passes only if geng, tee and BOTH checkers exit 0 (B's status is captured inside its
# process substitution, which PIPESTATUS does not cover), every count reconciles,
# and A and B report the same number of clean graphs.
set -u
if [ "$#" -ne 6 ]; then echo "usage: $0 N E RES MOD OUTDIR LABEL" >&2; exit 2; fi
N=$1; E=$2; RES=$3; MOD=$4; OUTDIR=$5; LABEL=$6
[ "$N" -le 31 ] || { echo "checker B only covers lengths 4, 8, 16: need N <= 31" >&2; exit 2; }
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); REPO=$(cd "$HERE/../../.." && pwd)
BUILD="$REPO/.build"; mkdir -p "$BUILD" "$OUTDIR"
cc -O3 -o "$BUILD/cycle_check" "$HERE/cycle_check.c"
cc -O3 -std=c11 -o "$BUILD/check_power_masks" "$REPO/verifier/check_power_masks.c"
STEM="$OUTDIR/${LABEL}_n${N}e${E}_${RES}of${MOD}"
sha() { sha256sum "$@" | awk '{print $1}'; }
GENGV=$(geng --version 2>&1 | head -1 | tr -d '\r')
GENG_BIN=$(command -v geng); GENG_SHA=$(sha "$GENG_BIN")
CMD=(geng -c ${GENG_EXTRA:-} -f -d2 -D3 "$N" "${E}:${E}" "${RES}/${MOD}")
START=$(date -u +%FT%TZ)
set -o pipefail
"${CMD[@]}" 2>"$STEM.geng.err" \
  | tee >(sha > "$STEM.sha") \
        >("$BUILD/check_power_masks" 2>"$STEM.B.err" | awk '$1==0{z++} END{print z+0}' > "$STEM.B.clean"; echo "${PIPESTATUS[0]}" > "$STEM.B.exit") \
  | "$BUILD/cycle_check" > "$STEM.A.out" 2> "$STEM.A.clean.g6"
PS=("${PIPESTATUS[@]}")
# process substitutions are not covered by PIPESTATUS: wait for their own records
for _ in $(seq 1 600); do [ -s "$STEM.B.exit" ] && [ -s "$STEM.sha" ] && break; sleep 1; done; wait
END=$(date -u +%FT%TZ)
GENG_EXIT=${PS[0]}; TEE_EXIT=${PS[1]}; A_EXIT=${PS[2]}
RAW=$(sed -nE 's/.*>Z[[:space:]]+([0-9]+).*/\1/p' "$STEM.geng.err" | head -1)
A_TOTAL=$(sed -nE 's/.*total=([0-9]+).*/\1/p' "$STEM.A.out")
A_CLEAN=$(sed -nE 's/.*powerfree=([0-9]+).*/\1/p' "$STEM.A.out")
A_C4=$(( ${A_TOTAL:-0} - $(sed -nE 's/.*C4free=([0-9]+).*/\1/p' "$STEM.A.out") ))
B_TOTAL=$(sed -nE 's/.*checked ([0-9]+).*/\1/p' "$STEM.B.err")
B_CLEAN=$(cat "$STEM.B.clean")
A_LINES=$(wc -l < "$STEM.A.clean.g6")
B_EXIT=$(cat "$STEM.B.exit" 2>/dev/null)
OK=PASS
for c in "$GENG_EXIT" "$TEE_EXIT" "$A_EXIT" "$B_EXIT"; do [ "$c" = 0 ] || OK=FAIL; done
[ -n "$RAW" ] && [ "$RAW" = "$A_TOTAL" ] && [ "$RAW" = "$B_TOTAL" ] || OK=FAIL
[ "$A_CLEAN" = "$B_CLEAN" ] && [ "$A_CLEAN" = "$A_LINES" ] && [ "$A_C4" = 0 ] || OK=FAIL
cat > "$STEM.json" <<JSON
{"label":"$LABEL","n":$N,"e":$E,"degree2_vertices":$((3*N-2*E)),"res":$RES,"mod":$MOD,
 "command":"${CMD[*]}","nauty_geng":"$GENGV","geng_binary":"$GENG_BIN","geng_binary_sha256":"$GENG_SHA",
 "checker_A":"cycle_check.c","checker_A_sha256":"$(sha "$HERE/cycle_check.c")",
 "checker_B":"verifier/check_power_masks.c","checker_B_sha256":"$(sha "$REPO/verifier/check_power_masks.c")",
 "start":"$START","end":"$END","geng_exit":$GENG_EXIT,"tee_exit":$TEE_EXIT,"checker_A_exit":$A_EXIT,"checker_B_exit":${B_EXIT:-null},
 "raw_count":${RAW:-null},"checker_A_count":${A_TOTAL:-null},"checker_B_count":${B_TOTAL:-null},
 "c4_seen":$A_C4,"clean_A":${A_CLEAN:-null},"clean_B":${B_CLEAN:-null},
 "stream_sha256":"$(cat "$STEM.sha")","clean_graphs_sha256":"$(sha "$STEM.A.clean.g6")","result":"$OK"}
JSON
echo "[$LABEL N=$N E=$E $RES/$MOD] raw=$RAW A=$A_TOTAL B=$B_TOTAL clean A=$A_CLEAN B=$B_CLEAN geng=$GENG_EXIT A_exit=$A_EXIT B_exit=$B_EXIT -> $OK"
[ "$OK" = PASS ]
