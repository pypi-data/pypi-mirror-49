# -*- coding: utf-8 -*-
"""Main module."""
import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

_declination_months = {
    'января': 'январь',
    'февраля': 'февраль',
    'марта': 'март',
    'апреля': 'апрель',
    'мая': 'май',
    'июня': 'июнь',
    'июля': 'июль',
    'августа': 'августь',
    'сентября': 'сентябрь',
    'октября': 'октябрь',
    'ноября': 'ноябрь',
    'декабря': 'декабрь',
}


class _Logger:
    def send_info(self, message):
        print('INFO: ' + message)

    def send_warning(self, message):
        print('WARNING: ' + message)

    def send_error(self, message):
        print('ERROR: ' + message)


class RabotaOtzyvyRu:
    BASE_URL = 'https://rabotaotzyvy.ru/'
    reviews = []

    def __init__(self, slug, logger=_Logger()):
        self.slug = slug
        self.logger = logger
        self.session = requests.Session()

    def start(self):
        self.request('GET', urljoin(self.BASE_URL, '{}.html'.format(self.slug)))
        self.reviews = list(self._collect_reviews())

    def _collect_reviews(self):
        """TODO: собрать комментраи над отзывами"""
        reviews_soup = self.soup.select('ol.comment-list>li.ticket-comment')
        if not reviews_soup:
            self.logger.send_warning('Reviews not found')
        for review_soup in reviews_soup:
            new_review = Review()
            new_review.text = review_soup.select_one(
                                                'div.ticket-comment-text>p').text
            date_string = review_soup.select_one(
                                        'span.ticket-comment-createdon').text
            new_review.date = self._convert_date(date_string)
            author = Author()
            author.name = review_soup.select_one(
                'div.ticket-comment-body.ticket-comment-guest'
                '>div.ticket-comment-header>span.ticket-comment-author').text
            new_review.author = author
            yield new_review

    @staticmethod
    def _convert_date(date_string):
        try:
            month_string = date_string[3:-5]
            month = _declination_months[month_string]
            return datetime.datetime.strptime(
                        date_string.replace(month_string, month),
                        '%d %B %Y').date()
        except KeyError:
            return None

    def request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        if not response.status_code == 200:
            self.logger.send_error(response.text)
            raise Exception("{}: {}".format(response.status_code,
                                            response.text))

        self.soup = BeautifulSoup(response.text, 'html.parser')
        return self.soup


class Author:
    name = ''


class Review:
    text = ''
    date = None
    author = None
    sub_reviews = []


if __name__ == '__main__':
    prov = RabotaOtzyvyRu('yandex-taxi-moskva-otzyvy-voditeley')
    prov.start()
    for review in prov.reviews:
        print(review.author.name, review.text[0:10], review.date)
