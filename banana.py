#!/usr/bin/env python
# encoding: utf-8
import sys
import random
from wn import *

def main():
  if len(sys.argv) != 3: sys.exit('usage: ./banana.py [word] [N_chain]')
  current_w = sys.argv[1].decode('utf-8')
  for n in range(int(sys.argv[2])):
    words = getWords(current_w)
    if words:
      sense = getSenses(words[0])
      l = getSynLinksRecursive(sense, 'hype', 'jpn')
      l += getSynLinksRecursive(sense, 'hypo', 'jpn')
      l = list(set(l))
      next_w = random.choice([w for w in l if w != current_w])
      print current_w, 'といったら', next_w
      current_w = next_w
    else:
      print >>sys.stderr, "(nothing found)"
      break

if __name__ == '__main__':
  main()
