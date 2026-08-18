#!/usr/bin/env bash
# Restart-resilient sharded geng runner: NSHARDS small shards, run WAVE_SIZE
# at a time, skipping shards whose output already exists (nonempty .done
# marker) so a mid-run restart only costs the currently-active wave.
set -u
N=$1; MINE=$2; MAXE=$3; NSHARDS=$4; WAVE=$5; OUTDIR=$6; shift 6
EXTRA_ARGS="$@"
mkdir -p "$OUTDIR"
i=0
while [ $i -lt $NSHARDS ]; do
  batch=()
  for ((j=0; j<WAVE && i<NSHARDS; j++, i++)); do
    if [ -f "$OUTDIR/shard${i}.done" ]; then continue; fi
    (
      nauty-geng -c -C -d3 -D3 $N $MINE:$MAXE ${i}/$NSHARDS $EXTRA_ARGS \
        > "$OUTDIR/shard${i}.g6" 2> "$OUTDIR/shard${i}.err" \
        && touch "$OUTDIR/shard${i}.done"
    ) &
    batch+=($!)
  done
  for pid in "${batch[@]:-}"; do
    [ -n "$pid" ] && wait "$pid"
  done
done
echo "all $NSHARDS shards complete"
