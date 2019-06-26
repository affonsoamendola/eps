#include <stdio.h>
#include <stdlib.h>

typedef enum boolean {false, true} bool;

typedef int TipoDado;

typedef struct _RegPilha
{
	TipoDado dado;
	struct _RegPilha* next;

} RegPilha;

typedef RegPilha* Pilha;

RegPilha* alocaRegPilha()
{
	RegPilha* novoElemento;
	novoElemento = (RegPilha*)calloc(1, sizeof(RegPilha));
	if(novoElemento == NULL) exit(-1);
	return	novoElemento;
}

Pilha criaPilha()
{
	Pilha novaPilha;
	novaPilha = alocaRegPilha();
	novaPilha->next = NULL;
	return novaPilha;
}

void destroyPilha(Pilha pilha)
{
	esvaziaPilha(pilha);
	free(pilha);
}

void esvaziaPilha(Pilha pilha)
{
	RegPilha *elementoAtual, *elementoProximo;
	elementoAtual = pilha;
	while(elementoAtual!=NULL)
	{
		elementoProximo = elementoAtual->next;
		free(elementoAtual);
		elementoAtual = elementoProximo;
	}
}

bool isPilhaVazia(Pilha pilha)
{
	if(pilha->next==NULL)
	{
		return true;
	}
	else
	{
		return false;
	}
}

void empilha(Pilha pilha, TipoDado dado)
{
	RegPilha *novoElemento;
	novoElemento = alocaRegPilha();
	novoElemento->dado = dado;
	novoElemento->next = pilha->next;
	pilha->next = novoElemento;
}

TipoDado desempilha(Pilha pilha)
{
	RegPilha *elementoAtual;
	TipoDado dado;

	elementoAtual = pilha->next;
	dado = elementoAtual->dado;

	pilha->next = elementoAtual->next;
	free(elementoAtual);
	return dado;
}

int charToInt(char a)
{
	int b = a-'0';
	return b;
}

int ValorExpressao(char prefixa[])
{
	int sizeString, temp;

	int a, b, i;

	for(i = 0; i<512; i++)
	{
		if(prefixa[i] == '\0') break;
	}

	sizeString = i;

	Pilha pilhaValores;

	pilhaValores = criaPilha();
	
	for(i = sizeString; i >= 0; i--)
	{	
		if(charToInt(prefixa[i]) >= 0 && charToInt(prefixa[i]) <= 9)
		{
			a = charToInt(prefixa[i]);
			empilha(pilhaValores, a);
		}
		else if(prefixa[i] == '+')
		{
			a = desempilha(pilhaValores);
			b = desempilha(pilhaValores);
			a = a+b;
			empilha(pilhaValores, a);
		}
		else if(prefixa[i] == '*')
		{
			a = desempilha(pilhaValores);
			b = desempilha(pilhaValores);	
			a = a*b;
			empilha(pilhaValores, a);
		}
	}
	temp = desempilha(pilhaValores);
	esvaziaPilha(pilhaValores);
	return(temp);
}

int main()
{
	char pre[512];
	int v;
	scanf("%s", pre);
	v = ValorExpressao(pre);
	printf("%d\n", v);
	return 0;
}