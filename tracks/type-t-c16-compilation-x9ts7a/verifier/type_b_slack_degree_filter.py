#!/usr/bin/env python3
"""Fast streaming graph6 degree-profile filter.

Reads graph6 lines from stdin, decodes only enough to compute the degree
sequence (no full adjacency-object construction), and writes to stdout only
the lines whose degree multiset matches the target Family II profile:
exactly two vertices of degree 2, one of degree 4, sixteen of degree 3
(n=19). This lets a geng stream be filtered in place without ever storing
the full (huge) intermediate output.
"""

from __future__ import annotations

import sys


def degree_sequence_from_graph6(line: bytes, n: int) -> list:
    # graph6 body starts after the single-byte n descriptor (n<=62 case).
    body = line[1:]
    degrees = [0] * n
    bit_index = 0
    total_bits = n * (n - 1) // 2
    byte_iter = iter(body)
    current_byte = None
    bits_left_in_byte = 0
    value = 0

    i = 1
    j = 0
    for _ in range(total_bits):
        if bits_left_in_byte == 0:
            value = next(byte_iter) - 63
            bits_left_in_byte = 6
        bits_left_in_byte -= 1
        bit = (value >> bits_left_in_byte) & 1
        if bit:
            degrees[i] += 1
            degrees[j] += 1
        j += 1
        if j == i:
            i += 1
            j = 0
    return degrees


def main() -> int:
    n = 19
    target = sorted([2, 2, 4] + [3] * 16)
    matched = 0
    checked = 0
    for raw in sys.stdin.buffer:
        line = raw.rstrip(b"\n")
        if not line:
            continue
        checked += 1
        try:
            degrees = degree_sequence_from_graph6(line, n)
        except StopIteration:
            sys.stderr.write(f"skipping malformed/truncated line at count {checked}\n")
            continue
        if sorted(degrees) == target:
            matched += 1
            sys.stdout.buffer.write(raw if raw.endswith(b"\n") else raw + b"\n")
    sys.stderr.write(f"checked={checked} matched={matched}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
