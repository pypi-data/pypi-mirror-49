import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import traceback


class GetProxyIPs:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

        }
        self.original_proxy_ips = []
        self.proxy_ips = []
        self.url = 'https://www.xicidaili.com/'

    def set_proxy_ips(self):
        resp = requests.get(url=self.url, headers=self.headers)
        html = etree.HTML(resp.text)
        elements = html.xpath('//tr[@class="odd"]')
        for element in elements:
            live_time = element.xpath('.//td[7]//text()')[0]
            if '天' in live_time:
                ip = element.xpath('.//td[2]//text()')[0]
                port = element.xpath('.//td[3]//text()')[0]
                http_class = element.xpath('.//td[6]//text()')[0]
                if 'HTTP' in http_class:
                    proxy_ip = http_class.lower()+'://'+ip+':'+port
                    # proxy_ip = ip + ':' + port
                    self.original_proxy_ips.append(proxy_ip)

    def check_is_ip_alive(self, proxy_ip):
        try:
            if 'https' in proxy_ip:
                proxy = {
                    'https': proxy_ip
                }
            else:
                proxy = {
                    'http': proxy_ip
                }
            url = 'https://www.baidu.com/'

            resp = requests.get(url, headers=self.headers,
                                proxies=proxy, timeout=1)
            self.proxy_ips.append(proxy)
        except:
            pass

    def run(self):
        self.set_proxy_ips()
        with ThreadPoolExecutor(max_workers=30) as pthread:
            for proxy_ip in self.original_proxy_ips:
                pthread.submit(self.check_is_ip_alive, proxy_ip)


def get_proxy_ips():
    g = GetProxyIPs()
    g.run()
    return g.proxy_ips


if __name__ == '__main__':
    get_proxy_ips()




