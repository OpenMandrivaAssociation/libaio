%define	name	libaio
%define	version	0.3.104
%define	release	%mkrel 6

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
Source: 	%{name}-%{version}.tar.bz2
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
%setup -q

%build
%make

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}/usr libdir=%{buildroot}/%{_libdir} root=%{buildroot}

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

