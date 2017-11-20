import requests
from cachecontrol import CacheControl


session = requests.session()
cached_session = CacheControl(session)

response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache)

response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache)
