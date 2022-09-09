import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from datetime import datetime


class HabrParser:
    def __init__(self):
        self.cur_time = datetime.now().strftime('%d_%m_%Y %H_%M_%S')

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
    _cards = []

    async def parse_card_to_dict(self, session, card_url):
        html = await session.get(url=card_url, headers=self.headers)
        bs = BeautifulSoup(await html.text(), 'lxml')

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

        self._cards.append(
            {
                'title': title,
                'link': link,
                'safe_deal': 'Присутствует' if safe_deal else 'Отсутствует',
                'price': price,
                'date_and_time': date_and_time,
                'description': description
            }
        )

    async def collect_data(self):
        self._cards = []
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

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.parse_card_to_dict(session, item_url)) for item_url in refs]
            await asyncio.gather(*tasks)

    async def parse_card_to_message(self, update_only=False):
        return await self.update() if update_only else await self.upgrade()

    async def update(self):
        self.old_data = []
        self.new_data = []
        await self.collect_data()
        self.old_data.extend(self._cards)

    async def upgrade(self):
        output_message_data = []
        await self.collect_data()
        cards = self._cards
        for card in cards:
            if card['link'] not in [item['link'] for item in self.old_data]:
                output_message_data.append(card)
                self.new_data.append(card)
            else:
                self.new_data.append(card)

        self.old_data = self.new_data.copy()
        self.new_data = []

        return output_message_data

    def update_time(self):
        from datetime import datetime
        self.cur_time = datetime.now().strftime('%d_%m_%Y %H_%M_%S')

    async def parse_card_to_file(self):
        await self.create_general_coroutine_with_files()
        return f'{self.cur_time}.csv'

    async def create_general_coroutine_with_files(self):
        from aiocsv import AsyncWriter
        import aiofiles

        self.update_time()
        async with aiofiles.open(f'{self.cur_time}.csv',
                                 'w',
                                 newline='',
                                 encoding='utf-8') as file:
            writer = AsyncWriter(file)

            await writer.writerow(
                [
                    'Название',
                    'Ссылка',
                    'Безопасная сделка',
                    'Цена',
                    'Дата и время размещения',
                    'Описание'
                ]
            )

            general_data = [*self.get_file_data()]

            for item in general_data:
                await writer.writerow(
                    [
                        item['title'],
                        item['link'],
                        item['safe_deal'],
                        item['price'],
                        item['date_and_time'],
                        item['description']
                    ]
                )
            print(f'[INFO] File {self.cur_time}.csv successfully written!')

    def get_file_data(self):
        return self.old_data


async def main():
    habr_parser = HabrParser()
    print(await habr_parser.parse_card_to_message(True))
    print(await habr_parser.parse_card_to_message())
    print(await habr_parser.parse_card_to_file())


if __name__ == '__main__':
    asyncio.run(main())
