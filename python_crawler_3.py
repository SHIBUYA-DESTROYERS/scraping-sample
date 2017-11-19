import requests
import lxml.html



def main():
    """
    クローラのメイン処理
    """
    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        print(url)


def scrape_list_page(response):
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレータ関数
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url


if __name__ == '__main__':
    main()