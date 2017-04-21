import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% chaos.py"
	print "@attribute chaos_rt numeric %% response time"
	print "@attribute chais_size numeric %% response size"
	print "@attribute chaos_rcode numeric %% response code"
	print "@attribute chaos_version_bind numeric %% request field"
	print "@attribute chaos_version_hostname numeric %% request field"
	print "@attribute chaos_resp string %% response string"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)

def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)
	rdata = "N/A" if not len(rr.rr) else rr.rr[0].rdata
	version_bind = 0 if not len(rr.questions) else int(str("_".join(list(rr.questions[0].qname.label))) == "version_bind")
	hostname_bind = 0 if not len(rr.questions) else int(str("_".join(list(rr.questions[0].qname.label))) == "hostname_bind")

	return "%g,%d,%d,%d,%d,%s" % (
		res['rt'],
		res['size'],
		rr.header.rcode,
		version_bind,
		hostname_bind,
		rdata
	)
