#!/usr/bin/env python

# The AFINN lexicon was supposedly created with Twitter in mind.
# http://fnielsen.posterous.com/afinn-a-new-word-list-for-sentiment-analysis
# http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
from . import mean
import re
keys = ['afinn_sum', 'afinn_mean', 'afinn_pos_sum', 'afinn_neg_sum', 'afinn_abs_sum']

lookup = dict()
for line in open('/usr/local/data/afinn.txt'):
    if line:
        token, score = line.split('\t')
        lookup[token] = int(score)

def from_tokens(tokens):
    sentiments = [lookup.get(word, 0) for word in tokens]
    # sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    # sq_differences = [(sentiment - mean)**2 for sentiment in sentiments]
    # sd = math.sqrt(sum(sq_differences) / len(sq_differences))

    return {
        'afinn_sum': sum(sentiments),
        'afinn_mean': mean(sentiments),
        'afinn_pos_sum': sum(score for score in sentiments if score > 0),
        'afinn_neg_sum': sum(score for score in sentiments if score < 0),
        'afinn_abs_sum': sum(abs(s) for s in sentiments)
    }

def from_text(text):
    return from_tokens(re.split('\W+', text.lower()))
