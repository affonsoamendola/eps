'''

Para filtrar a imagem leopard_noise.png.
Executar python3 ep1_q3.py --help para ver as opcoes

'''

import cv2
import numpy as np
from argparse import ArgumentParser as parser

def gamma(array, c):
    x = len(array)
    y = len(array[0])

    if np.min(array) < 0:
        array2 = np.copy(array) - np.min(array)
    else:
        array2 = np.copy(array)

    array2 = np.array(array) / np.max(array)

    for i in range(x):
        for j in range(y):
            array2[i][j] = round(((array2[i][j]) ** c) * 255)
    array2 = np.array(array2, dtype='uint8')

    return array2

def bit8(array):
    x = len(array)
    y = len(array[0])

    if np.min(array) < 0:
        array2 = np.copy(array) - np.min(array)
    else:
        array2 = np.copy(array)

    m = np.max(array2)
    array2 = (array2 / m) * 255

    return np.array(array2, dtype='uint8')

def iiddft(img):
    imgmax = np.max(img)
    img = img / imgmax

    fft = np.fft.fft2(img)

    x = len(fft)
    y = len(fft[0])

    fftshif = np.fft.fftshift(fft)

    spectrum = np.abs(fft)
    spectrum_shifted = np.abs(fftshif)

    return imgmax, fft, spectrum

def inverse_fft(fft, imgmax):
    
    inversa = np.fft.ifft2(fft)
    inversa = inversa * imgmax

    return inversa

def filtro(fft):
    x = len(fft)
    y = len(fft[0])

    fft2 = np.copy(fft)
    fft2 = np.fft.fftshift(fft2)
    for i in range(0,x,48):
        for j in range(0,y,32):
            if (i != 0 or j != 0) and (i != 240 or j != 320):
                fft2[i][j] = 0

    fft2 = np.fft.fftshift(fft2)

    return fft2



def main():
    flags = parser(description="Apaga o filtro periodico da figura\
                    leopard_noise.png.")
    flags.add_argument('i1', help='Nome da figura de entrada \
                    (leopard_noise.png).')

    args = flags.parse_args()
    
    img = cv2.imread(args.i1)
    img = np.delete(np.delete(img,2,2), 1, 2)
    img = np.reshape(img, (len(img), len(img[0])))
    imgmax, fft, spectrum = iiddft(img)

    fft_shifted = np.fft.fftshift(fft)
    fft_shifted = gamma(fft_shifted, 0.1)
    cv2.imshow('FFT shifted', fft_shifted)

    fft_original = gamma(fft, 0.1)
    cv2.imshow('FFT original', fft_original)

    fft_filter = filtro(fft)
    fft_filter2 = np.fft.fftshift(fft_filter) * imgmax
    fft_filter2 = gamma(fft_filter2, 0.1)
    cv2.imshow('Filtered', fft_filter2)

    inversa = inverse_fft(fft_filter, imgmax)
    inversa_plot = bit8(inversa)
    cv2.imshow('Inversa', inversa_plot)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
    
