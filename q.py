# q.py
# Nicholas Pilkington

import numpy as np
import scipy.signal
import scipy.io.wavfile
import pickle
import sys
import pylab

def goetrzel(x, target_frequency, sample_rate):
	s_prev = 0
	s_prev2 = 0
	normalized_frequency = target_frequency / sample_rate
	coeff = 2.0 * np.cos(2.0 * np.pi * normalized_frequency)
	for sample in x:
	  s = sample + coeff * s_prev - s_prev2
	  s_prev2 = s_prev
	  s_prev = s
	power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2 ;
	return power

sample_rate, data = scipy.io.wavfile.read(sys.argv[1])
print sample_rate

length = 25000 # max freq is 10khz
skip   = 10000 # 0.1s precision
total = None

for tf in xrange(500, 1100, 100):
	
	spec = goetrzel(data, tf, sample_rate)
	windows = [data[start:start+length] for start in xrange(0, len(data) - length, skip)] 
	fourier = np.array([goetrzel(w, tf, sample_rate) for w in windows], dtype=np.float64)
	n       = len(fourier)
	time    = np.arange(n, dtype=np.float64) / n * len(data) / sample_rate

	#pylab.figure()
	#pylab.plot(time, fourier)
	#pylab.plot(time, [fourier.mean()] * len(time))
	#pylab.show()

	c = np.copy(fourier)
	M = c.mean()
	idx = np.where( c > M )
	fourier[idx] = 1
	idx = np.where( c <= M )
	fourier[idx] = 0

	
	if total is None:
		total = fourier
	else:
		total += fourier

	#pylab.figure()
	#pylab.plot(time, total,'r') # plotting the spectrum
	#pylab.show()

	startPeakIndex  = np.argmax(total)
	endPeakIndex = startPeakIndex
	while total[endPeakIndex] == total[startPeakIndex]:
		endPeakIndex += 1
	endPeakIndex -= 1

	#print time[startPeakIndex], time[endPeakIndex], total[startPeakIndex], total[endPeakIndex]
	midIndex = (startPeakIndex + endPeakIndex) // 2
	print int(time[midIndex]), int(total[midIndex])

	