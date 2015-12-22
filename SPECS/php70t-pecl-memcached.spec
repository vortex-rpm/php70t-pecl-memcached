%global php_zendabiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global pecl_name memcached
%global real_name php-pecl-memcached
%global basever 2
%global php_base php70t
%global date 20151222

Summary:      Extension to work with the Memcached caching daemon
Name:         %{php_base}-pecl-memcached
Version:      2.2.0
Release:      2.%{?date}.vortex%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: %{php_base}-devel, %{php_base}-pear
BuildRequires: zlib-devel
%{?el6:BuildRequires: libmemcached10-devel >= 1.0.13}
%{?el7:BuildRequires: libmemcached-devel}

%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web
applications by alleviating database load.

It also provides a session handler (memcached).


%prep
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so


; ----- Options to use the memcached session handler

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Tue Dec 22 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 2.2.0-2.20151222.vortex
- Git source.

* Tue May 26 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 2.2.0-1.vortex
- Update buildreqs to fix el7.

* Fri Oct  3 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com - 2.2.0-0.vortex
- Update to 2.2.0.

* Fri Apr  4 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com - 2.1.0-4.vortex
- Rebuilt with php55t.

* Fri Dec 06 2013 Ben Harper <ben.harper@rackspace.com> -  2.1.0-4.ius
- porting from php54-pecl-memcached

* Wed Nov 06 2013 Ben Harper <ben.harper@rackspace.com> -  2.1.0-3.ius
- adding provides per LB bug 1052542 comment #28

* Tue Nov 13 2012 Ben Harper <ben.harper@rackspace.com> -  2.1.0-2.ius
- building off libmemcached10-1.0.13-2

* Thu Nov 01 2012 Ben Harper <ben.harper@rackspace.com> - 2.1.0-1.ius
- porting from php53u-pecl-memcached
- updated release to 2.1.0

* Thu Jan 19 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.0.0-2
- Porting from EPEL to IUS

* Sat Jan 29 2011 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- EL-5 build, fix BR for php abi

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Sun Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

