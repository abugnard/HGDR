# Import libraries
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

# var = input("Please enter the coordinates of interest (Lat N/Lon E) [ex: 55.34 -32.32]: ")

var = '50 5'

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
                          'Poland', 'United Kingdom', 'Russia', 'Indonesia', 'India', 'Japan', 'United States']

print('\n\nList of country/country-region to download:\n----------------------')
for i in range(0, 17):
    Latitude = str(array_coord[2 * i])
    Longitude = str(array_coord[2 * i + 1])

    location = geolocator.reverse(Latitude + "," + Longitude, language="en")
    if not (isinstance(location, type(None))):
        address = location.raw['address']
        country = address.get('country', '')
        if country == 'Spain':
            location = geolocator.reverse(Latitude + "," + Longitude, language="es")
            address = location.raw['address']
            subregion = address.get('state', '')

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
        elif country == 'Russia':
            array_loc[i] = country + '/' + region
        elif country == 'United States':
            array_loc[i] = 'us/' + subregion
        elif country == 'United Kingdom':
            array_loc[i] = 'great-britain/' + subregion
        else:
            array_loc[i] = country + '/' + subregion

    elif country in country_with_subregion and len(subregion) == 0:
        array_loc[i] = None
    else:
        array_loc[i] = country

subregion = []
array_loc = filter(None, array_loc)
country_2_dl = list(set(array_loc))

dl_list, ISO_str = url_matcher.find_correspondence(country_2_dl)

link, size_MB = webscraper.find_link(dl_list)

size_coef = 3.5  # [s/MB] for the basic features (building highway place boundary)

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
print('Estimated time for extraction: {}h and {}min'.format(str(datetime.timedelta(seconds=np.sum(size_MB) *
                                                                                           size_coef * comp_time_factor))[
                                                                0],
                                                            str(datetime.timedelta(seconds=np.sum(size_MB) *
                                                                                           size_coef * comp_time_factor))[
                                                            2:4]))
print('----------------------------------------\n----------------------------------------\n')

time_start = time.time()

fme_path = 'fme.exe C:\\Users\\alexandre\\Documents\\HDR\\OSM_basic_v1_2.fmw'

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

param_geom = ' --GEOM "' + str(array_coord[3]) + ' ' + str(array_coord[6]) + ' ' + str(array_coord[5]) + ' ' + str(
    array_coord[2]) + '"'
param_ISO = ' --ISO_code "' + ISO_str + '"'

# for i in range(0, len(country_2_dl)):
#
#     link_i = link[i]
#     param_link1 = ' --URL_DL_1 "' + link_i + '"'
#     param_link2 = ' --URL_DL_2 "' + link_i + '"'
#     param_link3 = ' --URL_DL_3 "' + link_i + '"'
#     param_link4 = ' --URL_DL_4 "' + link_i + '"'

if not link:
    print('No data in this area.')
    exit()

param_link1 = ' --URL_DL_1 "' + link[0] + '"'
param_link2 = ' --URL_DL_2 "' + link[0] + '"'
param_link3 = ' --URL_DL_3 "' + link[0] + '"'
param_link4 = ' --URL_DL_4 "' + link[0] + '"'
param_link5 = ' --URL_DL_5 "' + link[0] + '"'
param_link6 = ' --URL_DL_6 "' + link[0] + '"'
param_link7 = ' --URL_DL_7 "' + link[0] + '"'
param_link8 = ' --URL_DL_8 "' + link[0] + '"'

if len(link) == 2:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
if len(link) == 3:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
if len(link) == 4:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
    param_link4 = ' --URL_DL_4 "' + link[3] + '"'
if len(link) == 5:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
    param_link4 = ' --URL_DL_4 "' + link[3] + '"'
    param_link5 = ' --URL_DL_5 "' + link[4] + '"'
if len(link) == 6:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
    param_link4 = ' --URL_DL_4 "' + link[3] + '"'
    param_link5 = ' --URL_DL_5 "' + link[4] + '"'
    param_link6 = ' --URL_DL_6 "' + link[5] + '"'
if len(link) == 7:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
    param_link4 = ' --URL_DL_4 "' + link[3] + '"'
    param_link5 = ' --URL_DL_5 "' + link[4] + '"'
    param_link6 = ' --URL_DL_6 "' + link[5] + '"'
    param_link7 = ' --URL_DL_7 "' + link[6] + '"'

if len(link) == 8:
    param_link2 = ' --URL_DL_2 "' + link[1] + '"'
    param_link3 = ' --URL_DL_3 "' + link[2] + '"'
    param_link4 = ' --URL_DL_4 "' + link[3] + '"'
    param_link5 = ' --URL_DL_5 "' + link[4] + '"'
    param_link6 = ' --URL_DL_6 "' + link[5] + '"'
    param_link7 = ' --URL_DL_7 "' + link[6] + '"'
    param_link8 = ' --URL_DL_8 "' + link[7] + '"'

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


full_path = fme_path + param_layer + param_link1 + param_link2 + param_link3 + param_link4 + param_link5 + \
            param_link6 + param_link7 + param_link8 + param_ISO + param_geom + str_writers + str_summary

print('------------------------\n------------------------\n')
print(full_path)
print('------------------------\n------------------------\n')

os.system(full_path)

time_end = time.time()
elapsed_time = float(time_end) - float(time_start)
elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
print('\n\nElapsed time: {} hours, {} min, {} sec'.format(elapsed_time[0:2], elapsed_time[3:5], elapsed_time[6:9]))

# https://community.safe.com/s/question/0D54Q00008515Q1SAI/fme-python-install-paramiko-expected-an-even-number-of-command-line-arguments-instead-got-9

# C:\Users\alexandre\AppData\Local\Temp
