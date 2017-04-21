
## called once before .each()
def init(results):
	print "% probes.py"
	print "@attribute probe_cc string %% probe country code"
	print "@attribute probe_asn string %% probe asn"


## called for each element in result JSON
#   pid: probe id
#   el:  element of the array containing probes data
def each(pid, el):
	asn = el["asn_v4"]
	cc = el["country_code"]
	if asn == None:
		asn = "N/A"
	if cc == None:
		cc = "N/A"
	return "%s,%s" % (
		cc,
		asn
	)
