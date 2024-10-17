%define major		0
%define libname		%mklibname ts %{major}
%define develname	%mklibname ts -d

Name:		tslib
Version:	1.18
Release:	2
Source0:	https://github.com/kergoth/tslib/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0:		use-format-argument-with-sprintf.patch
Summary:	Touchscreen access library
URL:		https://developer.berlios.de/projects/tslib/
License:	GPLv2+
Group:		System/Libraries

%description
Hardware independent touchscreen access library.

%package utils
Summary:	Touchscreen access library utilities
Group:		System/Kernel and hardware

%description utils
Hardware independent touchscreen access library.

This package contains the tslib utilities.

%package common
Summary:	Touchscreen access library common files
Group:		System/Kernel and hardware
BuildArch:	noarch

%description common
Hardware independent touchscreen access library.

This package contains the tslib configuration file and documentation.

%package -n %{libname}
Summary:	Touchscreen access library
Group:		System/Libraries
Requires:	%{name}-common >= %{version}
Obsoletes:	%{_lib}ts1.0_0 < 1.15-2

%description -n %{libname}
Hardware independent touchscreen access library.

%package -n %{develname}
Summary:	Development library and headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libts-devel = %{version}-%{release}

%description -n %{develname}
Development files (headers etc.) for %{name}.

%prep
%autosetup -p1
perl -pi -e 's,^# module_raw input$,module_raw input,' etc/ts.conf
# For quick verification during building:
grep "module_raw input" etc/ts.conf

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%files utils
%{_bindir}/ts_*

%files common
%doc README* AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/ts.conf
%{_mandir}/man*/*

%files -n %{libname}
%{_libdir}/*.so.%{major}{,.*}
%dir %{_libdir}/ts
%{_libdir}/ts/*.so

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/tslib.h
%{_libdir}/pkgconfig/*.pc
