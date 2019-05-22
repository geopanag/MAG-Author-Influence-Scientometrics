import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir("/data/home/gpanagopoulos/scientometrics/data")

#----------- 
pap_auth = pd.read_csv("paper_author.txt")
pap_auth = pap_auth.drop(pap_auth.columns[0],axis=1)
to_remove = pd.read_csv("ambig_authors_papers.txt")
to_remove.columns = ["AuthID","PapID","label"]

#--- Get the ids of authors with one paper and ambiguous names
to_remove = to_remove.loc[to_remove["label"]==0,"AuthID"].unique()

#----- Remove ambiguous authors from paper authors
pap_auth = pap_auth.loc[~pap_auth["AuthID"].isin(to_remove),:]

#------ Merge pap_auth and pap to get the citations
pap = pd.read_csv("papers_processed.txt",sep=";", encoding = "ISO-8859-1") 
#- Keep only cit and PapID
pap = pap.drop(pap.columns[[1,3,4]],axis=1)

pap_auth = pap.merge(pap_auth,on="PapID")

pap_auth.to_csv("clean_paper_authors.txt",index=False)

