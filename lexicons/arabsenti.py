from lexicons.base import LookupLexicon
from lexicons.lib import stats


class Arabsenti(LookupLexicon):
    # source:
    corpus_filepath = '/usr/local/data/arabsenti_lexicon.txt'

    def _parse_corpus(self, corpus_file):
        # the lexicon has the following sentiment scores: 0=NEUT, 1=POS, 2=NEG
        # we want to remap these as: NEG=-1, NEUT=0, POS=+1
        remapping = {'0': 0, '2': -1, '1': 1}
        # with codecs.open(lexicon, encoding='utf-8', mode='r') as corpus_file:
        for line in corpus_file:
            line = line.decode('utf8')
            parts = line.split(u'\t')
            # [0]         [1]   [2]        [3]       [4]   [5]            [6]
            # arabic_dia, freq, sentiment, buck_dia, buck, arabic_no_ham, arabic_ham = parts
            score = remapping[parts[2]]
            yield parts[0].strip(), score
            yield parts[5].strip(), score
            yield parts[6].strip(), score

    def read_token(self, token):
        # yields a single score for this token (0 if it's not a match)
        yield self._lookup.get(token, 0)

    def summarize_document(self, document):
        sentiments = list(self.read_document(document))
        return {
            'arabsenti_sum': sum(sentiments),
            'arabsenti_mean': stats.mean(sentiments),
            'arabsenti_sd': stats.sd(sentiments),
            'arabsenti_pos_sum': sum(score for score in sentiments if score > 0),
            'arabsenti_neg_sum': sum(score for score in sentiments if score < 0),
            'arabsenti_abs_sum': sum(abs(s) for s in sentiments)
        }
