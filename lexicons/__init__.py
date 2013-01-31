import re

stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before',
'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could',
"couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't",
'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's",
'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
"how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't",
'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my',
'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
'other', 'ought', 'our', 'ours ', 'ourselves', 'out', 'over', 'own', 'same',
"shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so',
'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them',
'themselves', 'then', 'there', "there's", 'these', 'they', "they'd",
"they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too',
'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll",
"we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's",
'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's",
'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're",
"you've", 'your', 'yours', 'yourself', 'yourselves']

chunk_break_re = re.compile(r'^|\s|$')
def split_document(document, number_of_splits):
    # split_document takes a @document: string and number of splits,
    # and returns non-overlapping substrings in that document that are
    # slightly adjusted to break only on whitespace
    length = len(document)
    chunk_length = length // number_of_splits
    splits = [0]
    for i in range(1, number_of_splits):
        candidate = chunk_length*i
        actual = chunk_break_re.search(document, candidate).start(0)
        splits += [actual, actual + 1]
    splits.append(-1)

    for start, end in zip(splits[::2], splits[1::2]):
        yield document[start:end]

def mean(xs):
    return sum(xs) / float(len(xs))
