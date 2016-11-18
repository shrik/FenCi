# -*- coding: utf-8 -*-   

import re

separator = set(u", . * : ' \" ： ， 。 ： ~ （ ） ( ) [ ] 【 】 。 ” ！ ， ；  、 “  ：  ；  ，  “ ？ \n".split(" "))

#TODO fix split to sentences

_DEBUG = False

def split_to_sentences(content):
    content = re.sub(r"\r|\n","",content)
    sentences = []
    last_index = 0 
    for index, character in enumerate(content):
        if character in separator:
            if index > 0:
                sentences.append(content[last_index+1:index])
            # print character, last_index,index - 1
            last_index = index
    if last_index != len(content):
        sentences.append(content[last_index:])
    if _DEBUG:
        for s in sentences:
            print "sentence is ", s
    return sentences


# return [[w1,w2...],...]
def split_to_sentences_words(sentences, length):
    sentences_words = []
    for sentence in sentences:
        sentences_words.append(split_sentence_to_words(sentence, length))
    return sentences_words


def split_sentence_to_words(sentence, length):
    words = []
    for index in range(len(sentence)-length + 1):
        word = sentence[index:(index+length)]
        words.append(word)
        if len(word) != length:
            raise "error"
    return words


