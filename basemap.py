import numpy as np
import itertools
import math
import os



def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def raster_extractor(array_coord, user_size, ISO_str, bm_choice):
    list_zoom = list(range(15, -1, -1))
    zoom = min(list_zoom, key=lambda x: abs((111 * 360) / (np.power(2, x)) - user_size))

    x_deg_list = []
    y_deg_list = []
    x_tile_list = []
    y_tile_list = []

    for i in range(0, 17):
        xy = deg2num(array_coord[2 * i], array_coord[1 + 2 * i], zoom)
        x_tile_list.append(xy[0])
        y_tile_list.append(xy[1])
        xy_tl = num2deg(xy[0], xy[1], zoom)
        y_deg_list.append(xy_tl[0])
        x_deg_list.append(xy_tl[1])

    x_deg_list = list(set(x_deg_list))
    y_deg_list = list(set(y_deg_list))
    x_tile_list = list(set(x_tile_list))
    y_tile_list = list(set(y_tile_list))

    x_deg_list = sorted(x_deg_list)
    y_deg_list = sorted(y_deg_list, reverse=True)
    x_tile_list = sorted(x_tile_list)
    y_tile_list = sorted(y_tile_list)

    y_deg_b = []

    y_tile_b = [x + 1 for x in y_tile_list]
    for x in x_tile_list:
        for y in y_tile_b:
            y_deg_b.append(num2deg(x, y, zoom)[0])

    print('Zoom: {}'.format(zoom))

    combi_tile = list(itertools.product(x_tile_list, y_tile_list))
    combi_corner = list(itertools.product(x_deg_list, y_deg_list))

    print('Tiles de download:')
    print(combi_tile)
    print('Top left corners of the tiles (lon,lat):')
    print(combi_corner)
    bm_available = ['http://tile.stamen.com/terrain-background',
                    'http://s3.amazonaws.com/com.modestmaps.bluemarble',
                    'http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile',
                    'https://a.tile.opentopomap.org',
                    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile',
                    'http://a.tile.stamen.com/watercolor',
                    'https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels',
                    'https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile',
                    'http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile',
                    'https://maps.wikimedia.org/osm-intl']

    ext = ['.png', '.jpg', '.jpg', '.png', '.jpg', '.png', '.png', '.jpg', '.jpg', '.png']

    xtiles = [-999] * 12
    ytiles = [-999] * 12
    xcorner = [-999] * 12
    ycorner = [-999] * 12
    ycorner_b = [-999] * 12

    k = 0

    for j in range(0, len(x_tile_list)):
        for i in range(0, len(y_tile_list)):
            xtiles[k] = x_tile_list[j]
            xcorner[k] = x_deg_list[j]
            k = k + 1

    for j in range(0, len(x_tile_list)):
        ytiles[j * len(y_tile_list):(j + 1) * len(y_tile_list) - 1] = y_tile_list
        ycorner[j * len(y_deg_list):(j + 1) * len(y_deg_list) - 1] = y_deg_list
        ycorner_b[j * len(y_deg_list):(j + 1) * len(y_deg_list) - 1] = y_deg_b

    ytiles = ytiles[0:12]
    ycorner = ycorner[0:12]
    ycorner_b = ycorner_b[0:12]

    for j in range(0, 12):
        if ytiles[j] == -999:
            ytiles[j] = ytiles[0]
            xtiles[j] = xtiles[0]
            xcorner[j] = xcorner[0]
            ycorner[j] = ycorner[0]
            ycorner_b[j] = ycorner_b[0]




    fme_path = 'fme.exe C:\\Users\\alexandre\\Documents\\HDR\\Rasterextractorv3.fmw'
    param_minLON = ' --min_lon "' + str(array_coord[3]) + '"'
    param_minLAT = ' --min_lat "' + str(array_coord[6]) + '"'
    param_maxLON = ' --max_lon "' + str(array_coord[5]) + '"'
    param_maxLAT = ' --max_lat "' + str(array_coord[2]) + '"'
    param_dest = ' --DestDataset_JPEG "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap"'
    param_dest2 = ' --DestDataset_PNGRASTER "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap"'
    param_dest3 = ' --DestDataset_JPEG2000 "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap"'
    param_dest4 = ' --DestDataset_JPEG2000_3 "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap\\subtiles"'
    param_dest5 = ' --DestDataset_PNGRASTER_3 "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap\\subtiles"'
    param_dest6 = ' --DestDataset_JPEG_4 "C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\' + '04_Basemap\\subtiles"'



    param_ISO = ' --ISO_code "' + ISO_str + '"'
    param_BM = ' --BASEMAP "' + bm_available[bm_choice] + '"'
    param_ext = ' --BASEMAP_ext "' + ext[bm_choice] + '"'
    param_zoom = ' --zoom "' + str(zoom) + '"'
    param_tiles = ''

    for i in range(0, 60):
        if i in range(0, 12):
            param_tiles = param_tiles + ' --x_' + str(i + 1) + ' "' + str(xtiles[i]) + '"'
        elif i in range(12, 24):
            param_tiles = param_tiles + ' --y_' + str(i + 1 - 12) + ' "' + str(ytiles[i - 12]) + '"'
        elif i in range(24, 36):
            param_tiles = param_tiles + ' --x_deg_' + str(i + 1 - 24) + ' "' + str(xcorner[i - 24]) + '"'
        elif i in range(36, 48):
            param_tiles = param_tiles + ' --y_deg_' + str(i + 1 - 36) + ' "' + str(ycorner[i - 36]) + '"'
        else:
            param_tiles = param_tiles + ' --y_deg_b_' + str(i + 1 - 48) + ' "' + str(ycorner_b[i - 48]) + '"'

    command_raster = fme_path + param_zoom + param_tiles + param_minLON + param_minLAT + param_maxLON + param_maxLAT\
                     + param_dest + param_dest2 + param_dest3 + param_dest4 + param_dest5 + param_dest6 + param_BM + param_ext + param_ISO
    print(command_raster)

    os.system(command_raster)

    return zoom