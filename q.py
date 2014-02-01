# q.py
# Nicholas Pilkington

import numpy as np
import scipy.signal
import scipy.io.wavfile
import pickle
import sys
import pylab
from scipy import stats

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

total = None

for tf in xrange(500, 10100, 100):

	print tf
	length = int(44100) # 
	skip   = 1000 # 0.1s precision
	
	windows = [data[start:start+length] for start in xrange(0, len(data) - length, skip)] 
	fourier = np.array([goetrzel(w, tf, sample_rate) for w in windows], dtype=np.float64)
	n       = len(fourier)
	time    = np.arange(n, dtype=np.float64) / n * len(data) / sample_rate

	c = np.copy(fourier)
	M = stats.scoreatpercentile(c, 95)
	print c.min(), c.max(), c.mean(), M
	
	pylab.figure()
	pylab.subplot(211)
	pylab.plot(time, fourier)
	pylab.plot(time, [M] * len(time))

	idx = np.where( c > M )
	fourier[idx] = 1
	idx = np.where( c <= M )
	fourier[idx] = 0

	
	if total is None:
		total = fourier
	else:
		total += fourier

	pylab.subplot(212)
	pylab.plot(time, total,'r') 
	pylab.show()

	peakValue = total.max()
	startPeakIndex = 0

	while startPeakIndex < len(time):

		if total[startPeakIndex] == peakValue:
			endPeakIndex = startPeakIndex + 1
			while endPeakIndex < len(time) and (total[endPeakIndex] == total[startPeakIndex]):
				endPeakIndex += 1
			endPeakIndex -= 1
			duration = time[endPeakIndex] - time[startPeakIndex]
			print "Peak duration: ", duration, "Start:", time[startPeakIndex], "Value: ", peakValue
			
			if duration > 1.0:
				print int(peakValue), (time[startPeakIndex] + duration / 2.0)
			startPeakIndex = endPeakIndex + 1

		else:
			startPeakIndex += 1