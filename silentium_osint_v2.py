import os
import argparse
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

class SilentiumOSINT:
    def __init__(self):
        self.version = "2.0.0 (Identity & Breach Edition)"
        self.banner = f"""
        =========================================
           SILENTIUM-SHIELD OSINT SUITE v{self.version}
           Target: Reverse Caller & Data Breach
        =========================================
        """
        # Konfigurasi API - Sir Indra, silakan isi API Key Anda di sini
        self.truecaller_api_key = "ISI_API_KEY_RAPIDAPI_TRUECALLER_ANDA"
        self.hibp_api_key = "ISI_API_KEY_HIBP_ANDA"

    def reverse_caller(self, phone_number):
        """Melacak identitas dari nomor HP menggunakan Truecaller API (via RapidAPI)"""
        # Menghapus '+' jika ada untuk penyesuaian format API
        clean_num = phone_number.replace('+', '')
        
        url = "https://truecaller4.p.rapidapi.com/api/v1/getDetails"
        querystring = {"phone": clean_num, "countryCode": "ID"}
        headers = {
            "X-RapidAPI-Key": self.truecaller_api_key,
            "X-RapidAPI-Host": "truecaller4.p.rapidapi.com"
        }

        try:
            if self.truecaller_api_key == "ISI_API_KEY_RAPIDAPI_TRUECALLER_ANDA":
                return "[-] Kredensial API Truecaller belum dikonfigurasi. Silakan update di source code."
                
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                data = response.json()
                name = data.get('data', [{}])[0].get('name', 'Identitas tidak ditemukan')
                email = data.get('data', [{}])[0].get('internetAddresses', [{}])[0].get('id', 'Tidak ada email terikat')
                return f"[+] Target Number: {phone_number}\n[+] Identified Name: {name}\n[+] Linked Email: {email}"
            else:
                return f"[-] Gagal melakukan Reverse Caller. Status: {response.status_code}"
        except Exception as e:
            return f"[-] Error Koneksi: {e}"

    def check_breach(self, account):
        """Mengecek jejak kebocoran data dari Email atau Nomor HP"""
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{account}"
        headers = {
            "hibp-api-key": self.hibp_api_key,
            "user-agent": "Silentium-Shield-OSINT"
        }

        try:
            if self.hibp_api_key == "ISI_API_KEY_HIBP_ANDA":
                return "[-] Kredensial API HaveIBeenPwned belum dikonfigurasi."

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                breaches = response.json()
                result = f"[!] PERINGATAN: Target {account} ditemukan dalam {len(breaches)} kebocoran data.\n"
                for breach in breaches:
                    result += f"    - {breach['Name']} ({breach['BreachDate']})\n"
                return result
            elif response.status_code == 404:
                return f"[+] Aman. Target {account} tidak ditemukan di database kebocoran publik."
            else:
                return f"[-] Gagal mengecek Breach Data. Status API: {response.status_code}"
        except Exception as e:
            return f"[-] Error Koneksi: {e}"

# --- Modul Antarmuka Grafis (GUI) ---
def launch_gui():
    root = tk.Tk()
    root.title("Silentium-Shield OSINT - V2.0")
    root.geometry("650x500")
    root.configure(bg="#050505")

    tool = SilentiumOSINT()

    tk.Label(root, text="SILENTIUM-SHIELD (IDENTITY & BREACH)", font=("Consolas", 14, "bold"), bg="#050505", fg="#00ff00").pack(pady=15)

    input_frame = tk.Frame(root, bg="#050505")
    input_frame.pack(pady=5)

    tk.Label(input_frame, text="Target (No HP/Email):", bg="#050505", fg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=5)
    entry_target = tk.Entry(input_frame, width=45, bg="#1a1a1a", fg="#00ff00", insertbackground="white", font=("Consolas", 10))
    entry_target.pack(side=tk.LEFT, padx=5)

    result_text = scrolledtext.ScrolledText(root, width=75, height=18, bg="#000000", fg="#00ff00", font=("Consolas", 10))
    
    def run_recon():
        target = entry_target.get().strip()
        result_text.delete(1.0, tk.END)
        if not target:
            result_text.insert(tk.END, "[-] Parameter kosong.")
            return
            
        result_text.insert(tk.END, "=== INITIATING IDENTITY TRACE ===\n")
        # Logika sederhana: Jika ada '@' berarti email, skip reverse caller
        if '@' not in target:
            result_text.insert(tk.END, tool.reverse_caller(target) + "\n\n")
        
        result_text.insert(tk.END, "=== INITIATING BREACH ANALYSIS ===\n")
        result_text.insert(tk.END, tool.check_breach(target) + "\n")

    tk.Button(root, text="Execute Reconnaissance", command=run_recon, bg="#004400", fg="white", font=("Consolas", 10, "bold")).pack(pady=10)
    result_text.pack(pady=10)
    
    root.mainloop()

# --- Modul Command Line Interface (CLI) ---
def main():
    parser = argparse.ArgumentParser(description="Silentium-Shield OSINT V2.0 - Identity & Breach Edition")
    parser.add_argument("-t", "--target", help="Target Email atau Nomor HP (contoh: +62812... atau target@email.com)")
    parser.add_argument("-g", "--gui", action="store_true", help="Jalankan mode GUI")
    
    args = parser.parse_args()
    tool = SilentiumOSINT()

    if args.gui:
        launch_gui()
    elif args.target:
        print(tool.banner)
        print("=== IDENTITY TRACE ===")
        if '@' not in args.target:
            print(tool.reverse_caller(args.target))
        else:
            print("[*] Target adalah Email, melewatkan pencarian nomor telepon.")
        
        print("\n=== DATA BREACH ANALYSIS ===")
        print(tool.check_breach(args.target))
    else:
        print(tool.banner)
        parser.print_help()

if __name__ == "__main__":
    main()
