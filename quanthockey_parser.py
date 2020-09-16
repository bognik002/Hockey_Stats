import requests
from bs4 import BeautifulSoup
from numpy import nan


def get_page(url, params={}):
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_table(page_soup):
    table = page_soup.find('table', {'id': 'statistics'})
    return table


def get_columns(table):
    columns = []
    for tr in table.thead.find_all('tr')[-1]:
        if tr.text:
            columns.append(tr.text)
    return columns


def get_contents(table):
    contents = []
    for tr in table.tbody.find_all('tr'):
        row = []
        i = 0
        for td in tr.find_all('td'):
            if td.text:
                row.append(td.text)
            elif not td.text and i != 1:
                row.append(nan)
            i += 1
        contents.append(row)
    return contents


def get_number_of_pages(page):
    tabletop = page.find('div', {'class': 'tabletop'})
    pages = []
    for page_n in tabletop.find_all('li'):
        if page_n.text:
            if page_n.text.isdigit():
                pages.append(page_n.text)
    if not pages:
        return 1
    return int(pages[-1])


