%define major 1
%define libname %mklibname aio %{major}
%define devname %mklibname aio -d
%define staticname %mklibname aio -d -s
# (tpg) This package uses ASMs to implement symbol versioning and is thus
# incompatible with LTO
%define _disable_lto 1

Summary:	Linux-native asynchronous I/O access library
Name:		libaio
Version:	0.3.113
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		https://pagure.io/libaio
Source0:	https://pagure.io/libaio/archive/libaio-%{version}/%{name}-%{version}.tar.gz

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

%description -n %{devname}
This archive contains the header-files for %{name} development.

# The static library is used by lvm2.
# Don't stop building it unless you drop its use there first.
%package -n %{staticname}
Summary:	Static library files for libaio
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
This archive contains the static library files for %{name} development.

%prep
%setup -q -a 0

mv %{name}-%{version} compat-%{name}-%{version}

%build
%set_build_flags
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the compat-libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd compat-%{name}-%{version}
%make_build CC=%{__cc} CFLAGS="%{optflags} -Wall -I. -fPIC" LDFLAGS="%{build_ldflags}" soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
%make_build CC=%{__cc} CFLAGS="%{optflags} -Wall -I. -fPIC" LDFLAGS="%{build_ldflags}"

%install
cd compat-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
%make_install libdir=%{_libdir}
#make destdir=%{buildroot} prefix=/ libdir=%{libdir} usrlibdir=%{_libdir} \
#    includedir=%{_includedir} install

%files -n %{libname}
%{_libdir}/libaio.so.%{major}*

%files -n %{devname}
%doc COPYING TODO
%{_includedir}/*
%{_libdir}/libaio.so

%files -n %{staticname}
%{_libdir}/libaio.a
