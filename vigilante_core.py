import argparse
import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from googlesearch import search
from colorama import Fore, Style, init
import concurrent.futures

init(autoreset=True)

class VigilanteEngine:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.platforms = {
            "Instagram": "https://www.instagram.com/{}/",
            "Twitter/X": "https://twitter.com/{}",
            "GitHub": "https://github.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Medium": "https://medium.com/@{}"
        }

    def check_username(self, username):
        results = []
        def check_platform(name, url_template):
            url = url_template.format(username)
            try:
                res = requests.get(url, headers=self.headers, timeout=5)
                if res.status_code == 200:
                    return f"[+] {name}: {url}"
            except requests.RequestException:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_platform, name, url) for name, url in self.platforms.items()]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res: results.append(res)
        
        return results if results else ["[-] Tidak ada profil identik ditemukan."]

    def analyze_phone(self, phone_num):
        results = []
        try:
            parsed = phonenumbers.parse(phone_num, None)
            if phonenumbers.is_valid_number(parsed):
                region = geocoder.description_for_number(parsed, "en")
                isp = carrier.name_for_number(parsed, "en")
                results.append(f"[+] Status: Valid")
                results.append(f"[+] Country Code: {parsed.country_code}")
                results.append(f"[+] Region: {region if region else 'Unknown'}")
                results.append(f"[+] Carrier: {isp if isp else 'Unknown'}")
            else:
                results.append("[-] Invalid format. Gunakan format internasional (+62...).")
        except Exception as e:
            results.append(f"[-] Parsing Error: {e}")
        return results

    def google_dorking(self, query):
        results = []
        try:
            dork_query = f'"{query}" (intext:"cv" OR intext:"resume" OR inurl:"profile")'
            results.append(f"[~] Executing Dork: {dork_query}")
            search_res = search(dork_query, num_results=5, lang="en")
            for idx, res in enumerate(search_res, 1):
                results.append(f"[{idx}] {res}")
        except Exception as e:
            results.append(f"[-] Search Error: {e}")
        return results

# Eksekusi CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigilante OSINT - CLI Mode")
    parser.add_argument("-u", "--username", help="Target username")
    parser.add_argument("-p", "--phone", help="Target phone number")
    parser.add_argument("-n", "--name", help="Target name for Dorking")
    args = parser.parse_args()
    
    engine = VigilanteEngine()
    if args.username:
        for r in engine.check_username(args.username): print(r)
    elif args.phone:
        for r in engine.analyze_phone(args.phone): print(r)
    elif args.name:
        for r in engine.google_dorking(args.name): print(r)
    else:
        parser.print_help()
