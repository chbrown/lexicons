#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from collections import Counter
import json # as json

word_re = re.compile(r"[a-z]['a-z]*")

categories = ['funct', 'pronoun', 'ppron', 'i', 'we', 'you', 'shehe', 'they', 'ipron', 'article', 'verb', 'auxverb', 'past', 'present', 'future', 'adverb', 'preps', 'conj', 'negate', 'quant', 'number', 'swear', 'social', 'family', 'friend', 'humans', 'affect', 'posemo', 'negemo', 'anx', 'anger', 'sad', 'cogmech', 'insight', 'cause', 'discrep', 'tentat', 'certain', 'inhib', 'incl', 'excl', 'percept', 'see', 'hear', 'feel', 'bio', 'body', 'health', 'sexual', 'ingest', 'relativ', 'motion', 'space', 'time', 'work', 'achieve', 'leisure', 'home', 'money', 'relig', 'death', 'assent', 'nonfl', 'filler']

# print open('/usr/local/data/liwc_2007.trie').read()
_trie = json.load(open('/usr/local/data/liwc_2007.trie'))

def _walk(token, i, cursor):
    if '*' in cursor:
        return True, cursor['*']
    if '$' in cursor and i == len(token):
        return True, cursor['$']
    if i < len(token):
        letter = token[i]
        if letter in cursor:
            return _walk(token, i + 1, cursor[letter])
    return False, None


def from_tokens(tokens):
    counts = dict.fromkeys(categories + ['Dic'], 0)
    for token in tokens:
        success, cats = _walk(token, 0, _trie)
        if success:
            for category in cats:
                counts[category] += 1
            counts['Dic'] += 1

    return counts

# full analysis variables below:

full_columns = ['WC', 'WPS', 'Sixltr', 'Dic', 'Numerals'] + categories[:-1] + ['Period', 'Comma', 'Colon', 'SemiC', 'QMark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'OtherP', 'AllPct']

punctuation = [
    ('Period', '.'),
    ('Comma', ','),
    ('Colon', ':'),
    ('SemiC', ';'),
    ('QMark', '?'),
    ('Exclam', '!'),
    ('Dash', '-'), # –—
    ('Quote', '"'), # “”
    ('Apostro', "'"), # ‘’
    ('Parenth', '()[]{}'),
    ('OtherP', '#$%&*+-/<=>@\\^_`|~')
]

def from_text(text):
    text = text.lower()
    tokens = word_re.findall(text)
    # tokens = [token for token in re.split(r'\b', text) if token != '' and token != None]
    # tokens = re.split(r'\b\W+\b', text)
    # tokens = re.findall(r"(\w|')+", text)
    wc = max(len(tokens), 1)
    sentence_count = max(len(re.findall(r"[.!?]+", text)), 1)

    counts = {'WC': wc, 'WPS': wc / float(sentence_count),
        'Sixltr': len([1 for token in tokens if len(token) > 6]),
        'Numerals': len([1 for token in tokens if token.isdigit()])}

    category_counts = from_tokens(tokens)
    counts.update(category_counts)

    character_counts = Counter(text)
    for name, chars in punctuation:
        counts[name] = sum(character_counts[char] for char in chars)
    counts['Parenth'] = counts['Parenth'] / 2.0
    counts['AllPct'] = sum(counts[name] for name, _ in punctuation)

    for column in full_columns[2:]:
        counts[column] = float(counts[column]) / wc

    return counts

def print_liwc_results(counts):
    values = ['%d' % counts['WC'], '%0.2f' % counts['WPS']] + \
        ['%0.2f' % (counts[column] * 100) for column in full_columns[2:]]

    for col, val in zip(full_columns, values):
        print '%16s %s' % (col, val)

def main():
    # warning: does not stream!
    counts = from_text(sys.stdin.read())
    print_liwc_results(counts)

if __name__ == '__main__':
    main()
