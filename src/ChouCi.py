# -*- coding: utf-8 -*-

_DEBUG = False
import utils
import math


class ChouCi(object):

    default_config = {"threshold": 20, "hard_ratio": 3, "free_entropy": 4, "longest_len": 3}

    def __init__(self, passage):
        # self.word_tree = self._wordlib_to_tree(wordlib)
        self.threshold = ChouCi.default_config["threshold"]
        self.hard_ratio = ChouCi.default_config["hard_ratio"]
        self.free_entropy = ChouCi.default_config["free_entropy"]
        self.longest_len = ChouCi.default_config["longest_len"]
        self.passage = passage
        self.word_sizes = {}
        self.result = {}

    def run():        
        self.establish_structure()
        self.calculate_inter_relation()
        self.calculate_free_entropy()

    def establish_structure(self):
        self.words = {}
        for word_len in range(1, self.longest_len + 1):
            sentences_words = utils.split_to_sentences_words(utils.split_to_sentences(self.passage), word_len)
            print word_len
            self.words[word_len] = self.establish_word_list(sentences_words, word_len)
            for s in sentences_words:
                for w in s:
                    if self.word_sizes.get(word_len, None) is None:
                        self.word_sizes[word_len] = 0
                    self.word_sizes[word_len] += 1
        print self.word_sizes


    def establish_word_list(self, sentences_words, word_len):
        root = {}
        for s_words in sentences_words:
            for index, word in enumerate(s_words):
                if root.get(word, None) is None:
                    root[word] = {"_count": 0}
                root[word]["_count"] += 1
                if index != 0:
                    left = s_words[index - 1][0]
                    if root[word].get("_left", None) is None:
                        root[word]["_left"] = {}
                    if root[word]["_left"].get(left, None) is None:
                        root[word]["_left"][left] = {"_count": 0}
                    root[word]["_left"][left]["_count"] += 1
                if index != len(s_words) - 1:
                    right = s_words[index + 1][-1]
                    if root[word].get("_right", None) is None:
                        root[word]["_right"] = {}
                    if root[word]["_right"].get(right, None) is None:
                        root[word]["_right"][right] = {"_count": 0}
                    root[word]["_right"][right]["_count"] += 1
        return root



    def get_word_count(self, word):
        word_len = len(word)
        return self.words.get(word_len, {}).get(word, {}).get("_count", 0)

    def get_word_left(self, word):
        word_len = len(word)
        return self.words.get(word_len, {}).get(word, {}).get("_left", {})

    def get_word_right(self, word):
        word_len = len(word)
        return self.words.get(word_len, {}).get(word, {}).get("_right", {})


    def get_total_count(self, word_len):
        return self.word_sizes.get(word_len, 0)


    def calculate_free_entropy(self):
        entropy = {}
        for word_len in range(1,4):
            for word in (self.words.get(word_len, {})).keys():
                if self.get_word_count(word) > self.threshold:
                    entropy[word] = {}
                    entropy[word]["l"] = {}
                    entropy[word]["l"]["_probabilities"] = {}
                    entropy[word]["l"]["_entropy"] = 0
                    left_sum = 0
                    left_of_word = self.get_word_left(word)
                    for left_c, v in left_of_word.iteritems():
                        left_sum += v["_count"]
                    for left_c, v in left_of_word.iteritems():
                        probability = v["_count"]/float(left_sum)
                        entropy[word]["l"]["_probabilities"][left_c] = probability
                        try:
                            entropy[word]["l"]["_entropy"] += (-probability * math.log(probability, 2))
                        except:
                            print probability,v["_count"],left_sum,word
                            raise "math error"

                    #right
                    entropy[word]["r"] = {}
                    entropy[word]["r"]["_probabilities"] = {}
                    entropy[word]["r"]["_entropy"] = 0
                    right_sum = 0
                    right_of_word = self.get_word_right(word)
                    for right_c, v in right_of_word.iteritems():
                        right_sum += v["_count"]
                    for right_c, v in right_of_word.iteritems():
                        probability = v["_count"]/float(right_sum)
                        entropy[word]["r"]["_probabilities"][right_c] = probability
                        try:
                            entropy[word]["r"]["_entropy"] += (-probability * math.log(probability, 2))
                        except:
                            print probability
                            raise "math error"
                    entropy[word]["min"] = min(entropy[word]["r"]["_entropy"], entropy[word]["l"]["_entropy"])
        self.result["entropy"] = entropy

    def calculate_inter_relation(self):
        result = {}
        for w_len in range(2,4):
            for word in (self.words.get(w_len, {})).keys():
                if self.get_word_count(word) > self.threshold:
                    result[word] = {"hard_ratio": 0}
                    comb = self.combinations_of_word(word)
                    for group in comb:
                        p = 1
                        for w in group:
                            p *= self.get_word_count(w) / float(self.get_total_count(len(w)))
                        hr = self.get_word_count(word)/ float(self.get_total_count(len(word))) / p
                        if result[word]["hard_ratio"] == 0 or hr < result[word]["hard_ratio"]:
                            result[word]["hard_ratio"] = hr
                    # print word
                    
        self.result["hard_ratio"] = result


    # For Debugger
    def analysis(self, word):
        for character in word:
            print character, self.get_word_count(character)
        print word[0:2], self.get_word_count(word[0:2]), self.result.get("hard_ratio", {}).get(word[0:2], None)
        print word[1:3], self.get_word_count(word[1:3]), self.result.get("hard_ratio", {}).get(word[1:3], None)
        print word, self.get_word_count(word), self.result.get("hard_ratio", {}).get(word, None)

        

    # 两字词或三字词
    def combinations_of_word(self, word):
        if len(word) == 2:
            return [[word[0], word[1]]]
        if len(word) == 3:
            return [[word[0:2],word[2]],[word[0],word[1:3]]]
        return []

    # def filter(entropy, hard_ratio, )

    def filter_by_entropy(self, entropy, threshold = None):
        if threshold is None:
            threshold = self.free_entropy
        words = []
        for word, info in entropy.iterate_items():
            if info["min"] < threshold:
                words.append(word)
                print word
        return words


    def filter_by_hard_ratio(self, hard_ratio, threshold = None):
        if threshold is None:
            threshold = self.hard_ratio
        words = []
        for word, info in hard_ratio.iterate_items():
            if info["hard_ratio"] > threshold:
                words.append(word)
                print word
        return words


    def filter(self, entropy, hard_ratio):
        a = self.filter_by_hard_ratio(hard_ratio, self.hard_ratio)
        b = self.filter_by_entropy(entropy, self.free_entropy)
        c = set(b)
        words = []
        for word in a:
            if c.include(word):
                print word
                words.append(word)
        return words

    # def print_free_entropy(top = 100):
    #     entropy = self.calculate_free_entropy()
    #     class A:
    #         def __init__():
    #             self.data = entropy

    #         def get_min_entropy(k)
    #             self.data.__getitem__(k)["min"]

    #     sorted_entropy = sorted(entropy, key= A().get_min_entropy)
    #     for index in range(top):
    #         print sorted_entropy.pop()

        

    



# 如何切分出单个字的词？？
# 找出每个字的特性，找一下组成词语的Pattern



    
'''
    1. split to words
    2. count the apperance of every word
    3. filter the words whose's counts is greater than threhold    
    4. calculate free entropy
    5. calculate hard_ratio


自由度运算
    count words apperances
    count left + word
    count word + right
    calculate 


内聚度运算


如何选取阈值？
'''


'''
单字词、二字词、三字词、四字词、五字词
如何处理单字词
容忍无法正确分出的词
如果有大量重复文本、句型等，会有什么影响，如何解决？
先执行、再分析Bad Case
解决一部分问题就行了，其它问题用其它的方式解决。
算法的效率是多少？
如果配合分词算法，多读几遍会有提升吗？

假设分词过后出先：水冰月，那么如何分词，水、冰、月，水冰、冰月、水冰月 分词的概率

好像不太适合4字及以上的词语，需要重新找方法。

左右应区分对待
'''