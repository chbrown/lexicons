#!/usr/bin/env node
var fs = require('fs');

function extend(array, l) {
  return array.push.apply(array, l);
}

function escapeRegex(text) {
  // from http://simonwillison.net/2006/Jan/20/escape/#p-6
  return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}

var json_trie = fs.readFileSync('/usr/local/data/liwc_2007.trie', 'utf8'),
  _trie = JSON.parse(json_trie),
  categories = ['funct', 'pronoun', 'ppron', 'i', 'we', 'you', 'shehe', 'they', 'ipron', 'article', 'verb', 'auxverb', 'past', 'present', 'future', 'adverb', 'preps', 'conj', 'negate', 'quant', 'number', 'swear', 'social', 'family', 'friend', 'humans', 'affect', 'posemo', 'negemo', 'anx', 'anger', 'sad', 'cogmech', 'insight', 'cause', 'discrep', 'tentat', 'certain', 'inhib', 'incl', 'excl', 'percept', 'see', 'hear', 'feel', 'bio', 'body', 'health', 'sexual', 'ingest', 'relativ', 'motion', 'space', 'time', 'work', 'achieve', 'leisure', 'home', 'money', 'relig', 'death', 'assent', 'nonfl', 'filler'],
  full_columns = ['WC', 'WPS', 'Sixltr', 'Dic', 'Numerals'],
  punctuations = [
    {name: 'Period', chars: '.'},
    {name: 'Comma', chars: ','},
    {name: 'Colon', chars: ':'},
    {name: 'SemiC', chars: ';'},
    {name: 'QMark', chars: '?'},
    {name: 'Exclam', chars: '!'},
    {name: 'Dash', chars: '-'},
    {name: 'Quote', chars: '"'},
    {name: 'Apostro', chars: "'"},
    {name: 'Parenth', chars: '()[]{}'},
    {name: 'OtherP', chars: '#$%&*+-/<=>@\\^_`|~'}
  ];
extend(full_columns, categories); // exclude filler? is that a bug?
extend(full_columns, ['Period', 'Comma', 'Colon', 'SemiC', 'QMark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'OtherP', 'AllPct']);
for (var p in punctuations) {
  var raw = punctuations[p].chars.split('').map(escapeRegex).join('|');
  punctuations[p].regex = new RegExp(raw, 'ig');
}

// async -- too much overhead?
// function init(callback) {
  // fs.readFile('/usr/local/data/liwc_2007.trie', 'utf8', function (err, data) {
  //   if (err) throw err;
  //   _trie = JSON.parse(data);
  //   callback(err);
  // });
// }

function _walk(token, i, cursor) {
  if ('*' in cursor)
    return cursor['*'];
  if ('$' in cursor && i === token.length)
    return cursor['$'];
  if (i < token.length) {
    var letter = token[i];
    if (letter in cursor)
      return _walk(token, i + 1, cursor[letter]);
  }
  return [];
}
function from_tokens(tokens) {
  var counts = {Dic: 0, WC: tokens.length};
  for (var i in categories)
    counts[categories[i]] = 0;

  for (var j in tokens) {
    var cats = _walk(tokens[j], 0, _trie);
    if (cats.length) {
      for (var k in cats) {
        counts[cats[k]]++;
      }
      counts.Dic++;
    }
  }

  return counts;
}

function from_text(text, opts) {
  if (opts === undefined) opts = {normalize: true};
  // 'split' produces about 300 more on the brown corpus than 'match' below
  var tokens = text.toLowerCase().split(/[^'a-z0-9A-Z]+/ig);
  // var tokens = text.toLowerCase().match(/[a-z]['a-z]*/g) || [''];
  var sentence_count = (text.match(/[.!?]+/g) || ['']).length;
  var sixltr = 0, numerals = 0;
  for (var i in tokens) {
    var token = tokens[i];
    if (token.length > 6)
      sixltr++;
    if (token.match(/^\d+$/))
      numerals++;
  }

  var counts = from_tokens(tokens);
  // Words per sentence is kind of weird if we're not proceeding incrementally.
  // We just count min(sentence-markers, 1) if normalize == false.
  // But then, the natural thing to do would be to count sentences per word in the LIWC analysis,
  // like everything else, and calculate 1/sentences per word, in post-processing, to get WPS
  counts.WPS = opts.normalize ? counts.WC / sentence_count : sentence_count;
  counts.Sixltr = sixltr;
  counts.Numerals = numerals;

  counts.AllPct = 0;
  for (var j in punctuations) {
    var punc = punctuations[j];
    counts[punc.name] = (text.match(punc.regex) || []).length;
    counts.AllPct += counts[punc.name];
  }
  // N.B.: I am ignoring the LIWC standard of dividing parentheses by two!
  // counts.Parenth = counts.Parenth / 2.0;
  // for (var k in punctuations)

  if (opts.normalize) {
    for (var c = 2; column = full_columns[c]; c++)
      counts[column] = counts[column] / counts.WC;
  }

  return counts;
}

// def print_liwc_results(counts):
//     values = ['%d' % counts['WC'], '%0.2f' % counts['WPS']] + \
//         ['%0.2f' % (counts[column] * 100) for column in full_columns[2:]]
//     for col, val in zip(full_columns, values):
//         print '%16s %s' % (col, val)

module.exports = {
  categories: categories,
  full_columns: full_columns,
  from_tokens: from_tokens,
  from_text: from_text
};

if (require.main === module) {
  var stdin = '';
  process.stdin.on('data', function(chunk) { stdin += chunk; });
  process.stdin.on('end', function() {
    var counts = from_text(stdin);
    console.dir(counts);
  });
  process.stdin.resume();
}
