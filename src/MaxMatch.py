
# Max Match Algorithm, Right-To-Left Order
# TODO Use more elegance function name and variable name
# TODO Support English words split 

_DEBUG = False

class MaxMatcher(object):
    def __init__(self, wordlib):
        self.word_tree = self._wordlib_to_tree(wordlib)


    # Every words, find by character
    # If no, then create one node, default child false, world false.
    #    if word not end, then set child true
    #    if word end, then set word true
    
    def _wordlib_to_tree(self, wordlib):
        tree = {}
        for word in wordlib:
            parent = tree
            for index, character  in enumerate(word):
                # init node
                if (parent.get(character, None) == None):
                    parent[character] = {"attr":{"word": False, "child": False}}
                
                if index + 1 == len(word):
                    # Word Ends
                    parent[character]["attr"]["word"] = True
                else:
                    # Word Not End
                    parent[character]["attr"]["child"] = True                
                parent = parent[character]
        if _DEBUG:
            print tree
        return tree

    # @param sentence String
    # @param worldlib Array of String
    def analysis(self, sentence):        
        splited = []
        start = 0
        while start < len(sentence):
            matched_length = self.max_matched_length(sentence[start:])
            start += matched_length            
            splited.append(matched_length)
        if _DEBUG:
            print(splited)
        return self._split_by_length(splited, sentence)

    def _to_utf8(self, sentence):
        # TODO convert sentence to utf8
        return sentence


    # return Max Matched Length
    def max_matched_length(self, characters):
        parent = self.word_tree
        last_word_index = 0 # first character could be a word        
        for index, character in enumerate(characters):
            if (parent.get(character, None) != None):
                if parent[character]["attr"]["word"]:
                    last_word_index = index          
                parent = parent[character]  
            else:
                # exit
                return last_word_index + 1
        return last_word_index + 1

    def _split_by_length(self, lengths, sentence):
        words = []
        start = 0
        for l in lengths:
            words.append(sentence[start:start + l])
            start += l
        return words


'''
python
import MaxMatch
mm = MaxMatch.MaxMatcher(["a", "b", "ab", "as", "abnomal", "ddd"])
mm.analysis("abnomaldasfcasredddf")




'''