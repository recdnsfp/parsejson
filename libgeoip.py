import GeoIP # sudo pip install geoip
import re
import string

geoip = GeoIP.open("/usr/share/GeoIP/GeoIPASNum.dat", GeoIP.GEOIP_STANDARD) # wget http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
pattern = re.compile('\W+')

def lookup(ip):
	asn = -1
	name = "?"
	res = geoip.org_by_addr(ip)
	if res:
		d = res.decode("iso-8859-1").encode("utf-8").split(" ")
		if len(d) > 0:
			asn = int(d[0][2:])
		if len(d) > 1:
			name = pattern.sub("", "_".join(d[1:])).upper()

	return (asn, name)
