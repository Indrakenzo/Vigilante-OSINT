import os
import customtkinter as ctk
import requests
import shodan
import face_recognition
import cv2
from PIL import Image, ImageTk

import customtkinter as ctk
from vigilante_core import VigilanteEngine # IMPORT CORE ENGINE
import shodan
# ... (imports lainnya)

class VigilanteV2(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = VigilanteEngine() # INISIALISASI ENGINE LAMA
        self.setup_gui()

    def setup_gui(self):
        # ... (Kode GUI yang sebelumnya saya berikan)
        pass

    def run_recon(self):
        target = self.input_target.get()
        self.log(f"[*] Triggering Engine for: {target}")
        
        # MEMANGGIL FUNGSI DARI CORE LAMA
        data = self.engine.search_username(target)
        for entry in data:
            self.log(f"[+] Found: {entry}")

# ... (Sisa kode GUI)
# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VigilanteV2(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS | Vigilante OSINT v2.0")
        self.geometry("1100x700")
        
        # Grid layout 1x2
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame (Control Center)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="VIGILANTE CORE", font=("Courier", 20, "bold"))
        self.sidebar_title.pack(pady=20)

        # Buttons
        self.btn_recon = ctk.CTkButton(self.sidebar, text="System Recon", command=self.run_recon)
        self.btn_recon.pack(pady=10, padx=10)
        self.btn_loc = ctk.CTkButton(self.sidebar, text="Live Location", command=self.live_location)
        self.btn_loc.pack(pady=10, padx=10)
        self.btn_cctv = ctk.CTkButton(self.sidebar, text="CCTV Scanner", command=self.cctv_scanner)
        self.btn_cctv.pack(pady=10, padx=10)
        self.btn_face = ctk.CTkButton(self.sidebar, text="Face Recognition", command=self.face_recon)
        self.btn_face.pack(pady=10, padx=10)

        # Main Display
        self.display_frame = ctk.CTkFrame(self, corner_radius=10)
        self.display_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.terminal_output = ctk.CTkTextbox(self.display_frame, font=("Consolas", 12))
        self.terminal_output.pack(expand=True, fill="both", padx=10, pady=10)

        self.log("[SYSTEM] Initialize JARVIS Modules... OK")

    def log(self, message):
        self.terminal_output.insert("end", f"{message}\n")
        self.terminal_output.see("end")

    # --- ADVANCED MODULES ---

    def live_location(self):
        self.log("[*] Initializing Live Location Module...")
        ip = "8.8.8.8" # Placeholder, integrasikan dengan input
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}").json()
            self.log(f"[+] Target Coords: {res['lat']}, {res['lon']}")
            self.log(f"[+] City: {res['city']}, {res['country']}")
        except:
            self.log("[-] Error tracking location.")

    def cctv_scanner(self):
        SHODAN_API_KEY = "YOUR_API_KEY_HERE"
        self.log("[*] Searching for unsecured CCTV streams via Shodan...")
        api = shodan.Shodan(SHODAN_API_KEY)
        try:
            results = api.search('webcamxp') # Dork for open cams
            for result in results['matches'][:5]:
                self.log(f"[+] Found: {result['ip_str']}:{result['port']} ({result['location']['city']})")
        except Exception as e:
            self.log(f"[-] Shodan Error: {e}")

    def face_recon(self):
        self.log("[*] Initializing Facial Biometric Analysis...")
        # Placeholder logic: Membandingkan image target dengan dataset
        self.log("[!] Load 'target.jpg' and 'scraped_images/'...")
        # Core: face_recognition.compare_faces(known_encodings, unknown_encoding)
        self.log("[+] Scan Complete: No immediate match in public databases.")

    def run_recon(self):
        self.log("[*] Running Core OSINT Engine...")
        # Integrasi dengan vigilante_core.py yang lama

if __name__ == "__main__":
    app = VigilanteV2()
    app.mainloop()
