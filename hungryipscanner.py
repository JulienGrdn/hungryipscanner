import sys
import threading
import socket
import subprocess
import platform
import ipaddress
import re
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, GObject

# -----------------------------------------------------------------------------
# CORE LOGIC
# -----------------------------------------------------------------------------

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

def get_local_ips_list(ip):
    parts = ip.split('.')
    prefix = ".".join(parts[:-1])
    return [f"{prefix}.{i}" for i in range(1, 255)]

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"
    except Exception:
        return "Error"

def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Reduced timeout to 1s for faster scanning in GUI
    command = ['ping', param, '1', '-W', '1', host] if platform.system().lower() != 'windows' else ['ping', param, '1', '-w', '1000', host]

    if not validate_ip(host):
        return None

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        match = re.search(r"time[=<]([\d.]+)", result.stdout)
        if match:
            return float(match.group(1))
        return None
    except subprocess.CalledProcessError:
        return None
    except Exception:
        return None

# -----------------------------------------------------------------------------
# DATA MODEL
# -----------------------------------------------------------------------------

class ScanResult(GObject.Object):
    __gtype_name__ = 'ScanResult'

    def __init__(self, ip, time_ms, hostname):
        super().__init__()
        self._ip = ip
        self._time_ms = time_ms
        self._hostname = hostname

    @GObject.Property(type=str)
    def ip(self):
        return self._ip

    @GObject.Property(type=str)
    def time_ms(self):
        return f"{self._time_ms:.1f} ms"

    @GObject.Property(type=str)
    def hostname(self):
        return self._hostname

    def get_raw_data(self):
        return [self._ip, self._time_ms, self._hostname]

# -----------------------------------------------------------------------------
# GUI APPLICATION
# -----------------------------------------------------------------------------

class NetworkScannerWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Hungry IP Scanner")
        self.set_default_size(650, 450)

        # State flags
        self.scanning = False
        self.stop_event = threading.Event()

        # Toast Overlay
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # Main Layout Box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.toast_overlay.set_child(content_box)

        # --- Header Bar (Topbar) ---
        header = Adw.HeaderBar()

        # Export Button (Top Left)
        self.btn_export = Gtk.Button(label="Export")
        self.btn_export.set_icon_name("document-save-symbolic") # Optional icon
        self.btn_export.connect("clicked", self.on_export_clicked)
        self.btn_export.set_sensitive(False)
        header.pack_start(self.btn_export)


        # About menu
        primary_menu = Gio.Menu()
        primary_menu.append("About", "win.about")
        menu_button = Gtk.MenuButton(menu_model=primary_menu, icon_name="open-menu-symbolic")
        header.pack_end(menu_button)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_activated)
        self.add_action(about_action)


        # Start Button (Top Right - Primary)
        self.btn_start = Gtk.Button(label="Scan")
        self.btn_start.add_css_class("suggested-action")
        self.btn_start.connect("clicked", self.on_start_clicked)
        header.pack_end(self.btn_start)

        # Stop Button (Top Right - Destructive)
        self.btn_stop = Gtk.Button(label="Stop")
        self.btn_stop.add_css_class("destructive-action")
        self.btn_stop.set_sensitive(False)
        self.btn_stop.connect("clicked", self.on_stop_clicked)
        header.pack_end(self.btn_stop)



        content_box.append(header)

        # --- Content Area ---

        # Results List (ColumnView)
        self.store = Gio.ListStore(item_type=ScanResult)

        self.selection_model = Gtk.SingleSelection(model=self.store)
        self.column_view = Gtk.ColumnView(model=self.selection_model)
        self.column_view.set_show_row_separators(True)
        self.column_view.set_show_column_separators(True)

        self.create_column("IP Address", "ip")
        self.create_column("Ping Time", "time_ms")
        self.create_column("Hostname", "hostname")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(self.column_view)
        scrolled_window.set_vexpand(True) # Fill remaining space

        content_box.append(scrolled_window)

        # --- Progress Bar (Bottom) ---
        self.progress_bar = Gtk.ProgressBar()
        # Remove margins so it sits flush at the bottom like a status bar
        self.progress_bar.set_fraction(0.0)
        content_box.append(self.progress_bar)

    def create_column(self, title, property_name):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_column_setup)
        factory.connect("bind", self.on_column_bind, property_name)

        column = Gtk.ColumnViewColumn(title=title, factory=factory)
        column.set_expand(True)
        self.column_view.append_column(column)

    def on_column_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_margin_start(10)
        list_item.set_child(label)

    def on_column_bind(self, factory, list_item, property_name):
        label = list_item.get_child()
        item = list_item.get_item()
        label.set_text(getattr(item, property_name))

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------

    def on_start_clicked(self, widget):
        self.scanning = True
        self.stop_event.clear()
        self.update_ui_state(scanning=True)
        self.store.remove_all()
        self.progress_bar.set_fraction(0.0)

        thread = threading.Thread(target=self.run_scan, daemon=True)
        thread.start()

    def on_stop_clicked(self, widget):
        self.stop_event.set()

    def on_export_clicked(self, widget):
        def save_file(dialog, result):
            try:
                file = dialog.save_finish(result)
                path = file.get_path()

                with open(path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["IP Address", "Ping Time (ms)", "Hostname"])
                    for i in range(self.store.get_n_items()):
                        item = self.store.get_item(i)
                        writer.writerow(item.get_raw_data())

                toast = Adw.Toast.new(f"Saved to {path}")
                self.toast_overlay.add_toast(toast)

            except Exception as e:
                print(f"Export failed: {e}")

        dialog = Gtk.FileDialog()
        dialog.set_initial_name("scan_results.csv")
        dialog.save(self, None, save_file)

    def update_ui_state(self, scanning):
        self.btn_start.set_sensitive(not scanning)
        self.btn_stop.set_sensitive(scanning)
        self.btn_export.set_sensitive(not scanning)

    # -------------------------------------------------------------------------
    # SCAN LOGIC (THREADED)
    # -------------------------------------------------------------------------

    def run_scan(self):
        local_ip = get_local_ip()
        target_list = get_local_ips_list(local_ip)
        total_ips = len(target_list)
        processed_count = 0

        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_ip = {executor.submit(ping_host, ip): ip for ip in target_list}

            for future in as_completed(future_to_ip):
                if self.stop_event.is_set():
                    break

                ip = future_to_ip[future]
                processed_count += 1

                fraction = processed_count / total_ips
                GLib.idle_add(self.progress_bar.set_fraction, fraction)

                try:
                    ms_time = future.result()
                    if ms_time is not None:
                        hostname = get_hostname(ip)
                        GLib.idle_add(self.add_result_row, ip, ms_time, hostname)
                except Exception as e:
                    print(f"Error checking {ip}: {e}")

        GLib.idle_add(self.on_scan_finished)

    def add_result_row(self, ip, ms_time, hostname):
        result_obj = ScanResult(ip, ms_time, hostname)
        self.store.append(result_obj)

    def on_scan_finished(self):
        self.scanning = False
        self.update_ui_state(scanning=False)
        self.progress_bar.set_fraction(1.0)
        toast = Adw.Toast.new("Scan Complete")
        self.toast_overlay.add_toast(toast)

    def _on_about_activated(self, action, param):
        """Shows the About Window."""
        dialog = Adw.AboutWindow(transient_for=self.get_root())
        dialog.set_application_name("Hungry IP Scanner")
        dialog.set_version("1.0")
        dialog.set_developer_name("Julien Grondin")
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.set_comments("A simple utility for scanning ip adresses over local network.")
        dialog.set_website("https://github.com/juliengrdn/hungryipscanner")
        dialog.set_copyright("© 2025 Julien Grondin")
        # Set icon if available
        try:
            Gtk.IconTheme.get_for_display(Gdk.Display.get_default()).add_resource_path("/")
            dialog.set_icon_name("hungryipscannerlogo")
        except:
            pass  # Fallback to default icon
        dialog.show()

class NetworkScannerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.juliengrdn.hungryipscanner",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = NetworkScannerWindow(self)
        win.present()

if __name__ == "__main__":
    app = NetworkScannerApp()
    sys.exit(app.run(sys.argv))
