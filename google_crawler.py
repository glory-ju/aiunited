import pandas as pd
import requests
import re
import json
import time
import numpy as np
from tqdm import tqdm
from df_func import *

def find_params(df):

    df['key_words'] = df['store_addr'] + ' ' + df['store_name']

    dataset = []

    for n, keyword in tqdm(enumerate(df['key_words'].tolist())):
        time.sleep(np.random.randint(1, 3))
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                'cookie': 'OGPC=19025836-2:; OTZ=6182319_20_20__20_; SID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjM-D3OKDodiA0RM5Q4T34Tg.; __Secure-1PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjXzeBW1luBJPzmSeHj2MPNw.; __Secure-3PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKj_dijG7zA6b9wAR-ksa2diQ.; HSID=A1cbJgo3cmd9o4Y37; SSID=AzGv90Vg5d1cMLl1Z; APISID=otxhKN_r3r5yzlSp/AiLBIT5EBQz_7VDFH; SAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-1PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-3PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; 1P_JAR=2021-10-25-05; NID=511=j3aN7ARLOW4WdQ7VYzqiDT2X9bgxF7bxnzvfBqzVZIMsCYTY7MhwgRdgqinmsCpuxapZMqBSWj4ovVvp5rOOTI_4qB5Ifur8HWSEm-ZFltfDYEz2sv6HCZ5Bxy5SeJF44H9PhS-c90Ugm7gdlq-2LdBJnDzOyRFj9MLaviErk8KzVPokxGpiE7QoONtxXPD6cs2Em83IAdCBtwqUfHJqX_N4YYzpdkmQIx7_1C3nUICs2CtHxwqQraGVFECd4AcWgGW5YAvD17NZzbEsU4rEG0wfTH-VcmQfsyCLkZ9HeOyMSNHWQnRX; DV=s0qLE12XtocTUAuW96t36_4OpPBfyxc; SIDCC=AJi4QfGKSMePgNPX80AmvjI9tUM_m6uR54jqZmdBfSaU-S2lchqxxLSsKr9xvQgrz8R1DO3snsA; __Secure-3PSIDCC=AJi4QfE1RS4e_Hom3SDIg2n-ZiQX2C_q0loQU8-htb-Gpbobh2b5wYkepH2360JfrndsahiRp8kd',
            }

            params = (
                ('hl', 'ko'),
            )

            store_id = df['store_id'][n]
            review_cnt = 0
            review_param = None
            search_website = ''
            search_addr = ''
            search_tel = ''

            print(f'store_id : {store_id}\n')
            # print(keyword, end=" ")

            response = requests.get(f'https://www.google.com/maps/search/{keyword}', headers=headers, params=params)
            res_text = response.text

            # 정규표현식 작성 및 store pb값 추출
            var = re.compile('window.APP_INITIALIZATION_STATE.*?;window')
            var = var.search(res_text).group()
            var = var.lstrip('window.APP_INITIALIZATION_STATE=').rstrip(';window')

            response_json = json.loads(var)
            response_json = response_json[3][2].lstrip(")]}'\n")
            response_json = json.loads(response_json)
            response_json = response_json[0][1]

            for searchInfo in response_json:
                searchInfo = searchInfo[-1]

                if len(searchInfo) < 3:
                    continue

                if searchInfo[7] != None:
                    search_website = searchInfo[7][0]

                if searchInfo[39] != None:
                    search_addr = searchInfo[39]

                if searchInfo[178] != None:
                    search_tel = searchInfo[178][0][0]

                # 리뷰 총 개수 확인
                if searchInfo[4] != None:
                    review_cnt = int(searchInfo[4][3][1].replace('리뷰 ', '').replace('개', '').replace(',', ''))

                # g_link 확인
                if review_cnt != 0:
                    if searchInfo[37][0] != None:
                        review_param = searchInfo[37][0][0][29]

                    elif len(searchInfo[52][0]) > 0:
                        review_param = searchInfo[52][0]

                dataset.append(
                    [store_id, [int(review_param[0]), int(review_param[1])], review_cnt, search_addr, search_tel,
                     search_website])
        except:
            print('NO INFO')
            dataset.append([df['store_id'][n], '', 0, df['store_addr'][n], df['store_tel'][n]])

    lst = dataset

    return lst




#####################################

def fill_google_store_info(df, lst):
    # 기존 storeinfo_1 csv 빈 곳을 채워넣기 ..
    # g_link, tel, openhours 등

    df = df.fillna('')
    df['g_link'] = ''

    # 받은 param_list를 series 변환
    website_list = []
    g_link_list = []
    store_tel_list = []

    for idx, item in enumerate(lst):
        website_list.append(lst[idx][-1])
        g_link_list.append(lst[idx][1])
        store_tel_list.append(lst[idx][-2])

    website_series = pd.Series(website_list)
    g_link_series = pd.Series(g_link_list)
    store_tel_series = pd.Series(store_tel_list)

    print(g_link_series)

    # website 채우기
    df['website'] = website_series

    # 전화 번호 채우기
    df['store_tel'] = store_tel_series

    # glink 채우기
    df['g_link'] = g_link_series

    return df

#####################################



def collect_reviews(lst):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'cookie': 'OGPC=19025836-2:; OTZ=6182319_20_20__20_; SID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjM-D3OKDodiA0RM5Q4T34Tg.; __Secure-1PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjXzeBW1luBJPzmSeHj2MPNw.; __Secure-3PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKj_dijG7zA6b9wAR-ksa2diQ.; HSID=A1cbJgo3cmd9o4Y37; SSID=AzGv90Vg5d1cMLl1Z; APISID=otxhKN_r3r5yzlSp/AiLBIT5EBQz_7VDFH; SAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-1PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-3PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; NID=511=j3aN7ARLOW4WdQ7VYzqiDT2X9bgxF7bxnzvfBqzVZIMsCYTY7MhwgRdgqinmsCpuxapZMqBSWj4ovVvp5rOOTI_4qB5Ifur8HWSEm-ZFltfDYEz2sv6HCZ5Bxy5SeJF44H9PhS-c90Ugm7gdlq-2LdBJnDzOyRFj9MLaviErk8KzVPokxGpiE7QoONtxXPD6cs2Em83IAdCBtwqUfHJqX_N4YYzpdkmQIx7_1C3nUICs2CtHxwqQraGVFECd4AcWgGW5YAvD17NZzbEsU4rEG0wfTH-VcmQfsyCLkZ9HeOyMSNHWQnRX; 1P_JAR=2021-10-25-06; SIDCC=AJi4QfEFKPv5vpzcWPx635uf2vnq4uHXU4qpJhc_5rPbL2CQBBp3-eHUc4zQL1Y4qey3HXnayGw; __Secure-3PSIDCC=AJi4QfHigAdRZEZMitu3PSPZqg1o1f0_daQotCOgXk_3ddP9_USpRIdnpQoFxQFsTIPduOJuYjXU',
    }

    dataset = []

    for num in tqdm(range(len(lst))):
        time.sleep(1)
        try:
            print(lst[num])
            for i in range(0, lst[num][2], 10):
                store_id = lst[num][0]
                pb = f'!1m2!1y{lst[num][1][0]}!2y{lst[num][1][1]}!2m2!1i{i}!2i10!3e2!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sZ012YdKFJuW4mAWWz67ICg!7e81'
                params = (
                    ('authuser', '0'),
                    ('hl', 'ko'),
                    ('gl', 'kr'),
                    ('pb', pb))

                response = requests.get('https://www.google.com/maps/preview/review/listentitiesreviews',
                                        headers=headers,
                                        params=params)
                res_text = response.text
                res_text = res_text.replace(")]}'", "")

                # json으로 load
                info_json = json.loads(res_text)

                for j in info_json[2]:
                    portal_id = 1002
                    review_text = j[3]
                    score = j[4]
                    date = pd.to_datetime(f'{j[27]}', unit='ms')

                    if review_text == None:
                        pass

                    else:
                        dataset.append([store_id, portal_id, review_text, score, str(date)[0:10]])
                        # print(store_id, portal_id, review_text, score, str(date)[0:19])

        except:
            print('end of docs')
            pass

    review_df = pd.DataFrame(dataset, columns=['store_id', 'portal_id', 'review', 'score', 'date'])
    print('dataframe saved')

    return review_df

#
# df = read_csv('storeInfo_1.csv').iloc[0:100, 0:]
# print(df)
#
# store_info_lst = find_params(df)
# print(store_info_lst)
#
# store_info = fill_google_store_info(df, store_info_lst)
# print(store_info)
#
# store_info.to_csv('test_store_info.csv', index=False)

# df = read_csv('test_store_info.csv')
# df = df.drop(['key_words'], axis=1)
# df.to_csv('test_store_info_1.csv', index=False)

# collected_reviews = collect_reviews(store_info_lst)
# print(collected_reviews)
#
# collected_reviews.to_csv('test_reviews.csv', index=False)
