import os
os.chdir("/storage3/dcore")


with open("core_sizes_all.txt", 'r') as f:
	lines = [line.replace("\n", "").split() for line in f]
with open("dcore_image.csv", "w") as f:
	for line in lines:
		f.write(",".join([line[1], line[0], line[2]]) + "\n")

