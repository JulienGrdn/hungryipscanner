Name:           hungryipscanner
Version:        1.0
Release:        1%{?dist}
Summary:        A simple utility for scanning IP addresses over the local network

License:        MIT
URL:            https://github.com/juliengrdn/hungryipscanner
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Hungry IP Scanner is a simple utility for scanning IP addresses over the local
network. It provides a GUI built with GTK 4 and Libadwaita to display active
hosts on the network.

%prep
%autosetup -n HungryIPScanner-main

%build
# Nothing to build, just python scripts

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 hungryipscanner.py %{buildroot}%{_bindir}/hungryipscanner
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 com.github.juliengrdn.hungryipscanner.desktop %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
instal

%files
%license LICENSE
%doc README.md
%{_bindir}/hungryipscanner
%{_datadir}/hungryipscanner/
%{_datadir}/applications/com.github.juliengrdn.hungryipscanner.desktop
%{_datadir}/icons/hicolor/scalable/apps/hungryipscannerlogo.svg

%changelog
* Mon Dec 01 2025 Julien Grondin - 1.0-1
- Initial package
