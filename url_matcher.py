"""url_matcher.py
    Search for correspondence between the country/countries found by the geolocator and the geofabrik database.
"""
# Import libraries
from rapidfuzz import process, fuzz
import pandas as pd
import unidecode
from geopy.geocoders import Nominatim


def find_correspondence(country_2_dl):
    df_ISO = pd.DataFrame()
    df_ISO[['country', 'ISO']] = pd.read_csv('country_available_ISO.csv', sep = ';')
    df_subregion = pd.read_csv('subregion.csv')

    dl_num = len(country_2_dl)
    dl_list = [0] * dl_num
    iso_codes = ''
    i = 0
    for ctry2dl in country_2_dl:
        if (ctry2dl.find('/') != -1):
            if ctry2dl.split('/')[0] == 'Italy':
                df_IT = pd.read_csv('relation_IT.csv')

                search_str = unidecode.unidecode(ctry2dl.split('/')[1])
                most_similar = process.extractOne(search_str, df_IT['subregion'], scorer=fuzz.WRatio)
                output = most_similar[0]
                dl_list[i] = 'italy/' + df_IT[df_IT['subregion'] == output]['region'].values[0]

                ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

            elif ctry2dl.split('/')[0] == 'France':
                df_FR = pd.read_csv('relation_FR.csv')

                search_str = unidecode.unidecode(ctry2dl.split('/')[1])
                most_similar = process.extractOne(search_str, df_FR['subregion'], scorer=fuzz.WRatio)
                output = most_similar[0]
                dl_list[i] = 'france/' + df_FR[df_FR['subregion'] == output]['region'].values[0]

                ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

            elif ctry2dl.split('/')[0] == 'Indonesia':
                df_ID = pd.read_csv('relation_ID.csv')

                search_str = unidecode.unidecode(ctry2dl.split('/')[1])
                most_similar = process.extractOne(search_str, df_ID['subregion'], scorer=fuzz.WRatio)
                output = most_similar[0]
                dl_list[i] = 'indonesia/' + df_ID[df_ID['subregion'] == output]['region'].values[0]

                ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

            elif ctry2dl.split('/')[0] == 'India':
                df_IN = pd.read_csv('relation_IN.csv')

                search_str = unidecode.unidecode(ctry2dl.split('/')[1])
                most_similar = process.extractOne(search_str, df_IN['subregion'], scorer=fuzz.WRatio)
                output = most_similar[0]
                dl_list[i] = 'india/' + df_IN[df_IN['subregion'] == output]['region'].values[0]

                ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

            elif ctry2dl.split('/')[0] == 'Japan':
                df_JP = pd.read_csv('relation_JP.csv')

                search_str = unidecode.unidecode(ctry2dl.split('/')[1])
                most_similar = process.extractOne(search_str, df_JP['subregion'], scorer=fuzz.WRatio)
                output = most_similar[0]
                dl_list[i] = 'japan/' + df_JP[df_JP['subregion'] == output]['region'].values[0]

                ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

            elif ctry2dl.split('/')[0] == 'great-britain':

                if ctry2dl.split('/')[1] == 'england':

                    df_EN = pd.read_csv('relation_EN.csv')

                    search_str = unidecode.unidecode(ctry2dl.split('/')[2])

                    most_similar = process.extractOne(search_str, df_EN['subregion'], scorer=fuzz.WRatio)
                    output = most_similar[0]
                    dl_list[i] = 'great-britain/england/' + df_EN[df_EN['subregion'] == output]['region'].values[0]
                    ISO = df_ISO[df_ISO['country'] == dl_list[i]].index

                else:
                    search_str = unidecode.unidecode(ctry2dl)
                    most_similar = process.extractOne(search_str, df_subregion['State'], scorer=fuzz.WRatio)
                    dl_list[i] = most_similar[0]

                    ISO = df_ISO[df_ISO['country'] == most_similar[0]].index

            else:
                search_str = unidecode.unidecode(ctry2dl)
                most_similar = process.extractOne(search_str, df_subregion['State'], scorer=fuzz.WRatio)
                if most_similar[1] <= 90:
                    print('Attention low score for: {}'.format(search_str))
                    best_score = 0
                    for k in range(0, len(search_str.split(' '))):
                        most_similar_parse = process.extractOne(
                            search_str.split('/')[0] + '/' + search_str.split(' ')[k].split('/')[-1],
                            df_subregion['State'], scorer=fuzz.WRatio)
                        if best_score <= most_similar_parse[1]:
                            best_score = most_similar_parse[1]
                            best_url = most_similar_parse[0]
                    print('best match: {}'.format(best_url))
                    dl_list[i] = best_url
                else:
                    dl_list[i] = most_similar[0]

                ISO = df_ISO[df_ISO['country'] == most_similar[0]].index


        else:
            search_str = unidecode.unidecode(ctry2dl)
            most_similar = process.extractOne(search_str, df_ISO['country'], scorer=fuzz.WRatio)
            dl_list[i] = most_similar[0]

            ISO = df_ISO[df_ISO['country'] == most_similar[0]].index

        if i == dl_num -1:
            iso_codes = iso_codes + df_ISO['ISO'][ISO[0]]
        else:
            iso_codes = iso_codes + df_ISO['ISO'][ISO[0]] + '_'
        i = i + 1
    dl_list = list(set(dl_list))
    return dl_list, iso_codes
