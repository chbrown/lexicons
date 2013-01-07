# Setup

Python and Javascript libraries packaged together here;
mostly they are translations of each other, if both exist (as with LIWC, for example).

## LIWC

- liwc.py and liwc.js require `/usr/local/data/liwc_2007.trie`
  - MD5: bca2eeec79701ed88c40f8c9c75e5f7c
- liwc-regex.js requires `/usr/local/data/liwc_2007.csv`
  - MD5: 686df57d28941cf797704bd2d4f9a1a3

You can get the LIWC lexicon at [liwc.net](http://liwc.net/).

You can use dic2trie to convert the `.dic` file that the LIWC lexicon comes
with to a trie, for faster (streaming) analysis.

## Arabsenti

- arabsenti.py requires `/usr/local/data/arabsenti_lexicon.txt`
  - MD5: 0ed1192e4b6f10a29b353b3056ec179d

You can get the Arabsenti lexicon from [Muhammad Abdul-Mageed](http://mumageed.blogspot.com/).

Citation form:

    @inproceedings{abdul:2011,
      title={Subjectivity and sentiment analysis of modern standard Arabic},
      author={Abdul-Mageed, M. and Diab, M.T. and Korayem, M.},
      booktitle={Proceedings of the 49th Annual Meeting of the Association for
      Computational Linguistics: Human Language Technologies: short papers-Volume 2},
      pages={587--591},
      year={2011},
      organization={Association for Computational Linguistics}
    }

It requires Python 2.7+.

## AFINN

This is publicly available at [Finn Årup Nielsen's blog](http://fnielsen.posterous.com/afinn-a-new-word-list-for-sentiment-analysis), so I just left it in the code.

# Installation

    python setup.py install
    npm install
    npm link
