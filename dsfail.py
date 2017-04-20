import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "@attribute dsfail_rt numeric"
	print "@attribute dsfail_size numeric"
	print "@attribute dsfail_flags numeric %% header bit flags (decimal)"
	print "@attribute dsfail_rcode numeric %% response code"
	print "@attribute dsfail_qcount numeric %% query count"
	print "@attribute dsfail_acount numeric %% answer count"
	print "@attribute dsfail_nscount numeric %% authority count"
	print "@attribute dsfail_arcount numeric %% additional count"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	return "%g,%d,%s,%d,%d,%d,%d,%d" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode,
		rr.header.q,
		rr.header.a,
		rr.header.auth,
		rr.header.ar
	)
