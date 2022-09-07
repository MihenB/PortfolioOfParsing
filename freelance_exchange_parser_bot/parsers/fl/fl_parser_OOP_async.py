import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup


class FlParser:

    old_data = []
    new_data = []
    _cards = []
    cookies = {
        '__ddg1_': 'lIO0PA6BVZY7f0PeAmnk',
        'PHPSESSID': 'd30f161d56409587e2d558bfc1ed33a0',
        'new_pf0': '1',
        'new_pf10': '1',
        'hidetopprjlenta': '0',
        '_tm_lt_sid': '1658988047858.296898',
        '_ym_uid': '1658988049965280990',
        '_ym_d': '1658988049',
        '_ga': 'GA1.2.1671831563.1658988049',
        '_gid': 'GA1.2.775792834.1658988049',
        '_ga_cid': '1671831563.1658988049',
        'mindboxDeviceUUID': 'a1769ead-5847-4cd6-9088-c94037f78647',
        'directCrm-session': '%7B%22deviceGuid%22%3A%22a1769ead-5847-4cd6-9088-c94037f78647%22%7D',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        'uechat_3_first_time': '1658988049689',
        'uechat_3_disabled': 'true',
        'new_pf0': '1',
        'cookies_accepted': '1',
        'uechat_3_mode': '0',
        'uechat_3_pages_count': '2',
    }

    headers = {
        'authority': 'www.fl.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__ddg1_=lIO0PA6BVZY7f0PeAmnk; PHPSESSID=d30f161d56409587e2d558bfc1ed33a0; new_pf0=1; new_pf10=1; hidetopprjlenta=0; _tm_lt_sid=1658988047858.296898; _ym_uid=1658988049965280990; _ym_d=1658988049; _ga=GA1.2.1671831563.1658988049; _gid=GA1.2.775792834.1658988049; _ga_cid=1671831563.1658988049; mindboxDeviceUUID=a1769ead-5847-4cd6-9088-c94037f78647; directCrm-session=%7B%22deviceGuid%22%3A%22a1769ead-5847-4cd6-9088-c94037f78647%22%7D; _ym_isad=2; _ym_visorc=w; uechat_3_first_time=1658988049689; uechat_3_disabled=true; new_pf0=1; cookies_accepted=1; uechat_3_mode=0; uechat_3_pages_count=2',
        'referer': 'https://www.fl.ru/projects/?kind=1',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    params = {
        'kind': '1',
    }
    # Пагинация осуществляется через params,
    # которые отвечают за подстановку к основному url части &kind=1 и &page=1,
    # т.е. необходимости прописывать их вручную нет: + str(page_num) + '&kind=1'

    async def parse_card_to_dict(self, session, card_link):
        response_card = await session.get('https://www.fl.ru/' + card_link, headers=self.headers)
        soup_card = BeautifulSoup(await response_card.text(), 'lxml')

        title_card = soup_card.find(class_='b-page__title').text.strip()
        try:
            soup_card.find(class_='b-layout__txt_fontsize_12 b-layout__txt_bold '
                                  'b-layout__txt_color_1da409 b-layout__txt_padright_5 '
                                  'b-layout__txt_text_decor_none').text.strip()
            safety_deal_status = 'Присутствует'
        except AttributeError:
            safety_deal_status = 'Отсутсвует'
        price = soup_card.find('span', class_='b-layout__bold').text.strip()
        description = soup_card.find('div', class_='b-layout__txt b-layout__txt_padbot_20').text.strip()
        date_and_time = soup_card.find('div', class_='b-layout__txt b-layout__txt_padbot_30') \
            .find('div', class_='b-layout__txt b-layout__txt_fontsize_11').text.strip().replace(' ', '')
        date_and_time = date_and_time[:16]
        link = 'https://www.fl.ru/' + card_link

        self._cards.append({
            'title': title_card,
            'safe_deal': safety_deal_status,
            'price': price,
            'date_and_time': date_and_time,
            'description': description,
            'link': link
        })

    async def collect_data(self):
        self._cards = []
        async with aiohttp.ClientSession() as session:
            for page_num in range(1, 10):

                response = requests.get('https://www.fl.ru/projects/?page=' + str(page_num) + '&kind=1',
                                        params=self.params,
                                        cookies=self.cookies,
                                        headers=self.headers)
                soup = BeautifulSoup(response.text, 'lxml')
                try:
                    soup.find('h1', class_='b-layout__txt b-layout__txt_fontsize_90 b-layout__txt_color_646464 '
                                           'b-layout__txt_bold b-layout__txt_lineheight_1').text.strip()
                    break
                except AttributeError:
                    # Версия метода findAll() больше не используется. На данный момент актуальна версия find_all()
                    cards_urls = [card.find('a').get('href') for card in soup.find_all('div', class_='b-post__grid')]

                    tasks = [asyncio.create_task(self.parse_card_to_dict(session, item_url)) for item_url in cards_urls]

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
    fl_parser = FlParser()
    print(await fl_parser.parse_card_to_message(True))
    print(await fl_parser.parse_card_to_message())
    print(await fl_parser.parse_card_to_file())


if __name__ == '__main__':
    asyncio.run(main())
