import cv2
import math
import numpy as np
import siamxt

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

	uint8image = np.array(image, dtype='uint8')


	for x in range(x_size):
		for y in range(y_size):
			uint8image[y][x] = image[y][x] * 255 #Apply the gamma thing

	return uint8image

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
	#assert(type(image[0][0]) is np.float64 and type(alpha[0][0]) is np.float64)

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


#def create_empty_image(sizex, sizey, channels):
#	return np.zeros(shape=[sizex, sizey], channels)

#def create_circle_image(sizex, sizey, radius, positionx, positiony):
#	empty_image = create_empty_image(sizex, sizey, 1)
#	circle_image = cv2.circle(empty_image, (positionx, positiony), radius, 255, -1)
#	return circle_image

image_raw = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

print("Got image: " + sys.argv[1])

cv2.imshow("Original", image_raw)
im_x_size = len(image_raw[0])
im_y_size = len(image_raw)

norm = normalize(image_raw)

print("Done.")

print("Applying FFT...", end='', flush=True)

ffted = apply_fft(norm)
#shifted = np.fft.fftshift(transformed)
ffted_mag = get_magnitude_image(ffted.real, ffted.imag)
#cv2.imshow("FFT Real Part", to_display(ffteds_real[i], 0.15))
#cv2.imshow("FFT Imag Part", to_display(ffteds_imag[i], 0.15))

print("Done.")

print("Finding Peaks...", end='', flush=True)

shifted = to_display(np.fft.fftshift(ffted_mag), 0.35)
norm_shift = normalize(shifted)
cv2.imshow("FFTED", shifted)

neg = to_uint8(norm_shift)#cv2.bitwise_not(to_uint8(normalize(shifted)))

#Connectivity-8 element:
bc = np.ones((3,3), dtype = bool)

maxtree = siamxt.MaxTreeAlpha(neg, bc)

area = maxtree.node_array[3,:]
area_ext = maxtree.computeExtinctionValues(area, "area")
maxtree.extinctionFilter(area_ext, 3)

max_tree_extinct_img = maxtree.getImage()

cv2.imshow("Maxtree filtered", max_tree_extinct_img)

peak_regions = shifted - max_tree_extinct_img 

cv2.imshow("Peaks", peak_regions)

thresholded = cv2.adaptiveThreshold(peak_regions, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                       				 cv2.THRESH_BINARY, 9, -20)

dilated = cv2.dilate(thresholded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)), 1)
inv_dilated = cv2.bitwise_not(dilated)

cv2.imshow("Dilated", inv_dilated)
filtered_final = alpha_mask_image(np.fft.fftshift(ffted), inv_dilated)
filtered_final_shifted = np.fft.fftshift(filtered_final)
cv2.imshow("Filtered_final", to_display(get_magnitude_image(filtered_final.real, filtered_final.imag), 0.35))

#bitmasks.append(cv2.adaptiveThreshold(to_uint8(normalize(shifted)), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 0))
#dilated = cv2.dilate(bitmasks[i], cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)), 1)
#dilated_inv = cv2.bitwise_not(dilated)
#cv2.circle(dilated_inv, (int(im_x_size/2), int(im_y_size/2)), 25, 255, -1)
#maskeds_real.append(alpha_mask_image(ffteds_real[i], np.fft.fftshift(normalize(dilated_inv))))
#maskeds_imag.append(alpha_mask_image(ffteds_imag[i], np.fft.fftshift(normalize(dilated_inv))))
#cv2.imshow("Dilated Bitmask Channel " + str(i), to_display(get_magnitude_image(maskeds_real[i], maskeds_imag[i]), 0.2))

print("Done.")

#complexed = append(combine_complex_image(maskeds_real[i], maskeds_imag[i]))

#shifted = np.fft.ifftshift(channel)
iffted = apply_ifft(combine_complex_image(filtered_final_shifted.real, filtered_final_shifted.imag))
final = to_display(iffted.real, 1.)
#channels.append(to_display(get_magnitude_image(reverse.real, reverse.imag), 1.))

cv2.imshow("Final image:", final)

cv2.waitKey(0)
cv2.destroyAllWindows()
