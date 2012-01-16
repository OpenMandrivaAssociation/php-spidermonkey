%define modname spidermonkey
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B05_%{modname}.ini

Summary:	JavaScript engine for PHP
Name:		php-%{modname}
Version:	0.1.5
Release:	%mkrel 0.1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/spidermonkey/
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
#[ "../package*.xml" != "/" ] && mv ../package*.xml .

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
