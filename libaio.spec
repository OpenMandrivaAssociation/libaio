%define major	1
%define	libname	%mklibname aio %{major}
%define	devname %mklibname aio -d

Summary: 	Linux-native asynchronous I/O access library
Name:		libaio
Version:	0.3.109
Release:	5
License: 	LGPLv2+
Group:	 	System/Libraries
Source0: 	ftp://ftp.kernel.org/pub/linux/libs/aio/%{name}-%{version}.tar.bz2
Patch0:		libaio-install-to-slash.patch
Patch1:		libaio-aarch64.patch
Patch2:		libaio-generic-syscall.patch

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
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package -n	%{devname}
Summary:	Development and include files for libaio
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel
Obsoletes:	%{_lib}aio-static-devel

%description -n	%{devname}
This archive contains the header-files for %{name} development.

%prep
%setup -q -a 0
mv %{name}-%{version} compat-%{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%{optflags}"
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
%make \
    soname='libaio.so.1.0.0' libname='libaio.so.1.0.0' \
    CC=%{__cc} \
    CFLAGS="%{optflags} -nostdlib -nostartfiles -I. -fPIC"
cd ..
%make CC=%{__cc} CFLAGS="%{optflags} -nostdlib -nostartfiles -I. -fPIC"

%install
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
%make libdir=%{buildroot}%{_libdir} \
	includedir=%{buildroot}%{_includedir} \
    install

rm -f %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%{_libdir}/libaio.so.%{major}*

%files -n %{devname}
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so

