from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import threading
import sys
import re
import os
from io import StringIO

# Import your server
from app import FF_CLIENT

class ServerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_thread = None
        self.is_running = False
        self.log_output = None
        self.uid = None
        self.password = None
        self.dat_file_path = None
        
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Level Up Server',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True,
            color=(0, 1, 0, 1)
        )
        layout.add_widget(title)
        
        # File selection button
        self.file_btn = Button(
            text='SELECT .DAT FILE',
            size_hint=(1, 0.08),
            background_color=(0.2, 0.5, 0.8, 1),
            font_size='16sp',
            bold=True
        )
        self.file_btn.bind(on_press=self.show_file_chooser)
        layout.add_widget(self.file_btn)
        
        # Status label
        self.status_label = Label(
            text='Server: STOPPED - Select .dat file first',
            size_hint=(1, 0.08),
            font_size='18sp',
            color=(1, 0, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # Log output area
        scroll = ScrollView(size_hint=(1, 0.62))
        self.log_output = TextInput(
            text='Server logs will appear here...\n',
            readonly=True,
            multiline=True,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0, 1, 0, 1),
            font_name='RobotoMono-Regular'
        )
        scroll.add_widget(self.log_output)
        layout.add_widget(scroll)
        
        # Control buttons
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        self.start_btn = Button(
            text='START SERVER',
            background_color=(0, 0.7, 0, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.start_btn.bind(on_press=self.start_server)
        
        self.stop_btn = Button(
            text='STOP SERVER',
            background_color=(0.7, 0, 0, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_server)
        
        btn_layout.add_widget(self.start_btn)
        btn_layout.add_widget(self.stop_btn)
        layout.add_widget(btn_layout)
        
        return layout
    
    def show_file_chooser(self, instance):
        """Show file chooser popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # File chooser
        filechooser = FileChooserListView(
            filters=['*.dat'],
            path=os.path.expanduser('~')
        )
        content.add_widget(filechooser)
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        select_btn = Button(text='SELECT', background_color=(0, 0.7, 0, 1))
        cancel_btn = Button(text='CANCEL', background_color=(0.7, 0, 0, 1))
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select .dat file',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def select_file(btn):
            if filechooser.selection:
                selected_path = filechooser.selection[0]
                self.parse_dat_file(selected_path)
                popup.dismiss()
        
        def cancel(btn):
            popup.dismiss()
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=cancel)
        
        popup.open()
    
    def parse_dat_file(self, file_path):
        """Parse .dat file to extract UID and password"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract password
            password_match = re.search(
                r'com\.garena\.msdk\.guest_password["\s:]+([A-F0-9]+)',
                content,
                re.IGNORECASE
            )
            
            # Extract UID
            uid_match = re.search(
                r'com\.garena\.msdk\.guest_uid["\s:]+(\d+)',
                content,
                re.IGNORECASE
            )
            
            if password_match and uid_match:
                self.password = password_match.group(1)
                self.uid = uid_match.group(1)
                self.dat_file_path = file_path
                
                self.file_btn.text = f'✓ File: {os.path.basename(file_path)}'
                self.file_btn.background_color = (0, 0.7, 0, 1)
                self.status_label.text = f'Ready - UID: {self.uid}'
                self.status_label.color = (0, 1, 1, 1)
                self.start_btn.disabled = False
                
                self.add_log(f"✓ Credentials loaded from {os.path.basename(file_path)}")
                self.add_log(f"  UID: {self.uid}")
                self.add_log(f"  Password: {self.password[:20]}...")
            else:
                self.add_log("❌ ERROR: Could not find UID or password in .dat file!")
                self.status_label.text = 'ERROR: Invalid .dat file'
                self.status_label.color = (1, 0, 0, 1)
                
        except Exception as e:
            self.add_log(f"❌ ERROR parsing .dat file: {str(e)}")
            self.status_label.text = 'ERROR: Failed to read file'
            self.status_label.color = (1, 0, 0, 1)
    
    def add_log(self, message):
        """Add message to log output"""
        if self.log_output:
            self.log_output.text += f"{message}\n"
            # Auto-scroll to bottom
            self.log_output.cursor = (0, len(self.log_output.text))
    
    def start_server(self, instance):
        """Start the server in a separate thread"""
        if not self.uid or not self.password:
            self.add_log("❌ ERROR: Please select a .dat file first!")
            return
            
        if not self.is_running:
            self.is_running = True
            self.status_label.text = 'Server: RUNNING'
            self.status_label.color = (0, 1, 0, 1)
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.file_btn.disabled = True
            
            self.add_log("=== Starting server... ===")
            self.add_log(f"Using UID: {self.uid}")
            
            # Redirect stdout to capture logs
            self.old_stdout = sys.stdout
            sys.stdout = LogRedirector(self)
            
            # Start server in background thread
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()
    
    def run_server(self):
        """Run the actual server code"""
        try:
            self.add_log("Initializing FF_CLIENT...")
            self.add_log("Connecting to Free Fire servers...")
            
            # Start the FF_CLIENT with parsed credentials
            FF_CLIENT(self.uid, self.password)
            
        except Exception as e:
            self.add_log(f"❌ CRITICAL ERROR: {str(e)}")
            import traceback
            self.add_log(traceback.format_exc())
            
            # Reset UI on error
            Clock.schedule_once(lambda dt: self.reset_ui_on_error(), 0)
    
    def reset_ui_on_error(self):
        """Reset UI when server encounters an error"""
        self.is_running = False
        self.status_label.text = 'Server: ERROR - Check logs'
        self.status_label.color = (1, 0.5, 0, 1)
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.file_btn.disabled = False
    
    def stop_server(self, instance):
        """Stop the server"""
        if self.is_running:
            self.is_running = False
            self.status_label.text = 'Server: STOPPED'
            self.status_label.color = (1, 0, 0, 1)
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.file_btn.disabled = False
            
            self.add_log("=== Stopping server... ===")
            
            # Restore stdout
            if hasattr(self, 'old_stdout'):
                sys.stdout = self.old_stdout
            
            self.add_log("⚠️ Note: Server may need app restart to fully stop")
            self.add_log("Server stopped!")
    
    def on_stop(self):
        """Cleanup when app closes"""
        self.stop_server(None)


class LogRedirector:
    """Redirect stdout to Kivy app logs"""
    def __init__(self, app):
        self.app = app
    
    def write(self, message):
        if message.strip():
            Clock.schedule_once(lambda dt: self.app.add_log(message.strip()), 0)
    
    def flush(self):
        pass


if __name__ == '__main__':
    ServerApp().run()
