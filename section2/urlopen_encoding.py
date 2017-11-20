import sys
import urllib.request

proxies = {
    'http': 'http://172.20.20.104:8080',
    'https': 'http://172.20.20.104:8080',
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
}

url = 'https://gihyo.jp/dp'

proxy_handler = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(proxy_handler)

request = urllib.request.Request(url=url, headers=headers)
f = urllib.request.urlopen(request)

encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding: ', encoding, file=sys.stderr)

text = f.read().decode(encoding)
print(text)