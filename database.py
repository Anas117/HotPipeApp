import sqlite3

def insertArticle(category, url, date, title, image, intro):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''insert into article values (?,?,?,?,?,?)''', (category, url, date, title, image, intro))
    connection.commit()

def getArticleByCategory(cat):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''select * from article where category = ?''', [cat])
    return c.fetchall()

def insertKeyword_url(keyword, url):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''insert into keyword_url values (?,?)''', (keyword, url))
    connection.commit()

def getUrlByKeyword(keyword, url):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''select * from keyword_url where keyword = ? and url like ? limit 100''', (keyword, url+'%'))
    return c.fetchall()
