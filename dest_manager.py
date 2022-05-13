
def param_setter(link):
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

    return param_link1, param_link2, param_link3, param_link4, param_link5, param_link6, param_link7, param_link8