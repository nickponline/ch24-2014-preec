# q.py
# Nicholas Pilkington

import numpy as np
import scipy.signal
import scipy.io.wavfile
import pickle
import sys
import pylab
from scipy import stats
import scipy.stats
import numpy
import scipy
import pylab

def goertzel(samples, target_frequency, sample_rate):
	s_prev = 0 
	s_prev2 = 0 
	normalized_frequency = 1.0 * target_frequency / sample_rate 
	coeff = 2.0 * np.cos(2.0 * np.pi * normalized_frequency) 
	for sample in samples:
	  s = sample + coeff * s_prev - s_prev2
	  s_prev2 = s_prev
	  s_prev = s
	power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2
	return power

sample_rate, data = scipy.io.wavfile.read(sys.argv[1])
window_length = 10100
print len(data) / sample_rate, "seconds."
mx = None

def make_window(data, i, sample_rate, fs):
	w = data[i * sample_rate - fs:i * sample_rate + fs]
	return w

for i in xrange(1, len(data) / sample_rate):
	
	window = data[i*sample_rate - window_length / 2:i*sample_rate + window_length/2]
	freq = np.array([goertzel(make_window(data, i, sample_rate, fs*100), fs * 100, sample_rate) for fs in xrange(5, 101)])
	#c = stats.scoreatpercentile(freq, 95)
	c = 1e8

	# pylab.figure()
	# pylab.title(str(i))
	# pylab.plot([fs*100 for fs in xrange(5, 101)], freq, 'ro')
	# pylab.plot([fs*100 for fs in xrange(5, 101)], [c for fs in xrange(5, 101)] )
	# pylab.savefig(str(i) + '.pdf')

	print " Second: ", i, len(freq[freq > c])