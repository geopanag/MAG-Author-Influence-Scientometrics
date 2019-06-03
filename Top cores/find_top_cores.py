import os
os.chdir("/storage/dcore/")

f = open("all_names.txt","r")

core_sizes = {}
with open("core_sizes_all.csv", "r") as cf:
    for line in cf:
        line = line.replace("\n", "").split()
        core_sizes[line[0] + "_" + line[1]] = int(line[2])

m_in = 0
m_out = 0
bci = 0
oci = 0
oci_cores = [0,0]
for l in f:
    parts = l.replace(".txt","").split("_")
    cin= int(parts[1])
    cout= int(parts[2])
    if core_sizes.get(str(cin) + "_" + str(cout), 0) == 0:
        continue        
    # biggest incore with the biggest possible outcore (lowest frontier)
    if(cin ==7850):
        if(cout>m_out): 
            m_out=cout
    # highest frontier
    if(cout == 7900):
        if(cin>m_in):
            m_in=cin
    # where the frontier intersects the diagonal
    if(cin==cout and cin>bci):
        bci = cin
    # where the frontier intersects the diagonal
    if((float(cin+cout))/2>oci):
        oci_cores =[cin,cout]
        oci = float(cin+cout)/2
