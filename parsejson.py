#!/usr/bin/env python

import json
import argparse
from collections import defaultdict

import dsfail
import nxdomain

# call handler.main() for each JSON array element in given file path
def process(db, handler, path):
	fh = open(path)
	jsobj = json.load(fh)

	handler.init(jsobj)
	for el in jsobj:
		if "prb_id" not in el: continue
		if "result" not in el: continue
		pid = el['prb_id']
		res = el["result"]

		try:
			out = handler.each(pid, el, res)
			if out: db[pid] += "," + out
		except Exception, e:
			print "%% error for probe_id %d: %s" % (pid, e)
			continue

def main():
	prs = argparse.ArgumentParser(description='Parse the Atlas results')
	prs.add_argument('--dsfail', help='path to dnssec-failed.org results')
	prs.add_argument('--nxd', help='path to NXDOMAIN results')
	args = prs.parse_args()

	# print file header
	print "@relation 'parsejson'"
	print "@attribute probe_id numeric"

	# process the input files
	db = defaultdict(str)
	if args.dsfail: process(db, dsfail, args.dsfail)
	if args.nxd: process(db, nxdomain, args.dsfail)

	# print the results
	print "@data"
	for pid,out in db.iteritems():
		print "%d%s" % (pid, out)

if __name__ == "__main__": main()
