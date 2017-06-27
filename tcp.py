import base64
import dnslib # sudo pip install dnslib

## called once before .each()
def init(results):
	print "% tcp.py"
	print "@attribute tcp_rt numeric      %% reply time"
	print "@attribute tcp_size numeric    %% size of the reply"
	print "@attribute tcp_flags numeric   %% header bit flags (decimal)"
	print "@attribute tcp_rcode numeric   %% response code"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

	return "%.1f,%d,%d,%d" % (
		res['rt'],
		res['size'],
		rr.header.bitmap,
		rr.header.rcode
	)

def fail(): return "-1,-1,-1,-1"
