# -*- coding: utf-8 -*-
from sets import Set
_DEBUG = True
class PassageParser(object):

    separator = Set(", . * : ' \" ： ， 。 ： ~ （ ） ( ) [ ] 【 】 ".split(" "))

    def __init__(self, content, algo):
        self.content = content
        self.algo = algo

    def parse(self):
        sentences = self.split_to_sentences()
        sentence_with_splited_words = []
        for sentence in sentences:
            sentence_with_splited_words.append(self.algo.analysis(sentence))
        return sentence_with_splited_words


    def split_to_sentences(self):
        sentences = []
        last_index = 0 
        for index, character in enumerate(self.content):
            if character in PassageParser.separator:
                sentences.append(content[last_index:index -1])
                last_index = index + 1
        if last_index != len(self.content):
            sentences.append(self.content[last_index:])
        if _DEBUG:
            print("sentences is : %s" % sentences)
        return sentences
