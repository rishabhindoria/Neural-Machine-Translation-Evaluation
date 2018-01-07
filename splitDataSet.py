#!/usr/bin/env python
import argparse  # optparse is deprecated
import math
from itertools import islice  # slicing for iterators


def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

train=open("dev.train","w")
test=open("dev.test","w")

trainlabels=open("data/dev.train.answers","w")
testlabels=open("data/dev.test.answers","w")

def main():
    alpha=0.9
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
            help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
    opts = parser.parse_args()
 
    # we create a generator and avoid loading all sentences into a list
    lines = open(opts.input).readlines()

    classlines = open("data/dev.answers").readlines()

    def sentences():
        with open(opts.input) as refHypo,open("data/dev.answers") as labels:
            for x, y in zip(refHypo, labels):
                x = x.strip()
                y = y.strip()
                list = [sentence.strip().split() for sentence in x.split(' ||| ')]
                list.append(y)
                yield list
    j=0
    prev=""
    starting=0
    ending=0

    for h1, h2, ref,label in islice(sentences(), opts.num_sentences):
        if(j==0):
            prev=ref
        j+=1
        if(ref==prev):
            prev=ref
            ending=j
        else:
            middle=starting+int(math.ceil((ending-starting)*.60))
            for i in range(starting,middle+1):
                train.write(lines[i])
                trainlabels.write(classlines[i])
            for i in range(middle+1,ending+1):
                test.write(lines[i])
                testlabels.write(classlines[i])
            prev=ref
            starting=j

# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
