#!/usr/bin/env python

import json
import argparse
from collections import defaultdict

import dsfail
import nxdomain
import dnskey
import nsid
import chaos
import whoami
import ipv6

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
	for el in jsobj:
		if "prb_id" not in el: continue
		if "result" not in el: continue
		pid = el['prb_id']
		res = el["result"]

		try:
			out = handler.each(pid, el, res)
			if out:
				db[pid] += "," + out
				db_counts[pid] += 1
		except Exception, e:
			print "%% error for probe_id %d: %s" % (pid, e)
			continue

def main():
	prs = argparse.ArgumentParser(description='Parse the Atlas results')
	prs.add_argument('--dsfail', help='path to dnssec-failed.org results')
	prs.add_argument('--nxd', help='path to NXDOMAIN results')
	prs.add_argument('--dnskey', help='path to DNSKEY results')
	prs.add_argument('--nsid', help='path to NSID results')
	prs.add_argument('--chaos', nargs='+', help='path to CHAOS results')
	prs.add_argument('--whoami', help='path to whoami results')
	prs.add_argument('--ipv6', help='path to ipv6 results')
	args = prs.parse_args()

	# print file header
	print "@relation 'parsejson'"
	print "@attribute probe_id numeric"

	# process the input files
	if args.dsfail: process(dsfail, args.dsfail)
	if args.nxd: process(nxdomain, args.nxd)
	if args.dnskey: process(dnskey, args.dnskey)
	if args.nsid: process(nsid, args.nsid)
	if args.chaos: # XXX: --chaos file1 --chaos file2
		for arg in args.chaos: process(chaos, arg)
	if args.whoami: process(whoami, args.whoami)
	if args.ipv6: process(ipv6, args.ipv6)

	# print the results
	print "@data"
	for pid,out in db.iteritems():
		if db_counts[pid] == db_count_max:
			print "%d%s" % (pid, out)
#		else:
#			print "%% %d skipped - not present in all files" % (pid)

if __name__ == "__main__": main()
