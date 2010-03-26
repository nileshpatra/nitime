#!/usr/bin/python

#Imports as before:
import numpy as np
from matplotlib.pyplot import figure,legend
from matplotlib.mlab import csv2rec
from nitime.timeseries import UniformTimeSeries
from nitime.utils import percent_change
import nitime.viz
reload(nitime.viz)
from nitime.viz import drawgraph_roi,matshow_roi

#This time Import the coherence analyzer 
from nitime.analysis import CoherenceAnalyzer

#This part is the same as before
TR=1.89
data_rec = csv2rec('data/fmri_timeseries.csv')
roi_names= np.array(data_rec.dtype.names)
n_samples = data_rec.shape[0]
data = np.zeros((len(roi_names),n_samples))

for n_idx, roi in enumerate(roi_names):
   data[n_idx] = data_rec[roi]

data = percent_change(data)
T = UniformTimeSeries(data,sampling_interval=TR)
T.metadata['roi'] = roi_names 
C = CoherenceAnalyzer(T)

#We look only at frequencies between 0.02 and 0.15 (the physiologically
#relevant band, see http://imaging.mrc-cbu.cam.ac.uk/imaging/DesignEfficiency:
freq_idx = np.where((C.frequencies>0.02) * (C.frequencies<0.15))[0]

idx_lcau = np.where(roi_names=='lcau')[0]
idx_rcau = np.where(roi_names=='rcau')[0]
idx_lput = np.where(roi_names=='lput')[0]
idx_rput = np.where(roi_names=='rput')[0]

idx = np.hstack([idx_lcau,idx_rcau,idx_lput,idx_rput])
idx1 = np.vstack([[idx[i]]*4 for i in range(4)]).ravel()
idx2 = np.hstack(4*[idx])

#Extract the coherence and average across these frequency bands: 
coh = C.coherence[idx1,idx2].reshape(4,4,C.frequencies.shape[0])
coh = np.mean(coh[:,:,freq_idx],2) #Averaging on the last dimension

drawgraph_roi(coh,roi_names[idx])
matshow_roi(coh,roi_names[idx])
