%define major_c 15
%define libname %mklibname %{name} %{major_c}
%define devname %mklibname -d %{name}

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.7.4
Release:	1
Group:		Development/C
License:	NetCDF
Url:		http://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
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

%package -n	%{devname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the netCDF-4 header files, shared devel libs, and
man pages.

%prep
%setup -qn netcdf-c-%{version}
%autopatch -p1

%build
%configure \
	--enable-shared \
	--disable-static \
	--enable-netcdf-4 \
	--enable-dap \
	--enable-extra-example-tests \
	--disable-dap-remote-tests

%make_build

%check
%ifarch %arm
make check || cat dap4_test/test-suite.log
%else
make check
%endif

%install
%make_install

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

# test plugins accidentally get installed
rm -f %{buildroot}%{_libdir}/libmisc.so
rm -f %{buildroot}%{_libdir}/libbzip2.so

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
