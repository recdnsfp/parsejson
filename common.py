def safe(s):
	if not s or s == None or s == "None": return "?"
	s = str(s)
	s = s.replace("\n", " ")
	s = s.replace("\\", "")
	s = s.replace(",", "")
	if s[0] != '"': s = '"' + s + '"'
	return s
