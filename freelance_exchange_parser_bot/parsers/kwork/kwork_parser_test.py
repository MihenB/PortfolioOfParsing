import re
import requests
from bs4 import BeautifulSoup

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
        'title': title,
        'link': link,
        'safe_deal': 'Присутствует' if safe_deal else 'Отсутствует',
        'price': price,
        'date_and_time': date_and_time,
        'description': description
    }

# Перед запуском нужно удалить тег <a> из index.html, который содержит next, иначе программа уйдет в
# бесконечный цикл: while soup.find('a', class_='next'):
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
    if update_only:
        update()
    else:
        return upgrade()


def update():
    old_data.extend(collect_data_test())


def upgrade():
    output_message_data = []
    global old_data, new_data
    cards = collect_data_test()

    for card in cards:
        if card['title'] not in [item['title'] for item in old_data]:
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
        print(f'[INFO] File parsers/{cur_time}_kwork.csv successfully written!')
        return f'parsers/{cur_time}_kwork.csv'


def create_test_file():
    response_html = requests.post('https://kwork.ru/projects',
                                  cookies=cookies,
                                  headers=headers,
                                  data=data).json()['data']['html']
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(response_html)


def collect_data_test():
    page = 1
    data.update(page=f'{page}')
    # response_html = requests.post('https://kwork.ru/projects',
    #                               cookies=cookies,
    #                               headers=headers,
    #                               data=data).json()['data']['html']
    with open('index.html', 'r', encoding='utf-8') as file:
        response_html = file.read()
    soup = BeautifulSoup(response_html, 'lxml')
    global old_data, new_data
    cards = []
    while soup.find('a', class_='next'):
        # page += 1
        # data.update(page=f'{page}')
        cards.extend(soup.find_all(class_='card__content pb5'))
        # response_html = requests.post('https://kwork.ru/projects',
        #                               cookies=cookies,
        #                               headers=headers,
        #                               data=data).json()['data']['html']
        soup = BeautifulSoup(response_html, 'lxml')
    else:
        cards.extend(soup.find_all(class_='card__content pb5'))

    return [parse_card_to_dict(card) for card in cards]


def injection():
    with open('index.html', 'a', encoding='utf-8') as file:
        file.write(
            """
<div class="card want-card js-card-1737080 js-want-container js-viewed" data-id="1737080">
  <div class="card__content pb5">
    <div class="mb15">
      <div class="d-flex relative">
        <div class="wants-card__left">
          <div class="wants-card__header-title first-letter breakwords pr250">
            <a href="https://kwork.ru/projects/1737080">Моя карточка</a>
          </div>
          <div class="wants-card__description-text br-with-lh">
            <div class="breakwords first-letter js-want-block-toggle js-want-block-toggle-summary">
              <div class="wants-card__space"></div>Задача для тех, кто крут <br /> Нужно найти и...&nbsp; <a href="javascript:void(0);" class="js-want-link-toggle-desc link_local">Показать полностью</a>
            </div>
            <div class="breakwords first-letter js-want-block-toggle js-want-block-toggle-full hidden">
              <div class="wants-card__space"></div>Задача для тех, кто чертовски хорош собой (и как программист, конечно)<br /><a href="javascript:void(0);" class="js-want-link-toggle-desc link_local">Скрыть</a>
            </div>
          </div>
        </div>
        <div class="wants-card__right m-hidden">
          <div class="wants-card__header-right-block">
            <div class="wants-card__header-controls projects-list__icons">
              <div class="wants-card__header-price wants-card__price m-hidden">
                <span class="fs12">Желаемый бюджет: до</span> 1 000 000&nbsp; <span class="rouble">₽</span>
              </div>
            </div>
          </div>
          <div class="wants-card__description-higher-price">Допустимый: <span class="nowrap">до 20 000 000&nbsp; <span class="rouble">₽</span>
            </span>
            <span class="kwork-icon icon-custom-help tooltipster" data-tooltip-text="Покупатель готов рассмотреть предложения с ценой выше его желаемого бюджета, если у исполнителя высокий уровень профессионализма."></span>
          </div>
        </div>
      </div>
      <div class="m-visible">
        <div class="wants-card__header-price wants-card__price mt10">
          <span class="fs12">Желаемый бюджет: до</span> 1 000 000&nbsp; <span class="rouble">₽</span>
        </div>
        <div class="wants-card__description-higher-price">Допустимый: <span class="nowrap">до 20 000 000&nbsp; <span class="rouble">₽</span>
          </span>
          <span class="kwork-icon icon-custom-help tooltipster" data-tooltip-text="Покупатель готов рассмотреть предложения с ценой выше его желаемого бюджета, если у исполнителя высокий уровень профессионализма."></span>
        </div>
      </div>
    </div>
    <div class="mb10 want-payer-statistic d-flex">
      <span class="user-avatar user-avatar-image s65 user-avatar-square js-user-avatar_block ">
        <span class="user-avatar__default" style="background: #7bc862;">k</span>
      </span>
      <div class="dib v-align-t ml10">
        <div>
          <div class="dib"> Покупатель: <a class="v-align-t" href="https://kwork.ru/user/krutsmedia">krutsmedia</a>&nbsp; </div>
        </div>
        <div class="dib v-align-t"> Размещено проектов на бирже: 2 <br>
        </div>
      </div>
    </div>
    <div class="query-item__info-wrap">
      <div class="query-item__info">
        <div class="force-font force-font--s12">
          <span>Осталось: 1 д. 23 ч. &nbsp;&nbsp;&nbsp;</span>
          <span>Предложений:&nbsp;0</span>
        </div>
      </div>
      <div class="query-item__bottom">
        <div class="query-item__bottom-review force-font force-font--s14 nowrap m-wMax">
          <button class="m-wMax kw-button kw-button--green-border kw-button--size-32 js-open-modal-review" data-project="1737080" data-edit-review="">Отправить отзыв</button>
        </div>
        <div class="query-item__bottom-seen force-font force-font--s11 query-seen_block  mr10">
          <img src="https://cdn.kwork.com/images/ico-galka-green.png" alt="" />
          <span>ПРОСМОТРЕНО</span>
        </div>
        <div class="query-item__bottom-offer force-font force-font--s14 nowrap m-wMax">
          <a class="m-wMax kw-button--size-mobile-40  kw-button kw-button--green kw-button--size-32 projects-offer-btn js-projects-offer-btn  js-send-notification" href="https://kwork.ru/new_offer?project=1737080">Предложить услугу</a>
        </div>
      </div>
    </div>
  </div>
</div>
            """
        )


def main():
    # create_test_file()
    parse_card_to_message(update_only=True)
    print(f'BEFORE INJECTION: {old_data}')
    injection()
    print(f'AFTER INJECTION_MESSAGE: {parse_card_to_message()}')
    print(f'AFTER INJECTION_FILE: {parse_card_to_file()}')


if __name__ == '__main__':
    main()
