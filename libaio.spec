%define	name	libaio
%define	version	0.3.104
%define	release	%mkrel 3

%define major	1
%define	libname	%mklibname aio %major
%define	libnamedev %{libname}-devel

%if %{mdkversion} < 200610
%define _requires_exceptions statically\\|linked
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}

Summary: 	Linux-native asynchronous I/O access library
License: 	LGPL
Group:	 	System/Libraries
Source: 	%{name}-%{version}.tar.bz2

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

%description -n	%{libnamedev}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

This archive contains the header-files for %{libname} development.

%package -n	%{libname}-static-devel
Summary:	Development components for libaio
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

This archive contains the static libraries (.a) 

%prep
%setup -q

%build
%make

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}/usr libdir=%{buildroot}/%{_libdir} root=%{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libaio.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libaio.a

