"""webscraper.py
    This function scans the web page of geofabrik.de to get the link and the date of the most current OSM map.
    Parameter: countries for which the link should be found.
"""
# Import libraries
import requests
from bs4 import BeautifulSoup
import tabulate
import re
import pandas as pd
import dateutil.parser as dparser


def find_link(dl_list):
    dl_num = len(dl_list)
    URL = 'https://download.geofabrik.de/'
    r = requests.get(URL)
    page_body = r.text
    soup = BeautifulSoup(page_body, 'html.parser')
    publications_wrappers = soup.find_all('td', class_='subregion')
    region = []
    for p in publications_wrappers:
        beg = str(p).index('href')
        end = str(p).index('.html')
        region_url = str(p)[beg + 6:end]
        region.append(region_url)

    dict_country = {k: v for v, k in enumerate(region)}
    publications_wrappers = soup.find_all('td', class_='subregion')

    for s in region:
        URL_region = 'https://download.geofabrik.de/' + s.lower() + '.html'
        r_r = requests.get(URL_region)
        page_body_r = r_r.text
        soup_r = BeautifulSoup(page_body_r, 'html.parser')
        publications_wrappers = soup_r.find_all('td', class_='subregion')
        country = []

        for p in publications_wrappers:

            if p.find('a').text[0].isupper():
                beg = str(p).index('href')
                end = str(p).index('.html')

                country_url = str(p)[beg + 7 + len(s):end]
                if p.find('a').text == 'Russian Federation':
                    country_url = 'russia'

                country.append(country_url)

        dict_country[s] = country

    data = dict_country
    table = tabulate.tabulate(data, tablefmt='html', headers=region)
    table

    rows = list(dict_country.values())
    rows_flatten = [j for sub in rows for j in sub]
    df = pd.DataFrame(data={"country": rows_flatten})
    df.to_csv("country_available.csv", sep=',', index=False)

    i = 0
    URL_down = [0] * dl_num
    URL_ground = [0] * dl_num
    last_update = [0] * dl_num

    for data2dl in dl_list:
        for key in dict_country.keys():
            if data2dl in dict_country[key]:
                users_choice = key
                URL_down[i] = 'https://download.geofabrik.de/' + users_choice.lower() + '.html'
                r_down = requests.get(URL_down[i])
                page_body_down = r_down.text
                soup_down = BeautifulSoup(page_body_down, 'html.parser')
                users_choice_down = data2dl
                URL_ground[
                    i] = 'https://download.geofabrik.de/' + users_choice.lower() + '/' + users_choice_down.lower() + '.html'
                print(URL_ground[i])

                r_ground = requests.get(URL_ground[i])
                page_body_ground = r_ground.text

                soup_ground = BeautifulSoup(page_body_ground, 'html.parser')
                last_update_raw = soup_ground.find_all('li')[0]

                xx = str(last_update_raw)
                r1 = re.findall("\d\d\d\d.\d\d.\d\d.\d\d.\d\d.\d\d", xx)
                if type(r1) == list:
                    r1 = r1[0]
                last_update[i] = dparser.parse(str(r1), fuzzy=True)
                print("Last Update the {:%d, %b %Y at %H:%M:%S}".format(last_update[i]))

        i = i + 1

    print('Links for download\n------------------')

    url_list = [0] * dl_num
    size_list = [0] * dl_num

    for i in range(0, dl_num):
        url_dl = URL_ground[i] + '-latest.osm.pbf'
        url_dl = url_dl.replace('.html', '')
        print('{}) {}'.format(i + 1, url_dl))
        url_list[i] = url_dl

        r = requests.get(URL_ground[i])
        page_body = r.text
        soup = BeautifulSoup(page_body, 'html.parser')
        publications_wrappers = soup.find_all('ul')
        str_size = str(publications_wrappers)

        check_GB_MB = str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21]

        if check_GB_MB.find('MB', 0) == -1:

            if check_GB_MB.find('KB', 0) == -1:

                found = re.findall("\d+\.\d+",
                                   str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])
                if not bool(found):
                    found = re.findall("\d+",
                                       str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])

                file_size = float(found[0]) * 1000

            else:
                found = re.findall("\d+\.\d+",
                                   str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])
                if not bool(found):
                    found = re.findall("\d+",
                                       str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])

                file_size = float(found[0]) * 0.001

        else:
            found = re.findall("\d+\.\d+",
                               str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])
            if not bool(found):
                found = re.findall("\d+",
                                   str_size[str_size.find('File size', 0) + 11: str_size.find('File size', 0) + 21])

            file_size = float(found[0])

        size_list[i] = file_size

    return url_list, size_list
