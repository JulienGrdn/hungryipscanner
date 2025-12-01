# Hungry IP Scanner

A simple utility for scanning IP addresses over the local network. Hungry IP Scanner allows you to quickly discover active devices on your subnet, view their ping times, and resolve hostnames.

![Hungry IP Scanner](hungryipscannerlogo.svg)

## Features

### Network Scanning
- Scans your local subnet (e.g., 192.168.1.x) for active devices
- Uses multi-threaded scanning for quick results

### Device Identification
- Resolves hostnames for discovered IP addresses
- Displays round-trip ping times in milliseconds
- Real-time progress updates via a bottom progress bar

### Export Results
- Export scan results to a CSV file
- Includes IP Address, Ping Time, and Hostname columns

### Interface
- Clean, adaptive user interface
- Built with GTK 4 and Libadwaita
- Dark mode support (follows system preference)

## Installation

### Dependencies

#### System Requirements
- Python 3
- GTK 4
- Libadwaita
- PyGObject

#### Fedora/RHEL
```bash
dnf copr enable juliengrdn/hungryipscanner
sudo dnf install hungryipscanner
```

### Running the Application

After installation, launch the application from your desktop menu or run:

```bash
hungryipscanner
```

Or run directly from the source directory:

```bash
python3 hungryip.py
```

## Usage

### Getting Started

1. **Launch the application**: Run `hungryipscanner`
2. **Start Scan**: Click the "Scan" button in the top right corner.
3. **Wait for results**: The list will populate with discovered devices.


## Technical Details

### Built With

- **GTK 4**: Modern toolkit for creating graphical user interfaces
- **Libadwaita**: GNOME's library for adaptive UI components
- **PyGObject**: Python bindings for GTK
- **Python Standard Library**: Uses `socket`, `subprocess`, and `threading` for networking tasks

## Configuration

The application automatically detects your local IP address and determines the subnet to scan. No manual configuration is required.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
