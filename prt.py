import sys

nf = sys.argv[1]
ss = sys.argv[2]

with open(nf, "a") as f:
	f.write(ss)
	f.write("\n")
