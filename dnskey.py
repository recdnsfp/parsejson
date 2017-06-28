import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% dnskey.py"
	print "@attribute dnskey_rt numeric    %% response time"
	print "@attribute dnskey_size numeric  %% response size"
	print "@attribute dnskey_flags numeric %% header bit flags (decimal)"
	print "@attribute dnskey_rcode numeric %% response code"
	print "@attribute dnskey_qcount numeric %% query count"
	print "@attribute dnskey_acount numeric %% answer count"
	print "@attribute dnskey_nscount numeric %% authority count"
	print "@attribute dnskey_arcount numeric %% additional count"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	return "%.1f,%d,%d,%d,%d,%d,%d,%d" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode,
		rr.header.q,
		rr.header.a,
		rr.header.auth,
		rr.header.ar
	)
