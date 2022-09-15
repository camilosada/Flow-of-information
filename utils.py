import os, requests
import numpy as np
from sklearn.preprocessing import StandardScaler

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


def z_score(X):
    # X: ndarray, shape (n_features, n_samples)
    ss = StandardScaler(with_mean=True, with_std=True)
    Xz = ss.fit_transform(X.T).T
    return Xz


def select_areas(regions,data,barea):

    all_dat_area=[]
    for region in regions:
        dat_area = data['spks'][barea==region]

        all_dat_area.append(dat_area)

    return all_dat_area