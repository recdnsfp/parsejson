#!/usr/bin/env python

import pickle
import argparse
import ArffReader
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# read samples
def read_samples(path):
	ar = ArffReader.ArffReader(open(path))
	ids = []
	X = []
	Y = []
	for obj in ar:
		x = []
		for f in ar.fields:
			v = -1
			if f == 'dsfail_rt': v = float(obj[f])
			elif f == 'dsfail_rdata': continue
			elif f == 'nxd_rt': v = float(obj[f])
			elif f == 'dnskey_rt': v = float(obj[f])
			elif f == 'nsid_rt': v = float(obj[f])
			elif f == 'chaos1_rt': v = float(obj[f])
			elif f == 'chaos1_resp': continue
			elif f == 'chaos2_rt': v = float(obj[f])
			elif f == 'chaos2_resp': continue
			elif f == 'whoami_rt': v = float(obj[f])
			elif f == 'whoami_ip': continue
			elif f == 'ipv6_rt': v = float(obj[f])
			else: v = int(obj[f])
			x.append(v)

		X.append(x)
		Y.append(int(obj['ok']))
		ids.append(int(obj['probe_id']))

	print "%s: read %d samples" % (path, len(X))
	return (ids, X, Y)

# train and optionally store
def train(X, Y, store):
	rf = RandomForestClassifier(n_jobs=-1)
	rf.fit(X, Y)

	if store:
		pickle.dump(rf, open(store, "wb"))

	return rf

def load(path):
	return pickle.load(open(path, "rb"))

def test(rf, ids, X, Y):
	ok = 0
	err = 0

	labels = rf.classes_
	P = rf.predict_proba(X)
	for pid, x, proba, y in zip(ids, X, P, Y):
		i = np.argmax(proba)
		l = labels[i]

		if proba[i] < 1:
			print "probability for id %d being %d is %g" % (pid, l, proba[i])

		if l == y:
			ok += 1
		else:
			print "error: %d is %s, not %s" % (pid, y, l)
			err += 1

	return (ok, err)

def main():
	prs = argparse.ArgumentParser(description='Train/test DNS rec. server model')
	prs.add_argument('--train', help='path to ARFF training file')
	prs.add_argument('--store', help='where to store the model')
	prs.add_argument('--load', help='where to load the model from')
	prs.add_argument('--test', help='path to ARFF testing file')
	args = prs.parse_args()

	Xtr, Ytr = None, None
	Xte, Yte = None, None
	rf = None

	if args.train:
		trids, Xtr, Ytr = read_samples(args.train)
		rf = train(Xtr, Ytr, args.store)

	if args.load:
		rf = load(args.load)

	if not rf: die("please specify --train or --load")

	if args.test:
		teids, Xte, Yte = read_samples(args.test)
		ok, err = test(rf, teids, Xte, Yte)

		print "test: ok=%d   err=%d" % (ok, err)

if __name__ == "__main__": main()
