%define major_c 7
%define major_cmm 4
%define major_fortran 5

%define libname %mklibname %{name} %{major_c}
%define libname_mm %mklibname %{name}mm %{major_cmm}
%define libname_fortran %mklibname %{name}_fortran %{major_fortran}
%define develname %mklibname -d %{name}
%define staticdevelname %mklibname -d -s %{name}

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		netcdf
Version:	4.1.3
Release:	2
Group:		Development/C
License:	NetCDF
URL:		http://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch2:		netcdf-4.1-pkgconfig.patch
BuildRequires:	gcc-gfortran
BuildRequires:	 hdf5-devel
BuildRequires:	curl-devel
BuildRequires:	zlib-devel
BuildRequires:	valgrind
BuildRequires:	texinfo
BuildRequires:	tetex-latex
BuildRequires:	groff
BuildRequires:	tirpc-devel

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

%package -n	%{develname}
Summary:	Development files for netcdf-4
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname_mm} = %{version}-%{release}
Requires:	%{libname_fortran} = %{version}-%{release}
Requires:	hdf5-devel
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < 4.0
Conflicts:	%{name} < 4.1

%description -n %{develname}
This package contains the netCDF-4 header files, shared devel libs, and
man pages.

%package -n	%{staticdevelname}
Summary:	Static libs for netcdf-4
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{staticdevelname}
This package contains the netCDF-4 static libs.

%prep
%setup -q
%patch2 -p1

%build
export FC="gfortran"
export F90="gfortran"
export CPPFLAGS="%{optflags} -fPIC"
export FFLAGS="-fPIC %{optflags}"
export F90FLAGS="$FFLAGS"
export FCFLAGS="$FFLAGS"

%define _disable_ld_no_undefined 1
%configure2_5x --enable-shared \
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
%defattr(-,root,root)
%doc COPYRIGHT README RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_bindir}/ncdump
%{_bindir}/nccopy
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
%{_bindir}/nc-config
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


%changelog
* Thu Dec 01 2011 Andrey Bondrov <abondrov@mandriva.org> 4.1.3-1mdv2012.0
+ Revision: 737102
- New version 4.1.3, new lib majors, remove odd lib provides

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 4.1.1-3
+ Revision: 666610
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 4.1.1-2mdv2011.0
+ Revision: 606819
- rebuild

* Sun Apr 25 2010 Emmanuel Andry <eandry@mandriva.org> 4.1.1-1mdv2010.1
+ Revision: 538712
- New version 4.1.1
- fix obsoletes

* Wed Feb 17 2010 Emmanuel Andry <eandry@mandriva.org> 4.1-1mdv2010.1
+ Revision: 506886
- BR tetex-latex
- netcdf doesn't like parallel on bs
- enable ncgen4 and dap
- disable dap remote tests

  + Funda Wang <fwang@mandriva.org>
    - fix build
    - New version 4.1

* Mon Jan 18 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-11mdv2010.1
+ Revision: 493073
- try to workaround linking issues against hdf5 disabling ld_no_undefined

* Sun Jan 17 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-10mdv2010.1
+ Revision: 492772
- rebuild for hdf5

* Sat Jan 16 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-9mdv2010.1
+ Revision: 492328
- update p0

* Fri Jan 15 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-8mdv2010.1
+ Revision: 491906
- add needed requires for devel package

* Fri Jan 15 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-7mdv2010.1
+ Revision: 491886
- do not obsolete provided library

* Fri Jan 15 2010 Emmanuel Andry <eandry@mandriva.org> 4.0.1-6mdv2010.1
+ Revision: 491864
- enable netcdf 4
- add linking patch from gentoo
- split libraries by languages
- fix obsoletes/provides

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 4.0.1-5mdv2010.0
+ Revision: 418729
- disable netcdf 4 for now

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 4.0.1-4mdv2010.0
+ Revision: 418635
- add missing provides

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 4.0.1-3mdv2010.0
+ Revision: 418622
- enable ncgen4
  explicit hdf5-devel for devel package

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 4.0.1-2mdv2010.0
+ Revision: 418610
- obsoletes old devel package to ease upgrade

* Thu Aug 20 2009 Emmanuel Andry <eandry@mandriva.org> 4.0.1-1mdv2010.0
+ Revision: 418519
- use libraries policy
- new majors 5 and 6
- disable test (1 test fails)
- New version 4.0.1
- drop P0
- update P1
- build with netcdf4 support (requires HDF5)
- update descriptions

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 4.0-1mdv2009.1
+ Revision: 365885
- fix str fmt

* Thu Aug 14 2008 Emmanuel Andry <eandry@mandriva.org> 4.0-1mdv2009.0
+ Revision: 271832
- New version
- fix license

* Sun Jul 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.6.3-1mdv2009.0
+ Revision: 232195
- 3.6.3
- added a patch from gentoo, though it won't help much
- use _disable_ld_as_needed and _disable_ld_no_undefined to make it build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Thauvin <nanardon@mandriva.org>
    - unzip source in %%install instead %%check

* Sun Jan 20 2008 Emmanuel Andry <eandry@mandriva.org> 3.6.2-4mdv2008.1
+ Revision: 155303
- fix devel static package name
- drop obsoletes

* Sat Jan 19 2008 Emmanuel Andry <eandry@mandriva.org> 3.6.2-3mdv2008.1
+ Revision: 155130
- fix obsoletes

* Sat Jan 19 2008 Emmanuel Andry <eandry@mandriva.org> 3.6.2-2mdv2008.1
+ Revision: 155081
- rebuild

* Thu Jan 03 2008 Emmanuel Andry <eandry@mandriva.org> 3.6.2-1mdv2008.1
+ Revision: 144107
- import netcdf


