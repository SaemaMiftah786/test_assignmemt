import pandas as pd
import requests
import os
import datetime
from time import time
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, **kwargs):
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.url = 'https://www.bbc.com/news'
        self.base_url = 'https://www.bbc.com'
        self.utc_time = datetime.datetime.utcnow()
        self.today_date = self.utc_time.strftime("%Y%m%d")
        self.retry = 2
        self.root_path = os.getcwd() + '/csv/'
        self.article_df = pd.DataFrame()
        self.file_name = (
            self.today_date + 'bbc.csv'
        )

    def timer_func(func):
        """This function shows the execution time of
        the function object passed"""
        def wrap_func(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
            return result
        return wrap_func

    def get_request(self, url):
        """make the request"""
        try:
            print(url)
            resp = requests.get(url, headers=self.headers)
            html = resp.content
            return html
        except Exception as e:
            print(f'URL Error: {e} Could not connect to URL !!')
            return

    def get_meta_data(self):
        """get the data"""
        sublinks = []
        meta_html = self.get_request(self.url)
        soup = BeautifulSoup(meta_html, 'html.parser')
        for sub_link in soup.findAll('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'):
            sublinks.append(sub_link['href'])
        return sublinks
    
    def get_data(self, article_links):
        """get the data"""
        for article_link in article_links:
            if self.base_url in article_link:
                url = article_link
                continue
            else:
                url = self.base_url + article_link
            article_data = self.get_request(url)
            html = BeautifulSoup(article_data, 'html.parser')
            headline = html.select('h1')[0].text.strip()
            
            if len(html.findAll('div', class_='ssrcss-68pt20-Text-TextContributorName')):
                author = html.findAll('div', class_='ssrcss-68pt20-Text-TextContributorName')[0].text.strip()
            else:
                author = ''
            
            full_article = ''
            for article in html.findAll('p', class_='ssrcss-1q0x1qg-Paragraph'):
                article_text = article.text.strip()
                full_article = full_article + article_text
            
            single_data = {
                'author': author,
                'headline': headline,
                'article_url': url,
                'text': [full_article],
                'date': self.utc_time.strftime("%Y-%m-%d")
            }
            temp_df = pd.DataFrame(single_data)
            self.article_df = pd.concat([self.article_df, temp_df])
        return 1

    def save_data(self):
        """save the data"""
        try:
            filename = self.root_path + self.file_name
            self.article_df.to_csv(filename, mode='a', index=False, encoding="utf-8")
            print(f'Successfully pushed {filename}')
        except Exception as e:
            print(f'Could not save to Buclet Excepttion: {e}')

    @timer_func
    def run(self):
        """perform scraping operations"""
        article_links = self.get_meta_data()
        success = self.get_data(article_links)
        if success:
            self.save_data()

if __name__ == '__main__':
    Scraper().run()
