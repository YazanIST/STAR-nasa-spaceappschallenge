import requests
import os

BASE = "https://standards.nasa.gov"
DOWNLOAD_DIR = "./collected_pdfs_2/"

with open('pdf_links.txt') as file:
    links = file.readlines()
    links = [link.strip() for link in links]

for i, pdf_link in enumerate(links):
    file_name = pdf_link.split("/")[-1]
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    response = requests.get(pdf_link)
    with open(file_path, 'wb') as pdf_file:
        pdf_file.write(response.content)
    print(f'{i + 1}/{len(links)} done.')
