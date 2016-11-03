
# Max Match Algorithm, Right-To-Left Order
# TODO Use more elegance function name and variable name


# @param sentence String
# @param worldlib Array of String
def analysis(sentence, wordlib):
	matched = ""
	left = sentence
	splited = []
	while len(left) > 0:
		matched, left = max_matched(left, wordlib)
		splited << matched
	return splited


# Extract the max matched word of the beginning of th sentence
# TODO optimize this algorithm, replace word array with word tree
# TODO Fix 技术总体 匹配  技术总监 和 技术 和 总体 ，这时应该切分为（技术|总体）
def max_matched(left, wordlib):
	matched = ""
	for character in left:
		to_be_matched = matched + character
		if is_match(to_be_matched, wordlib):
			matched = matched + character
		else:
			if matched == "":
				return character, left[1:-1]
			else:
				return matched, left[len(matched): -1]		


def max_matched(characters, word_tree):
	parent = word_tree
	word = ""
	last_word_index = 0 # first character could be a word
	for character, index in characters:
		if parent[character]:
			if parent[character]["attr"]["word"] = 1:
				last_word_index = index
			if parent[character]["attr"]["leaf"] = 1:
				exit_loop		
			parent = parent[character]
		else:
			exit_loop
	# pop laster word	



def get_matched_words(start_with, wordlib):
	matched = []
	for word in wordlib:
		if word[0:len(start_with)] == start_with:
			matched << word
	return matched


def is_match(to_be_matched, wordlib):
	if len(get_matched_words(to_be_matched, wordlib)) > 0:
		return true
	else:
		return false




def wordlib_to_tree(wordlib):
	tree = {}
	for word in wordlib:
		parent = tree
		for character,index in word:
			if parent[character] :
				if index == len(word):
					parent[character]["attr"]["word"] = 1
				else:
					parent[character]["attr"]["leaf"] = 0
			else:
				if index == len(word):
					parent[character] = {"attr": {"word": 0} }
				else:
					parent[character] = {"attr" : {"word": 1} }
			parent = parent[character]
	return tree
				






