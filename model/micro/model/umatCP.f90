!umatCP.f90
! ----------------------------------------------------------------------
!
!       Main interface to ABAQUS to compute 
!       crystal plasticity behavior
!     
!       (c) Robert Bosch GmbH, CR/AMP3
!
!       
!       Coded by:       Jannick Kuhn (CR/AMP3)
!       Modified by:    Erik Natkowski (CR/AMP3)
!
! ----------------------------------------------------------------------     

include "globals.f90"

subroutine uexternaldb(lop,lrestart,time,dtime,kstep,kinc)
    implicit none

    integer, intent(in) :: lop, lrestart, kstep, kinc
    double precision, intent(in) :: dtime
    double precision, intent(in) :: time

    integer :: rank
    if (lop == 0) then
        call MutexInit( 1 ) 
    end if
    
end subroutine uexternaldb

subroutine umat(stress,statev,ddsdde,sse,spd,scd,rpl,ddsddt,drplde,drpldt,stran, &
     dstran,time,dtime,temp,dtemp,predef,dpred,cmname, &
     ndi,nshr,ntens,nstatv,props,nprops,coords,drot,pnewdt, &
     celent,dfgrd0,dfgrd1,noel,npt,layer,kspt,kstep,kinc)
    use GlobalVariables, only: HallPetchFlag, kHallPetchCoeff, nFSCoeff, &
                               C_kelvin, D_kelvin, kHallPetchCoeff_KH1, &
                               kHallPetchCoeff_KH2, usePWFLModAlgo, defaultCutback, &
                               orientationRotMat
    
    include "aba_param.inc"
    !implicit none

    dimension stress(ntens), statev(nstatv), ddsdde(ntens,ntens), &
       ddsddt(ntens), drplde(ntens), stran(ntens), dstran(ntens), &
       predef(1), dpred(1), props(nprops), coords(3), drot(3,3), &
       dfgrd0(3,3), dfgrd1(3,3), time(2)

    ! define user material
    ! can access orientation by
    !    orientationRotMat(noel, :, :)

return
end subroutine umat

! In order to define crystal orientions the *Orientation option in the abaqus .inp file is used
! Abaqus then gives the rotated quantities for stress, strain ... to the UMAT so the user doesnt
! have to rotate them
subroutine orient(T,noel,npt,layer,kspt,coords,basis,orname,nnodes,cnodes,jnnum)
    use GlobalVariables, only: graindata_path, orientationRotMat, approxnumelements

    include 'ABA_PARAM.INC'

    character*80 orname
    dimension T(3,3), coord(3), basis(3,3), cnodes (3,nnodes)
    dimension jnnum(nnodes)

! Define the local variables 
    double precision :: phi1 = 0.d0                        ! Euler angles in Bunge notation in degrees
    double precision :: PHI = 0.d0
    double precision :: phi2 = 0.d0
    double precision :: phi1Rad, PHIRad, phi2Rad                            ! angles in rad
    double precision :: cosphi1, cosPHI, cosphi2, sinphi1, sinPHI, sinphi2  ! direction cosines
    double precision :: pi, rad2grad, grad2rad                              ! used constants
    integer :: io_error, read_error
    integer :: n
    integer :: GrainID
    character(30) :: IDString, string1, string2, string3, string4, string5
    character(256) :: outdir
    character(256) :: GrainDataPath
    integer :: lenoutdir
    integer :: thread_id = 0
    integer :: readunit
    double precision, dimension(:,:,:), allocatable   :: tempOrientationRotMat
    call MutexLock(1)
! Which grain is considered, is defined by the number at the end of the orientation name
    call split_string(orname, string1, IDString, "-")
    read(IDString, *) GrainID
! In order to be able to locate the graindata.txt file one apperently has to use this
    call GETOUTDIR(outdir, lenoutdir)
    GrainDataPath = trim(outdir)//graindata_path
    
! open the graindata.txt and read the lines. When the programm comes across the line with number GrainID the input
! 3 angles are read
    thread_id = get_thread_id()
    readunit = 101+thread_id 
    if (readunit .lt. 101) then
      readunit = 101
    end if
    
    open(unit=readunit, file=GrainDataPath, status="old", action="read", iostat=io_error)
    if (io_error ==0) then
        n = 1
        do
            read(readunit,*, iostat=read_error) phi1, PHI, phi2
            if (n == GrainID) then
                exit
            else if (read_error > 0) then
                stop "Data error in file graindata.txt"
            else if (read_error < 0 ) then
                write(*,*) "Did not find euler angles to grain id: ", GrainID, " in the graindata.txt"   ! reached end of file
                call XIT()
            end if
            n = n+1
        end do
    else
        write(*,*) "Could not open ", GrainDataPath, "(IO Error ", io_error, " on unit ", readunit , ")"
        call XIT()
    end if
    close(readunit)

!   Start calculation of the rotation matrix 
!   Do some precalculations for simplicity
    pi = dacos(-1.d0)
    rad2grad = 180.d0/pi
    grad2rad = pi/180.d0
    phi1Rad = phi1 * grad2rad
    PHIRad = PHI * grad2rad
    phi2Rad = phi2 * grad2rad
    cosphi1 = dcos(phi1Rad)
    cosPHI = dcos(PHIRad)
    cosphi2 = dcos(phi2Rad)
    sinphi1 = dsin(phi1Rad)
    sinPHI = dsin(PHIRad)
    sinphi2 = dsin(phi2Rad)

! Calculate the rotation matrix using abaqus name convention
    T = 0.d0
    T(1,1) = cosphi1*cosphi2 - sinphi1*sinphi2*cosPHI
    T(1,2) = sinphi1*cosphi2 + cosphi1*sinphi2*cosPHI
    T(1,3) = sinphi2*sinPHI
    T(2,1) = -cosphi1*sinphi2 - sinphi1*cosphi2*cosPHI
    T(2,2) = -sinphi1*sinphi2 + cosphi1*cosphi2*cosPHI
    T(2,3) = cosphi2*sinPHI
    T(3,1) = sinphi1*sinPHI
    T(3,2) = -cosphi1*sinPHI
    T(3,3) = cosPHI
    T = transpose(T)
    
! Save orientations to global variable
    if (.not. allocated(orientationRotMat)) then
            allocate(orientationRotMat(approxnumelements, 3, 3))
    end if
    
    if (size(orientationRotMat,1) .lt. noel) then
        ! re-allocate orientationRotMat if size is too small
        ! see https://stackoverflow.com/questions/8264336/how-to-get-priorly-unknown-array-as-the-output-of-a-function-in-fortran
        allocate(tempOrientationRotMat(noel,3,3))
        tempOrientationRotMat(:size(orientationRotMat,1),:,:) = orientationRotMat
        call move_alloc(tempOrientationRotMat,orientationRotMat)
    end if
    
    orientationRotMat(noel,:,:) = T
    
    call MutexUnlock(1)
    return
end subroutine orient

! split a string into 2 either side of a delimiter token
recursive SUBROUTINE split_string(instring, string1, string2, delim)
    CHARACTER(30) :: instring, delim
    CHARACTER(30), INTENT(OUT):: string1, string2
    INTEGER :: index

    instring = TRIM(instring)

    index = SCAN(instring,delim)
    string1 = instring(1:index-1)
    string2 = instring(index+1:)

END SUBROUTINE split_string
   
recursive subroutine removesp(str)

        ! Removes spaces, tabs, and control characters in string str

        implicit none
        character(len=*):: str
        character(len=1):: ch
        character(len=len_trim(str))::outstr
        integer :: lenstr, k, i, ich

        str=adjustl(str)
        lenstr=len_trim(str)
        outstr=' '
        k=0

        do i=1,lenstr
        ch=str(i:i)
        ich=iachar(ch)
        select case(ich)    
        case(0:32)  ! space, tab, or control character
        cycle       
        case(33:)  
        k=k+1
        outstr(k:k)=ch
        end select
        end do

        str=adjustl(outstr)

end subroutine removesp

subroutine XIT()
    include 'ABA_PARAM.INC'
    call ABORT()
    return
end
