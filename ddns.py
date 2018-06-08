#!/usr/bin/python
# -*- coding: utf-8 -*-

from alidns import Alidns
import time, requests, datetime
from bs4 import BeautifulSoup
from argparse import ArgumentParser

parser = ArgumentParser(prog='ddns', usage='python ddns.py -k access_key -s access_key_secret -d domain -r record')
parser.add_argument('-k', '--access_key', dest='access_key', nargs=1, type=str, required=True)
parser.add_argument('-s', '--access_key_secret', dest='access_key_secret', nargs=1, type=str, required=True)
parser.add_argument('-d', '--domain', dest='domain', nargs=1, type=str, required=True)
parser.add_argument('-r', '--record', dest='record', nargs=1, type=str, required=True)
args = parser.parse_args()

access_key = args.access_key[0]
access_key_secret = args.access_key_secret[0]
domain = args.domain[0]
record = args.record[0]

print('%s -> access_key %s' % (str(datetime.datetime.now()), access_key))
print('%s -> access_key_secret %s' % (str(datetime.datetime.now()), access_key_secret))
print('%s -> domain %s' % (str(datetime.datetime.now()), domain))
print('%s -> record %s' % (str(datetime.datetime.now()), record))

IP = ''

# code from https://blog.csdn.net/junbujianwpl/article/details/72353940
def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    return ip
def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]
def get_pub_ip():
    return get_out_ip(get_real_url())


alidns = Alidns(access_key, access_key_secret, domain)
alidns.list()
while True:
    try:
        ip = get_pub_ip()
        if ip != IP:
            alidns.add(record, ip)
            print('%s -> update ip from %s to %s' % (str(datetime.datetime.now()), IP, ip))
            IP = ip
        else:
            print('%s -> ip not change' % (str(datetime.datetime.now())))
    except Exception as ex:
        print(ex)
    try: 
        time.sleep(60 * 10)
    except:
        pass

