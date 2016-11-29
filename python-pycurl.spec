%global modname pycurl

Name:           python-%{modname}
Version:        7.43.0
Release:        6%{?dist}
Summary:        A Python interface to libcurl

License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://dl.bintray.com/pycurl/pycurl/pycurl-%{version}.tar.gz

# drop link-time vs. run-time TLS backend check (#1446850)
Patch2:         0002-python-pycurl-7.43.0-tls-backend.patch

BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  vsftpd

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package -n python2-%{modname}
Summary:        Python interface to libcurl for Python 2
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-bottle
BuildRequires:  python2-nose
BuildRequires:  python-pyflakes
Requires:       libcurl%{?_isa} >= %{libcurl_ver}

Provides:       %{modname} = %{version}-%{release}

%description -n python2-%{modname}
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

Python 2 version.

%package -n python3-%{modname}
Summary:        Python interface to libcurl for Python 3
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-bottle
BuildRequires:  python3-nose
BuildRequires:  python3-pyflakes
Requires:       libcurl%{?_isa} >= %{libcurl_ver}

%description -n python3-%{modname}
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -p1

# remove binaries packaged by upstream
rm -f tests/fake-curl/libcurl/*.so

# remove a test-case that relies on sftp://web.sourceforge.net being available
rm -f tests/ssh_key_cb_test.py

# remove tests depending on the 'flaky' nose plug-in (not available in Fedora)
grep '^import flaky' -r tests | cut -d: -f1 | xargs rm -fv

# drop options that are not supported by nose in Fedora
sed -e 's/ --show-skipped//' \
    -e 's/ --with-flaky//' \
    -i tests/run.sh

%build
%py2_build -- --with-nss
%py3_build -- --with-nss

%install
%py2_install
%py3_install
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%check
export PYTHONPATH=%{buildroot}%{python2_sitearch}
make test PYTHON=%{__python2} NOSETESTS="nosetests-%{python2_version} -v"
rm -fv tests/fake-curl/libcurl/*.so

export PYTHONPATH=%{buildroot}%{python3_sitearch}
make test PYTHON=%{__python3} NOSETESTS="nosetests-%{python3_version} -v"
rm -fv tests/fake-curl/libcurl/*.so

%files -n python2-%{modname}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python2_sitearch}/curl/
%{python2_sitearch}/%{modname}.so
%{python2_sitearch}/%{modname}-%{version}-*.egg-info

%files -n python3-%{modname}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc tests
%{python3_sitearch}/curl/
%{python3_sitearch}/%{modname}.*.so
%{python3_sitearch}/%{modname}-%{version}-*.egg-info

%changelog
* Mon May 29 2017 Kamil Dudka <kdudka@redhat.com> - 7.43.0-6
- Fix python2 subpackage name

* Wed May 03 2017 Kamil Dudka <kdudka@redhat.com> - 7.43.0-5
- drop link-time vs. run-time TLS backend check (#1446850)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.43.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 7.43.0-3
- Follow new packaging guidelines

* Fri Feb 26 2016 Kamil Dudka <kdudka@redhat.com> - 7.43.0-2
- require libcurl of the same architecture as python-pycurl

* Sat Feb 06 2016 Kamil Dudka <kdudka@redhat.com> - 7.43.0-1
- update to 7.43.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.21.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-3
- remove explicit dependency on keyutils-libs (reported by rpmlint)
- update FSF address in COPYING-LGPL (detected by rpmlint)

* Tue Jan 05 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-2
- avoid installing binaries generated in %%check to /usr/share

* Tue Jan 05 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-1
- update to 7.21.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 7.19.5.3-3
- Remove build dependency on cherrypy as it's no longer needed for testing

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 03 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.3-1
- update to 7.19.5.3

* Mon Nov 02 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.2-1
- update to 7.19.5.2

* Mon Sep 07 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.1-3
- introduce CURL_SSLVERSION_TLSv1_[0-2] (#1260408)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.1-1
- update to 7.19.5.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug  3 2014 Tom Callaway <spot@fedoraproject.org> - 7.19.5-2
- fix license handling

* Mon Jul 14 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.5-1
- update to 7.19.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 7.19.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Feb 06 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3.1-1
- update to 7.19.3.1

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-2
- add python3 subpackage (#1014583)

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-1
- update to 7.19.3

* Thu Jan 02 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.0.3-1
- update to 7.19.0.3

* Tue Oct 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.2-1
- update to 7.19.0.2

* Wed Sep 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.1-1
- update to 7.19.0.1

* Thu Aug 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-18.20130315git8d654296
- sync with upstream 8d654296

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-17.20120408git9b8f4e38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 09 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-16.20120408git9b8f4e38
- sync with upstream 9b8f4e38 (fixes #928370)
- add the GLOBAL_ACK_EINTR constant to the list of exported symbols (#920589)
- temporarily disable tests/multi_socket_select_test.py

* Wed Mar 06 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-15
- allow to return -1 from the write callback (#857875) 
- remove the patch for curl-config --static-libs no longer needed
- run the tests against the just built pycurl, not the system one

* Mon Feb 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-14
- apply bug-fixes committed to upstream CVS since 7.19.0 (fixes #896025)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 7.19.0-12
- Improve spec

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Dennis Gilmore <dennis@ausil.us> - 7.19.0-8
- add Missing Requires on keyutils-libs

* Tue Aug 17 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-7
- Add patch developed by David Malcolm to fix segfaults caused by a missing incref

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  2 2010 Karel Klic <kklic@redhat.com> - 7.19.0-5
- Package COPYING2 file
- Added MIT as a package license

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-3
- fix typo in the previous change

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-2
- add a require to reflect a dependency on libcurl version (#496308)

* Thu Mar  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-1
- Update to 7.19.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.18.2-2
- Rebuild for Python 2.6

* Thu Jul  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.2-1
- Update to 7.18.2
- Thanks to Ville Skyttä re-enable the tests and fix a minor problem
  with the setup.py. (Bug # 45400)

* Thu Jun  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.1-1
- Update to 7.18.1
- Disable tests because it's not testing the built library, it's trying to
  test an installed library.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.16.4-3
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-2
- BR openssl-devel

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-1
- Update to 7.16.4
- Update license tag.

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.2.1-1
- Update to released version.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.0-0.1.20061207
- Update to a CVS snapshot since development has a newer version of curl than is in FC <= 6

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-4
- Add -DHAVE_CURL_OPENSSL to fix PPC build problem.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-3
- Don't forget to Provide: pycurl!!!

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-2
- Remove INSTALL from the list of documentation
- Use python_sitearch for all of the files

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-1
- First version for Fedora Extras
