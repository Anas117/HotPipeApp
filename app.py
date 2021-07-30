import streamlit as st
from database import getArticleByCategory
import sys
import logging
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


def writeCol1():
    listArticle = getArticleByCategory(category)
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
st.sidebar.button('Load data')
st.sidebar.button('Clear data')

with col1:
    st.title('NewsLetter')
    category = st.text_input("Catégorie")
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

