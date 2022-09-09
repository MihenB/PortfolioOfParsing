import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

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

hour_urls = []
day_urls = []


def fill_lists_with_urls(url):
    page = 0
    filters = 'парсинг'

    global hour_urls, day_urls

    hour_urls = []
    day_urls = []

    params = {
        'page': f'{page}',
        'q': f'[{filters}]',
    }

    is_last_page = False

    while not is_last_page:
        params.update(page=f'{page + 1}')
        response = requests.get(headers=headers, url=url, params=params)
        bs = BeautifulSoup(response.text, 'lxml')
        bs = bs.find(id='tasks_list')

        for header in bs.find_all(class_='task__header'):
            time = " ".join(
                header.find(class_='params__published-at icon_task_publish_at').text.replace('~', '').split()[:2]
            )

            if re.search('дн|день', time):
                is_last_page = True
                break
            elif re.search('мин', time):
                card_url = main_url + header.find(class_='task__title').find('a')['href']
                hour_urls.append(card_url)
                day_urls.append(card_url)
            else:
                day_urls.append(main_url + header.find(class_='task__title').find('a')['href'])


def parse_card_to_dict(html, card_url):
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


def parse_cards_to_message():
    fill_lists_with_urls("https://freelance.habr.com/tasks")
    global hour_urls
    return [parse_card_to_dict(requests.get(url=url, headers=headers).text, url) for url in hour_urls]


def parse_cards_to_file():
    import datetime
    import csv

    fill_lists_with_urls("https://freelance.habr.com/tasks")
    global day_urls
    data = []
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S')
    counter = 0

    for url in day_urls:
        data.append(parse_card_to_dict(requests.get(url=url, headers=headers).text, url))
        counter += 1
        print(f'[INFO] Requested {counter} page(s)/card(s)')

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
        for item in data:
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
    # parse_card_to_file()
    dict_with_data = parse_cards_to_message()
    print(dict_with_data)


if __name__ == '__main__':
    main()
