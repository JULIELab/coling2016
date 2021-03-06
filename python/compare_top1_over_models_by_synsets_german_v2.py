import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy
from nltk.corpus import wordnet as wn
from pygermanet import load_germanet

def compare(models, gn):
    for i in range(len(models)):
        models[i] = gensim.models.Word2Vec.load_word2vec_format(
            models[i], binary=True)

    senses2rel = {}
    senses2count = {}

    for word in models[0].vocab:
        options = gn.lemmatise(word) + [word, word.capitalize()] + gn.lemmatise(word.capitalize())
        senses = sum([len(gn.synsets(w)) for w in options])
        if senses > 10:
            senses = 10

        if not senses in senses2rel:
            senses2rel[senses] = 0
        if not senses in senses2count:
            senses2count[senses] = 0

        senses2count[senses] += 1
        senses2rel[senses] += len(intersection(
            [[word for word, sim in model.most_similar(word, topn=1)] if word in model.vocab else [] for model in models]))
    return sorted([(senses, senses2rel[senses] / senses2count[senses]) for senses in senses2count])


def intersection(sequences):
    if len(sequences) < 2:
        raise Exception("Need multiple sequences for comparisson")
    inter = set(sequences[0])
    for s in sequences[1:]:
        inter = inter.intersection(set(s))
    return inter


def main():
    gn = load_germanet()

    if len(sys.argv) < 2:
        raise Exception(
            "Provide 1+ arguments:\n\t1+,model(s)")
    models = sys.argv[1:]

    senses2rel = compare(models, gn)
    print("senses reliability")
    for senses, rel in senses2rel:
        print(str(senses), str(rel))

if __name__ == "__main__":
    main()
