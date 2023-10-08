from bs4 import BeautifulSoup
import requests
import os

BASE = "https://standards.nasa.gov"

STARTING_URLS = [
    "https://standards.nasa.gov/all-standards?page=0", 
    "https://standards.nasa.gov/all-standards?page=1"
]

DOWNLOAD_DIR = "./collected_pdfs/"

standards_pages = []

for url in STARTING_URLS:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    filtered_links = soup.find_all('a', href=lambda href: href and href.startswith('/standard/'))
    for link in filtered_links:
        standards_pages.append(f"{BASE}{link['href']}")

pdf_links = []

for url in standards_pages:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    filtered_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    for link in filtered_links:
        pdf_link = f"{BASE}{link['href']}"
        print(pdf_link)
