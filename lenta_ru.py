from pprint import pprint
from lxml import html
import requests
import re


class LentaRuParser:
    url = 'https://lenta.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    def parse(self):
        response = requests.get(self.url, headers=self.headers)
        dom = html.fromstring(response.text)
        news_items = dom.xpath("//a[contains(@class, '_topnews')]")

        news_list = []

        for item in news_items:
            title = item.xpath(".//h3/text() | .//span[contains(@class, 'card')]/text()")[0]

            link = self.url + item.xpath(".//@href")[0]

            if not re.match('.*?-(\d+)-(\d+)-(\d+).*', str(link)) is None:
                re_pattern = re.match('.*?-(\d+)-(\d+)-(\d+).*', str(link))
                publication_date = [re_pattern.group(1), re_pattern.group(2), re_pattern.group(3)]
                publication_date = '.'.join(publication_date)

            elif not re.match('.*?/(\d+)/(\d+)/(\d+).*', str(link)) is None:
                re_pattern = re.match('.*?/(\d+)/(\d+)/(\d+).*', str(link))
                publication_date = [re_pattern.group(3), re_pattern.group(2), re_pattern.group(1)]
                publication_date = '.'.join(publication_date)

            else:
                publication_date = None

            source = 'Lenta.ru'

            news = {
                '1. title': title,
                '2. link': link,
                '3. date': publication_date,
                '4. source': source
            }

            news_list.append(news)

        return news_list


if __name__ == '__main__':
    parser = LentaRuParser()
    full_news = parser.parse()
    pprint(full_news)
