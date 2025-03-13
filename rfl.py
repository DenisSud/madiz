import sys

nf = sys.argv[1]

with open(nf, "r") as f:
	cnt = 0
	for i in f:
		print(cnt, i)
		cnt += 1
