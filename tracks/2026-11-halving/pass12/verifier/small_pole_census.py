#!/usr/bin/env python3
"""Two-algorithm verification INPUT for deletion census of prior cubic fixtures.

Fixture coverage ncap in {4,6,8,10,12} only. Does NOT certify catalog completeness,
not the ncap=14,16,18,20,22,24 requested in Task C.
"""
from pathlib import Path
import json
import sys
import networkx as nx
src=Path(__file__).resolve().parents[2]/'scripts'
sys.path.insert(0,str(src))
from mixed_gadget_census import all_bases


def cases():
 for capn,gs in sorted(all_bases().items()):
  for i,G in enumerate(gs):
   for root in sorted(G):
    P=G.copy();P.remove_node(root)
    if not nx.is_connected(P):continue
    assert sum(d==2 for _,d in P.degree())==3
    assert all(d in (2,3) for _,d in P.degree())
    yield capn,i,root,nx.convert_node_labels_to_integers(P,ordering='sorted')

def generate(filename):
 with open(filename,'w') as f:
  for capn,i,root,P in cases():
   edges=sorted(tuple(sorted(e)) for e in P.edges())
   f.write(' '.join(map(str,[capn,i,root,len(P),len(edges),*[z for e in edges for z in e]]))+'\n')

def verify(filename):
 with open(filename,'w') as f:
  for capn,i,root,P in cases():
   lengths=sorted({len(C) for C in nx.simple_cycles(P) if len(C)>=3})
   forbidden=not ({4,8,16,32}&set(lengths))
   f.write(f'ROOT|{capn}|{i}|{root}|{int(forbidden)}|'+','.join(map(str,lengths))+'\n')

def summarize(stream=None):
 from collections import Counter
 d=Counter(); s=Counter()
 if stream is not None:
  for line in Path(stream).read_text().splitlines():
   _,capn,_,_,clean,_=line.split('|')
   n=int(capn)-1;d[n]+=1;s[n]+=int(clean)
 else:
  for capn,_,_,P in cases():
   d[capn-1]+=1
   lengths={len(C) for C in nx.simple_cycles(P) if len(C)>=3}
   if not {4,8,16,32}&lengths:s[capn-1]+=1
 for n in sorted(d):print(f'ORDER {n}: rooted records={d[n]}, clean rooted records={s[n]}')

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--generate');parser.add_argument('--verify');parser.add_argument('--summary',action='store_true');args=parser.parse_args()
 if args.generate:generate(args.generate)
 if args.verify:verify(args.verify)
 if args.summary:summarize(args.verify if args.verify else None)
