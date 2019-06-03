import json
import os

os.chdir("/storage/mag10")

with open("incr_authors10.json","r") as f:
    auth = json.load(f)
    
f2 = open("incr_auth_dict.txt","w")
for key, value in auth.items():
    f2.write(key+" "+value+"\n")
f2.close()
