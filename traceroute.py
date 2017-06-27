import GeoIP # sudo pip install geoip
import re

gi = GeoIP.open("/usr/share/GeoIP/GeoIPASNum.dat", GeoIP.GEOIP_STANDARD) # wget http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz

# private ip addresses
private_ips = (
	"127.", "192.168.", "10.",
	"172.16.", "172.17.", "172.18.", "172.19.",
	"172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
	"172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31."
)

## called once before .each()
def init(results):
	print "% traceroute.py"
	print "@attribute tr_hopcount numeric %% number of public-ip hops to target"
	print "@attribute tr_aslen numeric    %% number of distinct ASes on the path"
	print "@attribute tr_exit_rtt numeric %% exit AS: max. RTT"
	print "@attribute tr_exit_asn numeric %% exit AS: last known ASN before target"
	print "@attribute tr_exit_net numeric %% exit AS: network name"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	# for tracking
	hops = []
	aspath = []
	hopcount = 0
	lastx = False

	# go through all hops
	for hop in res:
		if "result" not in hop: continue

		# find the min rtt hop details
		mrtt = -1.0
		mip = None
		for mes in hop["result"]:
			if "rtt" not in mes:
				if mrtt >= 0.0: continue
				if "from" in mes:
					mip = mes["from"]
				else:
					mip = "*"
			elif mrtt < 0 or mes["rtt"] < mrtt:
				mrtt = mes["rtt"]
				mip = mes["from"]

		# not found? go to next hop
		if not mip: continue

		# * again?
		if mip == "*":
			if lastx: continue
			lastx = True

		# private addr?
		if mip.startswith(private_ips): continue

		# add to hops[]
		hops.append((mrtt, mip))

	# convert hops to aspath
	last_org = "?"
	last_rtt = -1
	for hop in hops:
		rtt, ip = hop
		if ip == "*": continue

		asn = -1
		name = "?"
		g_as = gi.org_by_addr(ip)
		if g_as:
			d = g_as.decode("iso-8859-1").encode("utf-8").split(" ")
			if len(d) > 0: asn  = int(d[0][2:])
			if len(d) > 1: name = "-".join(d[1:]).replace(",", "")

		# add?
		if last_org != name:
			aspath.append((rtt, ip, asn, name))
			last_org = name
			last_rtt = rtt
		elif name != "?" and last_rtt < rtt:
			aspath.pop()
			aspath.append((rtt, ip, asn, name))
			last_rtt = rtt

	# hop count
	if len(hops) == 0:
		hopcount = -1
	elif hops[-1][1] == "*":
		hopcount = -1
	else:
		hopcount = len(hops)

	# aspath len
	if len(aspath) == 0:
		aslen = -1
	elif aspath[-1][2] == -1:
		aslen = -1
	else:
		aslen = len(aspath)

	# last known asnum, name, and rtt
	ntl_rtt, ntl_ip, ntl_asn, ntl_name = -1, "", -1, "?"
	for i in range(2, len(aspath)+1):
		ntl_rtt, ntl_ip, ntl_asn, ntl_name = aspath[-i]
		if ntl_asn != -1: break

	return "%d,%d,%.1f,%d,%s" % (hopcount, aslen, ntl_rtt, ntl_asn, ntl_name)
#	print " > ".join(["%d (%s)" % (x[2], x[3]) for x in aspath]))

def fail(): return "-1,-1,-1,-1,?"
