import streamlit as st
from database import getArticleByCategory, insertArticle, clearArticle, getCategories
import sys
from bs4 import BeautifulSoup
import logging
import requests
import datetime
from pysitemap import crawler
from database import getUrlByKeyword
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def anyWebsiteScrap(kw,url):
    if __name__ == '__main__':
        if '--iocp' in sys.argv:
            from asyncio import events, windows_events
            sys.argv.remove('--iocp')
            logging.info('using iocp')
            el = windows_events.ProactorEventLoop()
            events.set_event_loop(el)
        crawler(url, kw, out_file=url.split('.')[1]+'.xml', exclude_urls=[".pdf", ".png", ".jpg", ".zip", "&", ".css", ".json", "("])


def corpusScrape(dated, datef):
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
                    date = datetime.datetime.strptime(article.find('em').text.split()[1], '%d/%m/%Y').date()
                    if dated <= date <= datef:
                        link = article.find('a').get('href')
                        subject = article.find('a').get('title')
                        insertArticle(subject, link, date, title)
                    else:
                        i = -1
                        break
                url = category.get('href') + '/' + str(i)
                i = i + 1

    baseurl = 'https://www.01net.com/actualites/'
    url = baseurl
    i = 1
    while i > 0:
        s = BeautifulSoup(requests.get(url).content, 'lxml')
        articles = s.find_all("a", {"class": "table-cell-middle padding-inside-all"})
        articles.remove(articles[1])
        for article in articles:
            if "https:" in article.get('href'):
                link = article.get('href')
            else:
                link = "https:" + article.get('href')
            page = BeautifulSoup(requests.get(link).content, 'lxml')
            if page.find_all('time'):
                date = datetime.datetime.strptime(page.find('time').text.split()[0], '%d/%m/%Y').date()
            else:
                break
            if page.find("ul", {"class": "breadcrumb no-padding no-margin"}):
                cat = page.find("ul", {"class": "breadcrumb no-padding no-margin"}).find_all('li')
            else:
                break
            if dated <= date <= datef:
                insertArticle(article.find('h2').text, link, date, cat[len(cat) - 1].find('a').text.strip())
            if dated > date and len(page.find_all('time')) < 2:
                i = -1
                break
        i = i + 1
        url = baseurl + '/?page=' + str(i)
    list = ['https://www.usinenouvelle.com/aero-spatial/', 'https://www.usinenouvelle.com/auto/',
            'https://www.usinenouvelle.com/energie-petrole/', 'https://www.usinenouvelle.com/sante/',
            'https://www.usinenouvelle.com/agro/', 'https://www.usinenouvelle.com/transports-et-logistique/',
            'https://www.usinenouvelle.com/eco-social/', 'https://www.usinenouvelle.com/matieres-premieres/',
            'https://www.usinenouvelle.com/chimie-agrochimie/', 'https://www.usinenouvelle.com/cybersecurite/',
            'https://www.usinenouvelle.com/defense/', 'https://www.usinenouvelle.com/electronique-informatique/',
            'https://www.usinenouvelle.com/telecoms/', 'https://www.usinenouvelle.com/metallurgie-siderurgie/',
            'https://www.usinenouvelle.com/luxe/', 'https://www.usinenouvelle.com/biens-de-consommation/',
            'https://www.usinenouvelle.com/recyclage-et-services-a-l-environnement/',
            'https://www.usinenouvelle.com/btp-construction/', 'https://www.usinenouvelle.com/plasturgie-emballage/']
    for url in list:
        for year in range(dated.year, datef.year + 1):
            url = url + "annee_" + str(year) + "/"
            s = BeautifulSoup(requests.get(url).content, 'lxml')
            ss = s.find('ul', {'class': 'editoPaginationType1__list'}).find_all('li')
            end = ss[len(ss) - 1].find('a').text.strip()
            cat = s.find('div', {'class': 'epSousNavThema__title-main-bloc'}).text.strip()
            done = 0
            for article in s.find_all('div', {'class': 'editoCardType10__content'}):
                if dated <= datetime.datetime.strptime(article.find('time').get('datetime').split(' ')[0],
                                                       '%Y-%m-%d').date() <= datef:
                    insertArticle(article.find('h2').text.strip(), "https://www.usinenouvelle.com" + article.find('a', {
                        "class": "editoCardType10__link is-displayBlock"}).get('href'),
                                  article.find('time').get('datetime').split(' ')[0], cat)
                if dated > datetime.datetime.strptime(article.find('time').get('datetime').split(' ')[0],
                                                      '%Y-%m-%d').date():
                    done = 1
                    break
            if done == 0:
                for i in range(2, int(end)):
                    url2 = url + str(i) + "/"
                    s2 = BeautifulSoup(requests.get(url2).content, 'lxml')
                    done = 0
                    for article in s2.find_all('div', {'class': 'editoCardType10__content'}):
                        if dated <= datetime.datetime.strptime(article.find('time').get('datetime').split(' ')[0],
                                                               '%Y-%m-%d').date() <= datef:
                            insertArticle(article.find('h2').text.strip(),
                                          "https://www.usinenouvelle.com" + article.find('a', {
                                              "class": "editoCardType10__link is-displayBlock"}).get('href'),
                                          article.find('time').get('datetime').split(' ')[0], cat)
                        if dated > datetime.datetime.strptime(article.find('time').get('datetime').split(' ')[0],
                                                              '%Y-%m-%d').date():
                            done = 1
                            break
                    if done == 1:
                        break


def writeCol1():
    listArticle = []
    for cat in category:
        for arti in getArticleByCategory(str(cat).split("'")[1]):
            listArticle.append(arti)
    with articlesHolder.beta_container():
        displayList = []
        if include != "":
            for article in listArticle:
                if include in article[1]:
                    displayList.append(article)
        if exclude != "":
            for article in listArticle:
                if exclude not in article[1]:
                    displayList.append(article)
        if len(displayList) == 0:
            for article in listArticle:
                if dated <= datetime.datetime.strptime(article[2], '%Y-%m-%d').date() <= datef:
                    col1.write(f'''
                    * URL: {article[1]}
                    * Date: {article[2]}
                    * Titre: {article[3]}
                    ''')
        else:
            for article in displayList:
                col1.write(f'''
                    * URL: {article[1]}
                    * Date: {article[2]}
                    * Titre: {article[3]}
                    ''')


def writeCol2(kw,url):
    listArticle2 = getUrlByKeyword(kw, url)
    if len(listArticle2) == 0:
            anyWebsiteScrap(kw, url)
            listArticle2 = getUrlByKeyword(kw, url)
    with UrlsHolder.beta_container():
        displayList2 = []
        if include != "":
            for article in listArticle2:
                if include in article[1]:
                    displayList2.append(article)
        if exclude != "":
            for article in listArticle2:
                if exclude not in article[1]:
                    displayList2.append(article)
        if len(displayList2) == 0:
            for article in listArticle2:
                col2.write(f'''
                * {article[1]}
                ''')
        else:
            for article in displayList2:
                col2.write(f'''
                * {article[1]}
                ''')


articles = []
articles2 = []
col1, col2 = st.beta_columns(2)
include = st.sidebar.text_input('Url include')
exclude = st.sidebar.text_input('Url exclude')
dated = st.sidebar.date_input('Start date')
datef = st.sidebar.date_input('End date')
load = st.sidebar.button('Load data')
clear = st.sidebar.button('Clear data')

with col1:
    st.title('NewsLetter')
    category = st.multiselect('Category',getCategories())
    getArt = st.button("Get articles")
    articlesHolder = st.empty()
    if getArt:
        writeCol1()
with col2:
    st.title('Any Website')
    keyword = st.text_input("Keyword")
    url = st.text_input("Url")
    getUrl = st.button("Extract urls")
    UrlsHolder = st.empty()
    if getUrl:
        writeCol2(keyword,url)

if load:
    corpusScrape(dated,datef)
    st.experimental_rerun()

if clear:
    clearArticle()
    st.experimental_rerun()