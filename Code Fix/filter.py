import panda as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


eeg_data = pd.read_csv('demoeeg.csv')
values_eeg = eeg_data['col1'].values

emg_data = pd.read_csv('demoemg.csv')
values_emg = emg_data['col1'].values

len_eeg = len(values_eeg)
len_emg = len(values_emg)

if (len_eeg >= len_emg):
	values_eeg = values_eeg[:(len_eeg-len_emg)]
	size = len_emg

if (len_emg > len_eeg):
	values_emg = values_emg[:(len_emg-len_eeg)]
	size = len_eeg

fs = size
t = np.arange(size)/fs

fc = (max(values_eeg)+min(values_eeg))/2
b, a = signal.butter(5, fc, 'low')
lpf_eeg = signal.filtfilt(b, a, value_eeg)
plt.plot(t, lpf_eeg, label='EEG with LPF')

plt.plot(t, values_emg, label='EMG')

cross_corr = np.correlate(lpf_eeg, values_emg)
plt.plot(t, cross_corr, label='Cross Correlate')

plt.legend()
plt.show()