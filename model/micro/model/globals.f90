!globals.f90

! Module for general UMAT settings and variables
      module GlobalVariables
        implicit none
       
        ! ----------------------------------------------------------
        ! Settings for the user of the UMAT
        ! ----------------------------------------------------------
        
        ! Material parameters
        ! -------------------
        
        ! path to graindata.txt wrt the location of umatCP.f90
        character(len=256) :: graindata_path = "/../model/graindata.txt"
        
        ! ----------------------------------------------------------
        ! Technical stuff - DO NOT CHANGE!
        ! ----------------------------------------------------------
        
        integer :: approxnumelements = 5000000                                       ! Approximate maximum number of elements used in the analysis for allocation of arrays
                                                                                     ! If more elements are present, arrays are automatically extended
        
        ! UMAT variables
        double precision, dimension(:,:,:), allocatable   :: orientationRotMat       ! rotation matrix for global to local csys
    
      end module GlobalVariables
