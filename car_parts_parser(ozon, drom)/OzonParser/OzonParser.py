import time

from Parsers.parse_package.multypurpose_parser import ScrapSession
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def f(driver) -> None:
    actions = ActionChains(driver)
    element = driver.find_element('xpath', "/html/body/div[1]/div/div[1]/div[2]/div[3]/h2")
    actions.click(on_element=element).send_keys(Keys.END)
    actions.perform()
    time.sleep(0.5)


def get_info_cards(num_part):
    data = []
    session = ScrapSession()
    cards = session.render('https://www.ozon.ru/highlight/autoparts/?autoarticle=' + num_part + '&brand=infiniti',
                           func=f) \
        .soup.find_all('div', class_='y8j jy9')

    for card in cards:
        card_name = card.find('span', class_='v2d d3v v3d v5d tsBodyL jx0').text.strip()
        try:
            card_price = card.find('span', class_='ui-o7 ui-p0 ui-p3').text.strip()
        except AttributeError:
            card_price = card.find('span', class_='ui-o7 ui-p0').text.strip()

        card_link = card.find('a', class_='tile-hover-target jx0').get('href')
        card_delivery = card.find('span', class_='v2d d3v v3d v6d tsBodyM jy2').text.strip()
        data.append({
            'name': card_name,
            'link': card_link,
            'price': card_price,
            'info': card_delivery
        })

    return data


def main():
    data = get_info_cards('1520800Q0F')
    print(data)


if __name__ == '__main__':
    main()
