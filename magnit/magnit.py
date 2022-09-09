import requests
from bs4 import BeautifulSoup

def collect_data():
    cookies = {
        'PHPSESSID': 'qv3p335uvub5fab6jtdt2e732e',
        '_ga': 'GA1.2.1877116052.1659354542',
        '_gid': 'GA1.2.1691201019.1659354542',
        '_ym_uid': '1659354542542485556',
        '_ym_d': '1659354542',
        'BX_USER_ID': '02611974dc66359a3f2ae590f7e1529a',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        '_clck': '1bk8gdb|1|f3n|0',
        'mg_geo_id': '2425',
        '_clsk': '10ulc14|1659354573184|2|1|l.clarity.ms/collect',
        '_gat_UA-61230203-9': '1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'PHPSESSID=qv3p335uvub5fab6jtdt2e732e; _ga=GA1.2.1877116052.1659354542; _gid=GA1.2.1691201019.1659354542; _ym_uid=1659354542542485556; _ym_d=1659354542; BX_USER_ID=02611974dc66359a3f2ae590f7e1529a; _ym_isad=2; _ym_visorc=w; _clck=1bk8gdb|1|f3n|0; mg_geo_id=2425; _clsk=10ulc14|1659354573184|2|1|l.clarity.ms/collect; _gat_UA-61230203-9=1',
        'Pragma': 'no-cache',
        'Referer': 'https://magnit.ru/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://magnit.ru/promo/', cookies=cookies, headers=headers)
    #with open('magnit.html', 'w') as file:
    #    file.write(response.text)
    with open('magnit.html', 'r') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    cont = soup.find('div', class_='сatalogue__main js-promo-container')
    cards = cont.findAll('a', class_='card-sale card-sale_catalogue')
    for card in cards:
        title = card.find('div', class_='card-sale__title').text.strip()
        new_price_integer = card.find('div', class_='label__price label__price_new')\
            .find('span', class_='label__price-integer').text.strip()
        new_price_decimal = card.find('div', class_='label__price label__price_new')\
            .find('span', class_='label__price-decimal').text.strip()
        new_price = float(new_price_integer + '.' + new_price_decimal)
        print(title, new_price)


def main():
    collect_data()


if __name__ == '__main__':
    main()

