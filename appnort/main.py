import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import webbrowser
from appnort.scanner import Scanner
from appnort.categorizer import Categorizer
from appnort.pdf_generator import PDFGenerator
from appnort.config import ConfigManager

class AppnortApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()
        self.scanner = Scanner()
        self.categorizer = Categorizer(self.config.get("groq_api_key"), self.config.get("groq_model", "llama-3.3-70b-versatile"))
        self.pdf_generator = PDFGenerator()
        self.programs = []

        # Theme setup
        ctk.set_appearance_mode(self.config.get("theme", "System"))
        ctk.set_default_color_theme("blue")

        self.title("Appnort - Local Software Audit")
        self.geometry("900x600")

        self._create_widgets()

    def _create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Appnort", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left", padx=10)

        self.scan_button = ctk.CTkButton(self.header_frame, text="Scan Programs", command=self.start_scan)
        self.scan_button.pack(side="right", padx=10)

        self.export_button = ctk.CTkButton(self.header_frame, text="Export PDF", command=self.export_pdf, state="disabled")
        self.export_button.pack(side="right", padx=10)

        # Content Area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabview for List and Settings
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.pack(fill="both", expand=True)

        self.list_tab = self.tabview.add("Programs")
        self.settings_tab = self.tabview.add("Settings")

        # Program List (using Text widget for simplicity for now, ideally Treeview)
        # Using a ScrollableFrame for a list of items
        self.program_list_frame = ctk.CTkScrollableFrame(self.list_tab)
        self.program_list_frame.pack(fill="both", expand=True)
        
        self.status_label = ctk.CTkLabel(self.list_tab, text="Ready to scan.")
        self.status_label.pack(side="bottom", pady=5)

        # Settings
        self._create_settings_widgets()

    def _create_settings_widgets(self):
        # Appearance Mode
        self.appearance_label = ctk.CTkLabel(self.settings_tab, text="Theme:")
        self.appearance_label.pack(pady=(10, 0))
        
        self.appearance_var = ctk.StringVar(value=self.config.get("theme", "System"))
        self.appearance_combobox = ctk.CTkComboBox(
            self.settings_tab, 
            values=["System", "Light", "Dark"],
            variable=self.appearance_var,
            command=self.change_appearance_mode
        )
        self.appearance_combobox.pack(pady=5)

        self.api_key_label = ctk.CTkLabel(self.settings_tab, text="Groq API Key:")
        self.api_key_label.pack(pady=(10, 0))
        
        # Link to get key
        self.link_label = ctk.CTkLabel(self.settings_tab, text="Get API Key (Groq Console)", text_color=("blue", "light blue"), cursor="hand2")
        self.link_label.pack(pady=2)
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open("https://console.groq.com/keys"))

        self.api_key_entry = ctk.CTkEntry(self.settings_tab, width=300, show="*")
        self.api_key_entry.insert(0, self.config.get("groq_api_key", ""))
        self.api_key_entry.pack(pady=5)
        
        # Model Selection
        self.model_label = ctk.CTkLabel(self.settings_tab, text="AI Model:")
        self.model_label.pack(pady=(10, 0))
        
        self.model_var = ctk.StringVar(value=self.config.get("groq_model", "llama-3.3-70b-versatile"))
        self.model_combobox = ctk.CTkComboBox(
            self.settings_tab, 
            values=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            variable=self.model_var,
            width=250
        )
        self.model_combobox.pack(pady=5)

        self.remember_key_var = ctk.BooleanVar(value=True)
        self.remember_key_checkbox = ctk.CTkCheckBox(self.settings_tab, text="Remember Key", variable=self.remember_key_var)
        self.remember_key_checkbox.pack(pady=5)

        self.test_key_button = ctk.CTkButton(self.settings_tab, text="Test Connection", command=self.test_connection)
        self.test_key_button.pack(pady=10)

        self.save_settings_button = ctk.CTkButton(self.settings_tab, text="Save Settings", command=self.save_settings)
        self.save_settings_button.pack(pady=10)

    def test_connection(self):
        key = self.api_key_entry.get().strip()
        if not key:
            messagebox.showerror("Error", "Please enter an API key.")
            return

        self.test_key_button.configure(state="disabled", text="Testing...")
        threading.Thread(target=self._test_connection_thread, args=(key,), daemon=True).start()

    def _test_connection_thread(self, key):
        # Create a temp categorizer to test the key
        model = self.model_var.get()
        temp_cat = Categorizer(key, model)
        try:
            # Simple test categorization
            result = temp_cat._ai_categorize("Notepad++")
            if result and result != "Unknown":
                self.after(0, lambda: messagebox.showinfo("Success", "Connection Verified Successfully!"))
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Connection verified but AI returned 'Unknown'."))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Connection failed: {e}"))
        finally:
            self.after(0, lambda: self.test_key_button.configure(state="normal", text="Test Connection"))

    def save_settings(self):
        key = self.api_key_entry.get().strip()
        model = self.model_var.get()
        
        # Update current runtime categorizer
        self.categorizer.groq_api_key = key
        self.categorizer.model = model
        
        self.config.set("groq_model", model)

        if self.remember_key_var.get():
            self.config.set("groq_api_key", key)
            messagebox.showinfo("Settings", "Settings saved successfully!")
        else:
            # Clear from config if user doesn't want to remember, but keep in memory
            self.config.set("groq_api_key", "")
            messagebox.showinfo("Settings", "Settings applied for this session (Key not saved).")

    def start_scan(self):
        self.scan_button.configure(state="disabled")
        self.status_label.configure(text="Scanning...")
        threading.Thread(target=self._scan_process, daemon=True).start()

    def _scan_process(self):
        raw_programs = self.scanner.scan_installed_programs()
        self.programs = []
        
        total = len(raw_programs)
        # 1. Rule-based pass on all
        unknowns = []
        for i, prog in enumerate(raw_programs):
            if i % 10 == 0:
                self.status_label.configure(text=f"Rule Check: {i+1}/{total}...")
            
            # This now returns dict {"category": ..., "security": ...}
            # Only use rule-based first (or cache)
            res = self.categorizer.categorize(prog['name'])
            prog['category'] = res.get('category', 'Unknown')
            prog['security'] = res.get('security', 'Unknown')
            
            # Add to batch if Category is Unknown OR if we want Security stats and don't have them
            if self.categorizer.groq_api_key:
                if prog['category'] == 'Unknown' or prog['security'] == 'Unknown':
                    unknowns.append(prog)
            
            self.programs.append(prog)
        
        # 2. Batch AI pass for unknowns (and security checks)
        if unknowns:
            # We might have a lot of programs now, so batch status updates are important
            batch_size = 20
            total_unknowns = len(unknowns)
            
            for i in range(0, total_unknowns, batch_size):
                batch = unknowns[i:i+batch_size]
                names = [p['name'] for p in batch]
                
                self.status_label.configure(text=f"AI Analyzing: {i+1}/{total_unknowns} programs...")
                
                # Call batch API
                results = self.categorizer.batch_categorize(names)
                
                # Apply results back to program objects
                for prog in batch:
                    if prog['name'] in results:
                        data = results[prog['name']]
                        prog['category'] = data.get('category', 'Unknown')
                        prog['security'] = data.get('security', 'Unknown')
                    # We also need to update cache in memory if needed, 
                    # but batch_categorize already does that.
                    
                    # Also need to update the object in self.programs? 
                    # self.programs contains references to the same dicts, so yes.

        self.after(0, self._scan_complete)

    def _scan_complete(self):
        self.status_label.configure(text=f"Scan complete. Found {len(self.programs)} programs.")
        self.scan_button.configure(state="normal")
        self.export_button.configure(state="normal")
        self._update_program_list()

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.config.set("theme", new_appearance_mode)

    def _update_program_list(self):
        # Clear existing
        for widget in self.program_list_frame.winfo_children():
            widget.destroy()

        # Add header
        header = ctk.CTkFrame(self.program_list_frame)
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="Name", width=200, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Category", width=100, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Version", width=100, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        # Add items
        for prog in self.programs:
            row = ctk.CTkFrame(self.program_list_frame)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=prog['name'][:30], width=200, anchor="w").pack(side="left", padx=5)
            
            # Color code category?
            cat_label = ctk.CTkLabel(row, text=prog['category'], width=100, anchor="w")
            cat_label.pack(side="left", padx=5)
            
            ctk.CTkLabel(row, text=prog['version'][:15], width=100, anchor="w").pack(side="left", padx=5)

    def export_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_generator.generate_report(self.programs, file_path)
            messagebox.showinfo("Export", f"PDF exported to {file_path}")

if __name__ == "__main__":
    app = AppnortApp()
    app.mainloop()
