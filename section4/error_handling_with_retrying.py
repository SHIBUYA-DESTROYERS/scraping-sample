import requests
from retrying import retry

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


@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def fetch(url):
    """
    指定したURLを取得してResponseオブジェクトを返す．一時的なエラーが起きたら最大3回リトライする．
    """
    print('Retrying {0}...'.format(url))
    response = requests.get(url)
    print('Status: {0}'.format(response.status_code))
    if response.status_code not in TEMPORARY_ERROR_CODES:
        return response
    raise Exception('Too many tries.')


if __name__ == '__main__':
    main()