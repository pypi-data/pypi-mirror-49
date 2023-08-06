import Base
import requests
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import traceback

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

        }
proxy_ips = Base.get_proxy_ips()
print(len(proxy_ips))

while True:
    proxy_ip = proxy_ips[0]
    resp = ''
    try:
        resp = requests.get('https://www.baidu.com', proxies=proxy_ip)
    except:
        resp = ''
        pass
    if resp:
        break
    proxy_ips.remove(proxy_ip)

print('0000000000000000000000000')
# print(proxy_ips)
print(len(proxy_ips))

