from bs4 import BeautifulSoup
import json
import random
import requests
import re
from tqdm import tqdm
import os

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
MAX_ATTEMPTS = 5  # Number of attempts to access a website

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

# Clean supplier name
def clean_supplier_name(name):
    tokens = '?/\\:*"<>|'
    for token in tokens:
        name = name.replace(token, '')
    return name

# Scrap suppliers from json
def scrape_text_from_suppliers(json_filename: str, folder_persistance: str = 'data', max_suppliers: int = -1):
    data = json.load(open(json_filename, 'r'))
    data = data[:max_suppliers]
    docs = []
    suppliers = []
    if not os.path.exists(folder_persistance):
        os.makedirs(folder_persistance)
    for supplier in tqdm(data):
        supplier_name = supplier['supplier']
        suppliers.append(supplier)
        # Clean supplier name
        supplier_name = clean_supplier_name(supplier_name)
        supplier_file = os.path.join(folder_persistance, supplier_name + '.txt')
        if not os.path.exists(supplier_file):
            text = ''
            pages = supplier['pages']
            for page in pages:
                html_soup = scrape_website(page)
                if html_soup is not None:
                    html_soup_text = html_soup.findAll(text=True)
                    html_soup_text_visible = ''.join(list(filter(is_visible, html_soup_text)))
                    text += html_soup_text_visible
            with open(supplier_file, 'w') as f:
                f.write(text)
        else:
            with open(supplier_file, 'r') as f:
                text = f.read()
        docs.append(text)
    return docs, suppliers
