#! /usr/bin/python

import sys
import operator

#GLOBALS
REMOVE_PUNC = True
PUNCTUATION = [ch for ch in """(){}[]<>!?.:;,`'"@#$%^&*+-|=~/\\_"""]
OTHER_SYM = ['``']
WINDOW_SIZE = 1
FEATURE_SIZE = 250

PUNCTUATION.extend(OTHER_SYM)

def _usage():
	print
	print "Usage : python co-occurence.py <tokenized_data> <mode> (stopwords_list)"
	print
	print "<tokenized_data> : path to the tokenized data file"
	print
	print "<mode> : "
	print "\t 1 - default"
	print "\t 2 - remove stop words"
	print "\t 3 - use top 50 unigrams as stop words"
	print
	print "(stopwords_list) : argument reqd iff mode=2"
	print

def choose_features(tokens, stops):
	unigrams = {}
	for token in tokens:
		token = unicode(token, 'utf-8')

		if stops and token in stops:
			continue

		if REMOVE_PUNC and token in PUNCTUATION:
			continue

		freq = unigrams.get(token, 0)+1
		unigrams[token] = freq
	sorted_list = sorted(unigrams.items(), key=operator.itemgetter(1), reverse=True)
	features = [feature[0] for feature in sorted_list[0:FEATURE_SIZE]]
	return features

def initialize_features(tokens, features):
	weight = {}
	for feature in features:
		weight['L-' + feature] = 0
		weight['R-' + feature] = 0
	
	embeddings = {}
	for token in tokens:
		embeddings[token] = dict(weight)
	
	return embeddings

def compute_features(tokens, features):
	embeddings = initialize_features(tokens, features)

	i = 0
	while i < len(tokens):
		j=1
		token = tokens[i]
		while j <= WINDOW_SIZE:
			left = ''
			right = ''
			if i-j >= 0:
				left = tokens[i-j]
			if i+j < len(tokens):
				right = tokens[i+j]
			if left in features:
				embeddings[token]['L-' + left] += 1
			if right in features:
				embeddings[token]['R-' + right] += 1
			j += 1
		i += 1

	return embeddings

def co_occurrence(TOKENFILE, MODE, STOPFILE=None):
	tokens = []
	stops = []
	
	if MODE == 2:
		assert(STOPFILE is not None)
		fp = open(STOPFILE, 'r')
		stops = [x.strip('\n').lower() for x in fp.readlines()]
		fp.close()

	fp = open(TOKENFILE, 'r')
	tokens = [x.strip('\n').lower() for x in fp.readlines()]
	fp.close()

	features = choose_features(tokens, stops)
	if MODE == 3:
		stops = features[:50]
		features = choose_features(tokens, stops)
	embeddings = compute_features(tokens, features)
	return embeddings

def main():
	if len(sys.argv)<3 \
	or len(sys.argv)>4 \
	or (sys.argv[2] not in ['1', '2', '3']) \
	or (sys.argv[2] == '2' and len(sys.argv) != 4):
		_usage()
	
	TOKENFILE = sys.argv[1]
	MODE = int(sys.argv[2])
	STOPFILE = ''
	if MODE == 2:
	 	STOPFILE = sys.argv[3]
	print co_occurrence(TOKENFILE, MODE, STOPFILE)
	
if __name__ == "__main__":
	main()
