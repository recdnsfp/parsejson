import base64
import dnslib # sudo pip install dnslib
import re
import libgeoip
import common

## called once before .each()
def init(results):
	print "% whoami.py"
	print "@attribute whoami_rt numeric  %% response time"
	print "@attribute whoami_ip string   %% resolver ip address"
	print "@attribute whoami_asn numeric %% resolver asn"
	print "@attribute whoami_net string  %% resolver network name"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	if len(rr.rr) < 2 or not rr.rr[1].rdata: return fail()
	ip = str(rr.rr[1].rdata)
	asn, name = libgeoip.lookup(ip)

	return "%.1f,%s,%d,%s" % (
		res['rt'],
		common.safe(ip),
		asn,
		name
	)

def fail(): return "-1,?,-1,?"
