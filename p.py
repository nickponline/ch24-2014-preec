# p.py 
# Nicholas Pilkington

from math import radians, cos, sin, asin, sqrt
import os, sys

def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2.0 * asin(sqrt(a)) 

    # 6371 km is the radius of the Earth
    km = 6371 * c
    return km 

N = None
coords = []
solution = 0.0

with open(sys.argv[1], mode='r') as fd:
    N = int(fd.readline())

    for i in xrange(N):
        lat, lon = map(float, fd.readline().split())
        coords.append((lat, lon))

for i in xrange(0, N):
    solution += haversine(coords[i][1], coords[i][0], coords[(i+1)%N][1], coords[(i+1)%N][0] )

with open(sys.argv[2], mode='w') as fd:
    fd.write(str(solution))
    fd.write('\n')