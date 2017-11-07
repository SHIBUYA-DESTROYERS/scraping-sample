import re
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
bytes_content = f.read()

scanned_text = bytes_content[:1024].decode('ascii', errors='replace')

match = re.search(r'charset=["\']?([\w-]+)', scanned_text)
if match:
    encoding = match.group(1)
else:
    encoding = 'utf-8'

print('encoding: ', encoding, file=sys.stderr)

text = bytes_content.decode(encoding)
print(text)