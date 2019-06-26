import cv2
import math
import numpy as np

import sys

def gamma(array, exponent): 

	#Takes an image (Doesnt matter the dtype, as long as its floatX or intX)
	#And returns an 8Bit image with gamma exponentiation applied using exponent.
	
	x_size = len(array[0]) #Assuming a square image and adopting the structure of [y][x]
	y_size = len(array) 

	image = np.copy(array)

	if(np.min(image) < 0): #If image has a negative value somewhere, get it up to 0
		image = np.copy(image) - np.min(image)

	for x in range(x_size):
		for y in range(y_size):
			image[y][x] = image[y][x] ** exponent #Apply the gamma thing

	return image

def to_uint8(image):

	uint8image = image * 255 #Assumes normalized input image

	uint8image = np.array(uint8image, dtype='uint8')

	return uint8image

def normalize(image):
	#Takes an image and normalizes it.

	max_value = np.max(image)

	x_size = len(image[0])
	y_size = len(image)

	normalized = np.array(image, dtype='float64')

	for x in range(x_size):
		for y in range(y_size):
			normalized[y][x] = float(normalized[y][x]) / float(max_value)

	return normalized

def to_display(image, gamma_value):
	display = np.copy(image)

	display = normalize(display)
	display = gamma(np.abs(display), gamma_value)
	display = to_uint8(display)

	return display


def apply_fft(image):

	fft = np.fft.fft2(image)

	return fft

def apply_ifft(image):

	ifft = np.fft.ifft2(image)

	return ifft
'''
def noise_filter(image):
	x_size = len(image[0])
	y_size = len(image)

	filtered_image = np.copy(image)

	filtered_image = np.fft.fftshift(filtered_image)

	for x in range(0, x_size, 32):
		for y in range(0, y_size, 48):
			if (y != 240 or x != 320):
				if(x != 0 and y != 0):
					filtered_image[y][x] = 0

	filtered_image = np.fft.fftshift(filtered_image)

	return filtered_image
'''

def get_center(image, size_x, size_y):
	img_size_x = len(image[0])
	img_size_y = len(image)

	center = np.zeros((size_y, size_x))

	for x in range(size_x):
		for y in range(size_y):
			center[y][x] = image[y + img_size_y/2 - size_y/2][x + img_size_x/2 - size_x/2]
	
	return center

def select_points(image, treshold):
	img_size_x = len(image[0])
	img_size_y = len(image)

	selected_image = np.zeros((img_size_y, img_size_x), dtype='uint8')

	points_list = []

	for x in range(img_size_x):
		for y in range(img_size_y):
			if(image[y][x] > treshold):
				points_list.append([y - img_size_y/2, x - img_size_x/2])
				selected_image[y][x] = 255

	return selected_image, points_list


img = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = normalize(img)

img_fft = apply_fft(img)
img_fft_g = np.fft.fftshift(img_fft)

center = get_center(img_fft_g, 430, 70)
center_g = to_display(center, 0.1)

selected, points = select_points(center_g, 144)

cv2.imshow('FFT Center Area', center_g)
cv2.imshow('Selected Points', selected)

points = np.array(points)

y = points[:,1]
x = points[:,0]

coefs = np.polynomial.polynomial.polyfit(x, y, 1)
print "\n\n\n"
print "Angle is equal to : ", math.degrees(math.atan(coefs[1])), " degrees."

cv2.waitKey(0)
cv2.destroyAllWindows()

