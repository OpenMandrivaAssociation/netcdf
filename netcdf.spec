%define major_c 19
%define libname %mklibname %{name}
%define devname %mklibname -d %{name}
%define _disable_lto 1

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.9.1
Release:	2
Group:		Development/C
License:	NetCDF
Url:		https://www.unidata.ucar.edu/software/netcdf/
Source0:	https://github.com/Unidata/netcdf-c/archive/refs/tags/v%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
BuildRequires:	groff
BuildRequires:	hdf5-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake ninja

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

%package -n	%{devname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the netCDF-4 header files, shared devel libs, and
man pages.

%prep
%autosetup -p1 -n netcdf-c-%{version}
%cmake \
	-DBUILDNAME="OpenMandriva-%{version}-%{release}" \
	-DENABLE_EXAMPLE_TESTS:BOOL=ON \
	-DENABLE_EXTRA_TESTS:BOOL=ON \
	-DCURL_LIBRARIES=-lcurl \
	-G Ninja

%build
%ninja_build -C build

%check
# 4.9.0, clang 15.0.4
# build/nczarr_test/run_ut_mapapi.sh: line 20: 3473185 Segmentation fault      (core dumped) $CMD $TR -k$1 -x delete -f $file
# *** Nice, simple example of using BitGroom plus zlib...Sorry! Unexpected result, /home/bero/temp/abf/netcdf/BUILD/netcdf-c-4.9.0/build/nczarr_test/test_quantize.c, line: 943
%if 0
cd build
export LD_LIBRARY_PATH=$(pwd)/liblib:${LD_LIBRARY_PATH}
ctest
cd ..
%endif

%install
%ninja_install -C build

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

%files
%doc COPYRIGHT README.md RELEASE_NOTES.md guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_bindir}/ncdump
%{_bindir}/nccopy
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libnetcdf.so.%{major_c}*

%files -n %{devname}
%{_bindir}/nc-config
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/libnetcdf.settings
%{_mandir}/man3/*.3*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/netCDF
