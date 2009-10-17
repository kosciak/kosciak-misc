#!/usr/bin/python

__author__ = "Wojciech 'KosciaK' Pietrzok (kosciak@kosciak.net)"
__version__ = "0.1"

from lib.BeautifulSoup import BeautifulSoup

import urllib
import re
import sys
import csv


URL = 'http://www.adtaily.com/networks/%s/websites?page=%s'


def parse_page(writer, catalogue, page=1):
    print 'Parsing page %s' % page
    
    url = urllib.urlopen(URL % (catalogue, page))
    soup = BeautifulSoup(url)
    
    table = soup.find('table', attrs={'class': 'snippets'})
    for tr in table.findAll('tr'):
        # get name of the page
        name = tr.td.h4.a.string
        
        # get URL of the page
        url = tr.td.h4.a['href'].encode('utf-8')
        
        #get stats info
        stats = '?'
        stats_element = tr.find('p', attrs={'class': 'Stats'})
        if stats_element:
            stats = stats_element.strong.nextSibling.string[1:-11].replace(' ', '')
            if stats == 'wtrakc': 
                stats = '?'
        
        # get price
        price = tr.find('td', attrs={'class': 'Price'}).strong.string[0:-12]
        
        # calculate CPM
        cpm = '?'
        try:
            cpm = float(price) / int(stats) * 1000
        except:
            cpm = '?'
        
        # write to the file
        row = [name, url, stats, price.replace('.', ','), str(cpm).replace('.', ',')]
        print row
        writer.writerow(row)
    
    # find last page of the catalogue
    anchors = soup.findAll('a', href=re.compile('/networks/[0-9]+/websites\?page=[0-9]+'))
    if not anchors:
        return
    
    pages = []
    for anchor in anchors:
        number = re.match('/networks/[0-9]+/websites\?page=([0-9]+)', anchor['href']).group(1)
        pages.append(int(number))

    pages.sort()
    last = pages[-1]
    
    # parse next page if exists
    if last > page:
        next = page + 1
        parse_page(writer, catalogue, next)
    

def start(catalogue):
    print 'Parsing catalogue %s' % catalogue
    
    # Create new file (or overwrite existing one)
    file = open('adtaily_%s.csv' % catalogue, 'w')
    
    # Create CSV writer
    writer = csv.writer(file, dialect='excel-tab')
    
    # Add file headers
    writer.writerow(['Name', 'URL', 'Stats', 'Price', 'CPM'])
    
    parse_page(writer, catalogue)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        #print sys.argv[1]
        start(catalogue=sys.argv[1])
    else:
        print 'No arguments'


