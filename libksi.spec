#
# Conditional build
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	Guardtime KSI Client API for C
Summary(pl.UTF-8):	API klienckie Guardtime KSI dla C
Name:		libksi
Version:	3.21.3075
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/guardtime/libksi/tags
Source0:	https://github.com/guardtime/libksi/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b85e765ce654a0f03fe24c5ab0025a8d
Patch0:		%{name}-sh.patch
Patch1:		%{name}-doxygen.patch
URL:		http://www.guardtime.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	curl-devel
%{?with_apidocs:BuildRequires:	doxygen >= 1.8.0}
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	rpm-build >= 4.6
Requires:	ca-certificates
Requires:	openssl >= 0.9.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Client-side runtime library for accessing Guardtime's KSI Blockchain
Service.

%description -l pl.UTF-8
Biblioteka kliencka do dostępu do usługi KSI Blockchain firmy
Guardtime.

%package devel
Summary:	Header files for Guardtime KSI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Guardtime KSI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	openssl-devel >= 0.9.8

%description devel
Client-side development headers for accessing Guardtime's KSI
Blockchain Service.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki do dostępu do usługi KSI Blockchain
firmy Guardtime.

%package static
Summary:	Static Gaurdtime KSI library
Summary(pl.UTF-8):	Biblioteka statyczna Guardtime KSI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Gaurdtime KSI library.

%description static -l pl.UTF-8
Biblioteka statyczna Guardtime KSI.

%package apidocs
Summary:	API documentation for Guardtime KSI library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Guardtime KSI
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Guardtime KSI library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Guardtime KSI.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-cafile=/etc/certs/ca-certificates.crt

%{__make}

%if %{with apidocs}
%{__make} -C doc htmldoc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libksi.la
# changelog packaged as %doc, license is generic Apache v2.0 text
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libksi

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md changelog
%attr(755,root,root) %{_libdir}/libksi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libksi.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libksi.so
%{_includedir}/ksi
%{_pkgconfigdir}/libksi.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libksi.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{search,*.css,*.html,*.js,*.png}
%endif
