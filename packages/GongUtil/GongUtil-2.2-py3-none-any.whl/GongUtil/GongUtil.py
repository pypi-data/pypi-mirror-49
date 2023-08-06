import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import traceback
import re
'''

获取代理ips  e: proxy_ips = Base.get_proxy_ips()
            e2: proxy_ips = Base.get_proxy_ips(page=5)  设置爬取规模，规模越大的越多
'''


class GetProxyIPs:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

        }
        self.original_proxy_ips = []
        self.proxy_ips = []
        self.base_url = 'https://www.xicidaili.com/nn/'
        self.base_second_url = 'http://www.89ip.cn/index_{page}.html'

    def set_original_proxy_ips(self, url):
        try:
            resp = requests.get(url=url, headers=self.headers)
            html = etree.HTML(resp.text)
            elements = html.xpath('//tr[@class="odd"]')
        except:
            return
            # traceback.print_exc()
        for element in elements:
            live_time = element.xpath('.//td[9]//text()')[0]
            if '天' in live_time:
                ip = element.xpath('.//td[2]//text()')[0]
                port = element.xpath('.//td[3]//text()')[0]
                http_class = element.xpath('.//td[6]//text()')[0]
                if 'HTTP' in http_class:
                    proxy_ip = http_class.lower() + '://' + ip + ':' + port
                    # proxy_ip = ip + ':' + port
                    self.original_proxy_ips.append(proxy_ip)

    def set_second_original_proxy_ips(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            html = etree.HTML(resp.text)
            elements = html.xpath('//table[@class="layui-table"]//tbody//tr')
            for element in elements:
                ip = element.xpath('.//td[1]//text()')[0]
                ip = re.sub('[\n \t]', '', ip)
                port = element.xpath('.//td[2]//text()')[0]
                port = re.sub('[\n \t]', '', port)
                proxy_ip = 'http://'+ip+':'+port
                # print(proxy_ip)
                self.original_proxy_ips.append(proxy_ip)
        except:
            if url == 'http://www.89ip.cn/index_1.html':
                print('由于使用代理次数过于频繁，请换个ip再使用本接口，ip被代理网站封了')

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
            # print(proxy_ip + '----', resp.elapsed.total_seconds())
            self.proxy_ips.append(proxy)
        except:
            # traceback.print_exc()
            pass

    def run(self, max_page):
        # self.original_proxy_ips('https://www.xicidaili.com/nn/')
        with ThreadPoolExecutor(max_workers=max_page) as pthread:
            for page in range(1, max_page):
                url = self.base_url + str(page)
                pthread.submit(self.set_original_proxy_ips, url)
        if len(self.original_proxy_ips) < max_page:
            print('正在爬取备用ip代理网站')
            with ThreadPoolExecutor(max_workers=max_page) as pthread:
                for page in range(1, max_page):
                    url = self.base_second_url.format(page=page)
                    pthread.submit(self.set_second_original_proxy_ips, url)
        # print(len(self.original_proxy_ips))
        ''' 测试ip可用性 '''
        with ThreadPoolExecutor(max_workers=30) as pthread:
            for proxy_ip in self.original_proxy_ips:
                pthread.submit(self.check_is_ip_alive, proxy_ip)
        print('可用ip数量')
        print(len(self.proxy_ips))


def get_proxy_ips(max_page=5):
    g = GetProxyIPs()
    g.run(max_page)
    return g.proxy_ips


if __name__ == '__main__':
    # get_proxy_ips()
    pass



