import base64
import dnslib # sudo pip install dnslib
import libgeoip

## called once before .each()
def init(results):
	print "% nxdomain.py"
	print "@attribute nxd_rt numeric    %% response time"
	print "@attribute nxd_size numeric  %% response size"
	print "@attribute nxd_flags numeric %% header bit flags (decimal)"
	print "@attribute nxd_rcode numeric %% response code"
	print "@attribute nxd_rdata string  %% rdata of first answer"
	print "@attribute nxd_asn numeric   %% answer ASN"
	print "@attribute nxd_name string   %% answer network name"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	ip = str(rr.a.rdata) if rr.a.rdata else "?"
	asn, name = libgeoip.lookup(ip)

	return "%.1f,%d,%d,%d,%s,%d,%s" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode,
		ip,
		asn,
		name
	)

def fail(): return "-1,-1,-1,-1,?,-1,?"
