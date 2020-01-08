import scrapy
import time
import random
import sys
import os
from requests import get


class PastebinSpider(scrapy.Spider):
    name = 'pastebin_spider'
    start_urls = ['https://pastebin.com/5F6DiBM5']

    def parse(self, response):
        for li in response.css('.right_menu > li'):

            sleep_time = random.randint(3, 10)
            print('Sleeping for ' + str(sleep_time) + ' seconds')
            time.sleep(sleep_time)
            span_text = li.css('span ::text').get()
            print(span_text)
            syntax = ''
            if '|' in span_text:
                syntax = span_text.split('|')[0].strip() + '/'

            link = li.css('a').attrib['href']
            print('https://pastebin.com/raw' + link)
            with open('urls', 'a') as f:
                f.write('https://pastebin.com' + link + '\n')

            title = li.css('a ::text').get()
            filename = f'pastes/{syntax}' + link.strip('/')
            with open(filename, 'w+') as file:
                text = get('https://pastebin.com/raw' + link)
                file.write(title + '\n' + text.text)
                print('Created the file ' + os.getcwd() + f'/{filename}')

            yield {
                'title': title,
            }

        # for next_page in response.css('.right_menu > li > a'):
        #     yield response.follow(next_page, self.parse)
