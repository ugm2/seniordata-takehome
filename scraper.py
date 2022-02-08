from bs4 import BeautifulSoup
import json
import random
import requests
import re


header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17',
    'referer': 'https://www.google.com/',
    'Ugrade-Insecure-Requests': '0',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5'}


proxies = ['tebssdjk:3aarsmkklrx1@45.57.254.235:6273/',
           "tebssdjk:3aarsmkklrx1@138.128.68.70:7138/",
           "tebssdjk:3aarsmkklrx1@45.130.125.246:6263/",
           "tebssdjk:3aarsmkklrx1@23.229.107.73:7598/",
           "tebssdjk:3aarsmkklrx1@144.168.149.86:7135/",
           "tebssdjk:3aarsmkklrx1@23.236.183.90:8661/",
           "tebssdjk:3aarsmkklrx1@192.186.172.203:9203/"
           ]


session = requests.session()
MAX_ATTEMPTS = 3  # Number of attempts to access a website

# Return random proxy
def get_proxy():
    proxy_credentials = random.choice(proxies)
    return {"http": "http://" + proxy_credentials,
            "https": "http://" + proxy_credentials}

# Scraping website
def scrape_website(url):
    current_attempt = 1

    while current_attempt < MAX_ATTEMPTS:
        try:
            site = session.get(url, headers=header, proxies=get_proxy(), timeout=10)
            if site.status_code == requests.codes.ok:
                html_soup = BeautifulSoup(site.text, 'html.parser')

                # Check whether reCAPTCHA was detected
                if len(html_soup.find_all('div', class_='alert alert-info')) == 0:
                    return html_soup
                else:
                    print('reCAPTCHA detected when scraping ' + url)

        except Exception as e:
            print(e)

        current_attempt += 1

    print('Something went wrong when scraping ' + url)
    return None

# Filtering for visible text
def is_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

if __name__ == "__main__":
    data = json.load(open('./suppliers.json', 'r'))
    html_soup = scrape_website(data[0]['rootDomain'])  # Sample scraping

    if html_soup:
        # Extracting text only
        html_soup_text = html_soup.findAll(text=True)
        html_soup_text_visible = '\n'.join(list(filter(is_visible, html_soup_text)))
        html_soup_text_visible_cleaned = html_soup_text_visible.split()