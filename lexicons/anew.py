#!/usr/bin/env python
import re
from . import mean
keys = ['anew_pleasure', 'anew_arousal', 'anew_dominance']

lookup = dict()

# anew looks like:
# Word    Wdnum   ValMn   ValSD   AroMn   AroSD   DomMn   DomSD
# abduction   621 2.76    2.06    5.53    2.43    3.49    2.38
for line in open('/usr/local/data/anew.txt'):
    token, _, pleasure, _, arousal, _, dominance, _ = line.split('\t')
    if token and token != 'Word':
        lookup[token] = (float(pleasure), float(arousal), float(dominance))

# should do stemming on lexicon and words, at least deplural
def from_text(text):
    text = text.lower()
    tokens = re.findall(r'\w+', text)
    matches = [lookup[token] for token in tokens if token in lookup]
    pleasure, arousal, dominance = zip(*matches)
    return dict(zip(keys, [mean(pleasure), mean(arousal), mean(dominance)]))
