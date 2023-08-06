# encoding: utf-8

import itertools
import numpy as np

from collections import Counter


class NaiveBayes(object):


    def __init__(self):

        self._logprior      = None
        self._loglikelihood = None
        self._V             = None
        self._C             = None


    def flatten(self, l):

        return list(itertools.chain.from_iterable(l))


    def logprior(self, C):

        c = Counter(C)
        p = np.log2(c.values()) - np.log2(len(C))

        self._logprior = {c.keys()[i]:p[i] for i in range(len(c.keys()))}


    def V(self, D):

        D_flatten = self.flatten(D)
        self._V = np.unique(D_flatten)


    def loglikelihood(self, D, C):

        c_full = Counter(C)

        doc_merged = {i:[] for i in c_full.keys()}

        for i in range(len(C)):
            doc_merged[C[i]].append(D[i])

        for k, v in doc_merged.iteritems():
            doc_merged[k] = self.flatten(v)

        # num of words in each class
        c_count = {k:len(v) for k, v in doc_merged.iteritems()} 

        # each word counts in each class
        c_part = {c:Counter(doc_merged[c]) for c in c_full.keys()}

        # log likelihood
        len_V = len(self._V)

        self._loglikelihood = {c:{} for c in c_full.keys()}

        for c, cnt in c_part.iteritems():
            for w, w_cnt in cnt.iteritems():
                self._loglikelihood[c][w] = np.log2(float(w_cnt+1) / (c_count[c]+len_V))
            for w in set(self._V)-set(cnt.keys()):
                self._loglikelihood[c][w] = np.log2(1. / (c_count[c]+len_V))


    def cunique(self, C):

        self._C = np.unique(C)


    def fit(self, D, C):

        self.logprior(C)
        self.V(D)
        self.loglikelihood(D, C)
        self.cunique(C)


    def predict(self, d):

        score = []

        for c in self._C:
            s = self._logprior[c]
            for w in d:
                if w in self._V:
                    s += self._loglikelihood[c][w]
            score.append(s)

        c = self._C[np.argmax(score)]

        return c
