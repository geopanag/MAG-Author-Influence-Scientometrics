# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:10:35 2019

@author: georg
"""

#https://stackoverflow.com/questions/31925572/python-pandas-merge-or-filter-dataframe-by-another-is-there-a-better-way

import os 
import pandas as pd
import json

os.chdir("/storage/scientometrics/data")
#names = pd.read_csv("ambig_one_paper_authors.csv",header=None)
#pap_auth = pd.read_csv("clean_paper_authors.txt",header=None)

#pap_auth.columns = ["paper","author"]
#names.columns = ["author"]

#pap_auth = pap_auth["author"].unique()
#pap_auth = pd.DataFrame(pap_auth)
#pap_auth.columns=["author"]
#pap_auth = pap_auth.set_index("author")
#to_keep = pap_auth[~pap_auth.index.isin(names.index)].reset_index()

keep = pd.read_csv("authors_to_keep.csv",header=None) 
keep.columns = ["id"]
keep = keep.set_index("id")

mag = pd.read_csv("reduced_mag10.csv",header=None)
mag.columns = ["in","out","weight"]
del mag["weight"]

#-- filter edges based on giver
mag = mag.sort_values(by=['in'])
mag = mag.set_index("in")

mag = mag[mag.index.isin(keep.index)].reset_index()
print("done in nodes")

#-- filter edges based on receiver
mag = mag.sort_values(by=['out'])
mag = mag.set_index("out")

mag = mag[mag.index.isin(keep.index)].reset_index()
print("done out nodes")

#-- remove self edges
mag = mag[mag['in'] != mag['out']]

mag.to_csv("filtered_mag10.csv",header=False,index=False)

# convert to incremental ids

mag = pd.read_csv("filtered_mag10.csv",header=None)
mag.columns = ["in","out"]
#del mag["idx"]
mag.to_csv("filtered_mag10.csv",header=False,index=False)

f2 = open('incr_filtered_mag10.csv','w')

authors = {}

idx = 0
for index, row in mag.iterrows():
    t = [str(row["in"]),str(row["out"])]
    
    try:
        id1 = authors[t[0]] 
    except:
        id1 = len(authors)
        authors[t[0]] = id1
        
    try:
        id2 = authors[t[1]]
    except:
        id2 = len(authors)
        authors[t[1]] = id2
        
    f2.write(str(id1)+","+str(id2)+"\n")
    if(idx%10000000==0):
        print(idx)
    idx+=1

with open('incr_authors10.json', 'w') as f:
    json.dump(authors, f)
    
f.close()
f2.close()
