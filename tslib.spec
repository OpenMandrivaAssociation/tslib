
%define name	tslib
%define version	1.0
%define date	0
%define rel	5

%define api	0.0
%define major	0
%define libname	%mklibname ts %api %major
# (anssi) unversioned libts.so symlink exists, so no %api in develname
%define develname %mklibname ts -d

Name:		%{name}
Version:	%{version}
%if %{date}
Release:	%mkrel 0.%{date}.%{rel}
Source:		%name-%{date}.tar.bz2
%else
Release:	%mkrel %{rel}
Source:		http://download.berlios.de/tslib/%name-%version.tar.bz2
%endif
Patch0:		tslib-glibc2.8.patch
Summary:	Touchscreen access library
URL:		http://developer.berlios.de/projects/tslib/
License:	GPL
Group:		System/Libraries
BuildRoot:	%_tmppath/%name-root

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

%build
./autogen.sh
%configure2_5x --with-plugindir=%{_libdir}/ts%{api}_%{major}
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# (anssi) not needed for these libraries
rm %{buildroot}%{_libdir}/ts%{api}_%{major}/*.la

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files utils
%defattr(-,root,root)
%_bindir/ts_*

%files common
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%config(noreplace) %_sysconfdir/ts.conf

%files -n %{libname}
%defattr(-,root,root)
%_libdir/*-%{api}.so.%{major}*
%dir %_libdir/ts%{api}_%{major}
%_libdir/ts%{api}_%{major}/*.so

%files -n %{develname}
%defattr(-,root,root)
%_libdir/*.so
%_libdir/*.la
%_includedir/tslib.h
%_libdir/pkgconfig/*.pc
