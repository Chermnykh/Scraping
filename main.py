from pymongo import MongoClient
from pprint import pprint
from lenta_ru import LentaRuParser
from mail_ru import MailRuParser
from yandex_ru import YandexRuParser

client = MongoClient('127.0.0.1', 27017)
db = client['news']

full_news = LentaRuParser().parse()
full_news += YandexRuParser().parse()
full_news += MailRuParser().parse()


db.news.insert_many(full_news)
