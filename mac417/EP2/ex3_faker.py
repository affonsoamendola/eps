# -*- coding: utf-8 -*-
import numpy as np
import cv2
import siamxt
import math

def gamma(array, c):
    array2 = np.array(array, dtype=np.float64)

    if np.min(array2) < 0:
        array3 = np.copy(array2) - np.min(array2)
    else:
        array3 = np.copy(array2)

    array3 = np.array(array3) / np.max(array3)

    array3 = np.round((array3 ** c) * 255)
    array3 = np.array(array3, dtype='uint8')

    return array3


def PB(x,y,R):
    filtro = np.ones((x,y), dtype=np.float64)
    crit = [[0,0],[0,y],[x,0],[x,y]]
    for i in crit:
        if i[0] - R > 0:
            if i[1] - R > 0:
                xi = x - R
                yi = y - R
                for j in range(xi,x,1):
                    for k in range(yi,y,1):
                        if math.sqrt((j-x)**2+(k-y)**2) < R:
                            filtro[j][k] = 0
            else:
                xi = x - R
                yi = R
                for j in range(xi,x,1):
                    for k in range(0,yi,1):
                        if math.sqrt((j-x)**2+(k)**2) < R:
                            filtro[j][k] = 0
        else:
            if i[1] - R < 0:
                xi = R
                yi = R
                for j in range(0,xi,1):
                    for k in range(0,yi,1):
                        if math.sqrt((j)**2+(k)**2) < R:
                            filtro[j][k] = 0
            else:
                xi = R
                yi = y - R
                for j in range(0,xi,1):
                    for k in range(yi,y,1):
                        if math.sqrt((j)**2+(k-y)**2) < R:
                            filtro[j][k] = 0

    fltro = np.array(filtro, dtype='uint8')
    
    return filtro


def bit8(array):

    array2 = np.array(array, dtype=np.float64)

    if np.min(array2) < 0:
        array3 = np.copy(array2) - np.min(array2)
    else:
        array3 = np.copy(array2)

    m = np.max(array3)
    array3 = (array3 / m) * 255

    return np.array(array3, dtype='uint8')

def bit8lim(array, lim):

    array2 = np.array(array, dtype=np.float64)

    if np.min(array2) < 0:
        array3 = np.copy(array2) - np.min(array2)
    else:
        array3 = np.copy(array2)

    m = np.max(array3)
    array3 = (array3 / m) * lim

    return np.array(array3, dtype='uint8')


def iiddft(img):
    imgmax = np.max(img)
    img2 = img / imgmax

    fft = np.fft.fft2(img2) * imgmax
    
    spectrum = np.abs(fft)

    return imgmax, fft, spectrum

def inverse_fft(fft):
    
    inversa = np.fft.ifft2(fft)

    return inversa
        

def main():
    img = cv2.imread("palhaco.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fft = np.fft.fft2(img)
    spectrum = np.abs(fft)


    spec_plot = np.fft.fftshift(gamma(spectrum,0.2))
    cv2.imshow("FFT original.png", spec_plot)

    #EXTINCTION FILTER
    N = np.ones((3,3), dtype=bool)
    inv_spec = 255 - gamma(spectrum,0.35)

    cv2.imshow("inversa_Spec.png", np.fft.fftshift(inv_spec))
    mxt = siamxt.MaxTreeAlpha(inv_spec,N)
    n = 1
    area = mxt.node_array[3,:]
    area_ext = mxt.computeExtinctionValues(area,"height")
    mxt.extinctionFilter(area_ext,n)
    img_filt = mxt.getImage()
    img_filt = 255 - img_filt
    cv2.imshow("Filtrada max-tree.png", np.fft.fftshift(img_filt))

    #MÁXIMOS
    th2 = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                        cv2.THRESH_BINARY,591,0)
    radius = 19
    th2 = th2 * PB(len(img_filt),len(img_filt[0]),radius)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(9,9))
    #kernel = np.ones((3,3), dtype='uint8')
    th2 = cv2.dilate(th2,kernel,iterations = 2)
    for j in range(len(th2)):
        for k in range(len(th2[0])):
            if th2[j][k] == 255:
                th2[j][k] = 0
            else:
                th2[j][k] = 1

    max_apag = img_filt * th2
    cv2.imshow("max.png", np.fft.fftshift(bit8(max_apag)))
    fft_filt = fft * th2
    cv2.imwrite("FFT com filtro de maximos.png", np.fft.fftshift(gamma(\
                                            np.abs(fft_filt), 0.3)))
    inversa = inverse_fft(fft_filt)
    inversa = bit8(np.abs(inversa))
    cv2.imshow("Inversa filtrada.png", np.fft.fftshift(gamma(np.abs(fft_filt), 0.3)))

    cv2.imshow("Final.png", inversa)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    

main()
