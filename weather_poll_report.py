import urllib.request as request
import json

import matplotlib
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request as request
import imageio
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import seaborn as sns
import math
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from mpl_toolkits.basemap import Basemap, cm
import warnings


def basemap_test(array_coord):
    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
    API_KEY = 'beeb9ce4829f91765be3060efde0af4c'
    lat = array_coord[0]
    lon = array_coord[1]
    coord = []
    resol = 31
    for i in range(0, resol):
        for j in range(0, resol):
            coord.append(lat + ((array_coord[5]-array_coord[3])/(resol-1)) * i - ((array_coord[5]-array_coord[3])/(resol-1))*2)
            coord.append(lon + ((array_coord[5]-array_coord[3])/(resol-1)) * j - ((array_coord[5]-array_coord[3])/(resol-1))*2)

    a_coord = [[0 for x in range(2)] for y in range(resol * resol)]


    for i in range(0, resol * resol):
        for j in range(0, 2):
            if j == 0:
                a_coord[i][j] = coord[2 * i]
            else:
                a_coord[i][j] = coord[2 * i + 1]

    url_we = []
    for i in range(0, resol * resol):
        url_we.append('https://api.openweathermap.org/data/2.5/forecast?lat=' + str(coord[2 * i]) + '&lon=' + str(coord[2 * i + 1]) + '&appid=' + API_KEY)

    j = 0
    df = pd.DataFrame()
    df_ws = pd.DataFrame()
    df_wd = pd.DataFrame()

    progression = 0
    for url in url_we:

        r = requests.get(url)
        page_body = r.text
        soup = BeautifulSoup(page_body, 'html.parser')
        data = json.loads(str(soup))['list']
        temp = []
        ws = []
        wd = []
        dt = []
        for i in data:
            dt.append(i['dt'])
            temp.append(i['main']['temp'])
            ws.append(i['wind']['speed'])
            wd.append(i['wind']['deg'])

        temp[:] = [temps - 273.15 for temps in temp]
        df_ws[str(a_coord[j][:])] = ws
        df_wd[str(a_coord[j][:])] = wd
        df[str(a_coord[j][:])] = temp
        j = j + 1
        if j % round(resol*resol/10) == 0:
            progression = progression + 1
            print('Request of weather data {}% completed'.format(progression*10))
    dt_txt = []
    for i in data:
        dt_txt.append(i['dt_txt'])

    norm = matplotlib.colors.Normalize()
    norm.autoscale([x for xs in df_ws.values.tolist() for x in xs])
    cm = plt.cm.cool

    sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, orientation="vertical", pad=0.2)

    for k in range(0, len(df_ws)):
        print('Wind data: {}/{} generated... '.format(k, len(df_ws)))
        data_ws = df_ws.iloc[k].to_numpy()
        data_wd = df_wd.iloc[k].to_numpy()

        m = Basemap(projection='merc', llcrnrlat=array_coord[6], urcrnrlat=array_coord[2], llcrnrlon=array_coord[3],
                    urcrnrlon=array_coord[5], resolution='i')
        m.drawcoastlines()
        m.drawrivers(color='b')
        m.drawcountries(linewidth=0.8)


        m.fillcontinents(alpha=0.95, lake_color='b')
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90., 91., round((array_coord[5]-array_coord[3])/3, 1)), labels=[False, True, True, False])
        m.drawmeridians(np.arange(-180., 181., round((array_coord[5]-array_coord[3])/3, 1)), labels=[True, False, False, True])
        m.drawmapboundary(fill_color='black')

        x, y = np.meshgrid(np.linspace(array_coord[3], array_coord[5], resol), np.linspace(array_coord[6], array_coord[2], resol))

        v = []
        u = []

        for i in range(0, resol * resol):
            v.append(np.sqrt((data_ws[i] ** 2) / (1 + np.tan(data_wd[i] * np.pi / 180) ** 2)))
            u.append(np.sqrt(data_ws[i] ** 2 - v[i] ** 2))

            if data_wd[i] > 270:
                v[i] = -v[i]
            elif 90 < data_wd[i] <= 180:
                u[i] = -u[i]
            elif 0 <= data_wd[i] <= 90:
                u[i] = -u[i]
                v[i] = -v[i]
        progress = '\n' + ''.join(k * ['.'])
        m.quiver(x, y, u, v, scale=30, latlon=True, color=cm(norm(data_ws)), linewidth=2, edgecolors='k')
        plt.title('Wind speed and direction for ' + dt_txt[k] + progress)
        plt.savefig('ImageWind/Wind_' + str(k) + '.jpg')

    filenames = []
    for i in range(0, len(df)):
        filenames.append('ImageWind/Wind_' + str(i) + '.jpg')

    with imageio.get_writer('movie2.gif', mode='I', duration=0.4) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def print_report(coord, ISO_str):
    API_KEY = 'beeb9ce4829f91765be3060efde0af4c'
    lat = coord[0]
    lon = coord[1]
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + API_KEY
    url_airpoll = 'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=' + str(lat) + '&lon=' + str(
        lon) + '&appid=' + API_KEY

    r = requests.get(url)
    page_body = r.text
    soup = BeautifulSoup(page_body, 'html.parser')

    data = json.loads(str(soup))['list']

    dt = []
    temp = []
    feels_like = []
    temp_max = []
    temp_min = []
    pressure = []
    sea_level = []
    grnd_level = []
    humidity = []
    temp_kf = []
    w_id = []
    w_main = []
    w_description = []
    w_icon = []
    clouds_all = []
    wind_speed = []
    wind_deg = []
    wind_gust = []
    visibility = []
    pop = []
    rain_3h = []
    snow_3h = []
    sys_pod = []
    dt_txt = []

    for i in data:
        dt.append(i['dt'])
        temp.append(i['main']['temp'])
        feels_like.append(i['main']['feels_like'])
        temp_max.append(i['main']['temp_max'])
        temp_min.append(i['main']['temp_min'])
        pressure.append(i['main']['pressure'])
        sea_level.append(i['main']['sea_level'])
        grnd_level.append(i['main']['grnd_level'])
        humidity.append(i['main']['humidity'])
        temp_kf.append(i['main']['temp_kf'])
        w_id.append(i['weather'][0]['id'])
        w_main.append(i['weather'][0]['main'])
        w_description.append(i['weather'][0]['description'])
        w_icon.append(i['weather'][0]['icon'])
        clouds_all.append(i['clouds']['all'])
        wind_speed.append(i['wind']['speed'])
        wind_deg.append(i['wind']['deg'])
        wind_gust.append(i['wind']['gust'])
        visibility.append(i['visibility'])
        pop.append(i['pop'])
        if 'rain' in i:
            rain_3h.append(i['rain']['3h'])
        else:
            rain_3h.append(0)
        if 'snow' in i:
            snow_3h.append(i['snow']['3h'])
        else:
            snow_3h.append(0)
        sys_pod.append(i['sys']['pod'])
        dt_txt.append(i['dt_txt'])

    df = pd.DataFrame(dt_txt, columns=['time'])
    df['t_unix'] = dt
    df['temp'] = temp
    df['feels_like'] = feels_like
    df['temp_max'] = temp_max
    df['temp_min'] = temp_min
    df['pressure'] = pressure
    df['sea_level'] = sea_level
    df['grnd_level'] = grnd_level
    df['humidity'] = humidity
    df['temp_kf'] = temp_kf
    df['w_id'] = w_id
    df['w_main'] = w_main
    df['w_description'] = w_description
    df['w_icon'] = w_icon
    df['clouds_all'] = clouds_all
    df['wind_speed'] = wind_speed
    df['wind_deg'] = wind_deg
    df['wind_gust'] = wind_gust
    df['visibility'] = visibility
    df['pr_precip'] = pop
    df['rain_3h'] = rain_3h
    if snow_3h != []:
        df['snow_3h'] = snow_3h
    else:
        df['snow_3h'] = [0] * len(df)

    df['sys_pod'] = sys_pod
    df['temp'] = df['temp'] - 273.15
    df['temp_max'] = df['temp_max'] - 273.15
    df['temp_min'] = df['temp_min'] - 273.15
    df['feels_like'] = df['feels_like'] - 273.15
    df['wind_speed'] = df['wind_speed'] * 3.6
    df['wind_gust'] = df['wind_gust'] * 3.6
    df['visibility'] = df['visibility'] / 1000
    df['rain_3h'] = df['rain_3h'] / 3

    direction = []
    for line in df['wind_deg']:
        if 348.75 <= line < 11.25:
            direction.append('N')

        elif 11.25 <= line < 33.75:
            direction.append('NNE')

        elif 33.75 <= line < 56.25:
            direction.append('NE')

        elif 56.25 <= line < 78.75:
            direction.append('ENE')

        elif 78.75 <= line < 101.25:
            direction.append('E')

        elif 101.25 <= line < 123.75:
            direction.append('ESE')

        elif 123.75 <= line < 146.25:
            direction.append('SE')

        elif 146.25 <= line < 168.75:
            direction.append('SSE')

        elif 168.75 <= line < 191.25:
            direction.append('S')

        elif 191.25 <= line < 213.25:
            direction.append('SSW')

        elif 213.75 <= line < 236.25:
            direction.append('SW')

        elif 236.25 <= line < 258.75:
            direction.append('WSW')

        elif 258.75 <= line < 281.25:
            direction.append('W')

        elif 281.25 <= line < 303.75:
            direction.append('WNW')

        elif 303.75 <= line < 101.25:
            direction.append('NW')

        else:
            direction.append('NNW')

    df['wind_dir'] = direction

    fig, ax = plt.subplots(figsize=(15, 8))

    ax.plot(df.t_unix, df.temp, label='Temp. [°C]', color='b', linewidth=2)
    ax.fill_between(df.t_unix, df.temp_min, df.temp_max, alpha=0.5, label='min/max Temp.', color='b')
    ax.plot(df.t_unix, df.feels_like, label='Feels like [°C]', color='k')
    if min(min(df.temp), min(df.feels_like)) < 0:
        ax.fill_between(df.t_unix, min(min(df.temp), min(df.feels_like)) * 1.15, df.temp, color='k', alpha=0.15)
    else:
        ax.fill_between(df.t_unix, min(min(df.temp), min(df.feels_like)) * 0.85, df.temp, color='k', alpha=0.15)

    ax.margins(x=0)

    ax.set_title("Temperature for the next 5 days:", fontsize=17, loc='left')
    ax.set_ylabel('T [°C]', fontsize=13)
    ax.lines[1].set_linestyle("--")

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax.set_xticklabels(unix_plt, rotation=80)

    ax.legend(fontsize=14)

    plt.savefig('Weather_report_Temp.jpg', bbox_inches='tight', dpi=200)

    #######################################################################################################

    # If we were to simply plot pts, we'd lose most of the interesting
    # details due to the outliers. So let's 'break' or 'cut-out' the y-axis
    # into two portions - use the top (ax1) for the outliers, and the bottom
    # (ax2) for the details of the majority of our data
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 8))
    fig.subplots_adjust(hspace=0.1)  # adjust space between axes

    # plot the same data on both axes
    ax1.plot(df.t_unix, df.pressure, label='Pressure sea level [hPa]', color='r', linewidth=3)
    ax2.plot(df.t_unix, df.grnd_level, label='Pressure ground [hPa]', color='b', linewidth=3)

    # zoom-in / limit the view to different portions of the data
    ax1.set_ylim(min(df.pressure) - 1, max(df.pressure) + 1)  # outliers only
    ax2.set_ylim(min(df.grnd_level) - 1, max(df.grnd_level) + 1)  # most of the data

    # hide the spines between ax and ax2
    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])
    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax2.set_xticklabels(unix_plt, rotation=80)

    # Now, let's turn towards the cut-out slanted lines.
    # We create line objects in axes coordinates, in which (0,0), (0,1),
    # (1,0), and (1,1) are the four corners of the axes.
    # The slanted lines themselves are markers at those locations, such that the
    # lines keep their angle and position, independent of the axes size or scale
    # Finally, we need to disable clipping.

    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
    ax1.legend(fontsize=13)
    ax2.legend(fontsize=13)
    ax1.set_title("Pressure for the next 5 days:", fontsize=17, loc='left')
    ax1.set_ylabel('P [hPa]', fontsize=13)
    ax2.set_ylabel('P [hPa]', fontsize=13)

    plt.savefig('Weather_report_pressure.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    fig3, ax3 = plt.subplots(figsize=(15, 8))

    ax3 = sns.lineplot(data=df, x='t_unix', y='humidity', label='Humidity [%]', color='b')

    ax3.fill_between(df.t_unix, 0.70 * min(df.humidity), df.humidity, color='b', alpha=0.3)

    ax3.margins(x=0)

    ax3.set_title("Humidity for the next 5 days:", fontsize=17, loc='left')
    ax3.set_ylabel('H [%]', fontsize=13)
    ax3.set_xlabel('')

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax3.set_xticklabels(unix_plt, rotation=80)

    ax3.legend(fontsize=15)

    plt.savefig('Weather_report_humidity.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    fig3, ax3 = plt.subplots(figsize=(15, 8))

    ax3 = sns.lineplot(data=df, x='t_unix', y='clouds_all', label='Cloudiness [%]', color='k')

    ax3.fill_between(df.t_unix, 0.70 * min(df.clouds_all), df.clouds_all, color='k', alpha=0.3)

    ax3.margins(x=0)

    ax3.set_title("Cloudiness [%] for the next 5 days:", fontsize=17, loc='left')
    ax3.set_ylabel('C [%]', fontsize=13)
    ax3.set_xlabel('')

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax3.set_xticklabels(unix_plt, rotation=80)

    ax3.legend(fontsize=15)

    plt.savefig('Weather_report_clouds.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    ws = df.wind_speed
    wd = df.wind_deg

    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.set_title(
        'The wind rose located in the top right corner of each data map shows the general\nwind direction and speed for each sampling period. The circular format of the wind\nrose shows the direction the winds blew from and the length of each "spoke"\naround the circle shows how often the wind blew from that direction.',
        loc='left')
    ax.set_legend(title='Wind speed [km/h]')
    plt.savefig('Weather_report_wind_rose.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    fig5, ax5 = plt.subplots(figsize=(15, 8))

    ax5.plot(df.t_unix, df.wind_speed, label='Wind [m/s]', color='r', linewidth=2.5)
    ax5.fill_between(df.t_unix, df.wind_speed, df.wind_gust, alpha=0.4, label='Wind gust [m/s]', color='r')

    ax5.margins(x=0)

    ax5.set_title("Wind [km/h] for the next 5 days:", fontsize=17, loc='left')
    ax5.set_ylabel('WS [km/h]', fontsize=13)

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax5.set_xticklabels(unix_plt, rotation=80)

    for line in range(0, df.shape[0]):
        plt.text(df.t_unix[line], df.wind_gust[line] + 0.5, df.wind_dir[line], horizontalalignment='center', size=8,
                 color='black', weight='semibold')

    ax5.legend(fontsize=15)

    plt.savefig('Weather_report_wind.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    fig3, ax3 = plt.subplots(figsize=(15, 8))

    ax3 = sns.lineplot(data=df, x='t_unix', y='rain_3h', label='Rain Precipitation [mm/h]', color='b')
    ax3 = sns.lineplot(data=df, x='t_unix', y='snow_3h', label='Snow Precipitation [mm/h]', color='k')
    ax3.fill_between(df.t_unix, [0] * len(df), df.rain_3h, alpha=0.4, color='b')
    ax3.fill_between(df.t_unix, [0] * len(df), df.snow_3h, alpha=0.2, color='k')
    ax3.margins(x=0)

    ax3.set_title("Précipitation intensity [mm/h] and precipitation probability [] for the next 5 days", fontsize=17,
                  loc='left')
    ax3.set_ylabel('P [mm/h]', fontsize=13)
    ax3.set_xlabel('')
    # ax3.set_xticks(range(len(s_x)+1))
    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax3.set_xticklabels(unix_plt, rotation=80)

    for line in range(0, df.shape[0]):
        plt.text(df.t_unix[line], max(df.rain_3h[line], df.snow_3h[line]) + 0.05, round(df.pr_precip[line], 1),
                 horizontalalignment='center', size=8, color='black', weight='semibold')

    ax3.legend(fontsize=15)

    plt.savefig('Weather_report_rain.jpg', bbox_inches='tight', dpi=200)

    #########################################################################################################

    r_pol = requests.get(url_airpoll)
    page_body_pol = r_pol.text
    soup_pol = BeautifulSoup(page_body_pol, 'html.parser')
    data_pol = json.loads(str(soup_pol))['list']

    aqi = []
    co = []
    no2 = []
    no = []
    o3 = []
    so2 = []
    pm2_5 = []
    pm10 = []
    nh3 = []
    dt = []

    for i in data_pol:
        aqi.append(i['main']['aqi'])
        co.append(i['components']['co'])
        no2.append(i['components']['no2'])
        no.append(i['components']['no'])
        o3.append(i['components']['o3'])
        so2.append(i['components']['so2'])
        pm2_5.append(i['components']['pm2_5'])
        pm10.append(i['components']['pm10'])
        nh3.append(i['components']['nh3'])
        dt.append(i['dt'])

    t_text = []
    for line in dt:
        t_text.append(datetime.utcfromtimestamp(line).strftime('%Y-%m-%d %H:00'))

    df_poll = pd.DataFrame(t_text, columns=['time'])
    df_poll['dt'] = dt
    df_poll['co'] = co
    df_poll['no2'] = no2
    df_poll['no'] = no
    df_poll['so2'] = so2
    df_poll['pm2_5'] = pm2_5
    df_poll['pm10'] = pm10
    df_poll['nh3'] = nh3
    df_poll['o3'] = o3
    df_poll['aqi'] = aqi
    df_poll['co'] = df_poll['co'] / 1000

    aqi_txt = []
    for line in df_poll['aqi']:
        if line == 1:
            aqi_txt.append('Good')

        elif line == 2:
            aqi_txt.append('Fair')

        elif line == 3:
            aqi_txt.append('Moderate')

        elif line == 4:
            aqi_txt.append('Poor')

        else:
            aqi_txt.append('Very Poor')
    df_poll['aqi_txt'] = aqi_txt

    fig0, ax0 = plt.subplots(figsize=(15, 8))

    ax0 = sns.lineplot(data=df_poll, x='dt', y='no2', label='[NO$_2$]', color='b', linewidth=3)
    ax0 = sns.lineplot(data=df_poll, x='dt', y='no', label='[NO]', color='c', linewidth=3)
    # ax0.fill_between(df.t_unix,0.70 * min(df.clouds_all),df.clouds_all, color = 'k', alpha=0.3)
    # ax0 = sns.lineplot(data=df_poll, x = 'dt', y = 'co', label = 'CO', color = 'k', linewidth = 3)
    ax0 = sns.lineplot(data=df_poll, x='dt', y='nh3', label='[NH$_3$]', color='g', linewidth=3)
    ax0 = sns.lineplot(data=df_poll, x='dt', y='pm10', label='[PM$_{10}$]', color='r', linewidth=3)
    ax0 = sns.lineplot(data=df_poll, x='dt', y='pm2_5', label='[PM$_{2.5}$]', color='m', linewidth=3)
    ax0 = sns.lineplot(data=df_poll, x='dt', y='so2', label='[SO$_2$]', color='y', linewidth=3)

    # ax0 = sns.lineplot(data=df_poll, x = 'dt', y = 'o3', label = 'O3', color = 'c')

    temp = 0
    switch = []
    j = -1

    for line in df_poll['aqi']:
        j = j + 1
        if line == temp:
            continue
        else:
            temp = line
            switch.append(j)

    if switch != [0]:
        switch = switch[1:]

        aqi_beg = [0]
        aqi_end = [switch[0] - 1]
        for i in range(0, len(switch)):
            # 0 4  12 28 37 51 68 76 82  102 108
            # 3 11 27 36 50 67 75 81 101 107 114
            if i == 0:
                aqi_beg.append(switch[0])
                aqi_end.append(switch[1])

            elif i == len(switch) - 1:
                aqi_beg.append(switch[i])
                aqi_end.append(len(df_poll) - 1)

            else:
                aqi_beg.append(switch[i])
                aqi_end.append(switch[i + 1] - 1)

        for i in range(0, len(aqi_beg)):

            if df_poll['aqi'][aqi_beg[i]] == 1:
                face_col = 'g'
                alph = 0.2
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 2:
                face_col = 'r'
                alph = 0.1
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 3:
                face_col = 'r'
                alph = 0.25
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 4:
                face_col = 'r'
                alph = 0.4
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            else:
                face_col = 'r'
                alph = 0.55
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

        for i in range(0, len(switch)):
            if i == len(switch) - 2:
                plt.text(df_poll.dt[round((switch[i - 1] + len(df_poll)) / 2)], -0.1, df_poll.aqi_txt[len(df_poll) - 1],
                         horizontalalignment='center', size=10, color='black', weight='semibold')
            elif i == 0:
                plt.text(df_poll.dt[round((0 + switch[i + 1]) / 2)], -0.1, df_poll.aqi_txt[0],
                         horizontalalignment='center', size=10, color='black', weight='semibold')
            else:
                plt.text(df_poll.dt[round((switch[i - 1] + switch[i]) / 2)], -0.1, df_poll.aqi_txt[aqi_beg[i]],
                         horizontalalignment='center', size=10, color='black', weight='semibold')

    else:
        face_col = ['g', 'r', 'r', 'r', 'r']
        alph = [0.2, 0.1, 0.25, 0.4, 0.55]
        ax0.axvspan(dt[0], dt[-1], facecolor=face_col[df_poll.aqi[0] - 1], alpha=alph[df_poll.aqi[0] - 1])
        plt.text(df_poll.dt[round(len(df_poll) / 2)], -0.1, df_poll.aqi_txt[0], horizontalalignment='center', size=10,
                 color='black', weight='semibold')
    ax0.margins(x=0)

    ax0.set_title("Pollutant concentration in 10 [$\mu$g/m$^3$] and global Air Quality Index (text)", fontsize=17,
                  loc='left')
    ax0.set_ylabel('Concentration [$\mu$g/m$^3$]', fontsize=13)
    ax0.set_xlabel('')
    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax0.set_xticklabels(unix_plt, rotation=80)

    ax0.legend(loc=1, fontsize=15)
    plt.savefig('Weather_report_pol.jpg', bbox_inches='tight', dpi=200)

    ####################################################################################

    fig0, ax0 = plt.subplots(figsize=(15, 8))

    ax0 = sns.lineplot(data=df_poll, x='dt', y='o3', label='[O3]', color='c', linewidth=3)

    temp = 0
    switch = []
    j = -1

    for line in df_poll['aqi']:
        j = j + 1
        if line == temp:
            continue
        else:
            temp = line
            switch.append(j)

    if switch != [0]:

        switch = switch[1:]

        aqi_beg = [0]
        aqi_end = [switch[0] - 1]
        for i in range(0, len(switch)):
            # 0 4  12 28 37 51 68 76 82  102 108
            # 3 11 27 36 50 67 75 81 101 107 114
            if i == 0:
                aqi_beg.append(switch[0])
                aqi_end.append(switch[1])

            elif i == len(switch) - 1:
                aqi_beg.append(switch[i])
                aqi_end.append(len(df_poll) - 1)

            else:
                aqi_beg.append(switch[i])
                aqi_end.append(switch[i + 1] - 1)

        for i in range(0, len(aqi_beg)):

            if df_poll['aqi'][aqi_beg[i]] == 1:
                face_col = 'g'
                alph = 0.2
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 2:
                face_col = 'r'
                alph = 0.1
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 3:
                face_col = 'r'
                alph = 0.25
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 4:
                face_col = 'r'
                alph = 0.4
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            else:
                face_col = 'r'
                alph = 0.55
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

        for i in range(0, len(switch)):
            if i > 0:
                plt.text(df_poll.dt[round((switch[i - 1] + switch[i]) / 2)], min(df_poll.o3),
                         df_poll.aqi_txt[aqi_beg[i]], horizontalalignment='center', size=10, color='black',
                         weight='semibold')
            elif i == 0:
                plt.text(df_poll.dt[round((0 + switch[i]) / 2)], min(df_poll.o3), df_poll.aqi_txt[aqi_beg[0]],
                         horizontalalignment='center', size=10, color='black', weight='semibold')


    else:
        face_col = ['g', 'r', 'r', 'r', 'r']
        alph = [0.2, 0.1, 0.25, 0.4, 0.55]
        ax0.axvspan(dt[0], dt[-1], facecolor=face_col[df_poll.aqi[0] - 1], alpha=alph[df_poll.aqi[0] - 1])
        plt.text(df_poll.dt[round(len(df_poll) / 2)], min(df_poll.o3), df_poll.aqi_txt[0], horizontalalignment='center',
                 size=10,
                 color='black', weight='semibold')

    ax0.margins(x=0)

    ax0.set_title("Ozone concentration in [$\mu$g/m$^3$] and global Air Quality Index (text)", fontsize=17, loc='left')
    ax0.set_ylabel('Concentration [$\mu$g/m$^3$]', fontsize=13)
    ax0.set_xlabel('')

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax0.set_xticklabels(unix_plt, rotation=80)

    ax0.legend(loc=1, fontsize=15)

    plt.savefig('Weather_report_O3.jpg', bbox_inches='tight', dpi=200)

    ##############################################################################################

    fig0, ax0 = plt.subplots(figsize=(15, 8))

    ax0 = sns.lineplot(data=df_poll, x='dt', y='co', label='[CO]', color='k', linewidth=3)

    temp = 0
    switch = []
    j = -1

    for line in df_poll['aqi']:
        j = j + 1
        if line == temp:
            continue
        else:
            temp = line
            switch.append(j)

    if switch != [0]:

        switch = switch[1:]

        aqi_beg = [0]
        aqi_end = [switch[0] - 1]
        for i in range(0, len(switch)):
            # 0 4  12 28 37 51 68 76 82  102 108
            # 3 11 27 36 50 67 75 81 101 107 114
            if i == 0:
                aqi_beg.append(switch[0])
                aqi_end.append(switch[1])

            elif i == len(switch) - 1:
                aqi_beg.append(switch[i])
                aqi_end.append(len(df_poll) - 1)

            else:
                aqi_beg.append(switch[i])
                aqi_end.append(switch[i + 1] - 1)

        for i in range(0, len(aqi_beg)):

            if df_poll['aqi'][aqi_beg[i]] == 1:
                face_col = 'g'
                alph = 0.2
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 2:
                face_col = 'r'
                alph = 0.1
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 3:
                face_col = 'r'
                alph = 0.25
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            elif df_poll['aqi'][aqi_beg[i]] == 4:
                face_col = 'r'
                alph = 0.4
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

            else:
                face_col = 'r'
                alph = 0.55
                ax0.axvspan(dt[aqi_beg[i]], dt[aqi_end[i]], facecolor=face_col, alpha=alph)

        for i in range(0, len(switch)):
            if i > 0:
                plt.text(df_poll.dt[round((switch[i - 1] + switch[i]) / 2)], min(df_poll.co),
                         df_poll.aqi_txt[aqi_beg[i]], horizontalalignment='center', size=10, color='black',
                         weight='semibold')
            elif i == 0:
                plt.text(df_poll.dt[round((0 + switch[i]) / 2)], min(df_poll.co), df_poll.aqi_txt[aqi_beg[0]],
                         horizontalalignment='center', size=10, color='black', weight='semibold')

    else:
        face_col = ['g', 'r', 'r', 'r', 'r']
        alph = [0.2, 0.1, 0.25, 0.4, 0.55]
        ax0.axvspan(dt[0], dt[-1], facecolor=face_col[df_poll.aqi[0] - 1], alpha=alph[df_poll.aqi[0] - 1])
        plt.text(df_poll.dt[round(len(df_poll) / 2)], min(df_poll.co), df_poll.aqi_txt[0], horizontalalignment='center',
                 size=10, color='black', weight='semibold')

    ax0.margins(x=0)

    ax0.set_title("Carbon monoxyde concentration in [$\mu$g/m$^3$] and global Air Quality Index (text)", fontsize=17,
                  loc='left')
    ax0.set_ylabel('Concentration [$\mu$g/m$^3$]', fontsize=13)
    ax0.set_xlabel('')

    unix_plt = []
    i = -1
    for tm in df.time:
        i = i + 1
        if int(tm[10:13]) in [6, 12, 18, 0]:
            unix_plt.append(df.time[i])

    plt.locator_params(axis="x", nbins=len(unix_plt))
    ax0.set_xticklabels(unix_plt, rotation=80)

    ax0.legend(loc=1, fontsize=15)

    plt.savefig('Weather_report_CO.jpg', bbox_inches='tight', dpi=200)

    ##############################################################################
    ##############################################################################

    zoom = 12
    xy = deg2num(coord[0], coord[1], zoom)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

    url_map_context = 'https://a.tile.opentopomap.org/' + str(zoom) + '/' + str(xy[0]) + '/' + str(xy[1]) + '.png'
    BM = ImageReader(url_map_context)

    pdf_file = 'C:\\Users\\alexandre\\Documents\\HDR\\output_' + ISO_str + '\\Weather_report_' + ISO_str + '.pdf'
    img_file = ['Weather_report_Temp.jpg',
                'Weather_report_rain.jpg',
                'Weather_report_wind.jpg',
                'Weather_report_wind_rose.jpg',
                'Weather_report_pressure.jpg',
                'Weather_report_humidity.jpg',
                'Weather_report_clouds.jpg',
                'Weather_report_pol.jpg',
                'Weather_report_O3.jpg',
                'Weather_report_CO.jpg']

    STR_TITLE = 'Weather & Air Pollution Report'
    STR_SUBTITLE1 = 'Location: ' + str(round(lat, 4)) + ' N, ' + str(round(lon, 4)) + ' E'
    STR_SUBTITLE2 = 'From ' + str(df.time[0]) + ' to ' + str(df.time[len(df) - 1]) + ' (UTC)'
    PAGE = ['Page 1 of 6', 'Page 2 of 6', 'Page 3 of 6', 'Page 4 of 6', 'Page 5 of 6', 'Page 6 of 6', ]
    x1_start = 20
    y1_start = -200
    x2_start = 10
    y2_start = -550

    can = canvas.Canvas(pdf_file)
    can.setFont('VeraBd', 20)
    can.drawString(120, 800, "Weather & Air Pollution Report")
    can.drawImage('deco1.png', 40, 775, width=500, preserveAspectRatio=True, mask='auto')
    can.drawImage('deco2.png', 40, 20, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraIt', 12)
    can.drawString(120, 770, STR_SUBTITLE2)
    can.drawString(200, 750, STR_SUBTITLE1)

    can.setFont('VeraBd', 13)
    can.drawString(40, 470, 'Table of contents')
    can.setFont('VeraBI', 12)
    can.drawString(40, 450, 'Weather')
    can.drawString(40, 340, 'Pollution')
    can.setFont('Vera', 11)
    can.drawString(45, 435,
                   'Temperature ........................................................................................................')
    can.drawString(45, 420,
                   'Precipitation .........................................................................................................')
    can.drawString(45, 405,
                   'Wind .....................................................................................................................')
    can.drawString(45, 390,
                   'Pressure ..............................................................................................................')
    can.drawString(45, 375,
                   'Humidity .............................................................................................................')
    can.drawString(45, 360,
                   'Cloudiness ...........................................................................................................')
    can.drawString(45, 325,
                   'NO2, NO, NH3, SO2, PM2.5, PM10 ......................................................................')
    can.drawString(45, 310,
                   'Ozone (O3) .........................................................................................................')
    can.drawString(45, 295,
                   'Carbon monoxyde (CO) ......................................................................................')
    can.drawString(495, 435, 'Page 2')
    can.drawString(495, 420, 'Page 2')
    can.drawString(495, 405, 'Page 3')
    can.drawString(495, 390, 'Page 4')
    can.drawString(495, 375, 'Page 4')
    can.drawString(495, 360, 'Page 5')
    can.drawString(495, 325, 'Page 5')
    can.drawString(495, 310, 'Page 6')
    can.drawString(495, 295, 'Page 6')

    can.setFont('VeraIt', 6)
    can.drawString(40, 120 + 40,
                   'The presented data come the OpenWeather API, that use its own numerical weather prediction (NWP) model, which uses several data sources:')
    can.drawString(45, 110 + 40, '-- Global NWP models:')
    can.drawString(53, 102 + 40, '- NOAA GFS 0.25 and 0.5 grid sizes (7 x7 and 14 x14 [km])')
    can.drawString(53, 95 + 40, '- NOAA CFS')
    can.drawString(53, 88 + 40, '- ECMWF ERA')
    can.drawString(45, 78 + 40, '-- Weather stations:')
    can.drawString(53, 70 + 40, '- METAR stations')
    can.drawString(53, 63 + 40, '- Users’ stations')
    can.drawString(53, 56 + 40, '- Companies’ stations')
    can.drawString(45, 46 + 40, '-- Weather radar data:')
    can.drawString(53, 38 + 40, '- Satellite data')
    can.drawString(40, 28 + 40,
                   'OpenWeather download and save data from these sources. Then it is processed by its in-house set of algorithms, to improve its quality and accuracy.')
    can.drawString(40, 20 + 40,
                   'This data processing is being done in real time, to provide the latest nowcasts and forecasts.')

    can.drawImage(BM, 190, 490, width=200, preserveAspectRatio=True, mask='auto')
    # can.drawImage('logo.png', 30, 790, width=80, preserveAspectRatio=True, mask='auto')

    can.showPage()

    can.setFont('VeraBd', 13)
    can.drawString(20, 800, STR_TITLE)
    can.drawImage('deco1.png', 20, 780, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraBI', 10)
    can.drawString(20, 780, STR_SUBTITLE1)
    can.drawString(20, 765, STR_SUBTITLE2)
    can.setFont('VeraIt', 8)
    can.drawString(480, 20, PAGE[1])

    can.drawImage(img_file[0], x1_start, y1_start, width=520, preserveAspectRatio=True, mask='auto')
    can.drawImage(img_file[1], x2_start, y2_start, width=520, preserveAspectRatio=True, mask='auto')
    can.showPage()

    can.setFont('VeraBd', 13)
    can.drawString(20, 800, STR_TITLE)
    can.drawImage('deco1.png', 20, 780, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraBI', 10)
    can.drawString(20, 780, STR_SUBTITLE1)
    can.drawString(20, 765, STR_SUBTITLE2)
    can.setFont('VeraIt', 8)
    can.drawString(480, 20, PAGE[2])

    can.drawImage(img_file[2], x1_start, y1_start, width=520, preserveAspectRatio=True, mask='auto')
    can.drawImage(img_file[3], x2_start + 110, y2_start - 50, width=340, preserveAspectRatio=True, mask='auto')
    can.showPage()

    can.setFont('VeraBd', 13)
    can.drawString(20, 800, STR_TITLE)
    can.drawImage('deco1.png', 20, 780, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraBI', 10)
    can.drawString(20, 780, STR_SUBTITLE1)
    can.drawString(20, 765, STR_SUBTITLE2)
    can.setFont('VeraIt', 8)
    can.drawString(480, 20, PAGE[3])

    can.drawImage(img_file[4], x1_start, y1_start, width=520, preserveAspectRatio=True, mask='auto')
    can.drawImage(img_file[5], x2_start, y2_start, width=520, preserveAspectRatio=True, mask='auto')
    can.showPage()

    can.setFont('VeraBd', 13)
    can.drawString(20, 800, STR_TITLE)
    can.drawImage('deco1.png', 20, 780, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraBI', 10)
    can.drawString(20, 780, STR_SUBTITLE1)
    can.drawString(20, 765, STR_SUBTITLE2)
    can.setFont('VeraIt', 8)
    can.drawString(480, 20, PAGE[4])

    can.drawImage(img_file[6], x1_start, y1_start, width=520, preserveAspectRatio=True, mask='auto')
    can.drawImage(img_file[7], x2_start, y2_start, width=520, preserveAspectRatio=True, mask='auto')
    can.showPage()

    can.setFont('VeraBd', 13)
    can.drawString(20, 800, STR_TITLE)
    can.drawImage('deco1.png', 20, 780, width=500, preserveAspectRatio=True, mask='auto')

    can.setFont('VeraBI', 10)
    can.drawString(20, 780, STR_SUBTITLE1)
    can.drawString(20, 765, STR_SUBTITLE2)
    can.setFont('VeraIt', 8)
    can.drawString(480, 20, PAGE[5])

    can.drawImage(img_file[8], x1_start, y1_start, width=520, preserveAspectRatio=True, mask='auto')
    can.drawImage(img_file[9], x2_start, y2_start, width=520, preserveAspectRatio=True, mask='auto')
    can.showPage()

    can.save()
