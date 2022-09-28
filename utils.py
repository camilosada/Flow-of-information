import os, requests
import numpy as np
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

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


def plot_raster(dat_raster,trial_dat_raster_ST,i_trial,idx):

        fig,ax = plt.subplots(figsize=(6, 3))

        # evets
        ax.vlines(0.5,0,trial_dat_raster_ST.shape[0],color='c')
        ax.vlines((dat_raster['reaction_time'][idx[i_trial]][0]/1000)+0.5,0,trial_dat_raster_ST.shape[0],color='b')
        ax.vlines(dat_raster['gocue'][idx[i_trial]]+0.5,0,trial_dat_raster_ST.shape[0],color='g')
        ax.vlines(dat_raster['response_time'][idx[i_trial]]+0.5,0,trial_dat_raster_ST.shape[0],color='k')
        ax.vlines(dat_raster['feedback_time'][idx[i_trial]]+0.5,0,trial_dat_raster_ST.shape[0],color='m')
        # raster
        ax.eventplot(trial_dat_raster_ST[:,i_trial], color=".2")

        ax.legend(['stimulus onset','reaction_time','gocue', 'response_time', 'feedback_time'], fontsize=9)
        ax.set(xlabel="Time (s)", ylabel='Neurons')
        fig.tight_layout(pad=0.2, h_pad=1.3, w_pad=1.3)