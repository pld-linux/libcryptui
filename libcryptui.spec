#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# static library

Summary:	Interface components for OpenPGP
Summary(pl.UTF-8):	Elementy interfejsu dla OpenPGP
Name:		libcryptui
Version:	3.10.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libcryptui/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	409924734b60006fc96b34e4c3ee5ead
URL:		http://projects.gnome.org/seahorse/
BuildRequires:	dbus-glib-devel >= 0.35
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 0.6.4
BuildRequires:	gpgme-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgnome-keyring-devel >= 2.25.5
BuildRequires:	libnotify-devel >= 0.3
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	/sbin/ldconfig
Requires:	dbus-glib >= 0.35
Requires:	glib2 >= 1:2.32.0
Requires:	gpgme >= 1.0.0
Requires:	gtk+3 >= 3.0.0
Requires:	libgnome-keyring >= 2.25.5
Requires:	libnotify >= 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libcryptui is a library used for prompting for PGP keys.

%description -l pl.UTF-8
libcryptui to biblioteka używana przy zapytaniach o klucze PGP.

%package devel
Summary:	Header files required to develop with libcryptui
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcryptui
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib >= 0.35
Requires:	glib2-devel >= 1:2.32.0
Requires:	gtk+3-devel >= 2.91.7

%description devel
The libcryptui-devel package contains the header files for the
libcryptui library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libcryptui.

%package static
Summary:	Static libcryptui library
Summary(pl.UTF-8):	Statyczna biblioteka libcryptui
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcryptui library.

%description static -l pl.UTF-8
Statyczna biblioteka libcryptui.

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
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcryptui.la

%find_lang cryptui

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
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/seahorse-daemon
%attr(755,root,root) %{_libdir}/libcryptui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcryptui.so.0
%{_libdir}/girepository-1.0/CryptUI-0.0.typelib
%{_datadir}/cryptui
%{_datadir}/GConf/gsettings/org.gnome.seahorse.recipients.convert
%{_datadir}/dbus-1/services/org.gnome.seahorse.service
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.recipients.gschema.xml
%{_pixmapsdir}/cryptui
%{_mandir}/man1/seahorse-daemon.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcryptui.so
%{_includedir}/%{name}
%{_datadir}/gir-1.0/CryptUI-0.0.gir
%{_pkgconfigdir}/cryptui-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcryptui.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
