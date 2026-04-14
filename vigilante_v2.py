import customtkinter as ctk
import threading
from vigilante_core import VigilanteEngine

# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VigilanteV2(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS | Vigilante OSINT v2.0")
        self.geometry("1100x700")
        
        self.engine = VigilanteEngine() # Load backend engine

        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="VIGILANTE CORE", font=("Courier", 20, "bold"))
        self.sidebar_title.pack(pady=20)

        # Inputs
        self.input_target = ctk.CTkEntry(self.sidebar, placeholder_text="Username / Phone / Name")
        self.input_target.pack(pady=10, padx=10, fill="x")

        # Buttons
        self.btn_recon = ctk.CTkButton(self.sidebar, text="Run Recon (All)", command=self.run_recon)
        self.btn_recon.pack(pady=10, padx=10)
        
        self.btn_loc = ctk.CTkButton(self.sidebar, text="Live Location Trace", command=self.dummy_loc)
        self.btn_loc.pack(pady=10, padx=10)

        # Main Display Terminal
        self.display_frame = ctk.CTkFrame(self, corner_radius=10)
        self.display_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.terminal = ctk.CTkTextbox(self.display_frame, font=("Consolas", 13), text_color="#00FF00", fg_color="black")
        self.terminal.pack(expand=True, fill="both", padx=10, pady=10)

        self.log("[SYSTEM] Initialize JARVIS Modules... OK")
        self.log("[SYSTEM] Awaiting Target Parameters...")

    def log(self, message):
        self.terminal.insert("end", f"{message}\n")
        self.terminal.see("end")

    def run_recon(self):
        target = self.input_target.get()
        if not target:
            self.log("[-] ERROR: Target tidak boleh kosong.")
            return

        self.log(f"\n[!] INITIATING AGGRESSIVE RECON FOR: {target}")
        
        # Jalankan di thread terpisah agar GUI tidak freeze
        def process():
            self.log("\n[*] 1. Username Enumeration Phase...")
            for res in self.engine.search_username(target):
                self.log(res)
                
            self.log("\n[*] 2. Telephony Metadata Phase...")
            if target.startswith("+"):
                for res in self.engine.analyze_phone(target):
                    self.log(res)
            else:
                self.log("[-] Target bukan format nomor telepon. Skipped.")
                
            self.log("\n[*] 3. Search Engine Dorking Phase...")
            for res in self.engine.google_dorking(target):
                self.log(res)

            self.log("\n[+] RECON OPERATION COMPLETE.")

        threading.Thread(target=process).start()

    def dummy_loc(self):
        self.log("[*] Fitur Live Location & CCTV memerlukan validasi Token API (Shodan/OSM).")

if __name__ == "__main__":
    app = VigilanteV2()
    app.mainloop()
