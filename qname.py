import base64
import dnslib # sudo pip install dnslib
import common

## called once before .each()
def init(results):
	print "% qname.py"
	print "@attribute qname_rt numeric   %% reply time"
	print "@attribute qname_size numeric %% size of the reply"
	print "@attribute qname_ok numeric   %% 1 if letter case ok"
	print "@attribute qname_rdata string %% rdata of first reply"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	if str(rr.a.rname): # == "FaCeBoOk.cOm.":
		ok = 1
	else:
		ok = 0

	return "%.1f,%d,%d,%s" % (
		res['rt'],
		res['size'],
		str(rr.a.rname) == "FaCeBoOk.cOm.",
		common.safe(rr.a.rdata)
	)

#def fail(): return "-1,-1,-1,?"
