#!/bin/bash
# certify_shard.sh N M D RES MOD OUTDIR LABEL
# One certified shard: geng -c -f -d3 -D<D> N M:M RES/MOD | check_c8.
# geng options + fixed edge count pin the degree sequence (excess identity), so
# no separate degree filter is needed; c4_seen must stay 0 (geng -f sanity).
# Captures both pipe exit codes, raw/checked counts, stream checksum, survivors,
# and writes a JSON manifest entry. Streaming (no large temp file).
set -u
N=$1; M=$2; D=$3; RES=$4; MOD=$5; OUTDIR=$6; LABEL=$7
REPO=/Users/rohansharma/Desktop/Code/erdos64
CHK="$REPO/verifier/check_c8"
mkdir -p "$OUTDIR"
STEM="$OUTDIR/${LABEL}_n${N}m${M}_${RES}of${MOD}"
GENGV=$(geng -h 2>&1 | head -1 | tr -d '\r')
CHKSHA=$(shasum -a 256 "$REPO/verifier/check_c8.c" | awk '{print $1}')
CMD="geng -c -f -d3 -D${D} ${N} ${M}:${M} ${RES}/${MOD}"
START=$(date -u +%FT%TZ)
set -o pipefail
$CMD 2>"$STEM.geng.err" \
  | tee >(shasum -a 256 | awk '{print $1}' > "$STEM.sha") \
  | "$CHK" > "$STEM.surv" 2>"$STEM.chk.err"
PS=("${PIPESTATUS[@]}")
wait
END=$(date -u +%FT%TZ)
GENG_EXIT=${PS[0]}; CHK_EXIT=${PS[2]}
RAW=$(sed -nE 's/.*>Z[[:space:]]+([0-9]+).*/\1/p' "$STEM.geng.err" | head -1)
CHECKED=$(sed -nE 's/.*checked ([0-9]+) graphs.*/\1/p' "$STEM.chk.err")
C4=$(sed -nE 's/.*c4_seen=([0-9]+).*/\1/p' "$STEM.chk.err")
SURV=$(sed -nE 's/.*c8free_survivors=([0-9]+).*/\1/p' "$STEM.chk.err")
STREAMSHA=$(cat "$STEM.sha" 2>/dev/null)
RECON="FAIL"; [ -n "${RAW:-}" ] && [ "${RAW:-}" = "${CHECKED:-}" ] && RECON="OK"
cat > "$STEM.json" <<JSON
{
  "label":"$LABEL","n":$N,"m":$M,"maxdeg":$D,"res":$RES,"mod":$MOD,
  "command":"$CMD","nauty_geng":"$GENGV","checker":"check_c8.c","checker_src_sha256":"$CHKSHA",
  "start":"$START","end":"$END","geng_exit":${GENG_EXIT},"check_exit":${CHK_EXIT},
  "raw_count":${RAW:-null},"checked_count":${CHECKED:-null},"c4_seen":${C4:-null},
  "c8free_survivors":${SURV:-null},"reconcile":"$RECON","stream_sha256":"$STREAMSHA"
}
JSON
echo "[shard $RES/$MOD] geng_exit=$GENG_EXIT check_exit=$CHK_EXIT raw=$RAW checked=$CHECKED c4_seen=$C4 survivors=$SURV reconcile=$RECON sha=${STREAMSHA:0:12}"
# non-zero script exit if anything is off, so the caller can gate
[ "$GENG_EXIT" = 0 ] && [ "$CHK_EXIT" = 0 ] && [ "$RECON" = OK ] && [ "${C4:-1}" = 0 ]
