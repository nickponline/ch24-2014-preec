#!/usr/bin/python
from scipy.misc import imread,imsave
import numpy
import sys

fname = sys.argv[1]
#fname = '../PROBLEMSET/input/R/10.png'

im = imread(fname, flatten=True).astype('int32')
ops = []

def swap(x1, y1, x2, y2):
    d = -1 # XXX
    ops.append((x1, y1, d))
    t = im[y1,x1]
    im[y1,x1] = im[y2,x2]
    im[y2,x2] = t
    
    #print 'Swapping %d;%d and %d;%d' % (x1, y1, x2, y2)
    
def simple():
    found = True
    while found:
        found = False
        for y in range(im.shape[0]):
            for x in range(1,im.shape[1]):
                if im[y,x] < im[y,x-1]:
                    ops.append((x-1,y,2))
                    #print 'Swapping at %d;%d (values %d and %d)' % (x,y,im[y,x],im[y,x-1])
                    swap(x, y, x - 1, y)
                    found = True

def greedy1():
    # Build up the image from darkest to lightest, greedily choosing which row
    # to put the next darkest pixel on based on how many swaps we would need to
    # move it there.
    #
    # It's not perfect (if we have to move a pixel across a row which has already
    # been fixed in place, then we need some extra swaps in order to restore
    # sanity), but it seems to do a pretty good job.
    nxpos = numpy.zeros(im.shape[0],dtype='int32')
    counts = [len(im[im==i]) for i in range(256)]
    positions = [set([(x[1],x[0]) for x in zip(*numpy.nonzero(im==i))]) for i in range(256)]
    for i in range(256):
        if counts[i] > 0:
            print '%d pixels with intensity %d' % (counts[i], i)
        for j in range(counts[i]):
            # Find the best spot to place this guy.
            closest = im.shape[0] + im.shape[1]
            best = -1
            bx = -1
            by = -1
            for y in range(im.shape[0]):
                x = nxpos[y]
                if x >= im.shape[1]:
                    # No more room
                    continue
                # Short-circuit if we have the right guy under our feet
                if im[y,x] == i:
                    best = y
                    closest = 0
                    bx = x
                    by = y
                    break
                
                for (x2,y2) in positions[i]:
                    # XXX this search could probably be way more efficient, but
                    # it works for now...
                    dist = abs(y2 - y) + abs(x2 - x)
                    if best == -1 or dist < closest:
                        closest = dist
                        best = y
                        bx = x2
                        by = y2
            
            assert(best != -1)
            
            positions[i].remove((bx,by))
            
            y = best
            x = nxpos[y]
            sxy = []
            print '%d; %d of %d: moving %d,%d to %d,%d (%d)' % (i, j, counts[i], bx, by, x, y, len(ops))
            while bx != x or by != y:
                if bx != x and by != y:
                    d = numpy.random.randint(2)
                elif bx != x:
                    d = 0
                else:
                    d = 1
                
                if d == 0:
                    nx = bx - 1 if bx > x else bx + 1
                    ny = by
                else:
                    nx = bx
                    ny = by - 1 if by > y else by + 1
                
                oldi = im[ny,nx]
                swap(bx, by, nx, ny)
                
                if nx < nxpos[ny]:
                    if len(sxy) == 0:
                        sxy.append((bx, by))
                    sxy.append((nx, ny))
                else:
                    positions[oldi].remove((nx,ny))
                    if len(sxy) > 0:
                        for s in range(len(sxy) - 1, 0, -1):
                            swap(sxy[s - 1][0], sxy[s - 1][1], sxy[s][0], sxy[s][1])
                        positions[oldi].add(sxy[0])
                        sxy = []
                    else:
                        positions[oldi].add((bx, by))
                        
                bx = nx
                by = ny
            
            nxpos[y] += 1
            
        if counts[i] > 0:
            print 'Got %d swaps so far' % (len(ops))
            
#simple()
greedy1()

# TODO: actually write out our swap operations. The greedy ones should form
# nice lines of linked swaps and be amenable to writing out in an efficient way.
print 'Done with %d swaps' % (len(ops))

if len(sys.argv) > 2:
    imsave(sys.argv[2], im)

