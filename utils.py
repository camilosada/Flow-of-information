import os, requests
import numpy as np

def download_data(url,fname):

    for j in range(len(url)):
        if not os.path.isfile(fname[j]):
            try:
                r = requests.get(url[j])
            except requests.ConnectionError:
                print("!!! Failed to download data !!!")
            else:
                if r.status_code != requests.codes.ok:
                    print("!!! Failed to download data !!!")
                else:
                    with open(fname[j], "wb") as fid:
                        fid.write(r.content)


def load_data(fname):
    alldata = np.array([])
    for j in range(len(fname)):
        alldata = np.hstack((alldata, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))
    
    return alldata