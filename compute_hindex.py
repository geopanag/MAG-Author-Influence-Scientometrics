import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir("/data/home/gpanagopoulos/scientometrics/data")

pap_auth = pd.read_csv("clean_paper_authors.txt")
pap_auth = pap_auth.loc[pap_auth["Cit"]!=0,:]
pap_auth["Cit"] = pap_auth["Cit"].apply(lambda x: [x])
pap_auth = pap_auth.drop(pap_auth.columns[0],axis=1)

pap_auth = pap_auth.groupby("AuthID").agg(sum).reset_index()

def compute_h_index(x):    
    tmp = x
    tmp.sort(reverse = True)
    if(len(tmp)==0):
        return 0 
    for i in range(len(tmp)):
        if(tmp[i]<i+1):
            i=i-1
            break
    return i+1

pap_auth["Hindex"] = pap_auth["Cit"].apply(compute_h_index)

hindex = pd.read_csv("hindex.txt")
authors = pd.read_csv("authors.txt")
dat = hindex.merge(authors,left_on="AuthID",right_on="id")
del dat["id"]

dat.shape #92191737

dat.to_csv("full_hindex.csv",index=False)

dat = dat.groupby("name").agg(max).reset_index()

dat.columns = ["author","hindex"]
dat["surname"] = dat["author"].apply(lambda x:x.split(" ")[-1])
dat.to_csv("final_hindex.csv",index=False)

dat.shape
dat[dat['name'].str.contains('barabasi')] # 128
dat[dat['name'].str.contains('karypis')] # 73
dat[dat['name'].str.contains('varlamis')] # 15
dat[dat['name'].str.contains('vazirg')] # 36
dat[dat['name'].str.contains('leskovec')] # 68