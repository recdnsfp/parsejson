## called once before .each()
def init(results):
	print "@attribute dsfail_rt numeric"
	print "@attribute dsfail_size numeric"
	print "@attribute dsfail_ancount numeric"

## called for each element in result JSON
#   pid: probe id
#   el:  element of the result array
#   res: el[result] (just a shortcut)
def each(pid, el, res):
	return "%g,%d,%d" % (
		res['rt'],
		res['size'],
		res['ANCOUNT'])
