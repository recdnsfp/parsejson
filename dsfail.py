import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% dsfail.py"
	print "@attribute dsfail_rt numeric"
	print "@attribute dsfail_size numeric"
	print "@attribute dsfail_flags numeric %% header bit flags (decimal)"
	print "@attribute dsfail_rcode numeric %% response code"
	print "@attribute dsfail_rdata string %% rdata of first reply"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	return "%g,%d,%d,%d,%s" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode,
		(rr.a.rdata if rr.a.rdata else "?")
	)

def fail(): return "-1,-1,-1,-1,?"
