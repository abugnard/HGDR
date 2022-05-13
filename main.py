# Import libraries
import math

import numpy as np
import show_map
from geopy.geocoders import Nominatim
import url_matcher
import webscraper
import os
import time
import datetime
import pandas as pd
import unidecode
from rapidfuzz import process, fuzz

import webscraper2
from contribution_evolution import evol_osm
from popDens100m import pop100m
from dest_manager import param_setter

# var = input("Please enter the coordinates of interest (Lat N/Lon E) [ex: 55.34 -32.32]: ")


var = '50.54567446372534 5.503536742977153'

Lat = float(var.split(' ')[0])
Lon = float(var.split(' ')[1])

if Lat >= 0 and Lon >= 0:
    print("You entered: " + str(Lat) + 'N ' + str(Lon) + 'E')

elif Lat < 0 and Lon >= 0:
    print("You entered: " + str(-Lat) + 'S ' + str(Lon) + 'E')

elif Lat < 0 and Lon < 0:
    print("You entered: " + str(-Lat) + 'S ' + str(-Lon) + 'W')

elif Lat >= 0 and Lon < 0:
    print("You entered: " + str(Lat) + 'N ' + str(-Lon) + 'W')

user_coord = (Lat, Lon)

# user_size_square = float(input("Size of the bounding box [km]: "))

user_size_square = 50  # [km]
distance = user_size_square / 2

degree = distance / (6378 * (np.pi / 180) * np.cos(user_coord[0] * np.pi / 180))

array_coord = show_map.map_html(user_coord, degree)

geolocator = Nominatim(user_agent="geoapiExercises")

array_loc = [0] * 25

country_with_subregion = ['Netherlands', 'France', 'Germany', 'Italy', 'Spain', 'Brazil', 'Canada',
                          'Poland', 'United Kingdom', 'Russia', 'Indonesia', 'India', 'Japan', 'United States',
                          'China', 'Belgium', 'Ukraine', 'Sweden', 'Norway', 'Switzerland', 'Australia', 'Czechia',
                          'Finland', 'Slovakia', 'Austria', 'Argentina', 'Mexico']

print('Processing ... ')
for i in range(0, 17):
    Latitude = str(array_coord[2 * i])
    Longitude = str(array_coord[2 * i + 1])

    location = geolocator.reverse(Latitude + "," + Longitude, language="en")

    if not (isinstance(location, type(None))):
        print(location.raw['address'])
        address = location.raw['address']
        country = address.get('country', '')

        if country == 'Spain':
            location = geolocator.reverse(Latitude + "," + Longitude, language="es")
            address = location.raw['address']
            subregion = address.get('state', '')
            if address.get('ISO3166-2-lvl4', '') == 'ES-CN':
                country = 'Canarias'
            elif address.get('ISO3166-2-lvl4') == 'ES-CN':
                country = 'Ceuta'
            elif address.get('State', '') == 'Melilla':
                country = 'Melilla'



        elif country == 'Austria':
            location = geolocator.reverse(Latitude + "," + Longitude, language="de")
            address = location.raw['address']
            subregion = address.get('state', '')
        elif country == 'Australia' and address.get('territory', '') == 'Australian Capital Territory':
            subregion = 'Australian Capital Territory'

        elif country == 'Netherlands':
            subregion = address.get('state', '')
            if address.get('ISO3166-2-lvl3', '') == 'NL-AW':
                country = 'Aruba'
            elif address.get('ISO3166-2-lvl3', '') == 'NL-CW':
                country = 'Curacao'
            elif address.get('ISO3166-2-lvl3', '') == 'NL-SX':
                country = 'Sint Maarten'

        elif country == 'France':
            subregion = address.get('state', '')
            if address.get('ISO3166-2-lvl3', '') == 'FR-BL' or address.get('ISO3166-2-lvl3', '') == 'FR-BL' or address.get('ISO3166-2-lvl6', '') == 'FR-BL':
                country = 'Saint Barthelemy'
            elif address.get('state', '') == 'Saint Martin (France)':
                country = 'Saint Martin'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-TF' or address.get('ISO3166-2-lvl3', '') == 'FR-TF' or address.get('ISO3166-2-lvl6', '') == 'FR-TF':
                country = 'France Taaf'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-MQ' or address.get('ISO3166-2-lvl3', '') == 'FR-MQ' or address.get('ISO3166-2-lvl6', '') == 'FR-MQ':
                country = 'Martinique'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-GUA' or address.get('ISO3166-2-lvl3', '') == 'FR-GP' or address.get('ISO3166-2-lvl6', '') == 'FR-GP':
                country = 'Guadeloupe'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-LRE' or address.get('ISO3166-2-lvl3', '') == 'FR-LRE' or address.get('ISO3166-2-lvl6', '') == 'FR-LRE':
                country = 'Reunion'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-MAY' or address.get('ISO3166-2-lvl3', '') == 'FR-MAY' or address.get('ISO3166-2-lvl6', '') == 'FR-MAY':
                country = 'Mayotte'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-GF' or address.get('ISO3166-2-lvl3', '') == 'FR-GF' or address.get('ISO3166-2-lvl6', '') == 'FR-GF':
                country = 'Guyane'
            elif address.get('ISO3166-2-lvl4', '') == 'FR-PF' or address.get('ISO3166-2-lvl3', '') == 'FR-PF' or address.get('ISO3166-2-lvl6', '') == 'FR-PF':
                country = 'French Polynesia'
            elif address.get('region', '') == 'Saint Pierre and Miquelon':
                country = 'Saint Pierre and Miquelon'

        elif country == 'United States':
            subregion = address.get('state', '')
            if address.get('state', '') == 'Guam':
                country = 'Guam'
            elif address.get('state', '') == 'Northern Mariana Islands':
                country = 'Northern Mariana Islands'
            elif address.get('state', '') == 'American Samoa':
                country = 'American Samoa'
            elif address.get('state', '') == 'Puerto Rico':
                country = 'Puerto Rico'
            elif address.get('state', '') == '' and address.get('county', '') == '':
                country = []
        elif country == 'Slovakia':
            location = geolocator.reverse(Latitude + "," + Longitude, language="sk")
            address = location.raw['address']
            subregion = address.get('state', '')
            subregion = subregion.replace(' kraj', '')

        elif country == 'Belgium':
            subregion = address.get('region', '') + '/' + address.get('municipality', '')

        elif country == 'Norway':
            subregion = address.get('county', '')
            city = address.get('municipality', '')
            reg = address.get('region')
            if isinstance(reg, type(None)):
                reg = ''
            if address.get('county', '') == 'Bouvet Island':
                country = 'Bouvet Island'

        elif country in ['Sweden', 'Czechia', 'Finland']:
            subregion = address.get('county', '')


        elif country in ['Palestinian Territory', 'Israel']:
            country = 'Israel and Palestine'

        elif country in ['Haiti', 'Dominican Republic']:
            country = 'Haiti-and-Domrep'

        elif country == 'Eswatini':
            country = 'Swaziland'

        elif country == 'Poland':
            location = geolocator.reverse(Latitude + "," + Longitude, language="pl")
            address = location.raw['address']
            subregion = unidecode.unidecode(address.get('state', '')).replace('wojewodztwo ', '')

        elif country == 'Brazil':
            location = geolocator.reverse(Latitude + "," + Longitude, language="pt")
            address = location.raw['address']
            subregion = address.get('region', '').replace('Região ', '')
        elif country == 'Japan':
            subregion = address.get('province', '')
        elif country == 'United States':
            subregion = address.get('state', '')
            subregion = subregion.replace('United States Virgin Islands', 'us-virgin-island')
        elif country == 'Germany':
            location = geolocator.reverse(Latitude + "," + Longitude, language="de")
            address = location.raw['address']
            subregion = address.get('state', '')
        elif country == 'United Kingdom':
            if address.get('state', '') == 'England':
                subregion = 'england/' + address.get('county', '')
                if address.get('county', '') == '':
                    if address.get('archipelago', '') == 'Isles of Scilly':
                        subregion = 'england/cornwall'
                    elif address.get('city', '') == 'Southend-on-Sea':
                        subregion = 'england/essex'
                    elif address.get('state_district', '') == 'Greater London':
                        subregion = 'england/greater-london'
                    elif address.get('city', '') == 'Southampton':
                        subregion = 'england/hampshire'
                    elif address.get('city', '') == 'Nottingham':
                        subregion = 'england/nottinghamshire'
                    elif address.get('state_district', '') == 'Yorkshire and the Humber':
                        subregion = 'england/south-yorkshire'
                    elif address.get('city', '') == '':
                        subregion = ''
                    else:
                        subregion = 'england/merseyside'
            else:
                subregion = address.get('state', '')

        else:
            subregion = address.get('state', '')

        county = address.get('county', '')
        region = address.get('region', '')
    else:
        country = []

    if country in country_with_subregion and len(subregion) != 0:
        if country == 'France':
            array_loc[i] = country + '/' + county
            if county == 'South Corsica':
                array_loc[i] = 'France/Haute-Corse'
        elif country == 'Russia':
            array_loc[i] = country + '/' + region
        elif country == 'United States':
            array_loc[i] = 'us/' + subregion
        elif country == 'United Kingdom':
            if subregion == 'Northern Ireland':
                array_loc[i] = 'Ireland'
            else:
                array_loc[i] = 'great-britain/' + subregion

        else:
            array_loc[i] = country + '/' + subregion

    elif country in country_with_subregion and len(subregion) == 0:
        array_loc[i] = None
        if country == 'Norway':
            array_loc[i] = country + '/' + subregion + '/' + city + '/' + reg
    else:
        array_loc[i] = country
        print(country)
subregion = []
array_loc = filter(None, array_loc)
country_2_dl = list(set(array_loc))
print('...')
print('Searching for contribution data...')
print('...')
evol_osm(country_2_dl)

print(country_2_dl)
print("\nFinding corresponding country URL's...\n...")

list_scraper2 = ['Belgium', 'Anguilla', 'Trinidad and Tobago', 'Montserrat', 'British Virgin Islands', 'Barbados',
                 'Cayman Islands', 'Antigua and Barbuda', 'Falkland Islands', 'Guyana', 'Australia', 'San Marino',
                 'South Georgia and the South Sandwich Islands', 'Grenada', 'Saint Kitts and Nevis', 'China',
                 'Vatican City', 'Bermuda', 'Aruba', 'Curacao', 'Ukraine', 'Switzerland', 'Sweden', 'Norway',
                 'Czechia', 'Finland', 'Slovakia', 'Austria', 'Argentina', 'Sint Maarten', 'Turks and Caicos Islands',
                 'Saint Vincent and the Grenadines', 'Saint Lucia', 'Saint Barthelemy', 'Saint Martin', 'France Taaf',
                 'Guam', 'Northern Mariana Islands', 'American Samoa', 'Bouvet Island', 'Guadeloupe', 'Martinique',
                 'Guyane', 'Reunion', 'Mayotte', 'Puerto Rico', 'Kuwait', 'Bahrain', 'Qatar', 'United Arab Emirates',
                 'Oman', 'Saudi Arabia', 'Brunei', 'Malaysia', 'Singapore', 'Gibraltar', 'French Polynesia', 'Dominica',
                 'Haiti', 'Dominican Republic', 'Guernsey', 'Jersey', 'Mexico', 'Canarias','Ceuta', 'Melilla',
                 'British Indian Ocean Territory']



land_list = []
for land in country_2_dl:
    land = land.split('/')[0]
    land_list.append(land)

points = [z for z in zip(land_list) if z[0] in list_scraper2]

list_temp = []
for i in range(0, len(points)):
    list_temp.append(str(points[i])[2:-3])
print(country_2_dl)
list_ws1 = [x for x in country_2_dl if x.split('/')[0] not in list_temp]
print('From GeoFabrik: ')
print(list_ws1)

list_ws2 = [x for x in country_2_dl if x.split('/')[0] in list_temp]
print('From OSM.download: ')
print(list_ws2)

dl_list, ISO_str1 = url_matcher.find_correspondence(list_ws1)

print('Webscrapping...\n...')
print(
    '\n\nList of country/country-region to download from GeoFabrik:\n------------------------------------------------------------')
link1, size_MB1 = webscraper.find_link(dl_list)
link2, size_MB2, ISO_str2 = webscraper2.find_link(list_ws2, len(list_ws1))

ISO_str = ISO_str1 + ISO_str2
link = link1 + link2
size_MB = size_MB1 + size_MB2

param_geom = ' --GEOM "' + str(array_coord[3]) + ' ' + str(array_coord[6]) + ' ' + str(array_coord[5]) + ' ' + str(
    array_coord[2]) + '"'
param_ISO = ' --ISO_code "' + ISO_str + '"'
source_dens = ' --SourceDataset_GEOTIFF "C:\\Users\\alexandre\\PycharmProjects\\HGDR_geoFabrik\\ppp_2020_1km_Aggregated.tif"'
dest_dens = ' --DestDataset_GEOTIFF "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '02_PopDens"'
dest_dens_txt = ' --DestDataset_TEXTLINE "C:\\Users\\alexandre\\PycharmProjects\\HGDR_geoFabrik\\pop_dens_result.txt"'
fme_path = 'fme.exe C:\\Users\\alexandre\\Documents\\HDR\\popDens_tif2tif.fmw'

command_dens_ws = fme_path + source_dens + dest_dens + dest_dens_txt + param_ISO + param_geom
print(command_dens_ws)
os.system(command_dens_ws)
with open('pop_dens_result.txt') as f:
    lines = f.readlines()

pop_dens = float(lines[0][3:9])
print('\nPopulation density of the selected region: {} [capita/km2]'.format(
    round(pop_dens * (1e6 / (926 * 927 * np.cos(user_coord[0] * np.pi / 180))), 1)))

size_coef = 1.57  # [s/MB] for the basic features (building highway place boundary)
dens_coeff = 0.075  # [s km2/capita] for the basic features (building highway place boundary)

df_features = pd.read_csv('feature_factor.csv', sep=',')

basis = df_features['coef'][0] + df_features['coef'][2] + df_features['coef'][15] + df_features['coef'][22] + \
        df_features['coef'][23]

df_features['relative2basis'] = df_features['coef'] / basis

feature_choice = ['place', 'building', 'highway', 'boundary']
features_all = ['aerialway', 'building', 'historic', 'natural', 'railway', 'waterway', 'aeroway', 'craft', 'landuse',
                'office', 'route', 'amenity', 'emergency', 'leisure', 'place', 'shop', 'barrier', 'geological',
                'man_made', 'power', 'sport', 'boundary', 'highway', 'military', 'public_transport', 'tourism']

comp_time_factor = df_features['relative2basis'][0]

for i in range(0, len(feature_choice)):
    pos = features_all.index(feature_choice[i])
    comp_time_factor = comp_time_factor + df_features['relative2basis'][pos + 1]

print('\n----------------------------------------\n----------------------------------------')
print('Size of the downloaded data: {} MB'.format(np.sum(size_MB)))
print('Estimated time for OSM data extraction: {}h and {}min'.format(str(datetime.timedelta(seconds=((np.sum(size_MB) *
                                                                                                      size_coef) + (
                                                                                                             pop_dens *
                                                                                                             dens_coeff))
                                                                                                    * comp_time_factor))[
                                                                         0],
                                                                     str(datetime.timedelta(seconds=((np.sum(size_MB) *
                                                                                                      size_coef) + (
                                                                                                             pop_dens *
                                                                                                             dens_coeff))
                                                                                                    * comp_time_factor))[
                                                                     2:4]))
print('----------------------------------------\n----------------------------------------\n')

time_start = time.time()

# features available:

# ______________________________________________________________________________
# | aerialway | building   | historic  | natural          | railway | waterway |
# |___________|____________|___________|_________________ |_________|__________|
# | aeroway   | craft      | landuse   | office           | route   |
# |___________|____________|___________|_________________ |_________|
# | amenity   | emergency  | leisure   | place            | shop    |
# |___________|____________|___________|_________________ |_________|
# | barrier   | geological | man_made  | power            | sport   |
# |___________|____________|___________|_________________ |_________|
# | boundary  | highway    | military  | public_transport | tourism |
# __________________________________________________________________|


param_layer = ' --FEATURETYPES "building highway boundary place"'
param_link = '"'

# for i in range(0, len(country_2_dl)):
#
#     link_i = link[i]
#     param_link1 = ' --URL_DL_1 "' + link_i + '"'
#     param_link2 = ' --URL_DL_2 "' + link_i + '"'
#     param_link3 = ' --URL_DL_3 "' + link_i + '"'
#     param_link4 = ' --URL_DL_4 "' + link_i + '"'

param_link1, param_link2, param_link3, param_link4, param_link5, param_link6, param_link7, param_link8 = param_setter(
    link)
data_writers = {'Feature': ['aerialway', 'building', 'historic', 'natural', 'railway', 'waterway',
                            'aeroway', 'craft', 'landuse', 'office', 'route', 'amenity', 'emergency',
                            'leisure', 'place', 'shop', 'barrier', 'geological', 'man_made', 'power',
                            'sport', 'boundary', 'highway', 'military', 'public_transport', 'tourism'],
                'Dest_num': ['', '_37', '_43', '_34', '_42', '_52', '_41', '_35', '_51', '_36', '_44', '_53', '_39',
                             '_55',
                             '_45', '_46', '_31', '_47', '_30', '_38', '_48', '_57', '_54', '_32', '_40', '_50']}

df_writers = pd.DataFrame(data_writers)

str_writers = ''
for i in range(0, len(df_writers)):
    str_writers = str_writers + ' --DestDataset_SHAPEFILE' + df_writers['Dest_num'][
        i] + ' "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + df_writers['Feature'][i] + '"'

str_summary = ' --DestDataset_TEXTLINE "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '00_SUMMARY\\summary_features.txt"'

# param_dest1 = ' --DestDataset_SHAPEFILE "C:\\Users\\alexandre\\Documents\\HDR\\output_tuvalu\\Line"'
# param_dest2 = ' --DestDataset_SHAPEFILE_5 "C:\\Users\\alexandre\\Documents\\HDR\\output_tuvalu\\Polygone"'
# param_dest3 = ' --DestDataset_SHAPEFILE_4 "C:\\Users\\alexandre\\Documents\\HDR\\output_tuvalu\\Point"'
# param_geom = r' --GEOM "<lt>?xml<space>version=<quote>1.0<quote><space>encoding=<quote>US_ASCII<quote><space' \
#                  r'>standalone=<quote>no<quote><space>?<gt><lt>geometry<gt><lt>polygon<gt><lt>line<gt><lt>coord<space>x' \
#                  r'=<quote>' + str(array_coord[3]) + '<quote><space>y=<quote>' + str(array_coord[6]) + \
#                  r'<quote><solidus><gt><lt>coord<space>x=<quote>' + str(array_coord[7]) + r'<quote><space>y=<quote>' + str(
#             array_coord[6]) + r'<quote><solidus><gt><lt>coord<space>x=<quote>' + str(array_coord[7]) + \
#                  r'<quote><space>y=<quote>' + str(array_coord[2]) + r'<quote><solidus><gt><lt>coord<space>x=<quote>' + str(
#             array_coord[3]) + r'<quote><space>y=<quote>' + str(array_coord[2]) + \
#                  r'<quote><solidus><gt><lt>coord<space>x=<quote>' + str(array_coord[3]) + r'<quote><space>y=<quote>' + str(
#             array_coord[6]) + r'<quote><solidus><gt><lt><solidus>line<gt><lt><solidus>polygon<gt><lt><solidus>geometry<gt>"'

fme_path = 'fme.exe C:\\Users\\alexandre\\Documents\\HDR\\OSM_basic_v1_2.fmw'
full_path = fme_path + param_layer + param_link1 + param_link2 + param_link3 + param_link4 + param_link5 + \
            param_link6 + param_link7 + param_link8 + param_ISO + param_geom + str_writers + str_summary

print('------------------------\n------------------------\n')
print(full_path)
print('------------------------\n------------------------\n')

os.system(full_path)

time_end = time.time()
elapsed_time = float(time_end) - float(time_start)
elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
print('\n\nElapsed time for OSM data: {} hours, {} min, {} sec'.format(elapsed_time[0:2], elapsed_time[3:5],
                                                                       elapsed_time[6:9]))
print('Density: {} [capita/km2]'.format(pop_dens * (1e6 / (926 * 927 * np.cos(user_coord[0] * np.pi / 180)))))
print('Total size {} [MB]'.format(np.sum(size_MB)))
print('\n-------------------------------------------------------\n')

URL_list_100m, year_100m = pop100m(country_2_dl)

# https://community.safe.com/s/question/0D54Q00008515Q1SAI/fme-python-install-paramiko-expected-an-even-number-of-command-line-arguments-instead-got-9

fme_path = 'fme.exe C:\\Users\\alexandre\\Documents\\HDR\\popDens100m_tif2tif.fmw'

dest100m = ' --DestDataset_GEOTIFF "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '02_PopDens"'

param_link1, param_link2, param_link3, param_link4, param_link5, param_link6, param_link7, param_link8 = param_setter(
    URL_list_100m)

year_100m = ' --year_last "' + year_100m + '"'

command_dens_100m = fme_path + param_link1 + param_link2 + param_link3 + param_link4 + param_link5 + param_link6 + \
                    param_link7 + param_link8 + param_ISO + param_geom + dest100m + year_100m

df_area = pd.read_csv('country_area.csv', sep=';').dropna()
df_area = df_area.drop_duplicates(subset='Country', keep="first")

area = 0
for ctry in list(set(list_ws1 + list_ws2)):
    search_str = ctry.split('/')[0]
    most_similar = process.extractOne(search_str, df_area['Country'], scorer=fuzz.WRatio)
    area = area + float(df_area[df_area['Country'] == most_similar[0]]['Area'])

time_WP = 0.00034 * area

print('Estimated time for extraction (total area of {} km2): {} [s]\n\n'.format(area, round(time_WP, -1)))
# sizeMB = surfacekm2/54'301
print(command_dens_100m)
time_start = time.time()
os.system(command_dens_100m)
time_end = time.time()
elapsed_time = float(time_end) - float(time_start)
elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
print('\n\nElapsed time for pop. density: {} hours, {} min, {} sec'.format(elapsed_time[0:2], elapsed_time[3:5],
                                                                           elapsed_time[6:9]))

# C:\Users\alexandre\AppData\Local\Temp
