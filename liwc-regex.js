#!/usr/bin/env node
var fs = require('fs');

var lexicon_regexes = [];
fs.readFileSync('/usr/local/data/liwc_2007.csv', 'utf8').split(/\n/g).forEach(function(line) {
  if (line) {
    var parts = line.split(/\t/);
    lexicon_regexes.push({
      regex: new RegExp('\\b' + parts[0].replace(/\*/, '\\w*') + '\\b', 'gi'),
      categories: parts[1].split(/,/)
    });
  }
});

var category_lookup = {}, categories = ['achiev', 'adverbs', 'affect', 'anger', 'anx', 'article', 'assent', 'auxvb', 'bio', 'body', 'cause', 'certain', 'cogmech', 'conj', 'death', 'discrep', 'excl', 'family', 'feel', 'filler', 'friends', 'funct', 'future', 'health', 'hear', 'home', 'humans', 'i', 'incl', 'ingest', 'inhib', 'insight', 'ipron', 'leisure', 'money', 'motion', 'negate', 'negemo', 'nonflu', 'numbers', 'past', 'percept', 'posemo', 'ppron', 'prep', 'present', 'pronoun', 'quant', 'relativ', 'relig', 'sad', 'see', 'sexual', 'shehe', 'social', 'space', 'swear', 'tentat', 'they', 'time', 'verbs', 'we', 'work', 'you'];
categories.forEach(function(category, i) { category_lookup[category] = i; });
function categoryToId(category) { return category_lookup[category]; }

function tokenwise(document) {
  return document.toLowerCase().match(/[a-z']+/g).map(trie);
}
function count(document) {
  var store = {};
  categories.forEach(function(category, i) {
    store[category] = 0;
  });
  store.total = 0;
  lexicon_regexes.forEach(function(entry) {
    var matches = document.match(entry.regex);
    if (matches) {
      var count = matches.length;
      entry.categories.forEach(function(category) {
        store[category] += count;
        store.total += count;
      });
    }
  });
  store.wc = document.match(/\s+/g).length + 1;
  return store;
}

module.exports = {
  categoryToId: categoryToId,
  categories: categories,
  tokenwise: tokenwise,
  count: count
};
