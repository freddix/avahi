Summary:	Free mDNS/DNS-SD implementation
Name:		avahi
Version:	0.6.31
Release:	11
License:	GPL v.2/LGPL
Group:		Applications
Source0:	http://avahi.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	2f22745b8f7368ad5a0a3fddac343f2d
Source1:	%{name}.png
Source2:	%{name}-tmpfiles.conf
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-destdir.patch
Patch2:		%{name}-browse-local.patch
Patch3:		%{name}-autoipd-sbin_ip.patch
Patch4:		%{name}-dhclient_hooks.patch
Patch5:		%{name}-standalone.patch
URL:		http://avahi.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libdaemon-devel
BuildRequires:	libglade-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	python-dbus
BuildRequires:	python-pygtk-devel
BuildRequires:	xmltoman
Requires(post,preun,postun):	systemd-units
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus
Provides:	group(avahi)
Provides:	user(avahi)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Avahi is an implementation the DNS Service Discovery and Multicast DNS
specifications for Zeroconf Computing. It uses D-BUS for communication
between user applications and a system daemon.

%package dnsconfd
Summary:	Configure local unicast DNS settings
Group:		Daemon
Requires:	%{name} = %{version}-%{release}

%description dnsconfd
avahi-dnsconfd connects to a running avahi-daemon and runs the script
/etc/avahi/dnsconfd.action for each unicast DNS server that is
announced on the local LAN. This is useful for configuring unicast DNS
servers in a DHCP-like fashion with mDNS.

%package autoipd
Summary:	Link-local IPv4 address automatic configuration daemon
Group:		Daemon
Requires:	%{name} = %{version}-%{release}

%description autoipd
Link-local IPv4 address automatic configuration daemon (IPv4LL).

%package libs
Summary:	Avahi client, common and core libraries
Group:		Libraries

%description libs
Avahi client, common and core libraries.

%package ui-libs
Summary:	Avahi ui library
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description ui-libs
Avahi ui libraries.

%package ui-gtk3-libs
Summary:	Avahi ui library, Gtk+3 version
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description ui-gtk3-libs
Avahi ui libraries, Gtk+3 version.

%package devel
Summary:	Header files for Avahi library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for Avahi library.

%package ui-devel
Summary:	Header files for Avahi ui library
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{version}-%{release}
Requires:	%{name}-ui-libs = %{version}-%{release}

%description ui-devel
This is the package containing the header files for Avahi library.

%package ui-gtk3-devel
Summary:	Header files for Avahi ui library
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{version}-%{release}
Requires:	%{name}-ui-gtk3-libs = %{version}-%{release}

%description ui-gtk3-devel
This is the package containing the header files for Avahi library.

%package glib
Summary:	Avahi GLib library bindings
Group:		Libraries

%description glib
Avahi GLib library bindings.

%package glib-devel
Summary:	Header files for Avahi GLib library bindings
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}

%description glib-devel
This is the package containing the header files for Avahi-glib
library.

%package -n mono-avahi
Summary:	Avahi MONO bindings
Group:		Libraries

%description -n mono-avahi
Avahi MONO bindings.

%package -n mono-avahi-devel
Summary:	Development files for MONO Avahi bindings
Group:		Development/Libraries
Requires:	mono-avahi = %{version}-%{release}
Requires:	monodoc

%description -n mono-avahi-devel
Development files for MONO Avahi bindings.

%package bookmarks
Summary:	Miniature web server
Group:		Applications

%description bookmarks
A Python based miniature web server that browses for mDNS/DNS-SD
services of type '_http._tcp' (i.e. web sites) and makes them
available as HTML links on http://localhost:8080/.

%package discover
Summary:	Avahi Zeroconf browser
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python-dbus
Requires:	python-pygtk-glade

%description discover
A tool for enumerating all available services on the local LAN
(python-pygtk implementation).

%package discover-standalone
Summary:	Avahi Zeroconf browser
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description discover-standalone
GTK+ tool for enumerating all available services on the local LAN.

%package utils
Summary:	Avahi CLI utilities
Group:		Applications

%description utils
Command line utilities using avahi-client.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I common
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-mono		\
	--disable-monodoc	\
	--disable-qt3		\
	--disable-qt4		\
	--disable-silent-rules	\
    	--disable-static 	\
	--with-autoipd-group=avahi		\
	--with-autoipd-user=avahi		\
	--with-avahi-priv-access-group=avahi	\
	--with-distro=none			\
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},/etc/rc.d/init.d,/var/lib/avahi-autoipd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install -D %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

cp $RPM_BUILD_ROOT%{_datadir}/%{name}/interfaces/{avahi-discover,avahi-discover-standalone}.ui

%py_postclean

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{en_NZ,sr@latin}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 105 -r -f avahi
%useradd -u 105 -r -d /run/avahi -s /bin/false -c "Avahi daemon" -g avahi avahi

%post
if [ -s /etc/localtime ]; then
    cp -fp /etc/localtime /etc/avahi/etc/localtime || :
fi
%systemd_post avahi-daemon.service

%preun
%systemd_preun avahi-daemon.service

%postun
if [ "$1" = "0" ]; then
        %userremove avahi
	%groupremove avahi
fi
%systemd_postun

%post dnsconfd
%systemd_post avahi-dnsconfd.service

%preun dnsconfd
%systemd_preun avahi-dnsconfd.service

%postun dnsconfd
%systemd_postun

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%post	ui-libs -p /usr/sbin/ldconfig
%postun	ui-libs -p /usr/sbin/ldconfig

%post	ui-gtk3-libs -p /usr/sbin/ldconfig
%postun	ui-gtk3-libs -p /usr/sbin/ldconfig

%post	glib -p /usr/sbin/ldconfig
%postun	glib -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/AUTHORS docs/COMPAT-LAYERS docs/NEWS docs/README docs/TODO
%attr(755,root,root) %{_sbindir}/avahi-daemon

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avahi/avahi-daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avahi/hosts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avahi/services/sftp-ssh.service
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avahi/services/ssh.service
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/*

%dir %{_datadir}/%{name}/interfaces
%dir %{_sysconfdir}/avahi
%dir %{_sysconfdir}/avahi/services

%{_libdir}/%{name}/service-types.db
%{_datadir}/%{name}/service-types
%{_mandir}/man5/*
%{_mandir}/man8/avahi-daemon.*

%{systemdunitdir}/avahi-daemon.service
%{systemdunitdir}/avahi-daemon.socket
%{systemdtmpfilesdir}/%{name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Avahi.service

%files dnsconfd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/avahi-dnsconfd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/avahi/avahi-dnsconfd.action
%{systemdunitdir}/avahi-dnsconfd.service
%{_mandir}/man8/avahi-dnsconfd.*

%files autoipd
%defattr(644,root,root,755)
%attr(750,avahi,avahi) /var/lib/avahi-autoipd
%attr(755,root,root) %{_sbindir}/avahi-autoipd
%attr(755,root,root) %{_sysconfdir}/%{name}/avahi-autoipd.action
%dir %{_sysconfdir}/dhclient-enter-hooks.d
%dir %{_sysconfdir}/dhclient-exit-hooks.d
%attr(755,root,root) /etc/dhclient-enter-hooks.d/avahi-autoipd
%attr(755,root,root) /etc/dhclient-exit-hooks.d/avahi-autoipd
%{_mandir}/man8/avahi-autoipd.*

%files libs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %ghost %{_libdir}/libavahi-client.so.?
%attr(755,root,root) %ghost %{_libdir}/libavahi-common.so.?
%attr(755,root,root) %ghost %{_libdir}/libavahi-core.so.?
%attr(755,root,root) %{_libdir}/libavahi-client.so.*.*.*
%attr(755,root,root) %{_libdir}/libavahi-common.so.*.*.*
%attr(755,root,root) %{_libdir}/libavahi-core.so.*.*.*
%{_libdir}/girepository-1.0/Avahi-0.6.typelib
%{_libdir}/girepository-1.0/AvahiCore-0.6.typelib

%files ui-libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libavahi-ui.so.?
%attr(755,root,root) %{_libdir}/libavahi-ui.so.*.*.*

%files ui-gtk3-libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libavahi-ui-gtk3.so.?
%attr(755,root,root) %{_libdir}/libavahi-ui-gtk3.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/API-CHANGES-0.6 docs/DBUS-API docs/HACKING docs/MALLOC
%attr(755,root,root) %{_libdir}/libavahi-client.so
%attr(755,root,root) %{_libdir}/libavahi-common.so
%attr(755,root,root) %{_libdir}/libavahi-core.so
%{_datadir}/%{name}/avahi-service.dtd
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/gir-1.0/Avahi-0.6.gir
%{_datadir}/gir-1.0/AvahiCore-0.6.gir
%{_includedir}/avahi-client
%{_includedir}/avahi-common
%{_includedir}/avahi-core
%{_pkgconfigdir}/avahi-client.pc
%{_pkgconfigdir}/avahi-core.pc

%files ui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavahi-ui.so
%{_includedir}/avahi-ui
%{_pkgconfigdir}/avahi-ui.pc

%files ui-gtk3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavahi-ui-gtk3.so
%{_pkgconfigdir}/avahi-ui-gtk3.pc

%if 0
%files -n mono-avahi
%defattr(644,root,root,755)
%{_gacdir}/avahi-sharp
%{_gacdir}/avahi-ui-sharp
%dir %{_monodir}/avahi-ui-sharp
%{_monodir}/avahi-ui-sharp/avahi-ui-sharp.dll

%files -n mono-avahi-devel
%defattr(644,root,root,755)
%{_libdir}/monodoc/sources/avahi-*
%{_monodir}/avahi-sharp
%{_pkgconfigdir}/avahi-sharp.pc
%{_pkgconfigdir}/avahi-ui-sharp.pc
%endif

%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libavahi-glib.so.?
%attr(755,root,root) %ghost %{_libdir}/libavahi-gobject.so.?
%attr(755,root,root) %{_libdir}/libavahi-glib.so.*.*.*
%attr(755,root,root) %{_libdir}/libavahi-gobject.so.*.*.*

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libavahi-glib.so
%attr(755,root,root) %{_libdir}/libavahi-gobject.so
%{_includedir}/avahi-glib
%{_includedir}/avahi-gobject
%{_pkgconfigdir}/avahi-glib.pc
%{_pkgconfigdir}/avahi-gobject.pc

%files bookmarks
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avahi-bookmarks
%{_mandir}/man1/avahi-bookmarks.*

%files discover
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avahi-discover
%dir %{py_sitedir}/avahi
%dir %{py_sitedir}/avahi_discover
%{_datadir}/%{name}/interfaces/avahi-discover.ui
%{py_sitedir}/avahi/*.py[co]
%{py_sitedir}/avahi_discover/*.py[co]
%{_desktopdir}/avahi-discover.desktop
%{_pixmapsdir}/avahi.png
%{_mandir}/man1/avahi-discover.*

%files discover-standalone
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avahi-discover-standalone
%{_datadir}/%{name}/interfaces/avahi-discover-standalone.ui

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avahi-browse
%attr(755,root,root) %{_bindir}/avahi-browse-domains
%attr(755,root,root) %{_bindir}/avahi-publish
%attr(755,root,root) %{_bindir}/avahi-publish-address
%attr(755,root,root) %{_bindir}/avahi-publish-service
%attr(755,root,root) %{_bindir}/avahi-resolve
%attr(755,root,root) %{_bindir}/avahi-resolve-address
%attr(755,root,root) %{_bindir}/avahi-resolve-host-name
%attr(755,root,root) %{_bindir}/avahi-set-host-name
%{_mandir}/man1/avahi-browse.*
%{_mandir}/man1/avahi-publish.*
%{_mandir}/man1/avahi-resolve.*
%{_mandir}/man1/avahi-set-host-name.*

