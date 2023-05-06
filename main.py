import requests
import base64
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import http
from random import choice

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
    for i in range(1, pages + 1):
        print(f'[ INFO ] page: {i}', end=' ')
        try:
            html = session.get(url + str(i)).text
            soup = BeautifulSoup(html, 'lxml')
            table = soup.find('table', id='proxy_list')
            rows = table.find_all('tr')
            l = len(proxies_list)
            for row in rows[1:]:
                try:
                    tds = row.find_all('td')
                    ip = get_ip(tds[0].find('script').text)
                    port = tds[1].find('span').text
                    protocol = tds[2].text.lower()
                    if protocol == 'https':
                        proxies_list.append({"https": f'{ip}:{port}', "http": ""})
                    elif protocol == 'http':
                        proxies_list.append({"http": f'{ip}:{port}', "https": ""})
                except Exception:
                    pass
            if len(proxies_list) > l:
                print('OK')
            else:
                print('ERROR')
        except Exception:
            print('ERROR')
    return proxies_list


def test_proxies(proxies_list) -> list:
    li = []
    urls = 'https://www.google.com/'
    url = 'http://povezlo.su/'
    for proxies in proxies_list:
        try:
            if proxies['https'] == "":
                response = requests.get(url, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    with open('http.txt', 'a') as file:
                        file.write(f"{proxies['http']}\n")
            else:
                response = requests.get(urls, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    with open('https.txt', 'a') as file:
                        file.write(f"{proxies['https']}\n")
            li.append(proxies)
            print(f'[ INFO ] {response.status_code}: {proxies}')
        except Exception:
            print(f'[ WARNING ] Bad proxies: {proxies}')
    return li


def main():
    # li = get_proxies_list(5)
    # print('[ INFO ] Proxies are collected')
    # print(test_proxies(li))
    li = []
    for item in http:
        li.append({"http": f'{item}', "https": ""})
    print(test_proxies(li))


if __name__ == '__main__':
    session = requests.session()
    session.headers = headers
    main()
