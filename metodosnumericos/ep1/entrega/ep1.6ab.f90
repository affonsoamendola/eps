PROGRAM ep1_6
IMPLICIT NONE
!Desativando as variaveis implicitas

    !Exercício Programa 1
    !Affonso Gino Amendola Neto, N°USP 9301753
    !
    !Determinar, a partir de uma serie de dados, a densidade 
    !numérica de grãos circundando uma estrela em uma camada de poeira
    
    DOUBLE PRECISION :: r_n 
    DOUBLE PRECISION :: r_x1
    DOUBLE PRECISION :: r_x2
    DOUBLE PRECISION :: r_criteria

    DOUBLE PRECISION :: r_return
    DOUBLE PRECISION :: CALCULATE_ROOT
    !----------------------------------------------------------------------------------------------------------------------------------------------------------]
    
    r_x1 = 0d0
    r_x2 = 2d0
    r_criteria = 1d-5

    r_return = CALCULATE_ROOT(r_x1, r_x2, r_criteria)
    PRINT*, r_return
END PROGRAM

DOUBLE PRECISION FUNCTION BLACK_BODY_EMISSION(d_wavelength, d_temp)

    DOUBLE PRECISION :: d_wavelength
    DOUBLE PRECISION :: d_temp
    DOUBLE PRECISION :: d_radiance

    DOUBLE PRECISION :: d_tempHolder

    DOUBLE PRECISION :: d_PlanckConst = 6.62607004d-34
    !Planck Constant in m²*kg*s^⁻1
    DOUBLE PRECISION :: d_c =  2.99792458d+8
    !Speed of Light in (m*s⁻1
    DOUBLE PRECISION :: d_BoltzmannConst = 1.38064852d-23
    !Boltzmann Constant in (microm)²*kg*s^-2*K^-1
    !Declaração de variaveis
    !-------------------------------------------------------------------------------

    d_tempHolder = 1d0/(EXP((d_PlanckConst*d_c)/(d_BoltzmannConst*d_temp*d_wavelength))-1d0)
    !Calcula o fator de planck em uma variavel separada para facilitar a leitura

    d_radiance = (d_tempHolder*2d0*d_PlanckConst*(d_c**2d0))/(d_wavelength**5d0)
    !calcula a radiancia a partir da equação de planck

    BLACK_BODY_EMISSION = d_radiance
    RETURN
END FUNCTION

DOUBLE PRECISION FUNCTION CALCULATE_ROOT(r_x1, r_x2, r_criteria)
    !Encontra a raiz da funcão R_FUNCTION usando o metodo da falsa posiçao, tendo como input um intervalo onde se supõe que só existe uma raiz

    DOUBLE PRECISION :: r_x1
    DOUBLE PRECISION :: r_x2
    
    DOUBLE PRECISION :: r_fx1
    DOUBLE PRECISION :: r_fx2 

    DOUBLE PRECISION :: r_criteria 
    DOUBLE PRECISION :: r_current_estimate
    DOUBLE PRECISION :: r_fcurrent_estimate

    DOUBLE PRECISION :: r_current_slope

    DOUBLE PRECISION :: EQ_46

    !Declaração de variaveis
    !-------------------------------------------------------------------------------

    r_fx1 = EQ_46(r_x1)
    r_fx2 = EQ_46(r_x2)
    r_current_estimate = r_x2
    r_fcurrent_estimate = r_fx2

    DO WHILE(r_fcurrent_estimate > r_criteria .OR. r_fcurrent_estimate < 0.-r_criteria)

        r_current_slope = (r_x1-r_x2)/(r_fx2-r_fx1)

        IF((r_x1-r_x2==r_x1 .OR. r_x2-r_x1==r_x2) .AND. (r_x1 /= 0.) .AND. (r_x2 /= 0.)) THEN
            PRINT *, "r_x1 or r_x2 is too small in comparison to r_x2 or r_x1 respectively, causing an addition with a factor smaller than Epsilon"
            EXIT
        ENDIF
        IF((r_fx2-r_fx1==r_fx2 .OR. r_fx1-r_fx2==rfx1) .AND. (r_fx1 /= 0.) .AND. (r_fx2 /= 0.)) THEN
            PRINT *, "r_fx1 or r_fx2 is too small in comparison to r_fx2 or r_fx1 respectively, causing an addition with a factor smaller than Epsilon"
            EXIT
        ENDIF

        r_current_estimate = r_x1 + r_current_slope*r_fx1
        r_fcurrent_estimate = EQ_46(r_current_estimate)

        IF((r_fx1*r_fcurrent_estimate)<0) THEN

            r_x2 = r_current_estimate
            r_fx2 = r_fcurrent_estimate

        ELSE IF((r_fx2*r_fcurrent_estimate)<0) THEN
          
            r_x1 = r_current_estimate
            r_fx1 = r_fcurrent_estimate

        ENDIF
    END DO

    CALCULATE_ROOT = r_current_estimate
    RETURN
END FUNCTION

REAL FUNCTION CALCULATE_ROOT_BISECTION(r_x1, r_x2, r_criteria)
    !Encontra a raiz da funcão R_FUNCTION usando o metodo da falsa posiçao, tendo como input um intervalo onde se supõe que só existe uma raiz

    REAL :: r_x1
    REAL :: r_x2
    
    REAL :: r_fx1
    REAL :: r_fx2 

    REAL :: r_criteria 
    REAL :: r_current_estimate
    REAL :: r_fcurrent_estimate

    REAL :: r_current_slope

    REAL :: EQ_46

    !Declaração de variaveis
    !-------------------------------------------------------------------------------

    r_fx1 = EQ_46(r_x1)
    r_fx2 = EQ_46(r_x2)
    r_current_estimate = r_x2
    r_fcurrent_estimate = r_fx2

    DO WHILE(r_fcurrent_estimate > r_criteria .OR. r_fcurrent_estimate < 0.-r_criteria)

        r_current_estimate = r_x1 + r_x2
        r_fcurrent_estimate = EQ_46(r_current_estimate)

        IF((r_fx1*r_fcurrent_estimate)<0) THEN

            r_x2 = r_current_estimate
            r_fx2 = r_fcurrent_estimate

        ELSE IF((r_fx2*r_fcurrent_estimate)<0) THEN
          
            r_x1 = r_current_estimate
            r_fx1 = r_fcurrent_estimate

        ENDIF
    END DO

    CALCULATE_ROOT_BISECTION = r_current_estimate
    RETURN
END FUNCTION

DOUBLE PRECISION FUNCTION EQ_46(r_n)
    
    DOUBLE PRECISION :: r_n 
    DOUBLE PRECISION :: r_j
    DOUBLE PRECISION :: r_k
    DOUBLE PRECISION :: r_radius_star
    DOUBLE PRECISION :: r_sun
    DOUBLE PRECISION :: r_pi
    DOUBLE PRECISION :: r_effective_t
    DOUBLE PRECISION :: r_radius_internal
    DOUBLE PRECISION :: r_radius_external
    DOUBLE PRECISION :: r_radius_grain
    DOUBLE PRECISION :: r_grain_temperature

    DOUBLE PRECISION :: r_result

    DOUBLE PRECISION :: BLACK_BODY_EMISSION 

    DOUBLE PRECISION  :: r_numerador
    DOUBLE PRECISION  :: r_denominador
    !Declaração de variaveis
    !--------------------------------------------------------------------

    r_sun = 6.957d8
    r_pi = 3.14159265359
    r_j = 1.6d0
    r_k = 2.2d0
    r_radius_star = 10d0
    r_effective_t = 3000d0
    r_radius_grain = 0.2d0
    r_radius_internal = 200d0
    r_radius_external = 2000d0
    r_grain_temperature = 800d0
    !Definindo as constantes colocadas pelo exercicio

    r_numerador = ((r_radius_star*r_sun)**2d0)*BLACK_BODY_EMISSION(r_j*1e-6, r_effective_t) + ((4d0*r_pi*(r_radius_grain*1d-6)**2d0)/3d0)*((r_radius_external*r_sun)**3-(r_radius_internal*r_sun)**3)*BLACK_BODY_EMISSION(r_j*1e-6,r_grain_temperature)*r_n
    r_denominador = ((r_radius_star*r_sun)**2d0)*BLACK_BODY_EMISSION(r_k*1e-6, r_effective_t) + ((4d0*r_pi*(r_radius_grain*1d-6)**2d0)/3d0)*((r_radius_external*r_sun)**3-(r_radius_internal*r_sun)**3)*BLACK_BODY_EMISSION(r_k*1e-6,r_grain_temperature)*r_n
    !Separei em numerador e denominador para facilitar a leitura

    r_result = (r_j*1e-6-r_k*1e-6) + 2.5d0*LOG10(r_numerador/r_denominador)
    EQ_46 = r_result
    RETURN
END FUNCTION 