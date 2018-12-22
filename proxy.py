#!/usr/bin/python
# Proxy Fetcher 0.3.1
# Author: Konstantin Mednikov
# Date 12 Dec 2018
# Kiev, Ukraine

import re
import sys
import cfscrape  # To overcome CloudFlare protection
# import argparse


# parser = argparse.ArgumentParser(description='Proxy Fetcher')
# parser.add_argument('integers', metavar='-n', type=int,help='an integer for the accumulator')
# parser.add_argument('-number', type=int, help='Specify how many proxies you want')
# parser.add_argument('-f', type=str, help='Custom filename. Default is \'proxy.list\'')
# parser.add_argument('-c', type=str, help='2-letter country name. Like \'GB\', or \'USCA\'')
# parser.add_argument('-here', type=str, help='Fetches proxies to Command line. Tip: don\'t do many!')
# args = parser.parse_args()

def find(data):
    matches = re.findall(r'(\d+\.\d+\.\d+\.\d+)<\/td><td>(\d+)', data.text)
    proxies = list()
    for p in matches:
        proxies.append(p[0] + ':' + p[1])
    return proxies


def save(list):
    with open(filename, "a") as f:
        for p in list:
            f.write(p + '\n')


def fetch(nb, country=''):
    proxies = list()
    url = r'https://hidemyna.me/en/proxy-list/?{1}maxtime=500&type=hs&start={0}#list'
    scraper = cfscrape.create_scraper()

    i = int(64 * round(float(nb) / 64))  # round to the closest multiply of 64
    if i == 0:  # if it rounded to 0, then set it to 64 to load one page
        i = 64

    if country:  # if there is a country modifier, modify it correctly
        country = 'country=' + country + '&'
    # iterate through pages
    for num in range(0, i, 64):
        data = scraper.get(url.format(num, country))

        if data.status_code == 200:
            proxies.extend(find(data))
        else:
            print('Couldn\'t connect:', data.status_code)
            quit()
    return proxies


def to_int(string):
        try:
            return int(string)
        except ValueError:
            return None


if __name__ == '__main__':
    # defaults
    nb = 64
    filename = 'proxy.list'
    country = ''

    if len(sys.argv) == 1:  # no arguments were passed, let's ask a user about the number of proxies
        print('Welcome to Proxy Fetcher')
        nb = to_int(input('number of proxies: '))

    if len(sys.argv) >= 2:  # the first argument is a number of proxies to fetch
        if sys.argv[1] == 'help':
            print('The first argument is a number of proxies, the second argument is a custom filename')
            quit()
        nb = to_int(sys.argv[1])
        if nb is None:
            print('The first argument is not a number!\nproxy.py [number of proxies] [filename] [country]')
            quit()

    if len(sys.argv) == 3:  # second argument is a custom filename
        filename = str(sys.argv[2])

    if len(sys.argv) == 3:  # countries
        country = sys.argc[4]

    if filename == 'here':
        for i, proxy in enumerate(fetch(nb)):
            if i == nb:
                break
            print(proxy)

    else:
        # flushing a file
        f = open(filename, "w")
        f.close()

        print('Fetching to', filename)
        print('It will take a few seconds...')
        proxies = fetch(nb)
        save(proxies)
        print('Saved {0} proxies'.format(len(proxies)))
