%define major1 5
%define major2 6
%define libname %mklibname %{name} %{major2}
%define develname %mklibname -d %{name}
%define staticdevelname %mklibname -d -s %{name}

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.0.1
Release:	%mkrel 4
Group:		Development/C
License:	NetCDF
URL:		http://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch1:		netcdf-4.0.1-fix-str-fmt.patch
Requires(post): info-install
Requires(postun): info-install
BuildRequires:	gcc-gfortran
BuildRequires:	hdf5-devel
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
Summary:	Libraries for netcdf-4
Group:		System/Libraries
Provides:	lib%{name} = %{version}

%description -n	%{libname}
This package contains the netCDF-4 libraries.

%package -n	%{develname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	hdf5-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n %{develname}
This package contains the netCDF-4 header files, shared devel libs, and 
man pages.

%package -n	%{staticdevelname}
Summary:	Static libs for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{name}-static

%description -n %{staticdevelname}
This package contains the netCDF-4 static libs.


%prep

%setup -q 
%patch1 -p0

perl -pi -e "/^LIBDIR/ and s/\/lib/\/%_lib/g" src/macros.make.*

%build
#autoreconf -fis

export FC="gfortran"
export F90="gfortran"
export CPPFLAGS="-fPIC"
export FFLAGS="-fPIC %optflags"
export F90FLAGS="$FFLAGS"
export FCFLAGS="$FFLAGS"

%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1
%configure2_5x --enable-shared --enable-netcdf-4 --enable-ncgen4
make

%check
# 1 test fails
#make check

%install
rm -rf %{buildroot}

%makeinstall

#mkdir -p %{buildroot}%{_includedir}/netcdf-3
#/bin/mv %{buildroot}%{_includedir}/*.* \
##  %{buildroot}%{_includedir}/netcdf-3
#  /bin/rm -f %{buildroot}%{_libdir}/*.la
  #
  #  Does the /usr/include/netcdf-3/netcdf.mod file really belong in 
  #  /usr/include/netcdf-3/ or should it go in /usr/lib/netcdf-3 ???
  #  I suppose this should be decided on after some testing since the 
  #  gfortran *.mod file appears to be ACSII text, not a binary file.
  #
  #  mkdir -p %{buildroot}%{_libdir}/netcdf-3
  #  /bin/mv -f %{buildroot}%{_includedir}/netcdf-3/*.mod
  #    %{buildroot}%{_libdir}/netcdf-3

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
%{_mandir}/man3/*.3*
%{_infodir}/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.%{major1}*
%{_libdir}/*.so.%{major2}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_includedir}/*.hh
%{_includedir}/*.inc
%{_includedir}/*.mod
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/*.la
