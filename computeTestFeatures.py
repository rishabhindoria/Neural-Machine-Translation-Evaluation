#!/usr/bin/env python
import argparse  # optparse is deprecated
import json
import math
import re
import string
from collections import Counter
from itertools import islice  # slicing for iterators

import nltk
import numpy
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

stops = stopwords.words('english')
WORD = re.compile(r'\w+')
stemmer = SnowballStemmer("english")
import nltk.metrics

def getPuncCount(text):
    count = 0
    for item in text:
        for char in item:
            if(char in string.punctuation):
                count+=1
    return count
def check_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True
def cos_sim(v1, v2):
    int = set(v1.keys()) & set(v2.keys())
    nr = sum([v1[x] * v2[x] for x in int])

    s1 = sum([v1[x] ** 2 for x in v1.keys()])
    s2 = sum([v2[x] ** 2 for x in v2.keys()])
    dr = math.sqrt(s1) * math.sqrt(s2)

    if not dr:
        return 0.0
    else:
        return float(nr) / dr

def text_to_word(text):
    words = WORD.findall(text)
    return Counter(words)

def syn_set(str):
    sset = []
    for synset in wordnet.synsets(str):
        for item in synset.lemmas():
            sset.append(item.name())
    return set(sset)

def word_matches(h, ref):
    refstem = []
    for word in ref:
        if check_ascii(word):
            refstem.append(stemmer.stem(word))
    word_count = 0
    for w in h:
        if w in ref and w not in string.punctuation:
            word_count += 1
        else:
            if check_ascii(w):
                if stemmer.stem(w) in refstem:
                    word_count += 1
                ss = syn_set(w)
                word_count+=sum(1 for st in ss if st in ref)
    return word_count


def main():

    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')

    opts = parser.parse_args()
    def sentences():
        with open(opts.input) as refHypo:
            for x in refHypo:
                x = x.strip()
                list = [sentence.strip().split() for sentence in x.split(' ||| ')]
                yield list

    j=0
    finalFeatures = numpy.empty((opts.num_sentences, 12))
    feature = []
    labels = numpy.empty((opts.num_sentences,1))
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        # if(j%1000==0):
        #     print(j)
        b1 = set(bigrams(h1))
        b2 = set(bigrams(h2))
        b3 = set(bigrams(ref))
        bi1 = len(b1.intersection(b3))
        bi2 = len(b2.intersection(b3))

        t1 = set(nltk.ngrams(h1,3))
        t2 = set(nltk.ngrams(h2,3))
        t3 = set(nltk.ngrams(ref,3))
        tr1 = len(t1.intersection(t3))
        tr2 = len(t2.intersection(t3))

        f1 = set(nltk.ngrams(h1,4))
        f2 = set(nltk.ngrams(h2,4))
        f3 = set(nltk.ngrams(ref,4))
        fr1 = len(f1.intersection(f3))
        fr2 = len(f2.intersection(f3))

        v = text_to_word(" ".join(c for c in ref if c not in string.punctuation))
        cosine_sim1 = cos_sim(text_to_word(" ".join(c for c in h1 if c not in string.punctuation)), v)
        cosine_sim2 = cos_sim(text_to_word(" ".join(c for c in h2 if c not in string.punctuation)), v)

        h1_match = float(word_matches(h1, set(v)))
        h2_match = float(word_matches(h2, set(v)))

        alpha = 0.9

        Rh1 = (float(h1_match) + float(bi1) + float(tr1) + float(fr1)) / float(len(v))
        Ph1 = (float(h1_match) + float(bi1) + float(tr1) + float(fr1)) / float(len(h1))
        Rh2 = (float(h2_match) + float(bi2) + float(tr2) + float(fr2)) / float(len(v))
        Ph2 = (float(h2_match) + float(bi2) + float(tr2) + float(fr2)) / float(len(h2))

        if Rh1 == 0.0 and Ph1 == 0.0:
            lh1 = 0
        else:
            lh1 = (Rh1 * Ph1) / ((Ph1 * alpha) + (Rh1 * (1 - alpha)))

        if Rh2 == 0.0 and Ph2 == 0.0:
            lh2 = 0
        else:
            lh2 = (Rh2 * Ph2) / ((Ph2 * alpha) + (Rh2 * (1 - alpha)))

        p1 = set(nltk.pos_tag(h1))
        p2 = set(nltk.pos_tag(h2))
        p3 = set(nltk.pos_tag(ref))

        pl1 = p1.intersection(p3)
        pl2 = p2.intersection(p3)

        feature.append(lh1)
        feature.append(lh2)
        feature.append(len(pl1))
        feature.append(len(pl2))
        feature.append(bi1)
        feature.append(bi2)
        feature.append(tr1)
        feature.append(tr2)
        feature.append(fr1)
        feature.append(fr2)
        feature.append(cosine_sim1)
        feature.append(cosine_sim2)

        finalFeatures[j] = feature
        feature = []
        j += 1
        if (j % 1000) == 0:
            print("iteration ",j)

    json_decoded = {}
    json_decoded['features'] = finalFeatures.tolist()
    json_file = open("testFeatures.json", 'w')
    data = json.dumps(json_decoded)
    json_file.write(data)


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()