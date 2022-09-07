import json
from parse_package.multypurpose_parser import ScrapSession
from config_yamap import cookies, headers


def write_to_json(data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open('result_data.json', 'w') as file:
        file.write(json_data)


def get_session():
    return ScrapSession()


def get_reviews_data(url):
    reviews_result_data = []
    url = url + 'reviews/'
    reviews_session = get_session()
    reviews_response = reviews_session.get(url=url, cookies=cookies, headers=headers, secured=True)
    reviews_soup = reviews_response.soup
    reviews = reviews_soup.find_all('div', class_='business-reviews-card-view__review')
    for review in reviews:
        try:
            name = review.find('span', itemprop='name').text.strip()
        except AttributeError:
            name = 'Name missing'
        try:
            text = review.find('span', class_='business-review-view__body-text').text.strip()
        except AttributeError:
            text = 'Review missing'
        reviews_result_data.append({
            'name': name,
            'text': text
        })
    return reviews_result_data


def get_photos_links(url):
    result_photos_links = []
    url += 'gallery/'
    photos_session = ScrapSession()
    response = photos_session.render(url, secured=True)
    photos_soup = response.soup
    photos = photos_soup.find_all(class_='photo-wrapper__photo')
    for photo in photos:
        try:
            photo_link = photo.get('src')
        except AttributeError:
            photo_link = 'Photo link missing'
        result_photos_links.append({
            'photo_link': photo_link
        })
    return result_photos_links


def get_all_snippets(url):
    page = 0
    cards_pages = []
    try:
        while True:
            page += 1
            params = {
                'll': '82.920430,55.030199',
                'page': page,
                'sll': '82.920430,55.030199',
                'sspn': '0.361176,0.117142',
                'z': '12',
            }
            session = get_session()
            response = session.get(url=url, params=params, cookies=cookies, headers=headers, secured=True)
            soup = response.soup
            soup.find('li', class_='search-snippet-view').find('div', class_='search-business-snippet-view__title') \
                .text.strip()
            cards_pages += soup.find_all('li', class_='search-snippet-view')
    except AttributeError:
        return cards_pages


def get_formatted_data(snippets):
    data = []
    for snippet in snippets:
        title = snippet.find('div', class_='search-business-snippet-view__title').text.strip()
        address = snippet.find('div', class_='search-business-snippet-view__address').text.strip()
        snippet_link = 'https://yandex.ru' + \
                       snippet.find('a', class_='search-snippet-view__link-overlay _focusable').get('href')
        reviews = get_reviews_data(snippet_link)
        photos = get_photos_links(snippet_link)
        data.append({
            'title': title,
            'address': address,
            'reviews': reviews,
            'photos_links': photos
        })
    return data


def main():
    snippets = get_all_snippets('https://yandex.ru/maps/65/novosibirsk/category/theater/184105872/')
    data = get_formatted_data(snippets)
    write_to_json(data)


if __name__ == '__main__':
    main()
