import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import unidecode
from rapidfuzz import process, fuzz


def pop100m(ctry_2_dl):
    df_iso3 = pd.read_csv('iso3_country.csv', sep=';')
    URL_100m = []

    for ctry in ctry_2_dl:
        if ctry == 'Haiti and Dominican Republic':
            ctry = 'Haiti'
        elif ctry.split('/')[0] == 'us-west':
            ctry = 'us'
        search_str = unidecode.unidecode(ctry.split('/')[0])
        most_similar = process.extractOne(search_str, df_iso3['Country'], scorer=fuzz.WRatio)
        output = most_similar[0]
        ISO3 = df_iso3[df_iso3['Country'] == output]['ISO3']

        URL = 'https://www.worldpop.org/rest/data/pop/wpgp?iso3=' + ISO3.values[0]

        r = requests.get(URL)
        page_body = r.text
        soup = BeautifulSoup(page_body, 'html.parser')
        list_url = [m.start() for m in
                    re.finditer('https://data.worldpop.org/GIS/Population/Global_2000_2020/', str(soup))]

        link_densPop100m = []
        if list_url == []:
            last_year = '2020'
        else:
            for link_num in list_url:
                link_densPop100m.append(str(soup)[link_num:link_num + 83])

            base_link = link_densPop100m[-1]
            last_year = base_link.split('/')[6]

        URL = 'https://data.worldpop.org/GIS/Population/Global_2000_' + last_year + '/' + last_year + '/' + ISO3.values[
            0] + '/' + ISO3.values[0].lower() + '_ppp_2020.tif'
        URL_100m.append(URL)
    return URL_100m, last_year