#!/usr/bin/env python3
""" Scrapes 4chan thread.
Usage:
    $ ./scraper.py [thread_url]
"""

import sys
import os

from multiprocessing import Pool
import requests

from bs4 import BeautifulSoup;
from tqdm import tqdm
from termcolor import cprint

def download_img(img_url):
    file_name = img_url.split('/')[-1]

    with open('out/'+file_name, 'wb') as f:
        response = requests.get(img_url)
        f.write(response.content)

def scrape_thread(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    thread = soup.find('div', {'class': 'thread'})
    imgs = thread.findAll('a', href=True, target='_blank')

    if 'out' not in os.listdir():
        os.mkdir('out')

    img_urls = []
    for img in imgs:
        img_urls += ['https:' + img['href']]

    cprint(' * Downloading...', 'blue', attrs=['bold'])
    with Pool(10) as p:
        for _ in tqdm(p.imap_unordered(download_img, img_urls),
                      total=len(img_urls)):
            pass

def main():
    scrape_thread(sys.argv[1])

if __name__ == '__main__':
    main()
