'''

O programa gera um arquivo de texto contendo pontos que estabelecem
um critério de seleção (pertencem ao padrão gerado na FFT que representa
as fileiras da plantação). O ajuste linear é aplicado nestes arquivos por
outra ferramenta que o usuário preferir.
Este programa apenas gera os pontos.

Executar python3 ep1_q4.py --help para ver as opcoes

'''

import cv2
import numpy as np
from argparse import ArgumentParser as parser
import matplotlib.pyplot as plt

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

    fft2 = np.zeros((70,430))
    fftshif = fft

    for i in range(70):
        for j in range(430):
            fft2[i][j] = fftshif[i+1695][j+2382]

    fft2 = np.abs(fft2)
    fft2 = gamma(fft2, 0.1)
 
    pos = []
    fft3 = np.zeros((70,430), dtype='uint8')
    for i in range(70):
        for j in range(430):
            if fft2[i][j] > 135:
                pos.append([i-33,j-210])
                fft3[i][j] = 255         

    return fft2, fft3, pos


def main():
    flags = parser(description="O programa gera um arquivo de texto contendo\
                                pontos que estabelecem um critério de seleção\
                                (pertencem ao padrão gerado na FFT que\
                                representa as fileiras da plantação).\
                                O ajuste linear é aplicado nestes arquivos\
                                por outra ferramenta que o usuário preferir.\
                                Este programa apenas gera apenas os pontos.")
    flags.add_argument('i1', help='Nome da figura de entrada \
                    (plantacao.jpg).')

    args = flags.parse_args()
    img = cv2.imread(args.i1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgmax, fft, spectrum = iiddft(img)

    fft_shifted = np.fft.fftshift(fft)

    centro, select, pos = filtro(fft_shifted)
    cv2.imshow("Centro", centro)
    cv2.imshow('Selected pixels', select)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #RETIRE O COMENTÁRIO SE DESEJAR UM .txt COM OS PONTOS SELECIONADOS
    '''with open('teste.txt', 'w') as f:
        for item in pos:
            f.write('%s %s \n' % (str(item[1]), str(item[0])))
    print("Arquivo de nome 'dados.txt' criado")
    print("O próximo passo é ajustar uma reta aos dados por MMQ")'''

    #PLOTA OS PONTOS COM O AJUSTE JÁ REALIZADO
    print('Ajuste linear já calculado')
    print('Para ver as coordenadas dos pontos utilizados para o ajuste, \
retire os comentários na função main')
    pos = np.array(pos)
    x = pos[:,0]
    y = pos[:,1]
    X = np.linspace(-200,200,500)
    Y = -7.1603030E-02*X

    plt.plot(y,-x,'b.',ls='none')
    plt.plot(X, Y, 'r-')
    plt.xlim(-200,200)
    plt.grid()
    plt.title("Espectro da plantação com ajuste linear")
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.show()

main()

    



