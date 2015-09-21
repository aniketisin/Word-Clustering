#! /usr/bin/python

import math, sys, random, operator
import cooccurrence

#GLOBALS
K = 50
MIN_CHANGES = 10000
REP = 25

def distance(a, b, features): 
	dist = 0 
	for feat in features:
		dist += (float(a['L-'+feat])-float(b['L-'+feat]))**2
		dist += (float(a['R-'+feat])-float(b['R-'+feat]))**2
	dist = math.sqrt(dist)
	return dist

def initialize_centroids(embeddings):
	centroids = dict.fromkeys(range(0, K))
	samples = random.sample(embeddings.keys(), K)
	for i in range(0, K):
		centroids[i] = (embeddings[samples[i]], [])
	return centroids

def find_closest_centroid(embeddings, clusters, features):
	previous_cluster = []
	for i in range(0, K):
		previous_cluster.append(clusters[i][1])
		clusters[i] = (clusters[i][0], [])

	no_of_changes = 0
	for each in embeddings.keys():
		distances = []
		for i in range(0, K):
			distances.append(distance(embeddings[each], clusters[i][0], features))
		closest = distances.index(min(distances))
		if each not in previous_cluster[closest]:
			no_of_changes += 1
		clusters[closest][1].append(each)

	return no_of_changes

def _centroid(lst, features, embeddings):
	centroid = {}
	no_of_feats = len(features)
	for feat in features:
		l_feat = 'L-'+feat
		r_feat = 'R-'+feat
		mean = 0
		for i in xrange(len(lst)):
			mean += embeddings[lst[i]][l_feat]
		mean /= no_of_feats
		centroid[l_feat] = mean
		
		mean = 0
		for i in xrange(len(lst)):
			mean += embeddings[lst[i]][r_feat]
		mean /= no_of_feats
		centroid[r_feat] = mean
	return centroid

def recompute_centroids(clusters, features, embeddings):
	for i in range(0, K):
		points = clusters[i][1]
		clusters[i] = (_centroid(points, features, embeddings), points)
	return clusters

def kmeans(embeddings, features):
	print "START"
	clusters = initialize_centroids(embeddings)
	no_of_changes = find_closest_centroid(embeddings, clusters, features)
	print "ITER START"
	while no_of_changes > MIN_CHANGES:
		print no_of_changes
		printCluster(clusters, embeddings, features)
		clusters = recompute_centroids(clusters, features, embeddings)
		no_of_changes = find_closest_centroid(embeddings, clusters, features)

	return clusters

def find_rep(cluster, embeddings, features):
	reps = []
	if len(cluster[1]) <= REP:
		return cluster[1]

	centroid = cluster[0]
	distances = {}
	for each in cluster[1]:
		distances[each] = distance(centroid, embeddings[each], features)
	sorted_x = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
	reps = [x[0] for x in sorted_x[:25]]
	return reps

def printCluster(clusters, embeddings, features):
	for i in range(0, K):
		print find_rep(clusters[i], embeddings, features)

def main():
	if len(sys.argv)<3 \
		or len(sys.argv)>4 \
		or (sys.argv[2] not in ['1', '2', '3']) \
		or (sys.argv[2] == '2' and len(sys.argv) != 4): 
		cooccurrence._usage()

	TOKENFILE = sys.argv[1]
	MODE = int(sys.argv[2])
	STOPFILE = ''
	if MODE == 2:
		STOPFILE = sys.argv[3]
	tokens = []
	stops = []
	
	if MODE == 2:
		fp = open(STOPFILE, 'r')
		stops = [x.strip('\n').lower() for x in fp.readlines()]
		fp.close()

	fp = open(TOKENFILE, 'r')
	tokens = [x.strip('\n').lower() for x in fp.readlines()]
	fp.close()

	features = cooccurrence.choose_features(tokens, stops)
	if MODE == 3:
		stops = features[:50]
		features = cooccurrence.choose_features(tokens, stops)
	embeddings = cooccurrence.compute_features(tokens, features)
	clusters = kmeans(embeddings, features)
	printCluster(clusters, embeddings, features)

if __name__ == '__main__':
	main()
