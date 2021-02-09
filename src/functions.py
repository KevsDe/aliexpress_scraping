import bs4
import lxml
import re
from selenium import webdriver
import pandas as pd

def web_scrapping_extraction(url, title, price, shipping, sales):
    dictionary = []
    for x in range(0, len(url)):
        information = {
            "url": url[x],
            "title": title[x],
            "price": price[x],
            "shipping": shipping[x],
            "sales": sales[x]
            }

        dictionary.append(information)

    return dictionary


def aliexpress_single_scraping(url):
        print('Scraping page 1')
        driver = webdriver.Safari()
        link = url + str(1)
        driver.get(link)
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        text = soup.find_all('script', type='text/javascript')
        text_string = (str(text))
        url_search = re.findall(r"es\.aliexpress\.com/item/\d*\.html", text_string, re.IGNORECASE)
        title_search = re.findall(r'},"title":"([\s\S]*?)",', text_string, re.IGNORECASE)
        price_scraping = re.findall(r'formattedPrice":"€ \d*,\d*', text_string, re.IGNORECASE)
        price_search = [re.findall(r'\d*,\d*', x, re.IGNORECASE) for x in price_scraping]
        price_search = [x for y in price_search for x in y]
        text_segment = re.findall(r'storeUrl(.*?)formattedPrice', text_string, re.IGNORECASE)
        shipping_search = []
        for x in text_segment:
            if re.search(r'Envío gratis', x, re.IGNORECASE) != None:
                shipping_search.append(0)
            elif re.search(r'€(.*?),\d\d', x, re.IGNORECASE) != None:
                word = re.search(r'€(.*?),\d\d', x, re.IGNORECASE).group(0).replace('€ ', '')
                shipping_search.append(word)
            else:
                shipping_search.append('Not shipping method found')
        sales_search = []
        for x in text_segment:
            if re.search(r'tradeDesc(.*?)\d ', x, re.IGNORECASE) != None:
                word = re.search(r'tradeDesc(.*?)\d ', x, re.IGNORECASE).group(0).replace('tradeDesc":"', '').rstrip()
                sales_search.append(word)
            else:
                sales_search.append('Not sales found')
        driver.quit()
        information = web_scrapping_extraction(url_search, title_search, price_search, shipping_search,
                                                    sales_search)
        df = pd.DataFrame(information)
        return df


def aliexpress_multiple_scraping (url, page):
    full_df = aliexpress_single_scraping(url+str(1))
    for x in range(2, page+1):
        print(f'Scraping page {x}')
        driver = webdriver.Safari()
        link = url + str(x)
        driver.get(link)
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        text = soup.find_all('script', type='text/javascript')
        text_string = (str(text))
        url_search = re.findall(r"es\.aliexpress\.com/item/\d*\.html", text_string, re.IGNORECASE)
        title_search = re.findall(r'},"title":"([\s\S]*?)",', text_string, re.IGNORECASE)
        price_scraping = re.findall(r'formattedPrice":"€ \d*,\d*', text_string, re.IGNORECASE)
        price_search = [re.findall(r'\d*,\d*', x, re.IGNORECASE) for x in price_scraping]
        price_search = [x for y in price_search for x in y]
        text_segment = re.findall(r'storeUrl(.*?)formattedPrice', text_string, re.IGNORECASE)
        shipping_search = []
        for x in text_segment:
            if re.search(r'Envío gratis', x, re.IGNORECASE) != None:
                shipping_search.append(0)
            elif re.search(r'€(.*?),\d\d', x, re.IGNORECASE) != None:
                word = re.search(r'€(.*?),\d\d', x, re.IGNORECASE).group(0).replace('€ ', '')
                shipping_search.append(word)
            else:
                shipping_search.append('Not shipping method found')
        sales_search = []
        for x in text_segment:
            if re.search(r'tradeDesc(.*?)\d ', x, re.IGNORECASE) != None:
                word = re.search(r'tradeDesc(.*?)\d ', x, re.IGNORECASE).group(0).replace('tradeDesc":"', '').rstrip()
                sales_search.append(word)
            else:
                sales_search.append('Not sales found')
        driver.quit()
        information = web_scrapping_extraction(url_search, title_search, price_search, shipping_search,
                                                    sales_search)
        df = pd.DataFrame(information)
        full_df = full_df.append(df)
    return full_df


