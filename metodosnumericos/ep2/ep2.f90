program ep2
implicit none

    REAL, dimension(2,2) :: r_MatrixA 
    REAL, dimension(2) :: r_MatrixB

    REAL, dimension(2) :: r_Pivot

    REAL :: r_largestValue
    
    INTEGER :: i_pivotLocation

    INTEGER :: i
    !-----------------------------------
    !Declaração de variáveis

    !  1 2
    !  3 2

    r_largest = r_MatrixA(1,1)
    i_pivotLocation = 1

    do i=0,size(r_MatrixA, 2)
        if(r_MatrixA(1,i+1) > r_largest)

            r_largest = r_MatrixA(1,i+1)
            i_pivotLocation = i+1

        end if
    end do
    r_Pivot(1)= i_pivotLocation
end program