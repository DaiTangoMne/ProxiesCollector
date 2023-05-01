import requests
from config import http
from bs4 import BeautifulSoup
import base64
import random
import re
from fake_useragent import UserAgent

url = 'http://free-proxy.cz/ru/proxylist/main/'

ua = UserAgent()

headers = {
    "Accept-Language": "ru,en;q=0.9",
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
}


def get_ip(text) -> str:
    match = re.findall(r'"(.+?)"', text)[0]
    s = base64.standard_b64decode(match)
    return s.decode('utf-8')


def get_proxies_list(pages: int) -> list:
    proxies_list = []
    proxies = {
        'http': random.choice(http)
    }
    for i in range(1, pages + 1):
        print(f'page: {i}')
        f1 = 1
        while f1:
            try:
                # session.proxies = proxies
                html = session.get(url + str(i)).text
                soup = BeautifulSoup(html, 'lxml')
                table = soup.find('table', id='proxy_list')
                rows = table.find_all('tr')
                for row in rows[1:]:
                    try:
                        tds = row.find_all('td')
                        ip = get_ip(tds[0].find('script').text)
                        port = tds[1].find('span').text
                        protocol = tds[2].text.lower()
                        if protocol == 'https':
                            proxies_list.append({"https": f'{ip}:{port}'})
                        elif protocol == 'http':
                            proxies_list.append({"http": f'{ip}:{port}'})
                    except Exception:
                        pass
                f1 = 0
            except Exception as ex:
                # old = proxies['http']
                # proxies = {
                #     'http': random.choice(http)
                # }
                # print(f'{ex}\n'
                #       f'old: {old}; new: {proxies["http"]}')
                pass

        return proxies_list


def main():
    print(get_proxies_list(4))


if __name__ == '__main__':
    session = requests.session()
    session.headers = headers
    main()
