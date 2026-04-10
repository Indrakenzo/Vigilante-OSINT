import argparse
import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from googlesearch import search
from colorama import Fore, Style, init
import concurrent.futures
import time

# vigilante_core.py (Tetap pertahankan fungsi utamanya)
import requests
# ... (imports lainnya)

class VigilanteEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0...'}

    def search_username(self, username):
        # Kembalikan hasil dalam bentuk list/dict agar GUI bisa menampilkan
        results = []
        # ... (logika pencarian)
        return results

    def analyze_phone(self, phone):
        # ... (logika telepon)
        return data_dict

init(autoreset=True)

class VigilanteOSINT:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # Daftar target platform untuk username enumeration
        self.platforms = {
            "Instagram": "https://www.instagram.com/{}/",
            "Twitter/X": "https://twitter.com/{}",
            "GitHub": "https://github.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Medium": "https://medium.com/@{}"
        }

    def print_banner(self):
        print(Fore.CYAN + """
    ▌ ▐·▪   ▄▄ • ▪  ▄▄▌   ▄▄▄·  ▐ ▄ ▄▄▄▄▄▄▄▄ .
   ▪█·█▌██ ▐█ ▀ ▪██ ██•  ▐█ ▀█ •█▌▐█•██  ▀▄.▀·
   ▐█▪█▌▐█·▄█ ▀█▄▐█·██▪  ▄█▀▀█ ▐█▐▐▌ ▐█.▪▐▀▀▪▄
    ███ ▐█▌▐█▄▪▐█▐█▌▐█▌ ▐▐█ ▪▐▌██▐█▌ ▐█▌·▐█▄▄▌
   . ▀  ▀▀▀·▀▀▀▀ ▀▀▀.▀▀▀ ▀  ▀ ▀▀▀ █▪ ▀▀▀  ▀▀▀ 
        [+] Advanced OSINT Aggregation Tool [+]
        """)

    def check_username(self, username):
        print(Fore.YELLOW + f"[*] Memulai Username Enumeration untuk: {username}")
        found_profiles = []
        
        def check_platform(name, url_template):
            url = url_template.format(username)
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    return f"{name}: {url}"
            except requests.RequestException:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_platform, name, url) for name, url in self.platforms.items()]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(Fore.GREEN + f"[+] Ditemukan: {result}")
                    found_profiles.append(result)
        
        if not found_profiles:
            print(Fore.RED + "[-] Tidak ada profil identik yang ditemukan pada platform target.")

    def analyze_phone(self, phone_num):
        print(Fore.YELLOW + f"\n[*] Menganalisis Metadata Nomor: {phone_num}")
        try:
            parsed_number = phonenumbers.parse(phone_num, None)
            if phonenumbers.is_valid_number(parsed_number):
                region = geocoder.description_for_number(parsed_number, "en")
                isp = carrier.name_for_number(parsed_number, "en")
                print(Fore.GREEN + f"[+] Status: Valid")
                print(Fore.GREEN + f"[+] Country Code: {parsed_number.country_code}")
                print(Fore.GREEN + f"[+] Region: {region if region else 'Unknown'}")
                print(Fore.GREEN + f"[+] Carrier: {isp if isp else 'Unknown'}")
            else:
                print(Fore.RED + "[-] Invalid phone number format. Gunakan format internasional (contoh: +62812...)")
        except Exception as e:
            print(Fore.RED + f"[-] Error parsing phone number: {e}")

    def google_dorking(self, query):
        print(Fore.YELLOW + f"\n[*] Menjalankan Search Engine Recon untuk: '{query}'")
        try:
            # Menggunakan dorks spesifik untuk mencari dokumen atau profil
            dork_query = f'"{query}" (intext:"cv" OR intext:"resume" OR inurl:"profile")'
            print(Fore.CYAN + f"[~] Dork: {dork_query}")
            results = search(dork_query, num_results=5, lang="en")
            for idx, res in enumerate(results, 1):
                print(Fore.GREEN + f"[{idx}] {res}")
        except Exception as e:
            print(Fore.RED + f"[-] Error during search execution: {e}")

    def execute(self, args):
        self.print_banner()
        if args.username:
            self.check_username(args.username)
        if args.phone:
            self.analyze_phone(args.phone)
        if args.name:
            self.google_dorking(args.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigilante OSINT - Data Aggregation Tool")
    parser.add_argument("-u", "--username", help="Target username untuk di-enumerasi")
    parser.add_argument("-p", "--phone", help="Target phone number (dengan kode negara, e.g., +62...)")
    parser.add_argument("-n", "--name", help="Nama lengkap target untuk Dorking")
    
    args = parser.parse_args()
    
    if not (args.username or args.phone or args.name):
        parser.print_help()
    else:
        app = VigilanteOSINT()
        app.execute(args)
