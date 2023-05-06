import requests
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    "Accept-Language": "ru,en;q=0.9",
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
}

url = 'http://free-proxy.cz/ru/'

proxies = {
            'http': '80.90.143.254:8080'
        }
try:
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response.status_code)
except Exception as ex:
    print(ex)