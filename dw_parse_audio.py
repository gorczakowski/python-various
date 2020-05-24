# This scraper program parses given DW website and downloads all audio files

import time
import requests
from requests_html import HTMLSession

# Example URL for testing
# address = 'https://learngerman.dw.com/en/eine-pizza-bitte/l-37279261/lv'
print('Input site URL: ')
address = input()

session = HTMLSession()
r = session.get(address)
audios = r.html.find('audio')
sources = [el.find('source')[0] for el in audios]
links = [el.attrs['src'] for el in sources]

length = len(links)
i = 0

for link in links:
    i += 1
    file_name = link.split('/')[-1]

    r = requests.get(link, stream=True)

    with open('./Downloads/' + file_name, 'wb') as f:
        f.write(r.content)

    print(f'{i}/{length}')
    print(file_name)
    print(r.headers['content-type'], '/ Encoding:', r.encoding, '/ Status:', r.status_code)
    print()

    time.sleep(1)
