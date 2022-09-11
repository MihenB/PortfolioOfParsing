from bs4 import BeautifulSoup
import pickle
# from pprint import pprint
# import time
# from selenium.webdriver import ActionChains
# from parse_package.multypurpose_parser import ScrapSession
# from Ad.config import url


# def click(driver):
#     actions = ActionChains(driver)
#     element = driver.find_element('xpath', "//html/body/div[2]/div/main/div[1]/div/div/div[2]/div[2]/div[2]/div["
#                                            "7]/div/div/a/span/span")
#     actions.click(on_element=element)
#     actions.perform()
#     time.sleep(3)


def get_data():
    # session = ScrapSession()
    services_dict = dict()
    group_title = None
    with open('index.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    soup = soup.find(class_='_16Pjigk').find_all('div')[1].find_all('tr')
    for item in soup:
        if 'price-list-item_top' in item['class']:
            group_title = item.find('td').text.strip()
            services_dict[group_title] = []
        elif 'price-list-item' in item['class'] and len(item['class']) == 1:
            services_dict[group_title].append(item.find('td').text.strip())
    with open('service_dict.pkl', 'wb') as file:
        pickle.dump(services_dict, file)


def main():
    get_data()


if __name__ == '__main__':
    main()
