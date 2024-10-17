%define modname drizzle
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A94_%{modname}.ini

Summary:	Drizzle Database API for PHP
Name:		php-%{modname}
Version:	0.4.2
Release:	%mkrel 10
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/drizzle
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		drizzle-0.4.2-php54x.diff
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	dos2unix
BuildRequires:	drizzle1-client-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension uses libdrizzle library to provide API for communicating with
drizzle and mysql databases.

%prep

%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

%patch0 -p1

cp %{SOURCE1} %{inifile}

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

perl -pi -e "s|include/libdrizzle|include/libdrizzle-1.0/libdrizzle|g" config.m4

%build
%serverbuild

export CPPFLAGS="-I%{_includedir}/libdrizzle-1.0"
phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

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
%doc ChangeLog CREDITS README drizzle.php package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-10mdv2012.0
+ Revision: 797108
- fix build (upstream)
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-9
+ Revision: 761218
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-8
+ Revision: 696411
- rebuilt for php-5.3.8

* Sun Aug 21 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-7
+ Revision: 695985
- fix build
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-6
+ Revision: 646627
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-5mdv2011.0
+ Revision: 629782
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-4mdv2011.0
+ Revision: 628093
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-3mdv2011.0
+ Revision: 600476
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-2mdv2011.0
+ Revision: 588758
- rebuild

* Sun Apr 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.2-1mdv2010.1
+ Revision: 531309
- 0.4.2
- rebuilt for php-5.3.2
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-3mdv2010.1
+ Revision: 468158
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-2mdv2010.0
+ Revision: 451263
- rebuild

* Wed Jul 08 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-1mdv2010.0
+ Revision: 393465
- P0: fix build with -Werror=format-security (from upstream cvs)
- import php-drizzle


* Sun Jul 05 2009 Oden Eriksson <oeriksson@mandriva.org> 0.4.1-1mdv2009.0
- initial Mandriva package
