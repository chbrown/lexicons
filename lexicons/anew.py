from lexicons.base import LookupLexicon
from lexicons.lib import stats


class Anew(LookupLexicon):
    # anew looks like:
    # Word    Wdnum   ValMn   ValSD   AroMn   AroSD   DomMn   DomSD
    # abduction   621 2.76    2.06    5.53    2.43    3.49    2.38
    # ... 2476 total entries ...
    corpus_filepath = '/usr/local/data/anew.txt'

    def _parse_corpus(self, corpus_file):
        # skip first line (the column headers)
        corpus_file.next()
        for line in corpus_file:
            token, _, pleasure, _, arousal, _, dominance, _ = line.split('\t')
            yield token, (float(pleasure), float(arousal), float(dominance))

    def read_token(self, token):
        # yield pleasure, arousal, dominance
        # yields a (pleasure, arousal, dominance) tuple
        yield self._lookup.get(token, (0, 0, 0))

    def summarize_document(self, document):
        # TODO: stem on lexicon and words, at least depluralize
        keys = ('anew_pleasure', 'anew_arousal', 'anew_dominance')
        sentiments = list(self.read_document(document))
        # pleasures, arousals, dominances = zip(*sentiments)
        return dict(zip(keys, map(stats.mean, zip(*sentiments))))
