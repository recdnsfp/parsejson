import libgeoip

## called once before .each()
def init(results):
	print "% ping.py"
	print "@attribute ping_min numeric %% minimum ping RTT"
	print "@attribute ping_from string %% ping source IP"
	print "@attribute ping_asn numeric %% source ASN"
	print "@attribute ping_net string  %% source network name"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	ip = el["from"] if "from" in el else "?"
	asn, name = libgeoip.lookup(ip)

	return "%.1f,%s,%d,%s" % (el["min"], ip, asn, name)

def fail(): return "-1,?,-1,?"
