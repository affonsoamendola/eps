import cv2
import math
import numpy as np
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
img2 = np.copy(img)
img3 = np.copy(img2)

mascara = int(sys.argv[2], 16) 	#Mascara de bits 
						#Outras mascaras interessantes 
						#3Fh = 00111111b
						#F0h = 11110000b
						#0Fh = 00001111b
						#3Ch = 00111100b

for i in range(len(img2)):
    for j in range(len(img2[0])):
    	pixel = (img2[i][j] & mascara)
    	img3[i][j] = pixel
        
cv2.imwrite("riven_" + sys.argv[2] + ".png", img3)
