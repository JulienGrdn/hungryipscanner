Name:           hungryipscanner
Version:        1.0
Release:        1%{?dist}
Summary:        A simple utility for scanning IP addresses over the local network

License:        MIT
# URL to the repository
URL:            https://github.com/JulienGrdn/hungryipscanner
# FIX 1: This must be a URL so Copr can download it
Source0:        %{url}/archive/main.tar.gz

BuildArch:      noarch
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
%autosetup -n hungryipscanner-main

%build
# Nothing to build for pure Python

%install
# 1. Install the main python script to /usr/bin/
mkdir -p %{buildroot}%{_bindir}
# Note: Ensure the script name below matches your file in the repo (e.g., hungryipscanner.py)
install -m 0755 hungryipscanner.py %{buildroot}%{_bindir}/hungryipscanner

# 2. Install the Desktop Entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 com.github.juliengrdn.hungryipscanner.desktop %{buildroot}%{_datadir}/applications/

# 3. Install the Icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 hungryipscannerlogo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

%files
%license LICENSE
%doc README.md
%{_bindir}/hungryipscanner
%{_datadir}/applications/com.github.juliengrdn.hungryipscanner.desktop
%{_datadir}/icons/hicolor/scalable/apps/hungryipscannerlogo.svg

%changelog
* Mon Dec 01 2025 Julien Grondin - 1.0-1
- Initial package
