import sqlite3

def insertArticle(title, url, date, category):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''select * from article where title = ?''', [title])
    if len(c.fetchall()) == 0:
        c.execute('''insert into article values (?,?,?,?)''', (title, url, date, category))
        connection.commit()

def getArticleByCategory(cat):
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''select * from article where category = ?''', [cat])
    return c.fetchall()

def getCategories():
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''select distinct category from article''')
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

def clearArticle():
    connection = sqlite3.connect('scrapedata.db')
    c = connection.cursor()
    c.execute('''delete from article''')
    connection.commit()

