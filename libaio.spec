%define	name	libaio
%define	version	0.3.109
%define	release	%mkrel 4

%define major	1
%define	libname	%mklibname aio %major
%define	libnamedev %mklibname aio -d
%define	libnamedev_static %mklibname aio -d -s

Name:		%{name}
Version:	%{version}
Release:	%{release}

Summary: 	Linux-native asynchronous I/O access library
License: 	LGPLv2+
Group:	 	System/Libraries
Source: 	ftp://ftp.kernel.org/pub/linux/libs/aio/%{name}-%{version}.tar.bz2
Patch0:		libaio-install-to-slash.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.
You may require this package if you want to install some DBMS.

%package -n     %{libname}
Summary:        Dynamic libraries for libaio
Group:          System/Libraries
Provides:	%name = %version-%release

%description -n %{libname}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package -n	%{libnamedev}
Summary:	Development and include files for libaio
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel

%description -n	%{libnamedev}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

This archive contains the header-files for %{libname} development.

%package -n	%{libnamedev_static}
Summary:	Development components for libaio
Group:		Development/C
Requires:	%{libnamedev} = %{version}-%{release}
Obsoletes:	%{libname}-static-devel

%description -n	%{libnamedev_static}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

This archive contains the static libraries (.a) 

%prep
%setup -q -a 0
mv %{name}-%{version} compat-%{name}-%{version}

%build
export CFLAGS="%{optflags}"
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
%make \
    soname='libaio.so.1.0.0' libname='libaio.so.1.0.0' \
    CFLAGS="%{optflags} -nostdlib -nostartfiles -I. -fPIC"
cd ..
%make CFLAGS="%{optflags} -nostdlib -nostartfiles -I. -fPIC"

%install
rm -rf %{buildroot}
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
%make libdir=%{buildroot}%{_libdir} \
	includedir=%{buildroot}%{_includedir} \
    install

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libaio.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so

%files -n %{libnamedev_static}
%defattr(-,root,root)
%{_libdir}/libaio.a



%changelog
* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.109-3mdv2011.0
+ Revision: 660209
- mass rebuild

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.109-2mdv2011.0
+ Revision: 602517
- rebuild

* Mon Jan 11 2010 Jérôme Brenier <incubusss@mandriva.org> 0.3.109-1mdv2010.1
+ Revision: 489443
- new version 0.3.109
- fix Source url

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.3.107-3mdv2010.0
+ Revision: 425512
- rebuild

* Sun Mar 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.107-2mdv2009.1
+ Revision: 355399
- drop useless patch
- ship missing files

* Mon Mar 09 2009 Emmanuel Andry <eandry@mandriva.org> 0.3.107-1mdv2009.1
+ Revision: 353132
- New version 0.3.107
- sync with fedora

* Mon Aug 25 2008 Emmanuel Andry <eandry@mandriva.org> 0.3.104-6mdv2009.0
+ Revision: 275993
- apply devel policy
- fix license
- check major

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 0.3.104-5mdv2009.0
+ Revision: 248409
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.3.104-3mdv2008.1
+ Revision: 128421
- kill re-definition of %%buildroot on Pixel's request
- import libaio


* Sat Mar 25 2006 Giuseppe Ghib� <ghibo@mandriva.com> 0.3.104-3mdk
- Added _requires_exceptions statically\\|linked for release < 200610
  (workaround for bug in rpm-mandriva-setup for 2006.0).

* Thu Mar 16 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.3.104-2mdk
- Rebuild with new rpm-mandriva-setup to avoid false dependencies in -devel

* Wed Dec 28 2005 Austin Acton <austin@mandriva.org> 0.3.104-1mdk
- initial import from Loic Baudry <loic.baudry@laposte.com> with fixes
