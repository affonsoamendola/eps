PROGRAM ep1
IMPLICIT NONE
!Desativando as variaveis implicitas

    !Exerc�cio Programa 1
    !Affonso Gino Amendola Neto, N�USP 9301753
    !
    !O objetivo desde exerc�cio � fazer uma subrotina que, dado um array num�rico de dimens�o 
    !arbitr�ria N, organizado  aleat�riamente,  retorne  um  array  ordenado  em  ordem 
    !crescente. Al�m disso, a subrotina deve calcular o n�mero de passos necess�rios para se 
    !cumprir a tarefa (Npassos).
    
    INTEGER :: i_N
    INTEGER :: i_stepsTaken
    REAL, ALLOCATABLE :: r_RandomNums(:)
    
    INTEGER :: i
    
    !Aloca��o de variaveis
    !----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    INTERFACE
        SUBROUTINE SORT_REAL_ARRAY(r_Array, i_stepsTaken)
            IMPLICIT NONE
            
            REAL, INTENT(INOUT)  :: r_Array(:)
            INTEGER, INTENT(OUT) :: i_stepsTaken
            
        END SUBROUTINE
    END INTERFACE
    !Declaracao da interface da subrotina
    
    PRINT *, "Digite o tamanho do array de n�meros aleatorios a ser organizado:"
    READ *, i_N
    !Obtem do usuario o tamanho do array
    
    ALLOCATE(r_RandomNums(i_N))
    r_RandomNums = 0
    !Aloca o espa�o nescess�rio para o array, e o inicializa com 0s

    CALL RANDOM_SEED()
    !Inicializa o randomizador com uma semente pseudoaleatoria

    DO i = 1, (i_N)
        CALL RANDOM_NUMBER(r_RandomNums(i))
    End DO
    !Preenche o array com n�meros aleat�rios

    PRINT *, "Array Aleat�rio"
    PRINT *, r_RandomNums
    !Printa os valores contidos no array n�o organizado

    CALL SORT_REAL_ARRAY(r_RandomNums, i_stepsTaken)
    !Chama a subrotina de organiza��o, para organizar o array

    PRINT *, "Array Ordenado"
    PRINT *, r_RandomNums
    !Printa os valores do array, agora organizado

    PRINT *, i_stepsTaken

END PROGRAM

SUBROUTINE SORT_REAL_ARRAY(r_Array, i_stepsTaken)
    IMPLICIT NONE

    REAL, INTENT(INOUT) :: r_Array(:)
    INTEGER, INTENT(OUT) :: i_stepsTaken

    REAL :: r_currentSmaller
    REAL :: r_tempHolder
    INTEGER :: i_smallerIndex

    INTEGER :: i
    INTEGER :: j
    !Aloca��o de variaveis
    !---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    i_stepsTaken = 0

    DO i=1, SIZE(r_Array)

        r_currentSmaller = r_Array(i)
        i_smallerIndex = i
        !Inicializa os menores valores encontrados como os primeiros valores, se eles n�o
        !forem de fato os menores, eles seram substituidos pelo menor valor no loop a seguir

        DO j = i, SIZE(r_Array)
        !Come�a o loop a partir da posi��o de i, para n�o substituir valores ja ordenados

            i_stepsTaken = i_stepsTaken + 1
            !Considerando uma compara��o como um passo, incrementa o valor de passos levados

            IF (r_currentSmaller > r_Array(j)) THEN

                i_stepsTaken = i_stepsTaken + 1
                !Considerando uma troca de valores como um passo, incrementa o valor de passos levados

                i_smallerIndex = j
                r_currentSmaller = r_Array(j)
            END IF
            !Se o valor sendo checado atualmente for menor que o suposto menor valor, troca o suposto 
            !menor valor pelo valor sendo checado atualmente, e o indice do suposto menor
            !valor pelo indice do checado atualmente

        END DO

        i_stepsTaken = i_stepsTaken + 1
        !Considerando uma troca de valores como um passo, incrementa o valor de passos levados 

        r_tempHolder = r_Array(i)
        r_Array(i) = r_currentSmaller
        r_Array(i_smallerIndex) = r_tempHolder
        !Troca o valor do indice i atual pelo menor valor encontrado no array inteiro.

    END DO
    !Para cada indice, a subrotina checa todos os valores a partir dele por um valor menor que ele, se encontrar
    !ela troca o valor contido no indice pelo menor valor encontrado
    !basicamente uma implementa��o de Selection Sort

END SUBROUTINE