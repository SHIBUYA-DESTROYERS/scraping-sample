import re
import sqlite3
import urllib.request
from html import unescape


def main():
    """
    メインの処理．fetch(), scrape(), save()の3つの関数を呼び出す．
    """

    html = fetch('https://gihyo.jp/dp')
    books = scrape(html)
    save('books.db', books)


def fetch(url):
    """
    引数urlで与えられたURLのWebページを取得する．
    WebページのエンコーディングはContent-Typeヘッダーから取得する．
    :return: str値のHTML
    """
    proxies = {
        'http': 'http://172.20.20.104:8080',
        'https': 'http://172.20.20.104:8080',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }

    url = 'https://gihyo.jp/dp'

    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)

    request = urllib.request.Request(url=url, headers=headers)
    f = urllib.request.urlopen(request)

    encoding = f.info().get_content_charset(failobj="utf-8")
    html = f.read().decode(encoding)

    return html


def scrape(html):
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す．
    :return: 書籍(dict)のリスト
    """

    books = []
    for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        url = 'https://gihyo.jp' + url

        title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
        title = re.sub(r'<.*?>', '', title)
        title = unescape(title)

        books.append({'url': url, 'title': title})

    return books


def save(db_path, books):
    """
    引数booksで与えられた書籍のリストをSQLiteデータベースに保存する．
    データベースのパスは引数db_pathで与えられる．
    :return: none
    """

    conn = sqlite3.connect(db_path)

    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS books')
    c.execute('''
      CREATE TABLE books (
        title text,
        url text
      )
    ''')

    c.executemany('INSERT INTO books VALUES (:title, :url)', books)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()