Name:           hungryipscanner
Version:        1.0
Release:        1%{?dist}
Summary:        A simple utility for scanning IP addresses over the local network

License:        MIT
URL:            https://github.com/JulienGrdn/hungryipscanner
Source0:        %{url}/archive/refs/heads/main.tar.gz

BuildArch:      noarch

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita

%description
A simple graphical IP scanner built with Python, GTK4, and Libadwaita.

%prep
# GitHub archive extracts to hungryipscanner-main
%setup -q -n hungryipscanner-main

%build
# Nothing to compile for Python

%install
# Install executable script
mkdir -p %{buildroot}%{_bindir}
install -m 0755 hungryipscanner.py %{buildroot}%{_bindir}/hungryipscanner

# Install desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 com.github.juliengrdn.hungryipscanner.desktop \
    %{buildroot}%{_datadir}/applications/

# Install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 hungryipscannerlogo.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/hungryipscanner.svg

%files
%license LICENSE
%doc %{_docdir}/%{name}/README.md

%{_bindir}/hungryipscanner
%{_datadir}/applications/com.github.juliengrdn.hungryipscanner.desktop
%{_datadir}/icons/hicolor/scalable/apps/hungryipscanner.svg

%changelog
* Mon Dec 01 2025 Julien Grondin - 1.0-1
- Initial package
