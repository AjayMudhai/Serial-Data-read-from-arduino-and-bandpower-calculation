import serial
import csv
import numpy as np
import pandas as pd
import scipy

from scipy import signal
from scipy.signal import freqz
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from drawnow import *
import time
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF


ch1Array=[]
ch2Array=[]
timeElasped=[]

wa=[]
ha=[]
ch1bandpassfiltred=[]
wa.append(1)
ha.append(1)
f=[]
psdch1=[]
bpch1=[]



ser = serial.Serial('/dev/ttyACM0',250000)
plt.ion()

 # Sample rate and desired cutoff frequencies (in Hz).
fs = 1000.
lowcut = 20.0
highcut = 450.0
fs = 1000; 
start=time.time();
   
   

def butter_bandpass(lowcut, highcut, fs, order=10):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=10):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    freq_response_plot(b,a)
    return y

def freq_response_plot(b,a):
    w, h = freqz(b, a, worN=2000)
    wa.pop(0)
    ha.pop(0)
    wa.append(w)
    ha.append(h)

def nextpow2(i):
    n = 1
    while n < i: n *= 2
    return n



samples = 0;


with open('serialdata.csv', 'w' ) as f:
    fieldnames = ['time', 'ch1d','ch2d']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
   

        
   
    while (i<4000):
        while (ser.inWaiting () == 0):
            pass
        data = ser.readline()
        dataArray = ser.readline().split(',')
        ch1 = float(dataArray[0])
        ch2 = float(dataArray[1])
        ch1Array.append(ch1)
        ch2Array.append(ch2)
        print i
        samples=samples+1;
        end=time.time();
        tm=float(end-start)
        writer.writerow({'time':tm, 'ch1d':ch1})
        #time.sleep(0.005)

ch1bandpassfiltred = butter_bandpass_filter(ch1Array, lowcut, highcut, fs, order=10)    
ch2bandpassfiltred = butter_bandpass_filter(ch2Array, lowcut, highcut, fs, order=10) 
m1=len(ch1bandpassfiltred)
n1=nextpow2(m1)
f,psdch1= scipy.signal.periodogram(ch1bandpassfiltred,fs=1000.0,window=None, nfft=n1, detrend='constant', return_onesided=True, scaling='density',)
ind_min = scipy.argmax(f > 25) - 1
ind_max = scipy.argmax(f > 450) - 1
bandpowerch1 = scipy.trapz(psdch1[ind_min: ind_max], f[ind_min: ind_max])
print bandpowerch1

m2=len(ch2bandpassfiltred)
n2=nextpow2(m1)
f,psdch2= scipy.signal.periodogram(ch2bandpassfiltred,fs=1000.0,window=None, nfft=n1, detrend='constant', return_onesided=True, scaling='density',)
ind_min = scipy.argmax(f > 25) - 1
ind_max = scipy.argmax(f > 450) - 1
bandpowerch2 = scipy.trapz(psdch2[ind_min: ind_max], f[ind_min: ind_max])
print bandpowerch2
        
