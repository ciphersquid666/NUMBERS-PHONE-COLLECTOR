from termcolor import colored
import re
import requests
from urllib.parse import urlparse

print(colored("=====================================", 'cyan'))
print(colored("[×] NumCollect Tool by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙", 'red'))
print(colored("[×] Use responsibly!", 'yellow'))
print(colored("=====================================", 'cyan'))

def validate_url(url):
    if not url:
        return None, colored("Error: URL cannot be empty.", "red")
    if not re.match(r'^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', url):
        return None, colored("Error: Invalid URL format.", "red")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url.strip()
    return url, None

def extract_phones(text):
    phone_pattern = r'\+[\d\s\-().]{9,}\d'
    phones = set(re.findall(phone_pattern, text))
    return [phone.strip() for phone in phones if len(phone.strip()) >= 10]

while True:
    url = input(colored("Enter domain (e.g., example.com) or 'exit' to quit: ", "cyan"))
    if url.lower() == 'exit':
        break
    parsed_url, error = validate_url(url)
    if error:
        print(error)
        continue
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(parsed_url, timeout=10, headers=headers, allow_redirects=True)
        r.raise_for_status()
        phones = extract_phones(r.text)
        domain = urlparse(parsed_url).netloc
        if not phones:
            print(colored(f"\nNo phone numbers found on {domain}.", "yellow"))
        else:
            print(colored(f"\nPhone numbers found on {domain}:", "green"))
            print(colored("-" * 40, "green"))
            for phone in sorted(phones):
                print(colored(f"  {phone}", "green"))
            print(colored("-" * 40, "green"))
    except requests.exceptions.RequestException as e:
        print(colored(f"\nError: Could not access {domain}. Details: {e}", "red"))
