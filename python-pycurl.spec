%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.18.2
Release:        1%{?dist}
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Patch0:		python-pycurl-no-static-libs.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  curl-devel >= 7.18.1
BuildRequires:  openssl-devel

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup0 -q -n pycurl-%{version}
%patch0 -p0
chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" %{__python} setup.py build

%check
export PYTHONPATH=$PWD/build/lib*
%{__python} tests/test_internals.py -q

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO examples doc tests
%{python_sitearch}/*

%changelog
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
