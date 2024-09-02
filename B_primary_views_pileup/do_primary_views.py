#import pandas as pd
import os
import sys
import pickle
from pathlib import Path
#from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, "/share/home/ychi/dev/")
from hires_utils.hires_utils.hires_io import parse_3dg
from hic_basic.structure.measure import primary_views

indir = "gs"
outfile = "s2728_primary_views.pkl"
ngrid = 32
cache_dir = "cache/"
#Nproc = 4

filis = os.listdir(indir)
samples = [i.split(".")[0] for i in filis]
filis = [os.path.join(indir,i) for i in filis]

def get_primary_views(fili, cache=True):
    data = parse_3dg(fili)
    print("Parsed %s" % fili)
    res = primary_views(data, ngrid, method="ray")
    print("Processing %s done." % fili)
    if cache:
        with open(cache_dir+Path(fili).stem+".pkl", "wb") as f:
            pickle.dump(res, f)
    return res
print("Start processing...")
#with ProcessPoolExecutor(Nproc) as executor:
#    res = executor.map(get_primary_views, filis)
ares = list(map(get_primary_views, filis))
print("All done.")
with open(outfile, "wb") as f:
    pickle.dump(dict(zip(samples,ares)), f)
