#include <stdio.h>
#include <stdlib.h>

#include <math.h>

/* 
	Affonso Gino Amendola Neto
	(https://github.com/affonsoamendola/)

	NUSP 9301753

	EP1-MAC122
	-------------------------------------

	Eu tenho o costume de escrever todos os meus códigos em english, mas as funções realmente pedidas em A B C D E eu mantive com
	os nomes originais em português do documento do EP1, fica meio confuso misturar duas linguas, mas assim fica claro onde estão os
	exercicios realmente pedidos.
*/

typedef struct _polyElement
{
	float coefficient;
	int exponent;
	struct _polyElement* nextElement;

} polyElement;

typedef polyElement* Polynomial;

polyElement* allocatePolyElement()
{
	polyElement* toReturn;

	toReturn = (polyElement*)malloc(sizeof(polyElement));

	if(toReturn == NULL)
	{
		printf("FOR SOME REASON, THE PROGRAM RAN OUT OF MEMORY, EITHER SOMETHING WENT VERY WRONG OR YOURE USING A 286 WITH 640KB OF RAM TO RUN IT, IF YOU ARE, MAD RESPECT");
		exit(1);
	}
	return toReturn;
}

Polynomial createEmptyPolynomial()
{
	polyElement* emptyPoly;

	emptyPoly = allocatePolyElement();

	emptyPoly->coefficient = 0.0f;
	emptyPoly->exponent = -1;
	emptyPoly->nextElement = emptyPoly;

	return emptyPoly;
}

void insertElement(Polynomial poly, float coefficient, int exponent)
{
	polyElement* currentElement;
	polyElement* nextElement;

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement->exponent > exponent)
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;

	}

	polyElement* toInsert;

	toInsert = allocatePolyElement();

	toInsert->coefficient = coefficient;
	toInsert->exponent = exponent;
	toInsert->nextElement = nextElement;

	currentElement->nextElement = toInsert;
}

polyElement* getElementAt(Polynomial poly, int index)
{
	polyElement* currentElement;
	polyElement* nextElement;

	currentElement = poly;
	nextElement = currentElement->nextElement;

	for(int i = 0; i < index; i++)
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;
	}

	return currentElement;
}

void printPolynomial(Polynomial poly)
{
	polyElement* currentElement;
	polyElement* nextElement;

	int firstElement = 1;

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement != poly)
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;
	
		if(firstElement == 0)
		{
			if((currentElement->coefficient) >= 0.0f)
			{
				printf("+");
			}
			else
			{
				printf("-");
			}
		}

		printf("%f*x^%d", fabs(currentElement->coefficient), currentElement->exponent);

		firstElement = 0;
	}

	printf("\n");
}

Polynomial CriaPolinomio(char expr[]){
  Polynomial p;
  int expo,r,n,nn;
  float coef,sinal = 1.0;
  char c;
 
  nn = 0;
  p = createEmptyPolynomial();

  while(1){
    r = sscanf(expr+nn," %f * x ^ %d %n",&coef, &expo,&n);
    if(r == 0 || r == EOF) 
      break;
    nn += n;
 
    insertElement(p, sinal*coef, expo);
     
    r = sscanf(expr+nn,"%c %n",&c,&n);
    if(r == EOF || r == 0)
      break;
    nn += n;
 
    if(c == '-')
      sinal = -1.0;
    else
      sinal = 1.0;
  }
  return p;
}


//A 
//---------------------------------------------------------

float Valor(Polynomial poly, float x)
{
	polyElement* currentElement;
	polyElement* nextElement;

	float currentValue = 0.0f;

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement != poly)
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;

		currentValue += (currentElement->coefficient)*(pow(x,(currentElement->exponent)));
	}

	return currentValue;
}

//B
//---------------------------------------------------------

void LiberaPolinomio(Polynomial poly)
{
	polyElement* currentElement;
	polyElement* nextElement;

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement != poly)
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;

		free(currentElement);
	}

	free(poly);

	//Não tenho total confiança se isso funcionaria, ACREDITO que funcionaria, já que o while percorre e libera todos os valores a 
	//partir do nó cabeça, mas ignora o nó cabeça, e o free(poly) libera o nó cabeça, ou seja deveria liberar todo o polinomio.
}

//C
//-----------------------------------------------------------

Polynomial Derivada(Polynomial poly)
{
	polyElement* currentElement;
	polyElement* nextElement;

	Polynomial derivative;
	derivative = createEmptyPolynomial();

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement != poly && ((nextElement->exponent) > 0))
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;
		
		insertElement(derivative, (currentElement->coefficient)*(currentElement->exponent), (currentElement->exponent)-1);
	}

	return derivative;
}

//D
//-----------------------------------------------------------

Polynomial SegundaDerivada(Polynomial poly)
{
	polyElement* currentElement;
	polyElement* nextElement;

	Polynomial derivative;
	derivative = createEmptyPolynomial();

	currentElement = poly;
	nextElement = currentElement->nextElement;

	while(nextElement != poly && ((nextElement->exponent) > 1))
	{
		currentElement = nextElement;
		nextElement = currentElement->nextElement;
		
		insertElement(derivative, (currentElement->coefficient)*((currentElement->exponent)-1)*(currentElement->exponent), (currentElement->exponent)-2);
	}

	return derivative;
}



int main()
{
	printf("Por favor insira um polinomio (max. 256 caracteres):\n");

	float x;

	//Limitei a entrada a um buffer de 256 bytes, poderia FACILMENTE ser aumentado pra 1000+ para impossibilitar qualquer problema
	//de leitura de polinomios muito grandes, mas 256 me parece um tamanho mais que razoavel para este buffer.
	char stringBuffer[256]; 

	scanf("%f %s", &x, stringBuffer);

	Polynomial poly = CriaPolinomio(stringBuffer);
	Polynomial deri1 = Derivada(poly);
	Polynomial deri2 = SegundaDerivada(poly);

	printf("%f\n", Valor(poly, x));
	printPolynomial(deri1);
	printPolynomial(deri2);

	LiberaPolinomio(poly);
	LiberaPolinomio(deri1);
	LiberaPolinomio(deri2);
}