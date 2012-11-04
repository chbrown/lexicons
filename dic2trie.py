import sys
import json
'''
The LIWC .dic format looks like this:
%
1   funct
2   pronoun
%
a   1   10
abdomen*    146 147
about   1   16  17

pipe that file into this, get a json trie on stdout
'''

categories = {}
trie = {}

def add(key, categories):
    cursor = trie
    for letter in key:
        if letter == '*':
            cursor['*'] = categories
            break
        if letter not in cursor:
            cursor[letter] = {}
        cursor = cursor[letter]
    cursor['$'] = categories

for line in sys.stdin:
    if not line.startswith('%'):
        parts = line.strip().split('\t')
        if parts[0].isdigit():
            # cache category names
            categories[parts[0]] = parts[1]
        else:
            # print parts[0], ':', parts[1:]
            add(parts[0], [categories[category_id] for category_id in parts[1:]])

# indent=4,
print json.dumps(trie, sort_keys=True)
