import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import dateutil.parser as dparser
from rapidfuzz import process, fuzz
import unidecode


def find_link(country_2_dl, size_ws1):
    iso_codes = ''
    df_ISO = pd.read_csv('country_available_ISO.csv', sep=';')
    dl_list = [0] * len(country_2_dl)
    link = [0] * len(country_2_dl)
    iso_add = [0] * len(country_2_dl)
    i = 0

    for ctry in country_2_dl:
        if ctry.split('/')[0] == 'Belgium':
            if ctry.split('/')[1] == 'Wallonia':
                german_wallonia = ['Saint Vith', 'Büllingen', 'Eupen', 'Kelmis', 'Lontzen', 'Raeren', 'Amel',
                                   'Büllingen', 'Burg-Reuland', 'Bütgenbach']
                if ctry.split('/')[2] in german_wallonia or ctry.split('/')[3] in german_wallonia:
                    dl_list[i] = 'extracts/europe/belgium/wallonia_german_community'
                    link[i] = 'https://download.openstreetmap.fr/extracts/europe/belgium/wallonia_german_community-latest.osm.pbf'
                    iso_add[i] = 'BE_gw'
                else:
                    dl_list[i] = 'extracts/europe/belgium/wallonia_french_community'
                    link[i] = 'https://download.openstreetmap.fr/extracts/europe/belgium/wallonia_french_community-latest.osm.pbf'
                    iso_add[i] = 'BE_fw'

            elif ctry.split('/')[1] in ['Brussels-Capital']:
                dl_list[i] = 'extracts/europe/belgium/brussels_capital_region'
                link[
                    i] = 'https://download.openstreetmap.fr/extracts/europe/belgium/brussels_capital_region-latest.osm.pbf'
                iso_add[i] = 'BE_bc'

            elif ctry.split('/')[1] in ['Flanders']:
                dl_list[i] = 'extracts/europe/belgium/flanders'
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/belgium/flanders-latest.osm.pbf'
                iso_add[i] = 'BE_fl'

        elif ctry.split('/')[0] == 'Mexico':
            df_CN = pd.read_csv('subregion3.csv')
            if ctry == 'Mexico/Lower California South':
                ctry = 'mexico/baja_california_sur'
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/north-america/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/north-america/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'MX'

        elif ctry.split('/')[0] == 'us-west':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/north-america/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/north-america/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'US'

        elif ctry in ['Kuwait', 'Bahrain', 'Qatar', 'United Arab Emirates', 'Oman', 'Saudi Arabia', 'Brunei', 'Malaysia', 'Singapore']:
            dl_list[i] = 'extracts/asia/' + ctry.lower().replace(' ', '_')
            link[i] = 'https://download.openstreetmap.fr/extracts/asia/' + ctry.lower().replace(' ', '_') + '-latest.osm.pbf'
            search_str = unidecode.unidecode(ctry)
            most_similar = process.extractOne(search_str, df_ISO['country'], scorer=fuzz.WRatio)
            ISO = df_ISO[df_ISO['country'] == most_similar[0]].index
            iso_add[i] = df_ISO['ISO'][ISO[0]]

        elif ctry == 'Gibraltar':
            dl_list[i] = 'extracts/europe/gibraltar'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/gibraltar-latest.osm.pbf'
            iso_add[i] = 'GI'

        elif ctry.split('/')[0] == 'Anguilla':
            dl_list[i] = 'extracts/central-america/anguilla'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/anguilla-latest.osm.pbf'
            iso_add[i] = 'AI'

        elif ctry.split('/')[0] == 'Trinidad and Tobago':
            dl_list[i] = 'extracts/central-america/trinidad_and_tobago'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/trinidad_and_tobago-latest.osm.pbf'
            iso_add[i] = 'TT'

        elif ctry.split('/')[0] == 'Guernsey':
            dl_list[i] = 'extracts/europe/guernesey'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/guernesey-latest.osm.pbf'
            iso_add[i] = 'GE'

        elif ctry.split('/')[0] == 'Jersey' :
            dl_list[i] = 'extracts/central-america/montserrat'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/jersey-latest.osm.pbf'
            iso_add[i] = 'JE'

        elif ctry.split('/')[0] == 'Montserrat':
            dl_list[i] = 'extracts/central-america/montserrat'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/montserrat-latest.osm.pbf'
            iso_add[i] = 'MS'

        elif ctry.split('/')[0] == 'Barbados':
            dl_list[i] = 'extracts/central-america/barbados'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/barbados-latest.osm.pbf'
            iso_add[i] = 'BB'

        elif ctry.split('/')[0] in ['Canarias', 'Ceuta', 'Melilla']:
            dl_list[i] = 'extracts/africa/spain/' + ctry.split('/')[0].lower()
            link[i] = 'https://download.openstreetmap.fr/extracts/africa/spain/' + ctry.split('/')[0].lower() + '-latest.osm.pbf'
            iso_add[i] = 'ES'

        elif ctry.split('/')[0] == 'British Virgin Islands':
            dl_list[i] = 'extracts/central-america/british_virgin_islands'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/british_virgin_islands-latest.osm.pbf'
            iso_add[i] = 'VG'

        elif ctry.split('/')[0] == 'British Indian Ocean Territory':
            dl_list[i] = 'extracts/asia/british_indian_ocean_territory'
            link[i] = 'https://download.openstreetmap.fr/extracts/asia/british_indian_ocean_territory-latest-latest.osm.pbf'
            iso_add[i] = 'IO'

        elif ctry.split('/')[0] == 'Antigua and Barbuda':
            dl_list[i] = 'extracts/central-america/antigua_and_barbuda'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/antigua_and_barbuda-latest.osm.pbf'
            iso_add[i] = 'AG'

        elif ctry.split('/')[0] == 'Cayman Islands':
            dl_list[i] = 'extracts/central-america/cayman_islands'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/cayman_islands-latest.osm.pbf'
            iso_add[i] = 'KY'

        elif ctry.split('/')[0] == 'Grenada':
            dl_list[i] = 'extracts/central-america/grenada'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/grenada-latest.osm.pbf'
            iso_add[i] = 'GD'

        elif ctry.split('/')[0] == 'Saint Kitts and Nevis':
            dl_list[i] = 'extracts/central-america/saint_kitts_and_nevis'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/saint_kitts_and_nevis-latest.osm.pbf'
            iso_add[i] = 'KN'

        elif ctry.split('/')[0] == 'Falkland Islands':
            dl_list[i] = 'extracts/south-america/falkland'
            link[i] = 'https://download.openstreetmap.fr/extracts/south-america/falkland-latest.osm.pbf'
            iso_add[i] = 'FK'

        elif ctry.split('/')[0] == 'Bermuda':
            dl_list[i] = 'extracts/north-america/bermuda'
            link[i] = 'https://download.openstreetmap.fr/extracts/north-america/bermuda-latest.osm.pbf'
            iso_add[i] = 'BM'

        elif ctry.split('/')[0] == 'Puerto Rico':
            dl_list[i] = 'extracts/central-america/puerto_rico'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/puerto_rico-latest.osm.pbf'
            iso_add[i] = 'PR'

        elif ctry.split('/')[0] == 'Turks and Caicos Islands':
            dl_list[i] = 'extracts/central-america/turks_and_caicos_islands'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/turks_and_caicos_islands-latest.osm.pbf'
            iso_add[i] = 'TC'

        elif ctry.split('/')[0] == 'Aruba':
            dl_list[i] = 'extracts/central-america/aruba'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/aruba-latest.osm.pbf'
            iso_add[i] = 'AW'

        elif ctry.split('/')[0] == 'Curacao':
            dl_list[i] = 'extracts/central-america/curacao'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/curacao-latest.osm.pbf'
            iso_add[i] = 'CW'

        elif ctry.split('/')[0] == 'Sint Maarten':
            dl_list[i] = 'extracts/central-america/sint_maarten'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/sint_maarten-latest.osm.pbf'
            iso_add[i] = 'SX'

        elif ctry.split('/')[0] == 'Saint Barthelemy':
            dl_list[i] = 'extracts/central-america/saint_barthelemy'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/saint_barthelemy-latest.osm.pbf'
            iso_add[i] = 'BL'

        elif ctry.split('/')[0] == 'Saint Vincent and the Grenadines':
            dl_list[i] = 'extracts/central-america/saint_vincent_and_the_grenadines'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/saint_vincent_and_the_grenadines-latest.osm.pbf'
            iso_add[i] = 'VC'

        elif ctry.split('/')[0] == 'Saint Martin':
            dl_list[i] = 'extracts/central-america/saint_martin'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/saint_martin-latest.osm.pbf'
            iso_add[i] = 'MF'

        elif ctry.split('/')[0] == 'Saint Lucia':
            dl_list[i] = 'extracts/central-america/saint_lucia'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/saint_lucia-latest.osm.pbf'
            iso_add[i] = 'LC'

        elif ctry.split('/')[0] == 'France Taaf':
            dl_list[i] = 'extracts/merge/france_taaf'
            link[i] = 'https://download.openstreetmap.fr/extracts/merge/france_taaf-latest.osm.pbf'
            iso_add[i] = 'TF'

        elif ctry.split('/')[0] == 'Mayotte':
            dl_list[i] = 'extracts/africa/mayotte'
            link[i] = 'https://download.openstreetmap.fr/extracts/africa/mayotte-latest.osm.pbf'
            iso_add[i] = 'YT'

        elif ctry.split('/')[0] == 'Guyane':
            dl_list[i] = 'extracts/south-america/guyane'
            link[i] = 'https://download.openstreetmap.fr/extracts/south-america/guyane-latest.osm.pbf'
            iso_add[i] = 'GF'

        elif ctry.split('/')[0] == 'Martinique':
            dl_list[i] = 'extracts/central-america/martinique'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/martinique-latest.osm.pbf'
            iso_add[i] = 'MQ'

        elif ctry.split('/')[0] == 'Guadeloupe':
            dl_list[i] = 'extracts/central-america/guadeloupe'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/guadeloupe-latest.osm.pbf'
            iso_add[i] = 'GP'

        elif ctry.split('/')[0] == 'Reunion':
            dl_list[i] = 'extracts/africa/reunion'
            link[i] = 'https://download.openstreetmap.fr/extracts/africa/reunion-latest.osm.pbf'
            iso_add[i] = 'RE'

        elif ctry.split('/')[0] == 'Saint Pierre and Miquelon':
            dl_list[i] = 'extracts/north-america/saint_pierre_et_miquelon'
            link[i] = 'https://download.openstreetmap.fr/extracts/north-america/saint_pierre_et_miquelon-latest.osm.pbf'
            iso_add[i] = 'PM'

        elif ctry.split('/')[0] == 'Guam':
            dl_list[i] = 'extracts/oceania/guam'
            link[i] = 'https://download.openstreetmap.fr/extracts/oceania/guam-latest.osm.pbf'
            iso_add[i] = 'GU'

        elif ctry.split('/')[0] == 'French Polynesia':
            dl_list[i] = 'extracts/oceania/polynesie'
            link[i] = 'https://download.openstreetmap.fr/extracts/oceania/polynesie.osm.pbf'
            iso_add[i] = 'PF'

        elif ctry.split('/')[0] == 'Northern Mariana Islands':
            dl_list[i] = 'extracts/oceania/northern_mariana_islands'
            link[i] = 'https://download.openstreetmap.fr/extracts/oceania/northern_mariana_islands-latest.osm.pbf'
            iso_add[i] = 'MP'

        elif ctry.split('/')[0] == 'Dominica':
            dl_list[i] = 'extracts/central-america/dominica'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/dominica-latest.osm.pbf'
            iso_add[i] = 'DM'

        elif ctry.split('/')[0] == 'Haiti':
            dl_list[i] = 'extracts/central-america/haiti'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/haiti.osm.pbf'
            iso_add[i] = 'HI'

        elif ctry.split('/')[0] == 'Dominican Republic':
            dl_list[i] = 'extracts/central-america/dominican_republic'
            link[i] = 'https://download.openstreetmap.fr/extracts/central-america/dominican_republic.osm.pbf'
            iso_add[i] = 'DR'

        elif ctry.split('/')[0] == 'American Samoa':
            dl_list[i] = 'extracts/oceania/american_samoa'
            link[i] = 'https://download.openstreetmap.fr/extracts/oceania/american_samoa-latest.osm.pbf'
            iso_add[i] = 'AS'

        elif ctry.split('/')[0] == 'Guyana':
            dl_list[i] = 'extracts/south-america/guyana'
            link[i] = 'https://download.openstreetmap.fr/extracts/south-america/guyana-latest.osm.pbf'
            iso_add[i] = 'GY'

        elif ctry.split('/')[0] == 'Bouvet Island':
            dl_list[i] = 'extracts/africa/bouvet_island'
            link[i] = 'https://download.openstreetmap.fr/extracts/africa/bouvet_island-latest.osm.pbf'
            iso_add[i] = 'NO'

        elif ctry.split('/')[0] == 'South Georgia and the South Sandwich Islands':
            dl_list[i] = 'extracts/south-america/south_georgia_and_south_sandwich'
            link[i] = 'https://download.openstreetmap.fr/extracts/south-america/south_georgia_and_south_sandwich-latest.osm.pbf	'
            iso_add[i] = 'GS'

        elif ctry.split('/')[0] == 'China':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/asia/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/asia/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'CN'
        elif ctry.split('/')[0] == 'Australia':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/oceania/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/oceania/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'AU'
        elif ctry.split('/')[0] == 'San Marino':
            dl_list[i] = 'extracts/europe/san_marino'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/san_marino-latest.osm.pbf'
            iso_add[i] = 'SM'

        elif ctry.split('/')[0] == 'Vatican City':
            dl_list[i] = 'extracts/europe/vatican_city'
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/vatican_city-latest.osm.pbf'
            iso_add[i] = 'VA'

        elif ctry.split('/')[0] == 'Ukraine':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'UA'

        elif ctry.split('/')[0] == 'Argentina':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry.replace(' Province','')
            if search_str == 'Argentina/Autonomous City of Buenos Aires':
                search_str = 'Argentina/buenos_aires_city'
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/south-america/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/south-america/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'AR'

        elif ctry.split('/')[0] == 'Switzerland':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'CH'

        elif ctry.split('/')[0] == 'Finland':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'FI'

        elif ctry.split('/')[0] == 'Slovakia':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'SK'

        elif ctry.split('/')[0] == 'Austria':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'AT'

        elif ctry.split('/')[0] == 'Sweden':
            print(ctry)
            df_CN = pd.read_csv('subregion3.csv')
            search_str = ctry
            if search_str == 'Sweden/Dalecarlia':
                search_str = 'Dalarna'

            search_str = search_str.replace('County', '')
            print(search_str)
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'SW'

        elif ctry.split('/')[0] == 'Czechia':

            df_CN = pd.read_csv('subregion3.csv')
            search_str = 'czech_republic' + ctry.split('/')[-1]
            if search_str == 'czech_republic/Central Bohemia':
                search_str = 'czech_republic/stredocesky'
            elif search_str == 'czech_republic/Olomouc Region':
                search_str = 'czech_republic/olomoucky'
            elif search_str == 'czech_republic/':
                search_str = 'czech_republic/praha'

            search_str = search_str.replace(' Kraj', '')
            search_str = search_str.replace(' kraj', '')
            search_str = search_str.replace('Kraj ', '')
            search_str = search_str.replace('kraj ', '')


            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'CZ'

        elif ctry.split('/')[0] == 'Norway':
            df_CN = pd.read_csv('subregion3.csv')
            search_str = '/'.join(ctry.split('/')[0:2])
            most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
            dl_list[i] = 'extracts/europe/' + most_similar[0]
            link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
            iso_add[i] = 'NO'

            if ctry.split('/')[-1] == 'Svalbard':
                dl_list[i] = 'extracts/europe/norway/svalbard'
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/norway/svalbard-latest.osm.pbf'
                iso_add[i] = 'NO'
            elif ctry.split('/')[2:3] == 'Oslo':
                dl_list[i] = 'extracts/europe/norway/oslo'
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/norway/oslo-latest.osm.pbf'
                iso_add[i] = 'NO'
            elif search_str == 'Norway/Vestfold og Telemark':
                search_str = 'Norway/Vestfold'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list[i] = 'extracts/europe/' + most_similar[0]
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
                iso_add[i] = 'NO'
                search_str = 'Norway/Telemark'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list.append('extracts/europe/' + most_similar[0])
                link.append('https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf')
                iso_add.append('NO')
            elif search_str == 'Norway/Troms og Finnmark':
                search_str = 'Norway/Troms'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list[i] = 'extracts/europe/' + most_similar[0]
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
                iso_add[i] = 'NO'
                search_str = 'Norway/Finnmark'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list.append('extracts/europe/' + most_similar[0])
                link.append('https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf')
                iso_add.append('NO')
            elif search_str == 'Norway/Viken':
                search_str = 'Norway/Akershus'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list[i] = 'extracts/europe/' + most_similar[0]
                link[i] = 'https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf'
                iso_add[i] = 'NO'
                search_str = 'Norway/Buskerud'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list.append('extracts/europe/' + most_similar[0])
                link.append('https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf')
                iso_add.append('NO')
                search_str = 'Norway/Oestfold'
                most_similar = process.extractOne(search_str, df_CN['State'], scorer=fuzz.WRatio)
                dl_list.append('extracts/europe/' + most_similar[0])
                link.append('https://download.openstreetmap.fr/extracts/europe/' + most_similar[0] + '-latest.osm.pbf')
                iso_add.append('NO')

        i = i + 1

    dl_list = list(set(dl_list))
    link = list(set(link))
    # region = ['extracts/europe/Belgium/brussels_capital_region','extracts/central-america/anguilla','extracts/asia/china/anhui','extracts/central-america/british_virgin_islands']
    size_list = []
    update_list = []

    i = 0
    print(
        '\nList of country/country-region to download from OSM extracts:\n------------------------------------------------------------')
    for s in dl_list:

        URL_region = 'https://download.openstreetmap.fr/' + '/'.join(s.lower().split('/')[0:-1]) + '/'

        r = requests.get(URL_region)
        page_body = r.text
        soup = BeautifulSoup(page_body, 'html.parser')
        index_found = str(soup).find(s.lower().split('/')[-1] + '-latest.osm.pbf</a></td><td align="right">')
        info = str(soup)[index_found + len('-latest.osm.pbf</a></td><td align="right">'): index_found + len(
            '-latest.osm.pbf</a></td><td align="right">') + 100]
        update = re.findall("\d\d\d\d.\d\d.\d\d \d\d.\d\d", info)
        size = re.findall("\d\d[KMG]|\d\d\d[KMG]|\d.\d[KMG]", info)[-1]
        size_float = float(size[:-1])
        if size[-1] == 'K':
            size_float = size_float / 1000
        elif size[-1] == 'G':
            size_float = size_float * 1000

        print('{}) {}'.format(i + 1 + size_ws1, s))
        print('/'.join(link[i].split('/')[0:-1]))
        print("Last Update the " + update[0])
        print('...............................................\n')

        size_list.append(size_float)

        update_list.append(update)
        if i == 0:
            iso_codes = '_' + iso_add[i] + '_'
        elif i == len(dl_list) - 1:
            iso_codes = iso_codes + iso_add[i]
        else:
            iso_codes = iso_codes + iso_add[i] + '_'
        i = i + 1
    print('Links for download (download.openstreetmap.fr)\n------------------')

    for k in range(0, len(dl_list)):

        print('{}) {}'.format(k + 1 + size_ws1, link[k]))
        print('File size: {} [MB]\n'.format(size_list[k]))

    return link, size_list, iso_codes
