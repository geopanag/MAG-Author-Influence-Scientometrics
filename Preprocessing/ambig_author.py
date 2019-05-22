import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir("/data/home/gpanagopoulos/scientometrics/data")

auth = pd.read_csv("authors.txt")
auth = auth.ix[auth.columns[0,2]]
# the unique display names are 83209107 and the normalized are 60m
idx = auth.iloc[:,1].apply(lambda x:x[0]<"a" or x[0]>"z")
auth=auth[~idx]
auth.to_csv("authors.txt",index=False)
auth.head(10)

print(len(p))
#auth = pd.read_csv("authors.txt")
ambig_names = auth.groupby('name').id.count()
print(len(ambig_names)) #out of the 63368053
p = ambig_names[ambig_names>1]
print(len(p)) # 23427411 have more then 1 id


plt.plot(p.values,color='b')
plt.xticks([])
#plt.set_size_inches(20, 11)
plt.xlabel('Unique Names', fontsize=15)
plt.ylabel('Number of IDS', fontsize=15)
#%matplotlib inline
#plt.savefig('../figures/ambiguous_names.pdf',figsize=(30,30))
plt.tight_layout()
#plt.figure(figsize=(20, 20))
plt.savefig('../figures/ambiguous_names.pdf')#, bbox_inches = 'tight')


#-- Find ambiguous names and add name specific id to each one
ambig_names = auth.groupby('name').id.count()
ambig = ambig_names[ambig_names.where(ambig_names>1).notnull()].index
ambig_names = pd.DataFrame({'name': ambig, 'id': range(0,len(ambig))})
auth = auth.merge(ambig_names, on='name')
auth.head(10)

auth.columns=["id","name","name_id"]
auth.to_csv("ambiguous_authors.txt",index=False)


#---- Keep only specific columns from paper authors
pap_auth = pd.read_csv("PaperAuthor.txt",sep="\t",header=None)
pap_auth = pap_auth[pap_auth.columns[[0,1]]]
pap_auth.columns = ["PapID","AuthID"]
pap_auth.to_csv("paper_author.txt",index=False)