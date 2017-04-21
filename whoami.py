import base64
import dnslib # sudo pip install dnslib
import GeoIP # sudo pip install geoip
import re

gi = GeoIP.open("/usr/local/share/GeoIP/GeoIPASNum.dat", GeoIP.GEOIP_STANDARD) # wget http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz

## called once before .each()
def init(results):
	print "% whoami.py"
	print "@attribute whoami_rt numeric %% response time"
	print "@attribute whoami_ip string %% resolver ip address"
	print "@attribute whoami_asn numeric %% resolver asn"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	abuf = base64.b64decode(res['abuf'])
	rr = dnslib.DNSRecord.parse(abuf)

 	if rr.a.rdata:
		ip = str(rr.a.rdata)
		g_as = gi.org_by_addr(ip)
		if g_as == None:
			asn = 0
		else:
			m = re.search('AS(\d+)\s+(.*)', g_as)
			asn = int(m.group(1))
			#as_descr = m.group(2)
	else:
		ip = "N/A"
		asn = 0

	return "%g,%s,%d" % (
		res['rt'],
		ip,
		asn
	)
