import time

import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)


def main():
    """
    メインの処理
    """
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!!')
    else:
        print('Error')


def fetch(url):
    """
    指定したURLを取得してResponseオブジェクトを返す．一時的なエラーが起きたら最大3回リトライする．
    """
    max_retries = 3
    retries = 0
    while True:
        try:
            print('Retrying {0}...'.format(url))
            response = requests.get(url)
            print('Status: {0}'.format(response.status_code))
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response

        except requests.exceptions.RequestException as ex:
            print('Exception occured: {0}'.format(ex))
            retries += 1
            if retries >= max_retries:
                raise Exception('Too many tries.')

            wait = 2 ** (retries - 1)
            print('Waiting {0} seconds...'.format(wait))
            time.sleep(wait)


if __name__ == '__main__':
    main()