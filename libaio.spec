%define major	1
%define	libname	%mklibname aio %{major}
%define	develname %mklibname aio -d
%define	staticname %mklibname aio -d -s

Summary: 	Linux-native asynchronous I/O access library
Name:		libaio
Version:	0.3.109
Release:	4
License: 	LGPLv2+
Group:	 	System/Libraries
Source0: 	ftp://ftp.kernel.org/pub/linux/libs/aio/%{name}-%{version}.tar.bz2
Patch0:		libaio-install-to-slash.patch

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
Provides:		%{name} = %{version}-%{release}

%description -n %{libname}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package -n	%{develname}
Summary:	Development and include files for libaio
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel

%description -n	%{develname}
This archive contains the header-files for %{libname} development.

%package -n	%{staticname}
Summary:	Development components for libaio
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Obsoletes:	%{libname}-static-devel

%description -n	%{staticname}
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

%files -n %{libname}
%{_libdir}/libaio.so.%{major}*

%files -n %{develname}
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so

%files -n %{staticname}
%{_libdir}/libaio.a

