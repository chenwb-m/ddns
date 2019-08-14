#!/usr/bin/python
# -*- coding: utf-8 -*-

from alidns import Alidns
import time, requests, datetime
# from bs4 import BeautifulSoup
from argparse import ArgumentParser
import sys
import signal

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

print('%s -> access_key %s' % (str(datetime.datetime.now()), access_key), flush=True)
print('%s -> access_key_secret %s' % (str(datetime.datetime.now()), access_key_secret), flush=True)
print('%s -> domain %s' % (str(datetime.datetime.now()), domain), flush=True)
print('%s -> record %s' % (str(datetime.datetime.now()), record), flush=True)

IP = ''

# # code from https://blog.csdn.net/junbujianwpl/article/details/72353940
# def get_out_ip(url):
#     r = requests.get(url)
#     txt = r.text
#     ip = txt[txt.find("[") + 1: txt.find("]")]
#     return ip
# def get_real_url(url=r'http://www.ip138.com/'):
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,da;q=0.5',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Host': 'www.ip138.com',
#         'Referer': url,
#         'Pragma': 'no-cache',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
#     }
#     r = requests.get(url, headers=headers)
#     txt = r.text
#     soup = BeautifulSoup(txt,"html.parser").iframe
#     return soup["src"]
# def get_pub_ip():
#     return get_out_ip(get_real_url())
def get_pub_ip():
    ip = requests.get('https://api.ipify.org', timeout=5).text
    return ip

def quit(signum, frame):
    print('stop', flush=True)
    sys.exit()

signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)
alidns = Alidns(access_key, access_key_secret, domain)
alidns.list()
while True:
    try:
        ip = get_pub_ip()
        if ip != IP:
            print('%s -> ip change from %s to %s' % (str(datetime.datetime.now()), IP, ip), flush=True)
            alidns.add(record, ip)
            print('%s -> updated ip from %s to %s' % (str(datetime.datetime.now()), IP, ip), flush=True)
            IP = ip
        else:
            print('%s -> ip not change' % (str(datetime.datetime.now())), flush=True)
    except Exception as ex:
        print(ex, flush=True)
    try:
        time.sleep(60 * 10)
    except:
        pass
