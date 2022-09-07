import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


class HabrParser:
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random,
    }

    main_url = 'https://freelance.habr.com'
    url = "https://freelance.habr.com/tasks"

    old_data = []
    new_data = []

    def parse_card_to_dict(self, card_url):
        html = requests.get(url=card_url, headers=self.headers).text
        bs = BeautifulSoup(html, 'lxml')

        title = re.sub(r'\n+', ' ', bs.find(class_='task__title').text).strip()

        link = card_url

        safe_deal = bool(bs.find(title='Безопасная сделка'))

        try:
            price = bs.find(class_="task__finance").find(class_='count').text
        except AttributeError:
            price = bs.find(class_='negotiated_price').text

        date_and_time = re.sub(r'\n+', ' ', bs.find(class_='task__meta').text).strip().replace('  ', ' ')

        def format_description(bs_obj):
            descript = re.sub(r'" rel="nofollow">.+?</a>', '', str(bs_obj))
            descript = descript.replace('<a href="', '')
            descript = descript.replace('<div class="task__description">\n', '')
            descript = descript.replace('\n</div>', '')
            descript = re.sub(r'<br/>', '\n', descript)
            descript = re.sub(r'<.+?>', '', descript)
            descript = re.sub(r'(\n){2,10}', '\n\n', descript)
            return descript

        try:
            description = format_description(bs.find(class_='task__description'))
        except Exception:
            description = 'Нет описания'

        return {
            'title': title,
            'link': link,
            'safe_deal': 'Присутствует' if safe_deal else 'Отсутствует',
            'price': price,
            'date_and_time': date_and_time,
            'description': description
        }

    def collect_data(self):
        page = 1
        filters = 'парсинг'

        params = {
            'page': f'{page}',
            'q': f'[{filters}]',
        }

        def get_soup(_params, _page):
            params.update(page=f'{page}')
            response = requests.get(headers=self.headers, url=self.url, params=params)
            return BeautifulSoup(response.text, 'lxml')

        soup = get_soup(params, page)

        total_orders = int(re.search(r'(\d+)', soup.find(class_='page-title').text)[0])

        items = []
        while len(items) != total_orders:
            items.extend(soup.find_all(class_='task task_list'))
            page += 1
            soup = get_soup(params, page)

        refs = [self.main_url + item.find(class_='task__title').find('a')['href'] for item in items]

        return [self.parse_card_to_dict(item_url) for item_url in refs]

    def parse_card_to_message(self, update_only=False):
        return self.update() if update_only else self.upgrade()

    def update(self):
        self.old_data = []
        self.new_data = []
        self.old_data.extend(self.collect_data())

    def upgrade(self):
        output_message_data = []

        cards = self.collect_data()
        for card in cards:
            if card['link'] not in [item['link'] for item in self.old_data]:
                output_message_data.append(card)
                self.new_data.append(card)
            else:
                self.new_data.append(card)

        self.old_data = self.new_data.copy()
        self.new_data = []

        return output_message_data

    def get_file_data(self):
        return self.old_data

    def parse_card_to_file(self):
        import datetime
        import csv

        cur_time = datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S')

        with open(f'{cur_time}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='excel')
            writer.writerow(
                [
                    'Название',
                    'Ссылка',
                    'Безопасная сделка',
                    'Цена',
                    'Дата и время размещения',
                    'Описание'
                ]
            )
            for item in self.old_data:
                writer.writerow(
                    [
                        item['title'],
                        item['link'],
                        item['safe_deal'],
                        item['price'],
                        item['date_and_time'],
                        item['description']
                    ]
                )
            print(f'[INFO] File {cur_time}.csv successfully written!')
            return f'{cur_time}.csv'


def main():
    habr_parser = HabrParser()
    print(habr_parser.parse_card_to_message(True))
    print(habr_parser.parse_card_to_message())
    print(habr_parser.parse_card_to_file())


if __name__ == '__main__':
    main()
