# -*- coding: utf-8 -*-

import os 
import pandas as pd
import json

os.chdir("/storage/scientometrics/data")

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

f2 = open('incr_fil_mag10.csv','w')

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
  
maximum_id = len(authors)  
f.close()
f2.close()

print(maximum_id)

del authors
del mag
del keep

size = maximum_id+1
outneighs = [None] * size
inneighs = [None] * size
author_outdegree = [0] * size
author_indegree = [0] * size

print("now creating edgelists")

idx = 0
f = open("incr_fil_mag10.csv","r")


for line in f:
    idx+=1
    t=line.strip().split(',')
    
    #if max(t)>m:
    #    m = max(t)
    if(t[0]==t[1]):
        continue
        
    try:
        inneighs[int(t[1])].append(t[0])
    except:
        inneighs[int(t[1])] = [t[0]]    

    try:
        outneighs[int(t[0])].append(t[1])
    except:
        outneighs[int(t[0])] = [t[1]]
       
    try:
        author_indegree[int(t[1])]+=1
    except:
        author_indegree[int(t[1])] =1
         
    try:
        author_outdegree[int(t[0])]+=1
    except:
        author_outdegree[int(t[0])] =1

        
    if(idx%10000000==0):
        print(idx)
        
f.close()

#print(m) # must be 33m
#print(list(outneighs.keys())[-1])
#print(list(inneighs.keys())[-1])
#print(len(outneighs))
#print(len(inneighs))

f_in = open('mag_ingraph_10.txt','w')
f_out = open('mag_outgraph_10.txt','w')
f_deg = open('auth_degree_10.txt','w')

for i in range(0,size):
    try:
        f_in.write(str(i)+"\t"+"\t".join(inneighs[i])+"\n")
    except:
        f_in.write(str(i)+"\n")
        
    try:
        f_out.write(str(i)+"\t"+"\t".join(outneighs[i])+"\n")
    except:
        f_out.write(str(i)+"\n")
        
    f_deg.write(str(author_outdegree[i])+"\t"+str(author_indegree[i])+"\n")
        
    if(i%100000==0):
        print(i)
        
f_in.close()
f_out.close()
f_deg.close()
