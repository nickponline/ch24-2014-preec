#!/usr/bin/python
from numpy.fft import fft
from scipy.io import wavfile
import numpy
import sys

def count(sec,wav):
    secf = fft(wav[(sec-0.5)*44100:(sec+0.5)*44100])
    n = 0
    for freq in range(500,11000,100):
        p = numpy.sum(numpy.abs(secf[freq-10:freq+10])**2)
        if p > 100000:
            n = n + 1
    return n

w = wavfile.read(sys.argv[1])
wav = (w[1] * 1.0 - 127) / 128.0
counts = numpy.array([count(sec,wav) for sec in range(1,len(wav) / 44100)])
print counts.max(), counts.argmax() + 1
