import siamxt
import cv2
import math
import numpy as np


import sys

def gamma(array, exponent): 
	#Takes an image (Doesnt matter the dtype, as long as its floatX or intX)
	#And returns an 8Bit image with gamma exponentiation applied using exponent.
	assert(type(array[0][0]) is np.uint8 or type(array[0][0] is np.float64))

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
	assert(type(image[0][0]) is np.float64)

	uint8image = np.copy(image)

	x_size = len(image[0])
	y_size = len(image)

	for x in range(x_size):
		for y in range(y_size):
			uint8image[y][x] = image[y][x] * 255 #Apply the gamma thing
	
	return uint8image.astype(np.uint8)

def normalize(image):
	#Takes an image and normalizes it.
	assert(type(image[0][0]) is np.float64 or type(image[0][0]) is np.uint8)

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
	if(gamma != 1.): #Just to make things faster
		display = gamma(np.abs(display), gamma_value)
	display = to_uint8(display)

	return display

def apply_fft(image):

	fft = np.fft.fft2(image)

	return fft

def apply_ifft(image):

	ifft = np.fft.ifft2(image)

	return ifft

def alpha_mask_image(image, alpha):
	assert(type(image[0][0]) is np.float64 and type(alpha[0][0]) is np.float64)

	x_size = len(image[0])
	y_size = len(image)

	masked_image = np.copy(image)

	alpha_norm = normalize(alpha)

	for x in range(x_size):
		for y in range(y_size):
				#print(str(masked_image[y][x]) + " * " + str(alpha_norm[y][x]))
				masked_image[y][x] = image[y][x] * alpha_norm[y][x]

	return masked_image

def get_magnitude_image(real, imaginary):
	assert(type(real[0][0]) is np.float64 and type(imaginary[0][0]) is np.float64)
	mag_img = np.copy(real)

	x_size = len(real[0])
	y_size = len(real)

	for x in range(x_size):
		for y in range(y_size):
			mag_img[y][x] = np.sqrt(real[y][x]**2 + imaginary[y][x]**2)
	return mag_img

def combine_complex_image(real, imaginary):
	comb_img = real.astype(np.complex128)

	x_size = len(real[0])
	y_size = len(real)

	for x in range(x_size):
		for y in range(y_size):
			comb_img[y][x] = complex(real[y][x], imaginary[y][x])

	return comb_img

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

print("Got image: " + sys.argv[1])

img_not = cv2.bitwise_not(img)

cv2.imshow("Inverted Image", img_not)


bc = np.ones((3,3), dtype=bool)

print("Building tree...", end='', flush=True)

tree_not = siamxt.MaxTreeAlpha(img_not, bc)

print("Done.")

print("Applying area-open filter...", end='', flush=True)

tree_not.areaOpen(25)

print("Done.")

print("Reconstructing Image...", end='', flush=True)

rec_img = tree_not.getImage()
final = cv2.bitwise_not(rec_img)

print("Done.")

cv2.imshow("Original Image", img)
cv2.imshow("Filtered Image", final)

cv2.waitKey(0)
cv2.destroyAllWindows()