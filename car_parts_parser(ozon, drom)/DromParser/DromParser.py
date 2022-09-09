from Parsers.parse_package.multypurpose_parser import ScrapSession


def get_info_cards(num_part):
    data = []
    session = ScrapSession()

    cards = session.render('https://baza.drom.ru/oem/'+num_part+'/', proxies=True).soup \
        .find_all('tr', class_='bull-item bull-item_inline -exact bull-item bull-item_inline')

    for card in cards:
        card_name = card.find('a', class_='bulletinLink bull-item__self-link auto-shy').text.strip()
        card_link = card.find('a', class_='bulletinLink bull-item__self-link auto-shy').get('href')
        card_city = card.find('span', class_='bull-delivery__city').text.strip()
        try:
            card_price = card.find('span', class_='price-block__price').text.strip()
        except AttributeError:
            try:
                card_price = card.find('span', class_='price-per-quantity__price').text.strip()
            except AttributeError:
                card_price = '-'
        data.append({
            'name': card_name,
            'link': card_link,
            'price': card_price,
            'info': card_city
        })
    return data


def main():
    data = get_info_cards('1660063G20')
    print(data)


if __name__ == '__main__':
    main()
