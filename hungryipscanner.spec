Name:           Hungry IP Scanner
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
%setup -q

%build
# Nothing to build, just python scripts

%install
%make_install

%files
%license LICENSE
%doc README.md
%{_bindir}/hungryipscanner
%{_datadir}/hungryipscanner/
%{_datadir}/applications/com.github.juliengrdn.hungryipscanner.desktop
%{_datadir}/icons/hicolor/scalable/apps/hungryipscannerlogo.svg

%changelog
* Sat May 25 2025 Julien Grondin - 1.0-1
- Initial package
