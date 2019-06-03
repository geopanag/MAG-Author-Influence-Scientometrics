import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir("/storage/scientometrics/data")

pap_auth = pd.read_csv("paper_author.txt")
pap_auth["AuthID"] = pap_auth["AuthID"].astype(str)
pap_auth["AuthID"] = pap_auth["AuthID"].astype(str)

#---- authors with only one paper:
one_paper_auth = pap_auth.groupby("AuthID").agg("count").reset_index()
one_paper_auth = one_paper_auth.loc[one_paper_auth["PapID"]==1,"AuthID"]

print(str(one_paper_auth.shape[0]*100/len(pap_auth["AuthID"].unique()))+" percent of the unique authors have only one paper")

auth = pd.read_csv("ambiguous_authors.txt")
auth = auth.drop(auth.columns[1],1)
auth["id"] = auth["id"].astype(str)

#---- unique ambiguous author names
print(auth.shape[0])

#----- All the ambiguous authors with one paper 
one_paper_auth = auth.merge(one_paper_auth.to_frame(name="id"),on = "id")
#----- All the ambiguous authors with papers 
ambig_pap_auth = auth.merge(pap_auth,left_on="id",right_on="AuthID")


#----- Join tables to have: paper, ambiguous_author, one-paper author or not 
one_paper_auth.columns = ["id","name_one_paper"] 
ambig_pap_auth = one_paper_auth.merge(ambig_pap_auth,left_on="id",right_on="AuthID",how="right")


ambig_pap_auth["name_one_paper"] = ambig_pap_auth["name_one_paper"].astype(str).apply(lambda x:x.replace(".0",""))

# Rows with NAN belong to ambiguous authors that have more than one paper (they werent in the one pap auth)
wh = ambig_pap_auth["name_one_paper"]=="nan"

# author-paper rows of ambiguous authors with more than one papers
sum(wh)

# to be removed
sum(~wh)

x = ambig_pap_auth.loc[-wh,"AuthID"].unique()

x.to_csv("ambig_one_paper_authors.csv",index=False,header=False)

ambig_pap_auth.loc[wh,"name_one_paper"]  = ambig_pap_auth.loc[wh,"AuthID"] 

#--- Signify who is a one-paper id (0) and who is not (1)
#wh = auths["name_id"] == auths["AuthID"]
ambig_pap_auth.loc[:,"AuthID"]  = 0
ambig_pap_auth.loc[wh,"AuthID"] = 1
ambig_pap_auth.columns=["ID","PapID","OnePaper"]
ambig_pap_auth.to_csv("ambig_authors_papers.txt",index=False)



sum(auths["label"]==0)
auths.shape

# Percentage of authors with 1 paper
to_remove = pd.read_csv("ambig_authors_papers.txt")
to_remove.columns = ["AuthID","PapID","label"]
to_remove = to_remove.loc[to_remove["label"]==1,"AuthID"].unique()
t = auth.loc[~auth["id"].isin(to_remove),:]



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
