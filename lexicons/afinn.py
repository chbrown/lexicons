from lexicons.base import LookupLexicon
from lexicons.lib import stats


class Afinn(LookupLexicon):
    '''
    The AFINN lexicon was created with Twitter in mind. It consists of 2,477 entries (2,462 unigrams + 15 bigrams) each assigning a word (or pair of words) to an integer score between -5 to +5. -5 is very negative, +5 is very positive.

    The corpus has the following frequencies for each score:

    | score | count |
    |------:|------:|
    |    +5 |     5 |
    |    +4 |    45 |
    |    +3 |   172 |
    |    +2 |   448 |
    |    +1 |   208 |
    |     0 |     1 |
    |    -1 |   309 |
    |    -2 |   966 |
    |    -3 |   264 |
    |    -4 |    43 |
    |    -5 |    16 |

    Links:

    * http://fnielsen.posterous.com/afinn-a-new-word-list-for-sentiment-analysis ->
      - http://web.archive.org/web/20130328101613/http://fnielsen.posterous.com/afinn-a-new-word-list-for-sentiment-analysis
    * http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
      - http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
    * http://arxiv.org/abs/1103.2903
    '''
    keys = ['afinn_sum', 'afinn_mean', 'afinn_pos_sum', 'afinn_neg_sum', 'afinn_abs_sum']
    # source:
    corpus_filepath = '/usr/local/data/afinn.txt'

    def _parse_corpus(self, corpus_file):
        for line in corpus_file:
            token, score = line.split('\t')
            yield token, int(score)

    def read_token(self, token):
        # yields a single score for this token (0 if it's not a match)
        yield self._lookup.get(token, 0)

    def summarize_document(self, document):
        sentiments = list(self.read_document(document))
        return {
            'afinn_sum': sum(sentiments),
            'afinn_mean': stats.mean(sentiments),
            'afinn_sd': stats.sd(sentiments),
            'afinn_pos_sum': sum(score for score in sentiments if score > 0),
            'afinn_neg_sum': sum(score for score in sentiments if score < 0),
            'afinn_abs_sum': sum(abs(s) for s in sentiments)
        }
