import time
import re

import requests
import lxml.html



def main():
    """
    クローラのメイン処理
    """
    session = requests.Session()
    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        time.sleep(1)
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)


def scrape_list_page(response):
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレータ関数
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response):
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する
    """
    root = lxml.html.fromstring(response.content)
    ebook = {
        'url': response.url,
        'title': root.cssselect('#bookTitle')[0].text_content(),
        'price': root.cssselect('.buy')[0].text.strip(),
        'content': [normalize_space(h3.text_content()) for h3 in root.cssselect('#content > h3')],
    }
    return ebook


def normalize_space(s):
    """
    連続する空白を1つのスペースに置き換え，前後の空白は削除した新しい文字列を取得する．
    """
    return re.sub(r'\s+', ' ', s).strip()


if __name__ == '__main__':
    main()