import base64
import dnslib # sudo pip install dnslib
import re
import libgeoip
import json

## called once before .each()
def init(results):
	print "% whoami2.py"
	print "@attribute whoami2_rt numeric  %% response time"
	print "@attribute whoami2_ip string   %% resolver ip address"
	print "@attribute whoami2_asn numeric %% resolver asn"
	print "@attribute whoami2_net string  %% resolver network name"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)
	if len(rr.rr) < 1 or not rr.rr[0].rdata: return fail()
	j = json.loads(str(rr.rr[0].rdata)[1:-1])
	ip = j['ip']
	asn, name = libgeoip.lookup(ip)

	return "%.1f,%s,%d,%s" % (
		res['rt'],
		ip,
		asn,
		name
	)

def fail(): return "-1,?,-1,?"
