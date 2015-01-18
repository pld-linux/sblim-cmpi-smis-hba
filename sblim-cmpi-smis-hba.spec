Summary:	SBLIM CMPI HBA providers based on SMI-S standards
Summary(pl.UTF-8):	Dostawcy danych HBA oparci na standardach SMI-S dla SBLIM CMPI
Name:		sblim-cmpi-smis-hba
Version:	1.0.0
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/sblim-smis-hba-%{version}.tar.bz2
# Source0-md5:	9bdcba6f2192d39d5000a0707ed5abc1
Patch0:		%{name}-hbaapi.patch
URL:		http://sblim.sourceforge.net/
BuildRequires:	hbaapi-devel >= 2.2
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
BuildRequires:	sblim-indication_helper-devel
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI HBA providers based on SMI-S standards. These providers
assist in storage management.

%description -l pl.UTF-8
Dostawcy danych kart kontrolerów, oparci na standardach SMI-S.
Pomagają w zarządzaniu nośnikami danych.

%prep
%setup -q -n sblim-smis-hba-%{version}
%patch0 -p1

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/sblim-smis-hba-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_SMIS_{ECTP,HBA_HDR}.reg \
	-m %{_datadir}/%{name}/Linux_SMIS_{ECTP,HBA_HDR}.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_SMIS_{ECTP,HBA_HDR}.reg \
		-m %{_datadir}/%{name}/Linux_SMIS_{ECTP,HBA_HDR}.mof >/dev/null
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_Common.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_ECTP_Provider.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiSMIS_HBA_HDR_Provider.so*
%dir %{_datadir}/sblim-smis-hba
%{_datadir}/sblim-smis-hba/Linux_SMIS_ECTP.mof
%{_datadir}/sblim-smis-hba/Linux_SMIS_ECTP.reg
%{_datadir}/sblim-smis-hba/Linux_SMIS_HBA_HDR.mof
%{_datadir}/sblim-smis-hba/Linux_SMIS_HBA_HDR.reg
%attr(755,root,root) %{_datadir}/sblim-smis-hba/provider-register.sh
