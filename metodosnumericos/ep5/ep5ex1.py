import numpy as np

def pontoMedio(x0, x1, n):
	
	h = (abs(x1-x0))/float(n)
	soma = 0

	for i in range(n):
		xi0 = x0 + h*i
		xi1 = x0 + h*(i+1)

		medio = (xi0 + xi1)/2
		soma += f_pontoMedio(medio)*h

	return soma

def f_pontoMedio(x):

	return (np.sin(x))

print(pontoMedio(0.0,np.pi(),10))
