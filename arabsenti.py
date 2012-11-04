# -*- coding: utf-8 -*-
import codecs
import re
from collections import Counter

lexicon = '/usr/local/data/arabsenti_lexicon.txt'

translator = {'0': 0, '2': -1, '1': 1}  # sentiment: # 0=NEUT # 1=POS # 2=NEG

lex = {}
with codecs.open(lexicon, encoding='utf-8', mode='r') as txt_fp:
    for line in txt_fp:
        arabic_dia, freq, sentiment, buck_dia, buck, arabic_no_ham, arabic_ham = map(unicode.strip, line.split(u'\t'))
        if sentiment:
            # if arabic_dia in lex:
            # and lex[arabic_ham] != translator[sentiment]
                # print 'Already stored!', arabic_dia, lex[arabic_dia], 'new', translator[sentiment]
            lex[arabic_dia] = translator[sentiment]
            lex[arabic_ham] = translator[sentiment]
            lex[arabic_no_ham] = translator[sentiment]


def tokens(token_list):
    sentiments = Counter(lex.get(token) for token in token_list)
    return dict(pos=sentiments.get(1, 0), neg=sentiments.get(-1, 0), zero=sentiments.get(0, 0))


whitespace = re.compile(r'\s+')
def document(text):
    return tokens(whitespace.split(text))

# def write_js(stream):
#     lex_json = json.dumps(lex, ensure_ascii=False, indent=2, sort_keys=True)
#     stream.write(u'var arabsenti_lexicon = %s;\n' % lex_json)
#     stream.write(u'''
#     function arabsenti(text) {
#       var tokens = text.split(/\s+/);

#       var sum = 0, abs_sum = 0, count = 0;
#       tokens.forEach(function(token) {
#         var sentiment = arabsenti_lexicon[token];
#         if (sentiment !== undefined) {
#           sum += sentiment;
#           abs_sum += Math.abs(sentiment);
#           count++;
#         }
#       });
#       return {sum: sum, abs_sum: abs_sum, count: count, mean: parseFloat(sum) / count, };
#     }
#     ''')

# if __name__ == '__main__':
    # write_js(sys.stdout)
    # with codecs.open(js, encoding='utf-8', mode='w') as js_fp:
        # write_js(js_fp)

# var sum = function(vector) {
#   var accumulator = 0; vector.forEach(function (num) { accumulator += num; }); return accumulator; };
# var abs_sum = function(vector) {
#   var accumulator = 0; vector.forEach(function (num) { accumulator += Math.abs(num); }); return accumulator; };
