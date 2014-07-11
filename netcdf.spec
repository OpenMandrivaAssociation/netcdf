%define major_c 7
%define major_cmm 4
%define major_fortran 5
%define libname %mklibname %{name} %{major_c}
%define libname_mm %mklibname %{name}mm %{major_cmm}
%define libname_fortran %mklibname %{name}_fortran %{major_fortran}
%define devname %mklibname -d %{name}

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.1.3
Release:	10
Group:		Development/C
License:	NetCDF
Url:		http://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch2:		netcdf-4.1-pkgconfig.patch
BuildRequires:	gcc-gfortran
BuildRequires:	groff
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(zlib)

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

%description -n	%{libname}
This package contains the netCDF-4 C libraries.

%package -n	%{libname_mm}
Summary:	C++ libraries for netcdf-4
Group:		System/Libraries

%description -n	%{libname_mm}
This package contains the netCDF-4 C++ libraries.

%package -n	%{libname_fortran}
Summary:	Fortran libraries for netcdf-4
Group:		System/Libraries

%description -n	%{libname_fortran}
This package contains the netCDF-4 fortran libraries.

%package -n	%{devname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname_mm} = %{version}-%{release}
Requires:	%{libname_fortran} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the netCDF-4 header files, shared devel libs, and
man pages.

%prep
%setup -q
%apply_patches

%build
export FC="gfortran"
export F90="gfortran"
export CPPFLAGS="%{optflags} -fPIC"
export FFLAGS="-fPIC %{optflags}"
export F90FLAGS="$FFLAGS"
export FCFLAGS="$FFLAGS"
export LIBS="-ltirpc"
%define _disable_ld_no_undefined 1
%configure2_5x \
	--enable-shared \
	--disable-static \
	--enable-netcdf-4 \
	--enable-ncgen4 \
	--enable-dap \
	--enable-extra-example-tests \
	--disable-dap-remote-tests

make

%check
make check

%install
%makeinstall_std

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -


%files
%doc COPYRIGHT README RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_bindir}/ncdump
%{_bindir}/nccopy
%{_mandir}/man1/*.1*
%{_infodir}/*

%files -n %{libname}
%{_libdir}/libnetcdf.so.%{major_c}*

%files -n %{libname_mm}
%{_libdir}/libnetcdf_c++.so.%{major_cmm}*

%files -n %{libname_fortran}
%{_libdir}/libnetcdff.so.%{major_fortran}*

%files -n %{devname}
%{_bindir}/nc-config
%{_includedir}/*.h
%{_includedir}/*.hh
%{_includedir}/*.inc
%{_includedir}/*.mod
%{_libdir}/*.so
%{_mandir}/man3/*.3*
%{_libdir}/pkgconfig/*.pc

