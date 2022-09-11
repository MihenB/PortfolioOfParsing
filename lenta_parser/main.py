import csv
import datetime
import random

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


class ParseLent:
    _cur_time = None

    def __init__(self, url=''):
        self.url = url
        self.end_page = self.get_end_page()
        self.data = []
        ParseLent._cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    def make_request(self, current_page: int):
        url_page = f'?page='
        ua = UserAgent()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': ua.random
        }
        cookies = {
            'CityCookie': 'spb',
            'Store': '0012'
        }
        return requests.get(url=self.url + url_page + str(current_page), headers=headers, cookies=cookies)

    def get_end_page(self) -> int:
        soup = BeautifulSoup(self.make_request(1).text, 'lxml')
        li_next = str(soup.find('li', {'class': 'next'}).getText)
        end_page = int(re.search(r'rel="1 == \d+', li_next)[0].split('==')[1].strip())
        return end_page

    @staticmethod
    def parse_card(card) -> list:
        title = card.find('div', {'class': 'sku-card-small-header__title'}).get_text(strip=True)

        old_price_item = card.find('div', {'class': 'sku-card-small-prices__item sku-card-small-prices__item--regular'})
        old_price_integer = old_price_item \
            .find('span', {'class': 'price-label__integer'}) \
            .get_text(strip=True) \
            .replace(u'\xa0', ' ')
        old_price_decimal = old_price_item.find('small', {'class': 'price-label__fraction'}).get_text(strip=True)
        old_price = f'{old_price_integer}.{old_price_decimal}'

        new_price_item = card.find('div', {'class': 'sku-card-small-prices__item sku-card-small-prices__item--primary'})
        new_price_integer = new_price_item \
            .find('span', {'class': 'price-label__integer'}) \
            .get_text(strip=True) \
            .replace(u'\xa0', ' ')
        new_price_decimal = new_price_item.find('small', {'class': 'price-label__fraction'}).get_text(strip=True)
        new_price = f'{new_price_integer}.{new_price_decimal}'

        try:
            discount = card.find('div', {'class': 'discount-label-small discount-label-small--sku-card '
                                                  'sku-card-small__discount-label'}).get_text(strip=True)
        except AttributeError:
            discount = f'{round((1 - int(new_price_integer.replace(" ", "")) / int(old_price_integer.replace(" ", ""))) * 100)}%'

        image_ref_pattern = re.compile(r'src=".+"')
        picture = str(card.find('div', {'class': 'square__inner'}).getText)
        image_ref = image_ref_pattern.search(picture)[0].replace('"', '')[4:]

        return [title,
                old_price,
                new_price,
                discount,
                image_ref]

    def parse_page(self, current_page: int) -> None:
        soup = BeautifulSoup(self.make_request(current_page).text, 'lxml')
        cards = soup.find_all('div', {'class': 'sku-card-small-container'})
        for card in cards:
            self.data.append(self.parse_card(card))

    def get_data(self) -> str:
        with open(f'log_file_{ParseLent._cur_time}.txt', 'w') as log_file:
            log_file.write('Pages skipped:\n')

            loading = 0
            print('Loading:\n#', end='')

            for current_page in range(1, self.end_page + 1):

                current_condition = int(current_page / self.end_page * 100)
                loading_line = '#' if loading != current_condition else ''
                loading = current_condition
                print(loading_line, end='')

                try:
                    self.parse_page(current_page)
                except requests.exceptions.ConnectionError:
                    log_file.write(f'{current_page}\n')
                    continue
            return self.write_data_to_file()

    def write_data_to_file(self, name_of_file='') -> str:

        with open(
                f'ЛЕНТА_{name_of_file}_{ParseLent._cur_time}.csv',
                'w',
                encoding='utf-8',
                newline=''
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    'Продукт',
                    'Старая цена',
                    'Новая цена',
                    'Процент скидки',
                    'Ссылка на изображение',
                ]
            )
            writer.writerows(
                self.data
            )

        return f'Файл ЛЕНТА_{name_of_file}_{ParseLent._cur_time}.csv успешно записан!'


if __name__ == '__main__':
    my_parser = ParseLent(url='https://lenta.com/promo/')
    name = my_parser.get_data()