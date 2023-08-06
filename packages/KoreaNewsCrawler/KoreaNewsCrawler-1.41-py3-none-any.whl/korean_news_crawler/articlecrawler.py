#!/usr/bin/env python
# -*- coding: euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from korea_news_crawler.exceptions import *
from korea_news_crawler.articleparser import ArticleParser
import os
import calendar
import requests
import csv
import re


class ArticleCrawler(object):
    def __init__(self):
        self.parser = ArticleParser()
        self.categories = {'��ġ': 100, '����': 101, '��ȸ': 102, '��Ȱ��ȭ': 103, 'IT����': 105,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'IT_science': 105}
        self.selected_categories = []
        self.date = {'start_year': 0, 'end_year': 0, 'end_month': 0}

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    def set_date_range(self, start_year, end_year, end_month):
        args = [start_year, end_year, end_month]
        if start_year > end_year:
            raise InvalidYear(start_year, end_year)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    def make_news_page_url(self, category_url, start_year, last_year, start_month, last_month):
        maked_url = []
        final_startmonth = start_month
        final_lastmonth = last_month
        for year in range(start_year, last_year + 1):
            if year != last_year:
                start_month = 1
                last_month = 12
            else:
                start_month = final_startmonth
                last_month = final_lastmonth
            for month in range(start_month, last_month + 1):
                for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                    url = category_url
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)
                    url = url + str(year) + str(month) + str(month_day)
                    final_url = url  # page ��¥ ������ �ְ� page ������ ���� url �ӽ� ����

                    # totalpage�� ���̹� ������ ������ �̿��ؼ� page=1000���� ������ totalpage�� �˾Ƴ�
                    # page=1000�� �Է��� ��� �������� �������� �ʱ� ������ page=totalpage�� �̵� ��
                    totalpage = self.parser.find_news_totalpage(final_url + "&page=1000")
                    for page in range(1, totalpage + 1):
                        url = final_url  # url page �ʱ�ȭ
                        url = url + "&page=" + str(page)
                        maked_url.append(url)
        return maked_url

    def crawling(self, category_name):
        # MultiThread PID
        print(category_name + " PID: " + str(os.getpid()))

        # �� ī�װ� ��� ���� �� CSV
        file = open('Article_' + category_name + '.csv', 'w', encoding='euc_kr', newline='')
        wcsv = csv.writer(file)

        # ��� URL ����
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
            self.categories.get(category_name)) + "&date="
        # start_year�� 1�� ~ end_year�� end_mpnth ��¥���� ��縦 �����մϴ�.
        final_urlday = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'], 1, self.date['end_month'])
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in final_urlday:

            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = requests.get(URL)
            document = BeautifulSoup(request.content, 'html.parser')
            tag_document = document.find_all('dt', {'class': 'photo'})

            post = []
            for tag in tag_document:
                post.append(tag.a.get('href'))  # �ش�Ǵ� page���� ��� ������ URL�� post ����Ʈ�� ����

            for content_url in post:  # ��� URL
                # ũ�Ѹ� ��� �ð�
                sleep(0.01)
                # ��� HTML ������
                request_content = requests.get(content_url)
                document_content = BeautifulSoup(request_content.content, 'html.parser')

                try:
                    # ��� ���� ������
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # ���� ��� ���� �ʱ�ȭ
                    text_headline = text_headline + self.parser.clear_headline(str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # ������ ��� ��� ���� ó��
                        continue

                    # ��� ���� ������
                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # ���� ��� ���� �ʱ�ȭ
                    text_sentence = text_sentence + self.parser.clear_content(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # ������ ��� ��� ���� ó��
                        continue

                    # ��� ��л� ������
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # ��л� �ʱ�ȭ
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # ������ ��� ��� ���� ó�� ��.
                        continue
                    # CSV �ۼ�
                    wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])

                except Exception as ex:  # UnicodeEncodeError ..
                    pass
        file.close()

    def start(self):
        # MultiProcess ũ�Ѹ� ����
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("IT����", "��Ȱ��ȭ")  # ��ġ, ����, ��Ȱ��ȭ, IT����, ��ȸ ī�װ� ��� ����
    Crawler.set_date_range(2017, 2018, 4)  # 2017�� 1������ 2018�� 4������ ũ�Ѹ� ����
    Crawler.start()
