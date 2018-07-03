%define major 1
%define libname %mklibname aio %{major}
%define devname %mklibname aio -d

Summary:	Linux-native asynchronous I/O access library
Name:		libaio
Version:	0.3.111
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Source0:	https://fedorahosted.org/releases/l/i/libaio/%{name}-%{version}.tar.gz
Patch0:		libaio-install-to-destdir-slash-usr.patch

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.
You may require this package if you want to install some DBMS.

%package -n %{libname}
Summary:	Dynamic libraries for libaio
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package -n %{devname}
Summary:	Development and include files for libaio
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}aio-static-devel < 0.3.109-5

%description -n %{devname}
This archive contains the header-files for %{name} development.

%prep
%setup -q -a 0
%apply_patches
mv %{name}-%{version} compat-%{name}-%{version}

%build
%setup_compile_flags
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
%make CC=%{__cc} CFLAGS="%{optflags} -fno-stack-protector -nostdlib -nostartfiles -I. -fPIC" soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
%make CC=%{__cc} CFLAGS="%{optflags} -fno-stack-protector -nostdlib -nostartfiles -I. -fPIC"

%install
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
make destdir=%{buildroot} prefix=/ libdir=%{libdir} usrlibdir=%{_libdir} \
    includedir=%{_includedir} install

find %{buildroot} -name '*.a' -delete

%files -n %{libname}
%{_libdir}/libaio.so.%{major}*

%files -n %{devname}
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so
