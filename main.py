from bs4 import BeautifulSoup
from database import insertArticle
import datetime
import requests
import sys
import logging
from pysitemap import crawler

def anyWebsiteScrap(kw,url):
    if __name__ == '__main__':
        if '--iocp' in sys.argv:
            from asyncio import events, windows_events
            sys.argv.remove('--iocp')
            logging.info('using iocp')
            el = windows_events.ProactorEventLoop()
            events.set_event_loop(el)
        crawler(url, kw, out_file=url.split('.')[1]+'.xml', exclude_urls=[".pdf", ".png", ".jpg", ".zip", "&", ".css", ".json"])


"""def corpusScrape(dated, datef):
    html = requests.get('https://www.rtflash.fr/').content
    s = BeautifulSoup(html, 'lxml')
    for categories in s.find(id="nav").find_all('ul'):
        for category in categories.find_all('a'):
            url = category.get('href')
            title = category.get('title')
            i = 1
            while i > 0:
                page = BeautifulSoup(requests.get(url).content, 'lxml')
                articles = page.find_all("ul", {"class": "article-list"})
                for article in articles:
                    date = article.find('em').text
                    if dated <= datetime.datetime.strptime(date.split()[1], '%d/%m/%Y') <= datef:
                        img = article.find('img').get('src')
                        link = article.find('a').get('href')
                        subject = article.find('a').get('title')
                        intro = article.find('p').text
                        insertArticle(title, link, date, subject, img, intro)
                    else:
                        i = -1
                        break
                url = url + '/' + str(i)
                i = i + 1"""
html = requests.get('https://outilscollaboratifs.com/').content
s = BeautifulSoup(html, 'lxml')
i = 1
#while i > 0:
    #s.find_all('article')
"""html = requests.get('https://b-com.com/actualite').content
    html = requests.get('https://www.01net.com/').content
    html = requests.get('https://www.ionos.fr/digitalguide/hebergement/blogs/').content
    html = requests.get('https://www.maddyness.com/').content
    html = requests.get('https://siecledigital.fr/').content
    html = requests.get('https://www.usinenouvelle.com/').content
    html = requests.get('https://itsocial.fr/').content
    html = requests.get('https://medium.com/').content
    html = requests.get('https://www.journaldunet.com/').content"""
