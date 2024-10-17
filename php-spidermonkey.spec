%define modname spidermonkey
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B05_%{modname}.ini

Summary:	JavaScript engine for PHP
Name:		php-%{modname}
Version:	1.0.0
Release:	3
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/spidermonkey/
# https://github.com/christopherobin/php-spidermonkey
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.3.0
BuildRequires:	apache-devel >= 2.2.0
# breaks backporting, but that's already broken...
BuildRequires:	mozjs-devel >= 1.85
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension allow you to embed Mozilla's Javascript engine Spidermonkey in
PHP.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

# bork bork!
BORK=`pkg-config --libs mozjs185`
perl -pi -e "s|^SPIDERMONKEY_SHARED_LIBADD.*|SPIDERMONKEY_SHARED_LIBADD=$BORK|g" Makefile

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2012.0
+ Revision: 795501
- rebuild for php-5.4.x

* Thu Apr 19 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 791882
- fix build
- 1.0.0
- remove broken source
- 0.2.0

* Mon Jan 16 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.5-0.1
+ Revision: 761713
- quite tiresome shit here...
- still borked...
- grr!!!
- 0.1.5 (git snap)
- fix build
- rebuild
- rebuilt for php-5.3.8
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-7
+ Revision: 646685
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-6mdv2011.0
+ Revision: 629870
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-5mdv2011.0
+ Revision: 628190
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-4mdv2011.0
+ Revision: 600530
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-3mdv2011.0
+ Revision: 588868
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-2mdv2010.1
+ Revision: 514655
- rebuilt for php-5.3.2

* Wed Feb 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.4-1mdv2010.1
+ Revision: 510635
- 0.1.4

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-3mdv2010.1
+ Revision: 485483
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-2mdv2010.1
+ Revision: 468254
- rebuilt against php-5.3.1

* Tue Oct 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-1mdv2010.0
+ Revision: 454663
- 0.1.3

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2010.0
+ Revision: 452916
- import php-spidermonkey


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2010.0
- initial Mandriva package
