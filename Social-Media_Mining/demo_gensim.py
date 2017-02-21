#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from gensim.summarization import summarize
import sys


fname = sys.argv[1]

with open(fname, 'r') as f:
    content = f.read()
    summary = summarize(content, split=True)

    for i, sentence in enumerate(summary):
        print("%d) %s" % (i+1, sentence))