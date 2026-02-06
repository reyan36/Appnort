import platform
import winreg
import psutil
from typing import List, Dict

class Scanner:
    def __init__(self):
        self.os_type = platform.system()

    def scan_installed_programs(self) -> List[Dict[str, str]]:
        if self.os_type == 'Windows':
            return self._scan_windows()
        elif self.os_type == 'Darwin':
            return self._scan_macos()
        elif self.os_type == 'Linux':
            return self._scan_linux()
        else:
            print(f"Unsupported OS: {self.os_type}")
            return []

    def _scan_windows(self) -> List[Dict[str, str]]:
        programs = []
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        roots = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

        for root in roots:
            for path in uninstall_paths:
                try:
                    with winreg.OpenKey(root, path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0] if self._key_exists(subkey, "DisplayVersion") else "Unknown"
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0] if self._key_exists(subkey, "InstallLocation") else "Unknown"
                                        publisher = winreg.QueryValueEx(subkey, "Publisher")[0] if self._key_exists(subkey, "Publisher") else "Unknown"
                                        
                                        if name.strip():
                                            programs.append({
                                                "name": name,
                                                "version": version,
                                                "location": install_location,
                                                "publisher": publisher,
                                                "os": "Windows"
                                            })
                                    except OSError:
                                        continue
                            except OSError:
                                continue
                except OSError:
                    continue
        
        # Remove duplicates based on name
        unique_programs = {p['name']: p for p in programs}.values()
        return list(unique_programs)

    def _key_exists(self, key, subkey_name):
        try:
            winreg.QueryValueEx(key, subkey_name)
            return True
        except FileNotFoundError:
            return False

    def _scan_macos(self):
        # Stub for macOS
        return [{"name": "Mock App (Mac)", "version": "1.0", "location": "/Applications", "os": "Darwin"}]

    def _scan_linux(self):
        # Stub for Linux
        return [{"name": "Mock App (Linux)", "version": "1.0", "location": "/usr/bin", "os": "Linux"}]
