# This scraper program parses given DW website and downloads all audio files

import time
import requests
from requests_html import HTMLSession

# Example URL for testing
address = 'https://learngerman.dw.com/en/eine-pizza-bitte/l-37279261/lv'

# address = input('Input site URL: \n')

session = HTMLSession()
r = session.get(address)
audios = r.html.find('audio')
sources = [el.find('source')[0] for el in audios]
links = [el.attrs['src'] for el in sources]

length = len(links)

for i in range(length):
    file_name = links[i].split('/')[-1]

    r = requests.get(links[i], stream=True)

    with open('./Downloads/' + file_name, 'wb') as f:
        f.write(r.content)

    print(f'{i+1}/{length}')
    print(file_name)
    print(r.headers['content-type'], '/ Encoding:', r.encoding, '/ Status:', r.status_code)
    print()

    time.sleep(1)
