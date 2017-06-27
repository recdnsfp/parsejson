## called once before .each()
def init(results):
	print "% ping.py"
	print "@attribute ping_min numeric %% minimum ping RTT"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	return "%.1f" % el["min"]

def fail(): return "-1"
