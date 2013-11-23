# -*- coding: utf-8 -*-
import re
from lexicons.base import Lexicon
from collections import Counter
import json


class Liwc(Lexicon):
    corpus_filepath = '/usr/local/data/liwc_2007.trie'

    # category analysis variables:
    category_keys = ['funct', 'pronoun', 'ppron', 'i', 'we', 'you', 'shehe',
        'they', 'ipron', 'article', 'verb', 'auxverb', 'past', 'present', 'future',
        'adverb', 'preps', 'conj', 'negate', 'quant', 'number', 'swear', 'social',
        'family', 'friend', 'humans', 'affect', 'posemo', 'negemo', 'anx', 'anger',
        'sad', 'cogmech', 'insight', 'cause', 'discrep', 'tentat', 'certain',
        'inhib', 'incl', 'excl', 'percept', 'see', 'hear', 'feel', 'bio', 'body',
        'health', 'sexual', 'ingest', 'relativ', 'motion', 'space', 'time', 'work',
        'achieve', 'leisure', 'home', 'money', 'relig', 'death', 'assent', 'nonfl',
        'filler']

    # full analysis variables:
    meta_keys = ['WC', 'WPS', 'Sixltr', 'Dic', 'Numerals']
    puncuation_keys = [
        'Period', 'Comma', 'Colon', 'SemiC', 'QMark', 'Exclam',
        'Dash', 'Quote', 'Apostro', 'Parenth', 'OtherP', 'AllPct']
    punctuation = [
        ('Period', '.'),
        ('Comma', ','),
        ('Colon', ':'),
        ('SemiC', ';'),
        ('QMark', '?'),
        ('Exclam', '!'),
        ('Dash', '-'),  # –—
        ('Quote', '"'),  # “”
        ('Apostro', "'"),  # ‘’
        ('Parenth', '()[]{}'),
        ('OtherP', '#$%&*+-/<=>@\\^_`|~')
    ]

    def __init__(self):
        self.all_keys = self.meta_keys + self.category_keys[:-1] + self.puncuation_keys

        with open(self.corpus_filepath) as corpus_file:
            self._trie = json.load(corpus_file)

    # standard Lexicon functionality:

    def read_token(self, token, token_i=0, trie_cursor=None):
        if trie_cursor is None:
            trie_cursor = self._trie

        if '*' in trie_cursor:
            for category in trie_cursor['*']:
                yield category
        elif '$' in trie_cursor and token_i == len(token):
            for category in trie_cursor['$']:
                yield category
        elif token_i < len(token):
            letter = token[token_i]
            if letter in trie_cursor:
                for category in self.read_token(token, token_i + 1, trie_cursor[letter]):
                    yield category

    def read_document(self, document, token_pattern=r"[a-z]['a-z]*"):
        for match in re.finditer(token_pattern, document.lower()):
            for category in self.read_token(match.group(0)):
                yield category

    # extra (legacy) Liwc functionality:

    def summarize_document(self, document, token_pattern=r"[a-z]['a-z]*", normalize=True):
        sentence_count = len(re.findall(r"[.!?]+", document)) or 1

        # tokens is a bit redundant because it duplicates the tokenizing done
        # in read_document, but to keep read_document simple, we just run it again here.
        tokens = re.findall(token_pattern, document.lower())
        counts = Counter(self.read_document(document, token_pattern=token_pattern))
        counts['Dic'] = sum(counts.values())
        counts['WC'] = len(tokens)
        counts['WPS'] = counts['WC'] / float(sentence_count)
        counts['Sixltr'] = sum(len(token) > 6 for token in tokens)
        counts['Numerals'] = sum(token.isdigit() for token in tokens)

        # count up all characters so that we can get punctuation counts quickly
        character_counts = Counter(document)
        for name, chars in self.punctuation:
            counts[name] = sum(character_counts[char] for char in chars)
        # Parenth is special -- we only count one half of them (to match the official LIWC application)
        counts['Parenth'] = counts['Parenth'] / 2.0
        counts['AllPct'] = sum(counts[name] for name, _ in self.punctuation)

        if normalize:
            # normalize all counts but the first two ('WC' and 'WPS')
            for column in self.all_keys[2:]:
                counts[column] = float(counts[column]) / float(counts['WC'])

        # return a normal dict() rather than the Counter() instance
        result = dict.fromkeys(self.category_keys + ['Dic'], 0)
        result.update(counts)
        return result

    def print_summarization(self, counts):
        absolutes = ['%d' % counts['WC'], '%0.2f' % counts['WPS']]
        percentages = ['%0.2f' % (counts[key] * 100) for key in self.all_keys[2:]]

        for key, value in zip(self.all_keys, absolutes + percentages):
            print '%16s %s' % (key, value)
