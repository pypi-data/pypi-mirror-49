from collections import Counter
from plnlp.defs import FDIM, P_CASE, CASES, START_TOKEN, END_TOKEN, NUM, LBLS, UNK
import logging

def build_dict(words, max_words=None, offset=0):
    cnt = Counter(words)
    if max_words:
        words = cnt.most_common(max_words)
    else:
        words = cnt.most_common()
    return {word: offset+i for i, (word, _) in enumerate(words)}

def casing(word):
    if len(word) == 0: return word
    # all lowercase
    if word.islower(): return "aa"
    # all uppercase
    elif word.isupper(): return "AA"
    # starts with capital
    elif word[0].isupper(): return "Aa"
    # has non-initial capital
    else: return "aA"

def normalize(word):
    """
    Normalize words that are numbers or have casing.
    """
    #print(word)
    if word.isdigit(): return NUM
    else: return word.lower()

class ModelHelper(object):
    """
    This helper takes care of preprocessing data, constructing embeddings, etc.
    """
    def __init__(self, tok2id, max_length):
        self.tok2id = tok2id
        self.START = [tok2id[START_TOKEN], tok2id[P_CASE + "aa"]]
        self.END = [tok2id[END_TOKEN], tok2id[P_CASE + "aa"]]
        self.max_length = max_length

    def vectorize_example(self, sentence, labels=None):
        sentence_ = [[self.tok2id.get(normalize(word), self.tok2id[UNK]), self.tok2id[P_CASE + casing(word)]] for word
                     in sentence]
        if labels:
            labels_ = [LBLS.index(l) for l in labels]
            return sentence_, labels_
        else:
            return sentence_, [LBLS[-1] for _ in sentence]


    def vectorize(self, data):
        return [self.vectorize_example(sentence, labels) for sentence, labels in data]

    @classmethod
    def build(cls, data):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        # Preprocess data to construct an embedding
        # Reserve 0 for the special NIL token.
        tok2id = build_dict((normalize(word) for sentence, _ in data for word in sentence), offset=1, max_words=10000)
        tok2id.update(build_dict([P_CASE + c for c in CASES], offset=len(tok2id)))
        tok2id.update(build_dict([START_TOKEN, END_TOKEN, UNK], offset=len(tok2id)))
        assert sorted(tok2id.items(), key=lambda t: t[1])[0][1] == 1
        logger.info("Built dictionary for %d features.", len(tok2id))

        max_length = max(len(sentence) for sentence, _ in data)

        return cls(tok2id, max_length)


def read_conll(fstream):
    """
    Reads a input stream @fstream (e.g. output of `open(fname, 'r')`) in CoNLL file format.
    @returns a list of examples [(tokens), (labels)]. @tokens and @labels are lists of string.
    """
    ret = []

    current_toks, current_lbls = [], []
    for line in fstream:
        line = line.strip()
        if len(line) == 0 or line.startswith("-DOCSTART-"):
            if len(current_toks) > 0:
                assert len(current_toks) == len(current_lbls)
                ret.append((current_toks, current_lbls))
            current_toks, current_lbls = [], []
        else:
            assert "\t" in line, r"Invalid CONLL format; expected a '\t' in {}".format(line)
            tok, lbl = line.split("\t")
            current_toks.append(tok)
            current_lbls.append(lbl)
    if len(current_toks) > 0:
        assert len(current_toks) == len(current_lbls)
        ret.append((current_toks, current_lbls))
    return ret

def write_conll(fstream, data):
    """
    Writes to an output stream @fstream (e.g. output of `open(fname, 'r')`) in CoNLL file format.
    @data a list of examples [(tokens), (labels), (predictions)]. @tokens, @labels, @predictions are lists of string.
    """
    for cols in data:
        for row in zip(*cols):
            fstream.write("\t".join(row))
            fstream.write("\n")
        fstream.write("\n")