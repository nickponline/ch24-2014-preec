import cv2
import sys

image = cv2.imread(sys.argv[1])
cv2.imshow('Cineam', image)
cv2.waitKey(0)