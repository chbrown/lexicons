import re


class Lexicon(object):
    def read_token(self, token):
        # The base class lexicon is the identity lexicon (a unigram model)
        yield token

    def read_document(self, document):
        for match in re.finditer(r'\w+', document, re.UNICODE):
            for feature in self.read_token(match.group(0)):
                yield feature


class LookupLexicon(object):
    corpus_filepath = None

    def __init__(self):
        with open(self.corpus_filepath) as corpus_file:
            self._lookup = dict(self._parse_corpus(corpus_file))

    def _parse_corpus(self, corpus_file):
        '''Should yield (key, value) tuples, e.g., (token, score) or something like that'''
