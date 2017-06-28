import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% ipv6.py"
	print "@attribute ipv6_rt numeric    %% response time"
	print "@attribute ipv6_size numeric  %% response size"
	print "@attribute ipv6_flags numeric %% header bit flags (decimal)"
	print "@attribute ipv6_rcode numeric %% response code"
	print "@attribute ipv6_rdata string  %% rdata of first reply"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	return "%.1f,%d,%d,%d,%s" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode,
		(rr.a.rdata if rr.a.rdata else "?")
	)

def fail(): return "-1,-1,-1,-1,?"
