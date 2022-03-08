from pprint import pprint
from lxml import html
import requests
import re


class YandexRuParser:
    url = 'https://yandex.ru/news'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    def parse(self):
        response = requests.get(self.url, headers=self.headers)
        dom = html.fromstring(response.text)
        news_items = dom.xpath("//div[contains(@class, 'news-app__top')]/div")

        news_list = []

        for item in news_items:
            title = item.xpath(".//h2//text()")[0]
            link = item.xpath(".//span[contains(@class, 'source__source')]//@href")[0]

            publication_date = item.xpath(".//span[contains(@class, 'source__time')]/text()")[0]

            source = item.xpath(".//a[contains(@class, 'source-link')]/text()")[0]

            news = {
                '1. title': title.replace('\xa0', ' '),
                '2. link': link,
                '3. date': publication_date,
                '4. source': source
            }

            news_list.append(news)

        return news_list


if __name__ == '__main__':
    parser = YandexRuParser()
    full_news = parser.parse()
    pprint(full_news)
