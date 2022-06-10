
import pandas as pd
from rapidfuzz import process, fuzz
import unidecode


def stat_compiler(country_2_dl):
    df_stats = pd.read_csv('quality_OSM.csv', sep=';')
    i = 0
    for c in country_2_dl:
        if c == 'Haiti and Dominican Republic':
            c = 'Haiti'
            country_2_dl[i] = c.split('/')[0]
            i = i + 1
        elif c.split('/')[0] == 'us-west' or c.split('/')[0] == 'us':
            c = 'United States'
            country_2_dl[i] = c.split('/')[0]
            i = i + 1
        else:
            country_2_dl[i] = c.split('/')[0]
            i = i + 1
    i = 0
    print(country_2_dl)
    country_2_dl = list(set(country_2_dl))
    b_cap = len(country_2_dl) * [0]
    ISO2 = len(country_2_dl) * [0]
    ISO3 = len(country_2_dl) * [0]
    IDH = len(country_2_dl) * [0]
    PopuDens = len(country_2_dl) * [0]
    Population = len(country_2_dl) * [0]
    Areatot = len(country_2_dl) * [0]
    Country = len(country_2_dl) * [0]

    for ctry2dl in country_2_dl:
        search_str = unidecode.unidecode(ctry2dl)
        most_similar = process.extractOne(search_str, df_stats['Country'], scorer=fuzz.WRatio)
        ctry2dl = most_similar[0]
        b_cap[i] = round(float(df_stats[df_stats['Country'] == ctry2dl]['b_per_cap']), 1)
        ISO2[i] = str(df_stats[df_stats['Country'] == ctry2dl]['ISO2'].values)
        ISO3[i] = str(df_stats[df_stats['Country'] == ctry2dl]['ISO3'].values)
        IDH[i] = float(df_stats[df_stats['Country'] == ctry2dl]['IDH'])
        PopuDens[i] = float(df_stats[df_stats['Country'] == ctry2dl]['PopDens_cap_km2'])
        Population[i] = float(df_stats[df_stats['Country'] == ctry2dl]['Population'])
        Areatot[i] = float(df_stats[df_stats['Country'] == ctry2dl]['area_km2'])
        Country[i] = ctry2dl
        i = i + 1

    b_cap = [i for i in b_cap if i != 0]
    ISO2 = [i for i in ISO2 if i != 0]
    ISO3 = [i for i in ISO3 if i != 0]
    IDH = [i for i in IDH if i != 0]
    Country = [i for i in Country if i != 0]
    Areatot = [i for i in Areatot if i != 0]
    PopuDens = [i for i in PopuDens if i != 0]
    Population = [i for i in Population if i != 0]

    return b_cap, ISO2, ISO3, IDH, Country, Areatot, PopuDens, Population