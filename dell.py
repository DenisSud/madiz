import sys

nf = sys.argv[1]
nmb = sys.argv[2]
nnf = sys.argv[3]
ss = sys.argv[4]
ms = []

with open(nf, "r") as f:
	for i in f:
		ms.append(i)
with open(nnf, "w") as f:
	for i in range(len(ms)):
		if i == int(nmb):
			f.write(ss)
			f.write("\n")
		else:
			f.write(ms[i])
