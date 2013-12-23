%define date 0
%define rel 8

%define api 0.0
%define major 0
%define libname %mklibname ts %api %major
# (anssi) unversioned libts.so symlink exists, so no %api in develname
%define develname %mklibname ts -d

Name:		tslib
Version:	1.0
%if %{date}
Release:	%mkrel 0.%{date}.%{rel}
Source0:	%name-%{date}.tar.bz2
%else
Release:	8
Source0:	http://download.berlios.de/tslib/%name-%version.tar.bz2
%endif
Patch0:		tslib-glibc2.8.patch
Patch1:		tslib-1.0-automake1.13.patch

Summary:	Touchscreen access library
URL:		http://developer.berlios.de/projects/tslib/
License:	GPL
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

%description common
Hardware independent touchscreen access library.

This package contains the tslib configuration file and documentation.

%package -n %{libname}
Summary:	Touchscreen access library
Group:		System/Libraries
Requires:	%{name}-common = %{version}-%{release}

%description -n %{libname}
Hardware independent touchscreen access library.

%package -n %{develname}
Summary:	Development library and headers for %name
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libts-devel = %{version}-%{release}

%description -n %{develname}
Development files (headers etc.) for %name.

%prep
%setup -q
perl -pi -e 's,^# module_raw input$,module_raw input,' etc/ts.conf
# For quick verification during building:
grep "module_raw input" etc/ts.conf
%patch0 -p1
%patch1 -p0

%build
./autogen.sh
%configure2_5x --with-plugindir=%{_libdir}/ts%{api}_%{major}
%make

%install
%makeinstall_std
# (anssi) not needed for these libraries
rm %{buildroot}%{_libdir}/ts%{api}_%{major}/*.la

%files utils
%{_bindir}/ts_*

%files common
%doc README AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/ts.conf

%files -n %{libname}
%{_libdir}/*-%{api}.so.%{major}*
%dir %_libdir/ts%{api}_%{major}
%{_libdir}/ts%{api}_%{major}/*.so

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/tslib.h
%{_libdir}/pkgconfig/*.pc

