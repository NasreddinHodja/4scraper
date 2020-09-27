#!/usr/bin/env python3
""" Scrapes 4chan thread.
Usage:
    $ ./scraper.py [thread_url]
"""

import sys
import os

import requests
from tqdm import tqdm

from bs4 import BeautifulSoup;

def scrape_thread(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    thread = soup.find('div', {'class': 'thread'})
    imgs = thread.findAll('a', href=True, target='_blank')

    if 'out' not in os.listdir():
        os.mkdir('out')

    for img in tqdm(imgs):
        img_url = 'https:' + img['href']
        file_name = img_url.split('/')[-1]

        with open('out/'+file_name, 'wb') as f:
            response = requests.get(img_url)
            f.write(response.content)

scrape_thread(sys.argv[1])
