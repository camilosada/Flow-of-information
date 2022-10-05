import os, requests
import numpy as np
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
import seaborn as sns

import config


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
 

def check_neuron_activation(neurons,passive_neurons):

    diff_n = ( neurons.mean(axis=2).T -  passive_neurons.mean(axis=2)[:,0]).T

    return np.where(diff_n> 0)


def select_areas_firing(data_area,mask_trials):

    areas = []#np.unique(data_area['brain_area'])
    areas_firing = []

    nareas = len(config.BRAIN_GROUPS)
    NN = len(data_area['brain_area'])  # number of neurons
    barea = 7 * np.ones(NN, )  # 7 is "other ctx", neurons that were not able to be classified
    for j in range(nareas):
        barea[np.isin(data_area['brain_area'], config.BRAIN_GROUPS[j])] = j  # assign a number to each region
    

    for j,i_narea in enumerate(np.unique(barea).astype(int)):
        if i_narea != 7:
            area_spks = data_area['spks'][barea==i_narea][:,mask_trials ]
            area_passive_spks = data_area['spks'][barea==i_narea][:, mask_trials]
            area_spks = area_spks[check_neuron_activation(neurons=area_spks,passive_neurons=area_passive_spks)].reshape(-1,250)#
            
            areas_firing.append(area_spks)#.mean(axis=0))#/max(area_spks.mean(axis=0)))
            areas.append(config.REGIONS[i_narea])
        
    return areas,areas_firing


def plot_areas_spks(firing_areas,areas_unique):
    fig,ax = plt.subplots(figsize=(14, 3))

    mean_firing_areas = np.zeros((len(firing_areas),firing_areas[0].shape[1]))

    for i in range(len(firing_areas)):
    
        mean_firing_areas[i] = np.array(firing_areas[i]).mean(axis=0)/max(np.array(firing_areas[i]).mean(axis=0))


    sns.heatmap(mean_firing_areas, vmin=0,ax=ax,cmap="Blues")#(dt * np.arange(NT), ) 
    ax.set_yticklabels(areas_unique, rotation=0)
    ax.vlines([50], *ax.get_ylim(),color='r')
    ax.vlines([79], *ax.get_ylim(),color='b')
    ax.vlines([110], *ax.get_ylim(),color='g')
    ax.vlines([159], *ax.get_ylim(),color='y')

    ax.plot(np.argmax(mean_firing_areas, axis=0)+0.5,color='k')

    plt.legend(['stimulus onset','reaction_time','gocue', 'response_time'], fontsize=9)
    ax.set(xlabel='timebins (10 ms)')
    fig.tight_layout(pad=0.2, h_pad=1, w_pad=1)
    plt.show()