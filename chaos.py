import base64
import dnslib # sudo pip install dnslib

chaos_counter = 0

## called once before .each()
def init(results):
	global chaos_counter
	chaos_counter += 1
	print "% chaos.py"
	print "@attribute chaos%d_rt numeric %% response time" % chaos_counter
	print "@attribute chaos%d_size numeric %% response size" % chaos_counter
	print "@attribute chaos%d_rcode numeric %% response code" % chaos_counter
	print "@attribute chaos%d_version_bind numeric %% request field" % chaos_counter
	print "@attribute chaos%d_version_hostname numeric %% request field" % chaos_counter
	print "@attribute chaos%d_resp string %% response string" % chaos_counter

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
