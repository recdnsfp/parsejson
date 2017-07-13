import base64
import dnslib # sudo pip install dnslib
import common

## called once before .each()
def init(results):
	print "% serverid.py"
	print "@attribute serverid_rt numeric    %% response time"
	print "@attribute serverid_size numeric  %% response size"
	print "@attribute serverid_flags numeric %% header bit flags (decimal)"
	print "@attribute serverid_rcode numeric %% response code"
	print "@attribute serverid_resp string   %% rdata of first answer"

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
		common.safe(rr.a.rdata)
	)

def fail(): return "-1,-1,-1,-1,?"
