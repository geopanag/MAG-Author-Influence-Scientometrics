import os
import pandas as pd
os.chdir("/storage/dcore")

names = pd.read_csv("incr_names.csv")
pad = pd.read_csv('author_frontiers_groupby.csv', sep=' ',header=None)
pad.columns = ["incr","frontier"]
dat = pad.merge(names,on="incr",how="right")

del dat["incr"]
del dat["id"]

dat["last"] = dat["name"].apply(lambda x:x.split()[-1])

dat = dat[["name","frontier","last"]]
dat.to_csv("frontiers.csv",index=False)