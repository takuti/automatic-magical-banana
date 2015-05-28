#!/usr/bin/env python
# encoding: utf-8
import sys
import sqlite3
import random
from collections import namedtuple

conn = sqlite3.connect("wnjpn.db")

Word = namedtuple('Word', 'wordid lang lemma pron pos')

def getWords(lemma):
  cur = conn.execute("select * from word where lemma=?", (lemma,))
  return [Word(*row) for row in cur]

def getWord(wordid):
  cur = conn.execute("select * from word where wordid=?", (wordid,))
  return Word(*cur.fetchone())

Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

def getSenses(word):
  cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
  return [Sense(*row) for row in cur]

def getSense(synset, lang='jpn'):
  cur = conn.execute("select * from sense where synset=? and lang=?",
                     (synset,lang))
  row = cur.fetchone()
  return row and Sense(*row) or None

Synset = namedtuple('Synset', 'synset pos name src')

def getSynset(synset):
  cur = conn.execute("select * from synset where synset=?", (synset,))
  return Synset(*cur.fetchone())

SynLink = namedtuple('SynLink', 'synset1 synset2 link src')

def getSynLinks(sense, link):
  cur = conn.execute("select * from synlink where synset1=? and link=?",
                     (sense.synset, link))
  return [SynLink(*row) for row in cur]

l = []
def getSynLinksRecursive(senses, link, lang='jpn', _depth=0):
  for sense in senses:
    synLinks = getSynLinks(sense, link)
    if synLinks:
      l.append(getWord(sense.wordid).lemma)
      """
      print ''.join([' '*2*_depth,
                     getWord(sense.wordid).lemma,
                     ' ',
                     getSynset(sense.synset).name])
      """
    _senses = []
    for synLink in synLinks:
      sense = getSense(synLink.synset2, lang)
      if sense:
        _senses.append(sense)

    getSynLinksRecursive(_senses, link, lang, _depth+1)

if __name__ == '__main__':
  if len(sys.argv) != 3: sys.exit('usage: ./banana.py [word] [N_chain]')
  w = sys.argv[1].decode('utf-8')
  for n in range(int(sys.argv[2])):
    words = getWords(w)
    if words:
      sense = getSenses(words[0])
      getSynLinksRecursive(sense, 'hype', 'jpn')
      getSynLinksRecursive(sense, 'hypo', 'jpn')
      next_w = random.choice([x for x in list(set(l)) if x != w])
      print w, 'といったら', next_w
      l = []
      w = next_w
    else:
      print >>sys.stderr, "(nothing found)"
      break
