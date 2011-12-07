Name: jwhois
Version: 4.0
Release: 18%{?dist}
URL: http://www.gnu.org/software/jwhois/
Source0: ftp://ftp.gnu.org/gnu/jwhois/jwhois-%{version}.tar.gz
Patch0: jwhois-4.0-connect.patch
Patch1: jwhois-4.0-ipv6match.patch
Patch2: jwhois-4.0-conf.patch
Patch3: jwhois-4.0-gi.patch
Patch4: jwhois-4.0-enum.patch
Patch5: jwhois-4.0-fclose.patch
Patch6: jwhois-4.0-conf_update.patch
Patch7: jwhois-4.0-conf_update2.patch
Patch8: jwhois-4.0-dotster.patch
Patch9: jwhois-4.0-conf_update3.patch
Patch10: jwhois-4.0-conf_update4.patch
License: GPLv3
Group: Applications/Internet
Summary: Internet whois/nicname client
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libidn-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
A whois client that accepts both traditional and finger-style queries.

%prep
%setup -q
%patch0 -p1 -b .connect
%patch1 -p1 -b .ipv6match
%patch2 -p1 -b .conf
%patch3 -p1 -b .gi
%patch4 -p1 -b .enum
%patch5 -p1 -b .fclose
%patch6 -p1 -b .conf_update
%patch7 -p1 -b .conf_update2
%patch8 -p1 -b .dotster
%patch9 -p1 -b .conf_update3
%patch10 -p1 -b .conf_update4

iconv -f iso-8859-1 -t utf-8 < doc/sv/jwhois.1 > doc/sv/jwhois.1_
mv doc/sv/jwhois.1_ doc/sv/jwhois.1

%build
%configure
make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
rm -f "$RPM_BUILD_ROOT"%{_infodir}/dir
%find_lang jwhois

# Make "whois" jwhois.
ln -sf jwhois $RPM_BUILD_ROOT/%{_bindir}/whois
echo .so man1/jwhois.1 > $RPM_BUILD_ROOT/%{_mandir}/man1/whois.1

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*
%{_mandir}/man1/*
%lang(sv) %{_mandir}/sv/man1/jwhois.1*
%{_infodir}/jwhois.info.gz
%config(noreplace) %{_sysconfdir}/jwhois.conf

%post
if [ -f %{_infodir}/jwhois.info ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/jwhois.info %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/jwhois.info ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/jwhois.info %{_infodir}/dir || :
    fi
fi

%clean
rm -fr $RPM_BUILD_ROOT

%changelog
* Thu Sep  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-18
- Fix errors installing jwhois with --excludedocs
  Resolves: #515940

* Sun Aug 16 2009 Robert Scheck <robert@fedoraproject.org> - 4.0-17
- Update jwhois.conf for .edu.ar, .bs, .by, .dk, .name, .ng, .ps,
  .sg, .sl, .sv, .co.zw domains and handles from .name and .aero

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> - 4.0-15
- Update jwhois.conf for .al, .cu, .my and .so domains

* Thu Apr 23 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-14
- Update jwhois.conf to expect UTF-8 answer charset from whois.dotster.com
  Resolves: #496015

* Fri Mar 13 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-13
- jwhois.conf update for another few domains
  Resolves: #489161

* Fri Feb 27 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-12
- Large jwhois.conf update
  Resolves: #48677{3,4,5,6,8}, #48678{0,2-9}, #48679{0-9}
  Resolves: #48680{0-3}, #48682{2,3,7}, #48683{0,2-5,7-9}
  Resolves: #48684{0,2,3,5,7,8}, #48685{0,3,7}, #486862

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-10
- Close config file descriptor when finished reading the config file
- Add support for ENUM domains into jwhois.conf
  Resolves: #465182

* Fri Jan 23 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-9
- Change the server used for .gi domains

* Mon Oct 13 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-8
- Update to latest upstream config
  Resolves: #463972

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-7
- Rebuild

* Thu Dec  6 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-6
- Fix buildroot
- Fix matching of cidr-ipv6 network addressed (patch by Lubomir
  Kundrak <lkundrak@redhat.com>)
  Resolves: #280941

* Wed Nov 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-5
- Merge review: add _smp_mflag, remove RPM_BUILD_ROOT test in istall
  and clean, remove Obsoletes:, fix use of %% in changelog
  Resolves: #225955

* Tue Nov 20 2007 Lubomir Kundrak <lkundrak@redhat.com> - 4.0-4
- Fix connections to IPv4 servers

* Tue Oct  9 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-3
- Fix localized man pages not marked with %%lang (patch by Ville
  Skyttä <ville.skytta@iki.fi>)

* Tue Aug 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-2
- Fix license
- Rebuild

* Mon Jul  2 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.0-1
- Update to 4.0 (#246455)

* Fri Mar 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 3.2.3-11
- Change the server used for .se domains to whois.iis.se (patch by Johan
  Sare <johansare@gmail.com>)
  Resolves: #233207

* Sat Jan  6 2007 Miloslav Trmac <mitr@redhat.com> - 3.2.3-10
- Add automatic redirection for .com and .net domains (patch by Wolfgang
  Rupprecht <wsr+redhatbugzilla@wsrcc.com>)
  Resolves: #221668
- Update to upstream config as of Jan 6 2007

* Fri Jan  5 2007 Miloslav Trmac <mitr@redhat.com> - 3.2.3-9
- Ignore install-info errors in scriptlets
- Remove the trailing dot from Summary:

* Tue Oct 31 2006 Miloslav Trmac <mitr@redhat.com> - 3.2.3-8
- Actually use the new upstream config in non-rawhide branches

* Tue Oct 31 2006 Miloslav Trmac <mitr@redhat.com> - 3.2.3-7
- Backport IDN support
  Resolves: #205033
- Update to upstream config as of Oct 31 2006

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-6.1
- rebuild

* Tue May 16 2006 Miloslav Trmac <mitr@redhat.com> - 3.2.3-6
- Fix some uninitialized memory accesses
- Fix a typo in the ipv6 patch

* Mon May 15 2006 Miloslav Trmac <mitr@redhat.com> - 3.2.3-5
- Update to upstream config as of May 15 2006 (#191291)
- Add more IPv6 address ranges (#191290, original patch by Peter Bieringer)

* Wed Apr 19 2006 Miloslav Trmac <mitr@redhat.com> - 3.2.3-4
- Update to upstream config as of Apr 19 2006 (#188366)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2.3-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.3-3
- Ship ChangeLog

* Fri Aug  5 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.3-2
- Don't die on SIGPIPE if a browser is not present, improve the error message
  (#165149)

* Mon Aug  1 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.3-1
- Update to jwhois-3.2.3
- Don't compress jwhois.info manually

* Sun Jun 12 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-16
- Remove 'fuzzy' from ru.po header to make charset conversion work (#160165)

* Sat Jun 11 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-15
- Update to upstream config as of Jun 11 2005, remove patches accepted upstream

* Sat Apr 30 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-14
- Add an AfriNIC range (#156178)

* Mon Apr 11 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-13
- Update to upstream config as of Apr 11 2005 (get results in English 
  from whois.nic.ad.jp)

* Wed Mar 23 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-12
- Update to upstream CVS config as of Mar 23 2005 (#151900)
  Remove now unnecessary typos.patch

* Fri Mar  4 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-11
- Rebuild with gcc 4

* Sun Feb 20 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-10
- Update to upstream CVS config as of Feb 10 2005 (#147562);
  Remove now unecessary denic.patch, update update_2004.patch
- Fix .cd, .gi, .io (#146613, patch by Robert Scheck)

* Sun Jan  2 2005 Miloslav Trmac <mitr@redhat.com> - 3.2.2-9
- Add IPv6 address ranges, fix .pro, 223.0.0.0/8 (#143682, patch by Robert
  Scheck)

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 3.2.2-8
- Convert Swedish man page to UTF-8

* Mon Nov  1 2004 Miloslav Trmac <mitr@redhat.com> - 3.2.2-7
- Fix double free (#137693)

* Mon Sep 13 2004 Miloslav Trmac <mitr@redhat.com> - 3.2.2-6
- Recognize more redirections at whois.arin.net (#116423)

* Mon Sep 13 2004 Miloslav Trmac <mitr@redhat.com> - 3.2.2-5
- Update config file for .de (#132362, by Robert Scheck)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com> 3.2.2-2
- fix typos in jwhois.conf (#113012)

* Fri Jul 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- new upstream version 3.2.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.2.1

* Thu Jan 30 2003 Nalin Dahyabhai <nalin@redhat.com> 3.2.0-6
- search whois.publicinternetregistry.net instead of whois.internic.net for
  all '.org$' domains (#82802).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 3.2.0-5
- rebuilt

* Thu Dec 12 2002 Karsten Hopp <karsten@redhat.de> 3.2.0-4
- Requires(post,preun) doesn't seem to work properly

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de> 3.2.0-3
- require install-info

* Thu Nov 14 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.0-2
- don't bail out of %%install if make install doesn't create an info top node

* Mon Sep 30 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.0-1
- initial package
