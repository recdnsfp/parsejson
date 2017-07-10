#!/usr/bin/env python

import json
import argparse
import gzip
import string
from collections import defaultdict

import dsfail
import nxdomain
import dnskey
import whoami
import whoami2
import ipv6
import ping
import traceroute
import qname
import tcp
import hostname
import version
import serverid

db = defaultdict(str)
db_counts = defaultdict(int)
db_count_max = 0

# call handler.main() for each JSON array element in given file path
def process(handler, path):
	global db_count_max

	if path.endswith(".gz"):
		fh = gzip.open(path)
	else:
		fh = open(path)
	jsobj = json.load(fh)
	db_count_max += 1

	handler.init(jsobj)
	for el in jsobj:
		if "prb_id" not in el: continue
		pid = el['prb_id']

		# a resultset? take first
		if "resultset" in el:
			ok = [x for x in el["resultset"] if "result" in x]
			if len(ok) > 0: el = ok[0]

		# is error?
		if "result" not in el:
			if "fail" in dir(handler):
				db[pid] += "," + handler.fail()
				db_counts[pid] += 1
			continue

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
	prs.add_argument('--ping', help='path to ping results')
	prs.add_argument('--traceroute', help='path to traceroute results')
	prs.add_argument('--ipv6', help='path to ipv6 results')
	prs.add_argument('--qname', help='path to qname case results')
	prs.add_argument('--tcp', help='path to TCP results')
	prs.add_argument('--hostname', help='path to CHAOS hostname.bind results')
	prs.add_argument('--version', help='path to CHAOS version.bind results')
	prs.add_argument('--serverid', help='path to CHAOS id.server results')
	prs.add_argument('--dsfail', help='path to dnssec-failed.org results')
	prs.add_argument('--dnskey', help='path to DNSKEY results')
	prs.add_argument('--nxd', help='path to NXDOMAIN results')
	prs.add_argument('--whoami', help='path to whoami results')
	prs.add_argument('--whoami2', help='path to whoami2 results')
	args = prs.parse_args()

	# print file header
	print "@relation 'parsejson'"
	print "@attribute probe_id numeric"

	# process the input files
	if args.ping: process(ping, args.ping)
	if args.traceroute: process(traceroute, args.traceroute)
	if args.ipv6: process(ipv6, args.ipv6)
	if args.qname: process(qname, args.qname)
	if args.tcp: process(tcp, args.tcp)
	if args.hostname: process(hostname, args.hostname)
	if args.version: process(version, args.version)
	if args.serverid: process(serverid, args.serverid)
	if args.dsfail: process(dsfail, args.dsfail)
	if args.dnskey: process(dnskey, args.dnskey)
	if args.nxd: process(nxdomain, args.nxd)
	if args.whoami: process(whoami, args.whoami)
	if args.whoami2: process(whoami2, args.whoami2)

	# print the results
	printable = set(string.printable)
	print "@data"
	for pid,out in db.iteritems():
		if db_counts[pid] == db_count_max:
			print "%d%s" % (pid, filter(lambda x: x in printable, out))
#		else:
#			print "%% %d skipped - not present in all files" % (pid)

if __name__ == "__main__": main()
