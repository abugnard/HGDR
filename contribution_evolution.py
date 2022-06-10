"""show_map.py
    defines limits of the bounding box and print map from user's selection.
"""
# Import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
from rapidfuzz import process, fuzz
from datetime import datetime
import unidecode
import json
import datetime
import matplotlib.pyplot as plt
import webbrowser


def evol_osm(ctry_2_dl):
    ctry_done = [0] * len(ctry_2_dl)
    date_ = [0] * 31
    k = 0

    for ctry2dl in ctry_2_dl:
        if ctry2dl == 'Democratic Republic of the Congo':
            ctry2dl = 'Congo-Kinshasa'
        elif ctry2dl == 'Congo-Brazzaville':
            ctry2dl = 'Republic of the Congo'
        elif ctry2dl.split('/')[0] == 'us-west':
            ctry2dl = 'us'

        cr_el = [0] * 31
        mod_el = [0] * 31
        del_el = [0] * 31
        contr = [0] * 31
        if ctry2dl.split('/')[0] not in ctry_done:
            ctry_done[k] = ctry2dl.split('/')[0]
            k = k + 1
            if k > 1:
                print('...')
                print('Processing further countries ...')
                print('...')
            elif ctry2dl.split('/')[0] == 'great-britain':
                ctry2dl = 'United Kingdom'
            elif ctry2dl.split('/')[0] == 'us':
                ctry2dl = 'United States'
            elif ctry2dl.split('/')[0] == 'Falkland Islands':
                ctry2dl = 'Falkland Islands Islas Malvinas'
            for i in range(0, 31):
                URL = 'https://osmstats.neis-one.org/?item=countries&date='
                Previous_Date = datetime.datetime.today() - datetime.timedelta(days=i + 1)
                dt_string = Previous_Date.strftime("%d-%m-%Y")
                URL = URL + dt_string

                r = requests.get(URL)
                page_body = r.text
                soup = BeautifulSoup(page_body, 'html.parser')

                beg = str(soup).find('countryEdits = ')
                end = str(soup).find(';</script>')

                str_data = str(soup)[beg + 15:end]
                convertedDict = json.loads(str_data)

                df = pd.DataFrame(convertedDict)

                df = df.transpose()

                df.columns = ['Country', 'x', 'Contributors', 'y', 'Created elements', 'Modified elements',
                              'Deleted elements', 'y', 'z']
                df = df.sort_values(by='Created elements', ascending=False)

                if i == 0:
                    search_str = unidecode.unidecode(ctry2dl.split('/')[0])

                    most_similar = process.extractOne(search_str, df['Country'], scorer=fuzz.WRatio)

                    output = most_similar[0]
                    output = output.replace('(', '\(')
                    output = output.replace(')', '\)')


                contain_values = df[df['Country'].str.contains(output)]
                date_[i] = dt_string
                cr_el[i] = cr_el[i] + contain_values['Created elements'].values[0]
                mod_el[i] = mod_el[i] + contain_values['Modified elements'].values[0]
                del_el[i] = del_el[i] + contain_values['Deleted elements'].values[0]
                contr[i] = contr[i] + contain_values['Contributors'].values[0]

            df_evo = pd.DataFrame(cr_el, columns=['created elements'])
            df_evo['modified elements'] = mod_el
            df_evo['deleted elements'] = del_el
            df_evo['date'] = date_
            df_evo['Contributors'] = contr
            df_evo = df_evo.loc[::-1].reset_index(drop=True)

            mycolors = ['tab:pink', 'tab:blue', 'tab:green', 'tab:orange']
            columns = ['modified elements', 'deleted elements', 'created elements', 'Contributors']

            x = df_evo['date']
            y1 = df_evo['deleted elements']
            y2 = df_evo['modified elements']
            y3 = df_evo['created elements']
            y4 = df_evo['Contributors']

            fig, ax1 = plt.subplots(1, 1, figsize=(16, 9), dpi=80)

            ax1.fill_between(x, y1=y3, y2=y1, label=columns[2], alpha=0.4, color=mycolors[2], linewidth=2)
            ax1.fill_between(x, y1=y2, y2=y1, label=columns[0], alpha=0.4, color=mycolors[0], linewidth=2)
            ax1.fill_between(x, y1=y1, y2=0, label=columns[1], alpha=0.4, color=mycolors[1], linewidth=2)

            # Plot Line2 (Right Y Axis)
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.plot(x, y4, label=columns[3], color='tab:red', linewidth=3)

            # Decorations
            # ax1 (left Y axis)
            ax1.set_xlabel('date', fontsize=20)
            ax1.tick_params(axis='x', rotation=45, labelsize=12)
            ax1.set_ylabel('Created/Modified/Deleted Elements', fontsize=20)
            ax1.tick_params(axis='y', rotation=0)
            ax1.grid(alpha=.4)

            # ax2 (right Y axis)
            ax2.set_ylabel("Number of contributors", color='tab:red', fontsize=20)
            ax2.tick_params(axis='y', labelcolor='tab:red')
            # ax2.set_xticklabels(x, rotation=45, fontdict={'fontsize':10})
            ax2.set_title("Evolution of contribution for " + output + ' between ' + date_[30] + ' and ' + date_[0],
                          fontsize=22)
            fig.tight_layout()
            # Lighten borders
            plt.gca().spines["top"].set_alpha(0)
            plt.gca().spines["bottom"].set_alpha(.3)
            plt.gca().spines["right"].set_alpha(0)
            plt.gca().spines["left"].set_alpha(.3)

            ax1.legend(loc='best', fontsize=12)

            plt.savefig("OSM_last_month.png")
            new = 2
            webbrowser.open('html_evolution.html', new=new)
            print('Evolution for {} available !'.format(output))

        else:
            continue
