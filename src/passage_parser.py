# -*- coding: utf-8 -*-
from sets import Set
_DEBUG = True
class PassageParser(object):    

    def __init__(self, content, algo):
        self.content = content
        self.algo = algo

    def parse(self):
        sentences = self.split_to_sentences()
        sentence_with_splited_words = []
        for sentence in sentences:
            sentence_with_splited_words.append(self.algo.analysis(sentence))
        return sentence_with_splited_words



