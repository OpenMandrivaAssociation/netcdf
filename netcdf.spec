%define name netcdf
%define version 3.6.2
%define release %mkrel 1
%define major 4

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Libraries to use the Unidata network Common Data Form (netCDF)
License: distributable (see COPYRIGHT)
Source0: ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.bz2
Source1: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
URL: http://www.unidata.ucar.edu/packages/netcdf/index.html
Group: Development/C
BuildRequires: gcc-gfortran
Obsoletes: netcdf-devel <= %{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-root


%package devel
Summary:        Development files for netcdf-3
Group:          Development/C
Requires:       %{name} = %{version}-%{release}

%package static
Summary:        Static libs for netcdf-3
Group:          Development/C
Requires:       %{name} = %{version}-%{release}


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


%description devel
This package contains the netCDF-3 header files, shared devel libs, and 
man pages.

%description static
This package contains the netCDF-3 static libs.

%prep
%setup -q 
perl -pi -e "/^LIBDIR/ and s/\/lib/\/%_lib/g" src/macros.make.*

%build
export FC="gfortran"
export F90="gfortran"
export CPPFLAGS="-fPIC"
export FFLAGS="-fPIC %optflags"
export F90FLAGS="$FFLAGS"
export FCFLAGS="$FFLAGS"

%configure2_5x --enable-shared
%make


%install
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/netcdf-3
/bin/mv ${RPM_BUILD_ROOT}%{_includedir}/*.* \
  ${RPM_BUILD_ROOT}%{_includedir}/netcdf-3
  /bin/rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
  #
  #  Does the /usr/include/netcdf-3/netcdf.mod file really belong in 
  #  /usr/include/netcdf-3/ or should it go in /usr/lib/netcdf-3 ???
  #  I suppose this should be decided on after some testing since the 
  #  gfortran *.mod file appears to be ACSII text, not a binary file.
  #
  #  mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/netcdf-3
  #  /bin/mv -f ${RPM_BUILD_ROOT}%{_includedir}/netcdf-3/*.mod
  #    ${RPM_BUILD_ROOT}%{_libdir}/netcdf-3

%check
%make check

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYRIGHT README RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncdump
%{_mandir}/man1/*.1*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/netcdf-3
%{_libdir}/*.so
%{_mandir}/man3/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a



