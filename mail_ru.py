from pprint import pprint
from lxml import html
import requests
import re


class MailRuParser:
    url = 'https://news.mail.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    def parse(self):
        response = requests.get(self.url, headers=self.headers)
        dom = html.fromstring(response.text)
        news_elements = dom.xpath("//div[contains(@class, 'daynews__item')]")

        news_list = []

        for element in news_elements:
            title = element.xpath(".//text()")[0].replace('\xa0', ' ').replace('\r\n', '')
            link = element.xpath("./a/@href")[0]

            response = requests.get(link, headers=self.headers)
            dom = html.fromstring(response.text)

            publication_date = dom.xpath("//span[@datetime]/@datetime")[0]
            re_pattern = re.match('.*?(\d+)-(\d+)-(\d+).*', publication_date)
            publication_date = [re_pattern.group(3), re_pattern.group(2), re_pattern.group(1)]
            publication_date = '.'.join(publication_date)

            source = dom.xpath("//a[contains(@class,'breadcrumbs__link')]//text()")[0]

            news = {
                '1. title': title,
                '2. link': link,
                '3. date': publication_date,
                '4. source': source
            }

            news_list.append(news)

        return news_list


if __name__ == '__main__':
    parser = MailRuParser()
    full_news = parser.parse()
    pprint(full_news)
