import os
import pandas as pd
os.chdir("/storage/dcore")

def find_top(dat,names,degree,name):
    dat.columns = ["incr"]
    names = dat.merge(names,on="incr")
    names["deg"] = degree.loc[bci_names.incr,"deg"].values  
    del names["incr"]
    del names["id"]
    names= names.sort_values("deg",ascending =False)
    names.to_csv("top_"+name+".csv",index=False)


names = pd.read_csv("incr_names.csv")
degree = pd.read_csv("/storage/mag10/auth_degree_10.txt",sep="\t",header=None)
degree.columns = ["out","in"]
degree["deg"]  = degree["out"]+degree["in"]

upper = pd.read_csv("core_540_7900.txt",header=None)
bci = pd.read_csv("core_5600_5600.txt",header=None)
oci = pd.read_csv("core_7600_7480.txt",header=None)

find_top(bci,names,degree,"bci")
find_top(oci,names,degree,"oci")
find_top(upper,names,degree,"upper")


upper.columns = ["incr"]
bci.columns = ["incr"]
oci.columns = ["incr"]
names = pd.read_csv("incr_names.csv")

upper = names.merge(upper,on="incr")
del upper["incr"]
bci = names.merge(bci,on="incr")
del bci["incr"]
oci = names.merge(oci,on="incr")
del oci["incr"]

oci.to_csv("oci_ids.csv",index=False)
bci.to_csv("bci_ids.csv",index=False)
upper.to_csv("upper_ids.csv",index=False)
