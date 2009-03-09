%define	name	libaio
%define	version	0.3.107
%define	release	%mkrel 1

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
Source: 	%{name}-%{version}.tar.gz
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

%define libdir /%{_lib}
%define usrlibdir %{_prefix}/%{_lib}

%prep
%setup -a 0
%patch0 -p1
mv %{name}-%{version} compat-%{name}-%{version}

%build
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
%make soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
%make destdir=%{buildroot} prefix=/ libdir=%{buildroot}/%{_libdir} usrlibdir=%{usrlibdir} \
	includedir=%{_includedir} install

rm -rf %{buildroot}/home

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

