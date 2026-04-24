import os
import argparse
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import tkinter as tk
from tkinter import messagebox, scrolledtext

class SilentiumOSINT:
    def __init__(self):
        self.version = "1.0.0"
        self.banner = f"""
        =========================================
           SILENTIUM-SHIELD OSINT SUITE v{self.version}
           Target: IP, Phone Number, WhatsApp
        =========================================
        """

    def track_ip(self, ip_address):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data['status'] == 'success':
                return f"[+] Target IP: {ip_address}\n[+] Country: {data['country']}\n[+] City: {data['city']}\n[+] ISP: {data['isp']}\n[+] Lat/Lon: {data['lat']} / {data['lon']}"
            else:
                return f"[-] Gagal melacak IP: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return f"[-] Error: {e}"

    def track_phone(self, phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(parsed_number):
                region = geocoder.description_for_number(parsed_number, "id")
                isp = carrier.name_for_number(parsed_number, "id")
                time_zones = timezone.time_zones_for_number(parsed_number)
                wa_link = f"https://wa.me/{phone_number.replace('+', '')}"
                
                return f"[+] Target Number: {phone_number}\n[+] Region: {region}\n[+] Carrier: {isp}\n[+] Timezone: {time_zones[0] if time_zones else 'Unknown'}\n[+] WhatsApp Link: {wa_link}"
            else:
                return "[-] Nomor tidak valid. Pastikan menggunakan kode negara (contoh: +62...)"
        except Exception as e:
            return f"[-] Error: {e}"

# --- Modul Antarmuka Grafis (GUI) ---
def launch_gui():
    root = tk.Tk()
    root.title("Silentium-Shield OSINT Suite")
    root.geometry("600x450")
    root.configure(bg="#0c0c0c")

    tool = SilentiumOSINT()

    title_label = tk.Label(root, text="SILENTIUM-SHIELD OSINT", font=("Consolas", 16, "bold"), bg="#0c0c0c", fg="#00ff00")
    title_label.pack(pady=15)

    input_frame = tk.Frame(root, bg="#0c0c0c")
    input_frame.pack(pady=5)

    tk.Label(input_frame, text="Target (IP / +62...):", bg="#0c0c0c", fg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=5)
    entry_target = tk.Entry(input_frame, width=40, bg="#1e1e1e", fg="#00ff00", insertbackground="white", font=("Consolas", 10))
    entry_target.pack(side=tk.LEFT, padx=5)

    result_text = scrolledtext.ScrolledText(root, width=70, height=15, bg="#000000", fg="#00ff00", font=("Consolas", 10))
    
    def execute_scan():
        target = entry_target.get().strip()
        result_text.delete(1.0, tk.END)
        if not target:
            result_text.insert(tk.END, "[-] Harap masukkan parameter target yang valid.")
            return
            
        if target.startswith('+'):
            output = tool.track_phone(target)
        else:
            output = tool.track_ip(target)
            
        result_text.insert(tk.END, output)

    btn_scan = tk.Button(root, text="Initiate Scan", command=execute_scan, bg="#004400", fg="white", font=("Consolas", 10, "bold"), relief="flat")
    btn_scan.pack(pady=10)
    
    result_text.pack(pady=10)
    root.mainloop()

# --- Modul Command Line Interface (CLI) ---
def main():
    parser = argparse.ArgumentParser(description="Silentium-Shield OSINT Suite - Data Gathering Tool")
    parser.add_argument("-i", "--ip", help="Lacak alamat IP (contoh: 8.8.8.8)")
    parser.add_argument("-p", "--phone", help="Lacak nomor HP (gunakan format +62)")
    parser.add_argument("-g", "--gui", action="store_true", help="Buka dalam mode antarmuka grafis (GUI)")
    
    args = parser.parse_args()
    tool = SilentiumOSINT()

    if args.gui:
        launch_gui()
    elif args.ip:
        print(tool.banner)
        print(tool.track_ip(args.ip))
    elif args.phone:
        print(tool.banner)
        print(tool.track_phone(args.phone))
    else:
        print(tool.banner)
        parser.print_help()

if __name__ == "__main__":
    main()
