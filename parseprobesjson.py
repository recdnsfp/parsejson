#!/usr/bin/env python

import json
import argparse
from collections import defaultdict

import probes

db = defaultdict(str)
db_counts = defaultdict(int)
db_count_max = 0

# call handler.main() for each JSON array element in given file path
def process(handler, path):
	global db_count_max

	fh = open(path)
	jsobj = json.load(fh)
	db_count_max += 1

	handler.init(jsobj)
	for el in jsobj["objects"]:

		pid = el["id"]

		out = handler.each(pid, el)
		if out:
			db[pid] += "," + out
			db_counts[pid] += 1


def main():
	prs = argparse.ArgumentParser(description='Parse the Atlas probes database')
	prs.add_argument('--probes', help='path to probes database')
	args = prs.parse_args()

	# print file header
	print "@relation 'parseprobejson'"
	print "@attribute probe_id numeric"

	# process the input files
	if args.probes: process(probes, args.probes)

	# print the results
	print "@data"
	for pid,out in db.iteritems():
		if db_counts[pid] == db_count_max:
			print "%d%s" % (pid, out)
#		else:
#			print "%% %d skipped - not present in all files" % (pid)

if __name__ == "__main__": main()
