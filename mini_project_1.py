#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup

def open_url(url):
    # Connecting to webpage
    web_url = urllib.request.urlopen(url)
    # Getting HTML code of website
    data = web_url.read()
    # Parsing HTML using BeautifulSoup
    soup = BeautifulSoup(data, 'lxml')
    return soup

soup = open_url('https://www.fasttrack.co.uk')

# Finding the div elemnent located at footer where the link is present
refs = soup.find('div',{'class':'col-sm-4 col-md-3 col-6'})

# Finding all hyperlinks in divison
lnks = refs.find_all('a')

# extracting required url....Hopefully it is the last element in list
lnk = lnks[len(lnks)-1].get('href')

#connecting to required url
salad = open_url(lnk)

#Finding table link
t_links = salad.find_all('a',{'class':'button skew_forward'})
t_link = t_links[len(t_links)-2].get('href')

#Parsing the table page
tble = open_url(t_link)

#Getting the table
tbl = tble.find('table')

# Getting Headers
headers = []
heads = tbl.find_all('th')
for head in heads:
    headers.append(head.text.strip())
    
# Getting individual rows
rows = []
lines = tbl.find('tbody').find_all('tr')
for line in lines:
    cols=[]
    cells = line.find_all('td')
    for cell in cells:
        cols.append(cell.text.strip())
    
    rows.append(cols)

# Cleaning Data for 2nd Column
pattern = re.compile(r'[A-Z]')
for row in rows:
    m = pattern.finditer(row[1])
    for i in m:
        pos = i.start()
        
    part_1 = row[1][:pos]
    part_2 = row[1][pos:]
    row[1] = part_1 + '\n(' + part_2 + ')'
    
# Writing data to CSV
pd.DataFrame(rows, columns=headers).to_csv(f"Top100.csv")