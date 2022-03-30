from bs4 import BeautifulSoup
import requests
import time
import random
import csv

def _unpack_section(section):
    def str_to_float(string): return round(float(string.replace(',','.')), 2)
    
    section_data = []
    name = next(section.label.stripped_strings)
    attr = 'data-content'
    # retrieve data based on page structure
    if buttons := section.select('button'):
        for but in buttons:
            if b := but.get(attr):
                section_data.append((name, str_to_float(b)))
            else:
                for i in range(2):
                    b = but.get(attr + str(i+1))
                    name1 = name + ' ' + next(section.select('.calc-radio')[i].stripped_strings)
                    section_data.append((name1, str_to_float(b)))
    elif b := section.select_one('.priceval'):
        b = b.get('value')
        section_data.append((name, str_to_float(b)))
    else:
        # return only name when extraction fails
        section_data.append((name,))
    # returns list of tuples consisting of composite names and prices as floats
    return section_data

def _unpack_soup(soup):
    data = []
    sections = soup.select(':is(.calc-row):not(.calc0)')
    # retrieve data from all page sections
    for p in sections:
        data.extend(_unpack_section(p))
    # unique names for use in sorting
    uniques = list(dict.fromkeys([i[0] for i in data]))
    return sorted(data, key=lambda x: uniques.index(x[0]))

def scrape_single(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return _unpack_soup(soup)

def scrape_all(id1='', id2='', id3=''):
    """
    id1 - pietrowy z piwnica,
    id2 - parterowy bez piwnicy,
    id3 - taras
    """
    # IDs for settings (i.e. location) you can set on the page
    link1 = f'https://kb.pl/budowa/pietrowy-z-piwnica/sciany-dzialowe/{id1}'
    link2 = f'https://kb.pl/budowa/parterowy-bez-piwnicy/sciany-dzialowe/{id2}'
    link3 = f'https://kb.pl/przy-domu/taras/{id3}'

    # get all hrefs
    reqs = []
    for link in [link1, link2, link3]:
        reqs.append(requests.get(link))
        time.sleep(random.randint(5, 10))
    links = []
    links.append(BeautifulSoup(reqs[0].text, 'html.parser').select('.calc-menu a'))
    links.append(BeautifulSoup(reqs[1].text, 'html.parser').select('.calc-menu a'))
    links.append(BeautifulSoup(reqs[2].text, 'html.parser').select('.calc-menu-group'))
    links[2] = links[2][1].select('a')

    # convert hrefs to proper urls
    url = 'https://kb.pl'
    lst = []
    for i in links:
        for j in i[:-1]:
            lst.append(url + j.get('href'))
    links = lst

    # scrape proper
    data = []
    for url in links:
        data.extend(scrape_single(url))
        time.sleep(random.randint(10, 20))
    return data

# write aquired data to a file
def data_to_csv(data):
    uniq_data = list(dict.fromkeys([i for i in data]))

    # print items with missing price
    idx = [i for i in range(len(uniq_data)) if len(uniq_data[i]) == 1]
    for i in idx:
        print('No data -', uniq_data[i])

    with open('dump.txt', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(uniq_data)

# function requires the data to be pre-sorted by the first item
def group_by_name(data):
    new_data = []
    pointer = 0
    name = data[pointer][0]
    for i, item in enumerate(data):
        if name != item[0]:
            new_data.append((name, *[x[1] for x in data[pointer:i] if len(x) > 1]))
            pointer = i
            name = data[pointer][0]
    new_data.append((name, *[x[1] for x in data[pointer:] if len(x) > 1]))
    return new_data

