import pandas as pd
import requests
import re
import json
import datetime
from tqdm import tqdm



def action_google_store_info(storeInfo):
    if 'website' not in storeInfo.columns:
        storeInfo['website'] = pd.Series()
    storeInfo['g_link'] = pd.Series()

    for i in tqdm(range(len(storeInfo))):
        google_link, website = search_store(storeInfo['store_name'][i],
                                            storeInfo['store_addr'][i],
                                            storeInfo['store_addr_new'][i],
                                            storeInfo['store_tel'][i])
        if google_link:
            storeInfo.loc[i, 'g_link'] = google_link
        if website:
            storeInfo.loc[i, 'website'] = website
    
    return storeInfo


def search_store(store_name, store_addr, store_addr_new, store_tel):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',}
    response = requests.get('https://www.google.com/maps/search/'+ store_addr + ' ' + store_name, headers=headers)
    response_text = response.text

    p = re.compile('window.APP_INITIALIZATION_STATE=.*?[;]window')
    tmp = p.search(response_text).group()
    tmp = tmp.lstrip('window.APP_INITIALIZATION_STATE=').rstrip(';window')

    response_json = json.loads(tmp)
    response_json = response_json[3][2].lstrip(")]}'\n")
    response_json = json.loads(response_json)
    response_json = response_json[0][1]

    search_addr = search_tel = ''
    search_link = search_website = None
    review_param = None
    review_cnt = 0

    if pd.isna(store_addr_new): store_addr_new = ''
    if pd.isna(store_tel): store_tel = ''

    search_link = 'https://www.google.com/maps/search/'+ store_addr + ' ' + store_name

    for searchInfo in response_json:
        searchInfo = searchInfo[-1]

        if len(searchInfo) < 3:
            continue

        if searchInfo[39] != None:
            search_addr = searchInfo[39]
        if searchInfo[178] != None:
            search_tel = searchInfo[178][0][0]

        if store_addr in search_addr or store_addr_new in search_addr or store_tel.replace('-','') == search_tel.replace('-',''):
            # search_link = searchInfo[42]

            if searchInfo[7] != None:
                search_website = searchInfo[7][0]

            break

    return search_link, search_website