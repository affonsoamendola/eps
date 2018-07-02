import numpy as np
import matplotlib.pyplot as plt

def trapezio32(funcao, x0in, x1in):
	
	global n

	if(n == 0):
		n = 1

	x0 = np.float32(x0in)
	x1 = np.float32(x1in)

	h = (np.abs(x1-x0))/np.float32(n)
	soma = np.float32(0)

	for iteration in range(n):

		i = np.float32(iteration)

		#print("i=",i)

		xi0 = x0 + h*i
		xi1 = x0 + h*(i+1)

		ftrap0 = 0
		ftrap1 = 0

		if(xi0 in evaluated):
			#print("xi0 already evaluated")
			ftrap0 = evaluated[xi0]
		else:
			#print("evaluatin xi0")
			ftrap0 = funcao(xi0)
			evaluated[xi0] = ftrap0 

		if(xi1 in evaluated):
			#print("xi1 already evaluated")
			ftrap1 = evaluated[xi1]
		else:
			#print("evaluatin xi1")
			ftrap1 = funcao(xi1)
			evaluated[xi1] = ftrap1


		trap = h*(ftrap0+ftrap1)/np.float32(2)
		
		soma += trap

	n = n*2
	return soma

def trapezio64(funcao, x0in, x1in):
	
	global n

	if(n == 0):
		n = 1

	x0 = np.float64(x0in)
	x1 = np.float64(x1in)

	h = (np.abs(x1-x0))/np.float64(n)
	soma = np.float64(0)

	for iteration in range(n):

		i = np.float64(iteration)

		#print("i=",i)

		xi0 = x0 + h*i
		xi1 = x0 + h*(i+1)

		ftrap0 = 0
		ftrap1 = 0

		if(xi0 in evaluated):
			#print("xi0 already evaluated")
			ftrap0 = np.float64(evaluated[xi0])
		else:
			#print("evaluatin xi0")
			ftrap0 = np.float64(funcao(xi0))
			evaluated[xi0] = ftrap0 

		if(xi1 in evaluated):
			#print("xi1 already evaluated")
			ftrap1 = evaluated[xi1]
		else:
			#print("evaluatin xi1")
			ftrap1 = np.float64(funcao(xi1))
			evaluated[xi1] = ftrap1


		trap = h*(ftrap0+ftrap1)/np.float64(2)
		
		soma += trap

	n = n*2
	return soma

def simpson32(funcao, x0in,x1in):
	global n

	if(n == 0):
		n = 2

	x0 = np.float32(x0in)
	x1 = np.float32(x1in)

	h = (np.abs(x1-x0))/np.float32(n)
	soma = np.float32(0)

	


def blackbody32(wavelengthin):
	temperature = np.float32(2500)
	#Calculates blackbody radiation for determinate wavelength(in um), and temperature (in K)

	h = np.float32(6.62607004e-22)
	kb = np.float32(1.38064852e-11)
	c = np.float32(2.99792438e14)
	wavelength = np.float32(wavelengthin)

	a = (np.float32(2)*c*h*c)/(wavelength**np.float32(5))
	b = np.float32(1)/(np.exp((h*c/(wavelength*temperature))/kb)-np.float32(1))

	return a*b

def blackbody64(wavelengthin):
	temperature = np.float64(2500)
	#Calculates blackbody radiation for determinate wavelength(in um), and temperature (in K)

	h = np.float64(6.62607004e-22)
	kb = np.float64(1.38064852e-11)
	c = np.float64(2.99792438e14)
	wavelength = np.float64(wavelengthin)

	a = (np.float64(2)*c*h*c)/(wavelength**np.float64(5))
	b = np.float64(1)/(np.exp((h*c/(wavelength*temperature))/kb)-np.float64(1))

	return a*b

evaluated = {}
n = 

first = trapezio32(blackbody64,0.5,10)

tabela = []
tabela.append((n,first))

notDone = True

while(notDone):

	second = trapezio32(blackbody64,0.5,10)
	epsilon = (abs(second-first))/first

	tabela.append((n,epsilon))

	if(epsilon < 1e-12):
		notDone = False
	first = second

grafX = []
grafY = []

for i in range(len(tabela)):
	grafX.append(np.log2(tabela[i][0]))
	grafY.append(np.log10(tabela[i][1]))

plt.plot(grafX, grafY)
plt.show()
