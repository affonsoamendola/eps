program ep2
implicit none

    REAL, dimension(2,2) :: r_MatrixA 
    REAL, dimension(2) :: r_MatrixB

    REAL, dimension(2) :: r_Pivot

    REAL :: r_largestValue
    
    INTEGER :: i_pivotLocation

    INTEGER :: i
    !-----------------------------------
    
    interface
        subroutine pivotMatrix(r_Matrix, r_Pivot)
            implicit none

            REAL, dimension(:,:) :: r_Matrix
            REAL, dimension(:) :: r_Pivot

            REAL :: r_largestValue
            INTEGER :: i_pivotLocation

            INTEGER :: c
            INTEGER :: l
            INTEGER :: i

            LOGICAL :: l_alreadyPivoted

        end subroutine
    end interface

    r_MatrixA(1,1) = 1.
    r_MatrixA(2,1) = 3.
    r_MatrixA(1,2) = 2.
    r_MatrixA(2,2) = 4.

    CALL pivotMatrix(r_MatrixA, r_Pivot)

    PRINT *, r_MatrixA
    PRINT *, r_Pivot

end program

subroutine pivotMatrix(r_Matrix, r_Pivot)
    implicit none
        REAL, dimension(:,:) :: r_Matrix
        REAL, dimension(:) :: r_Pivot

        REAL :: r_largestValue
        INTEGER :: i_pivotLocation

        INTEGER :: c
        INTEGER :: l
        INTEGER :: i

        LOGICAL :: l_alreadyPivoted

        r_largestValue = r_Matrix(1,1)
        i_pivotLocation = 1

        do c=1,size(r_Matrix, 1)

            l_alreadyPivoted = .FALSE.
            do l=1, size(r_Matrix, 2)

                do i=1, size(r_Matrix,1)
                    if(l == r_Pivot(i)) then
                        l_alreadyPivoted = .TRUE.
                    end if
                end do

                if(r_Matrix(l,c) > r_largestValue .AND. l_alreadyPivoted .eqv. .FALSE.) then 
                    
                    r_largestValue = r_Matrix(l,c)
                    r_Pivot(c) = l
                
                end if
            end do    
        end do
    end subroutine