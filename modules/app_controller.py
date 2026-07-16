import subprocess
import platform
import os
import psutil

class AppController:
    def __init__(self):
        self.system = platform.system()
        
        # Common application paths/commands
        self.app_map = {
            'notepad': 'notepad.exe' if self.system == 'Windows' else 'gedit',
            'calculator': 'calc.exe' if self.system == 'Windows' else 'gnome-calculator',
            'browser': 'chrome.exe' if self.system == 'Windows' else 'google-chrome',
            'chrome': 'chrome.exe' if self.system == 'Windows' else 'google-chrome',
            'firefox': 'firefox.exe' if self.system == 'Windows' else 'firefox',
            'vscode': 'code.exe' if self.system == 'Windows' else 'code',
            'terminal': 'cmd.exe' if self.system == 'Windows' else 'gnome-terminal',
        }
    
    def open_app(self, app_name):
        """Open an application"""
        app_name = app_name.lower().strip()
        
        try:
            # Check if it's in our app map
            if app_name in self.app_map:
                command = self.app_map[app_name]
            else:
                command = app_name
            
            if self.system == 'Windows':
                os.startfile(command) if command.endswith('.exe') else subprocess.Popen(command, shell=True)
            else:
                subprocess.Popen([command])
            
            return f"✅ Opened {app_name}"
        
        except Exception as e:
            return f"❌ Could not open {app_name}: {str(e)}"
    
    def close_app(self, app_name):
        """Close an application"""
        app_name = app_name.lower().strip()
        
        try:
            closed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name in proc.info['name'].lower():
                        proc.kill()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                return f"✅ Closed {app_name}"
            else:
                return f"⚠️ {app_name} is not running"
        
        except Exception as e:
            return f"❌ Error closing {app_name}: {str(e)}"
    
    def list_running_apps(self):
        """List all running applications"""
        apps = []
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                apps.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return apps