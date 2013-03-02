#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Interface components for OpenPGP
Name:		libcryptui
Version:	3.6.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://download.gnome.org/sources/libcryptui/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	817b4c51e0d067429e976b0db1e758ae
URL:		http://projects.gnome.org/seahorse/
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gpgme-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libSM-devel
Requires:	glib2 >= 1:2.26.0
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libcryptui is a library used for prompting for PGP keys.

%description -l pl.UTF-8
Biblioteka libcryptui.

%package devel
Summary:	Header files required to develop with libcryptui
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcryptui
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf2-devel >= 2.24.0
Requires:	gtk+3-devel >= 2.91.7

%description devel
The libcryptui-devel package contains the header files and developer
documentation for the libcryptui library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libcryptui.

%package apidocs
Summary:	libcryptui library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libcryptui
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libcryptui library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libcryptui.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcryptui.la

%find_lang cryptui --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files -f cryptui.lang
%defattr(644,root,root,755)
%doc AUTHORS  NEWS README
%attr(755,root,root) %{_bindir}/seahorse-daemon
%{_mandir}/man1/seahorse-daemon.1*
%attr(755,root,root) %{_libdir}/libcryptui.so.*.*.*
%ghost %{_libdir}/libcryptui.so.0
%{_datadir}/cryptui
%{_datadir}/dbus-1/services/org.gnome.seahorse.service
%{_pixmapsdir}/cryptui/*/seahorse-*.*
%{_libdir}/girepository-1.0/CryptUI-0.0.typelib
%{_datadir}/GConf/gsettings/org.gnome.seahorse.recipients.convert
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.recipients.gschema.xml

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcryptui.so
%{_pkgconfigdir}/cryptui-0.0.pc
%{_includedir}/%{name}/
%{_datadir}/gir-1.0/CryptUI-0.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
