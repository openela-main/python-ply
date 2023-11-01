%global modname ply

%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-%{modname}
Summary:        Python Lex-Yacc
Version:        3.9
Release:        9%{?dist}
License:        BSD
URL:            http://www.dabeaz.com/ply/
Source0:        http://www.dabeaz.com/ply/%{modname}-%{version}.tar.gz
BuildArch:      noarch

Patch1:         Make-MD5-fingerprint-FIPS-compatible.patch

%description
PLY is a straightforward lex/yacc implementation. Here is a list of its 
essential features:
* It is implemented entirely in Python.
* It uses LR-parsing which is reasonably efficient and well suited for larger 
  grammars.
* PLY provides most of the standard lex/yacc features including support 
  for empty productions, precedence rules, error recovery, and support 
  for ambiguous grammars.
* PLY is straightforward to use and provides very extensive error checking.
* PLY doesn't try to do anything more or less than provide the basic lex/yacc 
  functionality. In other words, it's not a large parsing framework or a 
  component of some larger system. 

%if %{with python2}
%package -n python2-%{modname}
Summary:        Python Lex-Yacc
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description -n python2-%{modname}
PLY is a straightforward lex/yacc implementation. Here is a list of its 
essential features:
* It is implemented entirely in Python.
* It uses LR-parsing which is reasonably efficient and well suited for larger 
  grammars.
* PLY provides most of the standard lex/yacc features including support 
  for empty productions, precedence rules, error recovery, and support 
  for ambiguous grammars.
* PLY is straightforward to use and provides very extensive error checking.
* PLY doesn't try to do anything more or less than provide the basic lex/yacc 
  functionality. In other words, it's not a large parsing framework or a 
  component of some larger system.

Python 2 version.
%endif # with python2

%if %{with python3}
%package -n python3-%{modname}
Summary:        Python Lex-Yacc
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{modname}
PLY is a straightforward lex/yacc implementation. Here is a list of its 
essential features:
* It is implemented entirely in Python.
* It uses LR-parsing which is reasonably efficient and well suited for larger 
  grammars.
* PLY provides most of the standard lex/yacc features including support 
  for empty productions, precedence rules, error recovery, and support 
  for ambiguous grammars.
* PLY is straightforward to use and provides very extensive error checking.
* PLY doesn't try to do anything more or less than provide the basic lex/yacc 
  functionality. In other words, it's not a large parsing framework or a 
  component of some larger system.

Python 3 version.
%endif # with python3

%prep
%autosetup -c -N

pushd %{modname}-%{version}
%patch1 -p1
popd

%if %{with python2}
cp -ai %{modname}-%{version} python2
find python2/example/ -type f -exec chmod -x {} ';'
find python2/example/ -type f -name '*.py' -exec sed -i \
  -e '1{\@^#!/usr/bin/env python@d}' -e '1{\@^#!/usr/local/bin/python@d}' \
  {} ';'
rm -rf python2/*.egg-info
# extract license block from beginning of README.md
grep -B1000 "POSSIBILITY OF SUCH DAMAGE" python2/README.md > python2/LICENSE
%endif # with python2

%if %{with python3}
cp -ai %{modname}-%{version} python3
# extract license block from beginning of README.md
grep -B1000 "POSSIBILITY OF SUCH DAMAGE" python3/README.md > python3/LICENSE
%endif # with python3

%build
%if %{with python2}
pushd python2
  %py2_build
popd
%endif # with python2

%if 0%{?with_python3}
pushd python3
  %py3_build
popd
%endif # with python3

%install
%if %{with python2}
pushd python2
  %py2_install
popd
%endif # with python2

%if %{with python3}
pushd python3
  %py3_install
popd
%endif # with python3

%check
%if %{with python2}
pushd python2/test
  ./cleanup.sh
  %{__python2} testlex.py
  %{__python2} testyacc.py
popd
%endif # with python2

%if %{with python3}
pushd python3/test
  ./cleanup.sh
  %{__python3} testlex.py
  %{__python3} testyacc.py
popd
%endif # with python3

%if %{with python2}
%files -n python2-%{modname}
%doc python2/CHANGES python2/README.md
%license python2/LICENSE
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-%{version}-*.egg-info/
%endif # with python2

%if %{with python3}
%files -n python3-%{modname}
%doc python3/CHANGES python3/README.md
%license python3/LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}-*.egg-info/
%endif # with python3

%changelog
* Wed Jan  6 14:57:34 CET 2021 Christian Heimes <cheimes@redhat.com> - 3.9-9
- Include README.MD and LICENSE (#1464435)

* Mon Nov 11 2019 Christian Heimes <cheimes@redhat.com> - 3.9-8
- Make MD5 fingerprint FIPS compliant
- Resolves: rhbz#1747490

* Fri Jun 15 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.9-7
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 3.9-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.9-2
- Rebuild for Python 3.6

* Tue Nov 8 2016 Orion Poplawski <orion@cora.nwra.com> - 3.9-1
- Update to 3.9

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Apr 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 3.8-1
- Update to 3.8
- Follow new packaging guidelines
- Run tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 3.6-3
- Rebuilt for Python3.5 rebuild

* Tue Aug 18 2015 Stephen Gallagher <sgallagh@redhat.com> 3.6-2
- Fixes for chromium and SlimIt
- Resolves: rhbz#1242929
- Resolves: rhbz#1254372

* Tue Jul 14 2015 Stephen Gallagher <sgallagh@redhat.com> 3.6-1
- Update to latest ply 3.6 for Python 3 fixes

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Tom Callaway <spot@fedoraproject.org> - 3.4-1
- update to 3.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.3-4
- update to most recent python packaging guidelines
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Apr  3 2010 David Malcolm <dmalcolm@redhat.com> - 3.3-2
- add python3-ply subpackage

* Mon Oct 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.3-1
- update to 3.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.2-1
- update to 3.2, license change to BSD

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.5-2
- Rebuild for Python 2.6

* Fri Oct 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.5-1
- update to 2.5

* Mon Mar 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2.3-2
- add example dir as doc

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2.3-1
- Initial package for Fedora
