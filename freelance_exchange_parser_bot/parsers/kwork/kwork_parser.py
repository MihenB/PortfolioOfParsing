import re
import requests
from bs4 import BeautifulSoup


# class KWorkParser


old_data = []
new_data = []

cookies = {
    '_kmid': 'b63abb71fdcfa8202ac7217c720e9f96',
    '_kmfvt': '1659029404',
    'referrer_url': 'https%3A%2F%2Fkwork.ru%2Fprojects%3Fc%3D41%26attr%3D211',
    'site_version': 'desktop',
    'RORSSQIHEK': 'e579a6d645f0400395e6aac477ec2dbd',
    '_gcl_au': '1.1.633594093.1659029409',
    '_ga': 'GA1.2.1120050506.1659029409',
    '_gid': 'GA1.2.1372217572.1659029409',
    '_ym_uid': '1659016688889541339',
    '_ym_d': '1659029409',
    'isFacebookAvailable': 'false',
    'yandex_client_id': '1659016688889541339',
    '_ym_isad': '1',
    '_sp_ses.b695': '*',
    'google_client_id': '1120050506.1659029409',
    'uad': '1308823762e2c7c66063d950379270',
    'userId': '13088237',
    'slrememberme': '13088237_%242y%2410%24hj6O9rwwPj9t3FAE8FTyyuYVkLoYJ7rQ065tdj%2FlMAvpbvz0sNxUq',
    '_kmwl': '1',
    'show_mobile_app_banner_date': '1',
    '_ubtcuid': 'cl65bb67500004bf2ihbdihrh',
    '_sp_id.b695': '9134f199-8aab-40ab-9489-7d6e788d0499.1659029410.1.1659029758.1659029410.2b60caf9-26c0-4667-bbb7-971e3011ae37',
    '_gali': 'price-to',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_kmid=b63abb71fdcfa8202ac7217c720e9f96; _kmfvt=1659029404; referrer_url=https%3A%2F%2Fkwork.ru%2Fprojects%3Fc%3D41%26attr%3D211; site_version=desktop; RORSSQIHEK=e579a6d645f0400395e6aac477ec2dbd; _gcl_au=1.1.633594093.1659029409; _ga=GA1.2.1120050506.1659029409; _gid=GA1.2.1372217572.1659029409; _ym_uid=1659016688889541339; _ym_d=1659029409; isFacebookAvailable=false; yandex_client_id=1659016688889541339; _ym_isad=1; _sp_ses.b695=*; google_client_id=1120050506.1659029409; uad=1308823762e2c7c66063d950379270; userId=13088237; slrememberme=13088237_%242y%2410%24hj6O9rwwPj9t3FAE8FTyyuYVkLoYJ7rQ065tdj%2FlMAvpbvz0sNxUq; _kmwl=1; show_mobile_app_banner_date=1; _ubtcuid=cl65bb67500004bf2ihbdihrh; _sp_id.b695=9134f199-8aab-40ab-9489-7d6e788d0499.1659029410.1.1659029758.1659029410.2b60caf9-26c0-4667-bbb7-971e3011ae37; _gali=price-to',
    'Origin': 'https://kwork.ru',
    'Referer': 'https://kwork.ru/projects?c=41&attr=211&price-from=0&price-to=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.806 Yowser/2.5 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'c': '41',
    'attr': '211',
    'page': f'{1}',
}


def parse_card_to_dict(soup):
    title_with_href = soup.find(class_='wants-card__header-title first-letter breakwords pr250').find('a')

    title = title_with_href.text.strip()

    link = title_with_href['href'].strip()

    safe_deal = True  # на KWork все сделки идут через их собственную систему

    joint_price = soup.find(class_='wants-card__right m-hidden')

    price = f'{joint_price.find(class_="wants-card__header-price wants-card__price m-hidden").text.strip()}\n' \
            f'{joint_price.find(class_="wants-card__description-higher-price").text.strip()}'

    date_and_time = re.sub(r'\n+', ' ', soup.find(class_='query-item__info-wrap')
                           .find(class_='force-font force-font--s12').text).strip().replace('    ', ' - ')

    def format_description(bs_obj):
        descript = str(bs_obj).replace('<div class="breakwords first-letter js-want-block-toggle '
                                       'js-want-block-toggle-full hidden"><div class="wants-card__space"></div>', '')
        descript = re.sub(r'<a class="js-want-link-toggle-desc link_local" href="javascript:void\(0\);">Скрыть</a>',
                          '',
                          descript)
        descript = re.sub(r'(" rel="nofollow noopener)?" target="_blank">(.+?</a>)?',
                          '',
                          descript)
        descript = re.sub(r'<a( class=".+?")? href="',
                          '',
                          descript)
        descript = re.sub(r'<br/>',
                          '\n',
                          descript)
        descript = re.sub(r'<.+?>',
                          '',
                          descript)
        descript = re.sub(r'(\n){2,10}',
                          '\n\n',
                          descript)
        return descript

    description = format_description(
        soup.find('div', class_='breakwords first-letter js-want-block-toggle js-want-block-toggle-full hidden')
    )

    return {
        'title': title.replace(' ', ' '),
        'link': link.replace(' ', ' '),
        'safe_deal': 'Присутствует' if safe_deal else 'Отсутствует',
        'price': price.replace(' ', ' '),
        'date_and_time': date_and_time.replace(' ', ' '),
        'description': description.replace(' ', ' ')
    }


def collect_data():
    page = 1
    data.update(page=f'{page}')
    response_html = requests.post('https://kwork.ru/projects',
                                  cookies=cookies,
                                  headers=headers,
                                  data=data).json()['data']['html']
    soup = BeautifulSoup(response_html, 'lxml')
    global old_data, new_data
    cards = []
    while soup.find('a', class_='next'):
        page += 1
        data.update(page=f'{page}')
        cards.extend(soup.find_all(class_='card__content pb5'))
        response_html = requests.post('https://kwork.ru/projects',
                                      cookies=cookies,
                                      headers=headers,
                                      data=data).json()['data']['html']
        soup = BeautifulSoup(response_html, 'lxml')
    else:
        cards.extend(soup.find_all(class_='card__content pb5'))

    return [parse_card_to_dict(card) for card in cards]


def parse_card_to_message(update_only=False):
    return update() if update_only else upgrade()


def update():
    global old_data, new_data
    old_data = []
    new_data = []
    old_data.extend(collect_data())


def upgrade():
    output_message_data = []
    global old_data, new_data
    cards = collect_data()

    for card in cards:
        if card not in old_data:
            output_message_data.append(card)
            new_data.append(card)
        else:
            new_data.append(card)

    old_data = new_data.copy()
    new_data = []

    return output_message_data


def parse_card_to_file():
    import datetime
    import csv

    cur_time = datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S')

    with open(f'{cur_time}_kwork.csv', 'w', newline='', encoding='utf-8') as file:
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
        for item in old_data:
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
        print(f'[INFO] File {cur_time}_kwork.csv successfully written!')
        return f'{cur_time}_kwork.csv'


def main():
    print(parse_card_to_message(True))
    print(parse_card_to_message())
    print(parse_card_to_file())


if __name__ == '__main__':
    main()
