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

lep = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

lep = normalize(lep)

lep_fft = apply_fft(lep)
lep_fft_g = np.fft.fftshift(lep_fft)
lep_fft_g = to_display(lep_fft_g, 0.2)
cv2.imshow('FFT No Filter', lep_fft_g)

lep_ifft = apply_ifft(lep_fft)
lep_ifft_g = to_display(lep_ifft, 1)
cv2.imshow('IFFT No Filter', lep_ifft_g)

lep_filter = noise_filter(lep_fft)
lep_filter_fft_g = np.fft.fftshift(lep_filter)
lep_filter_fft_g = to_display(lep_filter_fft_g, 0.2)
cv2.imshow('FFT Filter', lep_filter_fft_g)

lep_filter_ifft = apply_ifft(lep_filter)
lep_filter_ifft_g = to_display(lep_filter_ifft, 1)
cv2.imshow('IFFT Filter', lep_filter_ifft_g)

cv2.waitKey(0)
cv2.destroyAllWindows()

