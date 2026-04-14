import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from googlesearch import search
import concurrent.futures

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
            "Medium": "https://medium.com/@{}"
        }

    def search_username(self, username):
        results = []
        def check_platform(name, url_template):
            url = url_template.format(username)
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    return f"[{name}] Found: {url}"
            except:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_platform, name, url) for name, url in self.platforms.items()]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res: results.append(res)
        return results if results else ["[-] No identical profiles found."]

    def analyze_phone(self, phone_num):
        try:
            parsed = phonenumbers.parse(phone_num, None)
            if phonenumbers.is_valid_number(parsed):
                region = geocoder.description_for_number(parsed, "en")
                isp = carrier.name_for_number(parsed, "en")
                return [f"Status: Valid", f"Country Code: {parsed.country_code}", f"Region: {region}", f"Carrier: {isp}"]
            return ["[-] Invalid format."]
        except Exception as e:
            return [f"[-] Error: {e}"]

    def google_dorking(self, query):
        results = []
        dork_query = f'"{query}" (intext:"cv" OR intext:"resume" OR inurl:"profile")'
        try:
            for idx, res in enumerate(search(dork_query, num_results=5, lang="en"), 1):
                results.append(f"[{idx}] {res}")
        except Exception as e:
            results.append(f"[-] Dorking Error: {e}")
        return results

    def check_breach(self, email):
        # Menggunakan API publik HaveIBeenPwned (Memerlukan API Key untuk versi penuh, ini adalah skema implementasi)
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        # Catatan: HIBP mewajibkan header 'hibp-api-key'. Anda bisa menggantinya dengan API OSINT lain.
        return ["[*] Modul Breach terinisialisasi. Menunggu validasi API Key..."]
