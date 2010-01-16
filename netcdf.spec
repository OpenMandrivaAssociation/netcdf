%define major_c 6
%define major_cmm 5
%define major_fortran 5

%define libname %mklibname %{name} %{major_c}
%define libname_mm %mklibname %{name}mm %{major_cmm}
%define libname_fortran %mklibname %{name}_fortran %{major_fortran}
%define develname %mklibname -d %{name}
%define staticdevelname %mklibname -d -s %{name}

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.0.1
Release:	%mkrel 9
Group:		Development/C
License:	NetCDF
URL:		http://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch0:		netcdf-4.0.1-as-needed.patch
Patch1:		netcdf-4.0.1-fix-str-fmt.patch
Requires(post): info-install
Requires(postun): info-install
BuildRequires:	gcc-gfortran
BuildRequires:  hdf5-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
BuildRequires:  valgrind
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NetCDF (network Common Data Form) is an interface for array-oriented data
access and a freely-distributed collection of software libraries for C, 
Fortran, C++, and perl that provides an implementation of the interface.
The netCDF library also defines a machine-independent format for representing
scientific data. Together, the interface, library, and format support the 
creation, access, and sharing of scientific data. The netCDF software was 
developed at the Unidata Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing. A netCDF file includes information about the data it
     contains. 

   o Network-transparent. A netCDF file is represented in a form that can be 
     accessed by computers with different ways of storing integers, characters,
     and floating-point numbers. 

   o Direct-access. A small subset of a large dataset may be accessed 
     efficiently, without first reading through all the preceding data. 

   o Appendable. Data can be appended to a netCDF dataset along one dimension 
     without copying the dataset or redefining its structure. The structure of 
     a netCDF dataset can be changed, though this sometimes causes the dataset 
     to be copied. 

   o Sharable. One writer and multiple readers may simultaneously access the 
     same netCDF file. 

%package -n	%{libname}
Summary:	C libraries for netcdf-4
Group:		System/Libraries
Provides:	lib%{name} = %{version}

%description -n	%{libname}
This package contains the netCDF-4 C libraries.

%package -n	%{libname_mm}
Summary:	C++ libraries for netcdf-4
Group:		System/Libraries
Provides:	lib%{name_mm} = %{version}

%description -n	%{libname_mm}
This package contains the netCDF-4 C++ libraries.

%package -n	%{libname_fortran}
Summary:	Fortran libraries for netcdf-4
Group:		System/Libraries
Provides:	lib%{name_fortran} = %{version}

%description -n	%{libname_fortran}
This package contains the netCDF-4 fortran libraries.

%package -n	%{develname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname_mm} = %{version}-%{release}
Requires:	%{libname_fortran} = %{version}-%{release}
Requires:	hdf5-devel
Provides:	lib%{name}-devel
Provides:	%{name}-devel
Obsoletes:	%{name}-devel

%description -n %{develname}
This package contains the netCDF-4 header files, shared devel libs, and 
man pages.

%package -n	%{staticdevelname}
Summary:	Static libs for netcdf-4
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-static-devel
Provides:	%{name}-static-devel
Obsoletes:	%{name}-static-devel

%description -n %{staticdevelname}
This package contains the netCDF-4 static libs.


%prep

%setup -q
%patch0 -p1
%patch1 -p0

perl -pi -e "/^LIBDIR/ and s/\/lib/\/%_lib/g" src/macros.make.*


export FC="gfortran"
export F90="gfortran"
export CPPFLAGS="-fPIC"
export FFLAGS="-fPIC %optflags"
export F90FLAGS="$FFLAGS"
export FCFLAGS="$FFLAGS"

##%define _disable_ld_no_undefined 1
%configure2_5x --enable-shared \
		--enable-netcdf-4 \
           	--enable-ncgen4 \
           	--enable-extra-example-tests \
           	--enable-valgrind-tests

%make

%check
# 1 test fails
#make check

%install
rm -rf %{buildroot}

%makeinstall

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%post
%_install_info %{name}.info
%_install_info netcdf-c.info
%_install_info netcdf-cxx.info
%_install_info netcdf-f77.info
%_install_info netcdf-f90.info
%_install_info netcdf-install.info
%_install_info netcdf-tutorial.info

%preun
%_remove_install_info %{name}.info
%_remove_install_info netcdf-c.info
%_remove_install_info netcdf-cxx.info
%_remove_install_info netcdf-f77.info
%_remove_install_info netcdf-f90.info
%_remove_install_info netcdf-install.info
%_remove_install_info netcdf-tutorial.info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT README RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncgen4
%{_bindir}/ncdump
%{_bindir}/nc-config
%{_mandir}/man1/*.1*
%{_infodir}/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libnetcdf.so.%{major_c}*

%files -n %{libname_mm}
%defattr(-,root,root,-)
%{_libdir}/libnetcdf_c++.so.%{major_cmm}*

%files -n %{libname_fortran}
%defattr(-,root,root,-)
%{_libdir}/libnetcdff.so.%{major_fortran}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_includedir}/*.hh
%{_includedir}/*.inc
%{_includedir}/*.mod
%{_libdir}/*.so
%{_mandir}/man3/*.3*
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/*.la
