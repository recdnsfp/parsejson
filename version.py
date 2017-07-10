import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% version.py"
	print "@attribute version_rt numeric    %% response time"
	print "@attribute version_size numeric  %% response size"
	print "@attribute version_flags numeric %% header bit flags (decimal)"
	print "@attribute version_rcode numeric %% response code"
	print "@attribute version_resp string   %% rdata of first answer"

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
		(str(rr.a.rdata).replace("\n", " ") if rr.a.rdata else "?")
	)

def fail(): return "-1,-1,-1,-1,?"
