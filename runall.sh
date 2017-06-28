#!/bin/bash

DSNAME="${1:-google}"

./parsejson.py \
	--whoami ../measurements/datasets/$DSNAME/whoami.json.gz \
	--ping ../measurements/datasets/$DSNAME/ping.json.gz \
	--traceroute ../measurements/datasets/$DSNAME/traceroute.json.gz \
	--ipv6 ../measurements/datasets/$DSNAME/v6only.json.gz \
	--qname ../measurements/datasets/$DSNAME/qname.json.gz \
	--tcp ../measurements/datasets/$DSNAME/tcp.json.gz \
	--hostname ../measurements/datasets/$DSNAME/ch_hostname.bind.json.gz \
	--version ../measurements/datasets/$DSNAME/ch_version.bind.json.gz \
	--serverid ../measurements/datasets/$DSNAME/ch_id.server.json.gz \
	--dsfail ../measurements/datasets/$DSNAME/dnssec-failed.json.gz \
	--dnskey ../measurements/datasets/$DSNAME/dnskey.json.gz \
	--nxd ../measurements/datasets/$DSNAME/nxdomain.json.gz \
	> ../measurements/datasets/$DSNAME.arff

