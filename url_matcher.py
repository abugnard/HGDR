"""url_matcher.py
    Search for correspondence between the country/countries found by the geolocator and the geofabrik database.
"""
# Import libraries
from rapidfuzz import process, fuzz
import pandas as pd
import unidecode


def find_correspondence(country_2_dl):
    df_ISO = pd.DataFrame()
    df_ISO[['country', 'ISO']] = pd.read_csv('country_available_ISO.csv',sep = ';')

    dl_num = len(country_2_dl)
    dl_list = [0] * dl_num
    iso_codes = ''
    i = 0

    for ctry2dl in country_2_dl:
        search_str = unidecode.unidecode(ctry2dl)
        most_similar = process.extractOne(search_str, df_ISO['country'], scorer=fuzz.WRatio)
        dl_list[i] = most_similar[0]
        ISO = df_ISO[df_ISO['country'] == most_similar[0]].index

        if i == dl_num -1:
            iso_codes = iso_codes + df_ISO['ISO'][ISO[0]]
        else:
            iso_codes = iso_codes + df_ISO['ISO'][ISO[0]] + '_'
        i = i + 1
    return dl_list, iso_codes
