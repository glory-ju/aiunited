import numpy as np


def store_info(idx):
    store = load['result']['place']['list'][idx]['name']
    store_x = load['result']['place']['list'][idx]['x']
    store_y = load['result']['place']['list'][idx]['y']
    store_addr = load['result']['place']['list'][idx]['address']
    store_addr_new = load['result']['place']['list'][idx]['roadAddress']
    store_tel = load['result']['place']['list'][idx]['tel']
    open_hours = load['result']['place']['list'][idx]['bizhourInfo']
    n_link = load['result']['place']['list'][idx]['id']
    website = load['result']['place']['list'][idx]['homePage']

    print(i+1, store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website, sep='\n')
    print()

def to_csv(i, idx):
    store = load['result']['place']['list'][idx]['name']
    store_x = load['result']['place']['list'][idx]['x']
    store_y = load['result']['place']['list'][idx]['y']
    store_addr = load['result']['place']['list'][idx]['address']
    store_addr_new = load['result']['place']['list'][idx]['roadAddress']
    store_tel = load['result']['place']['list'][idx]['tel']
    open_hours = load['result']['place']['list'][idx]['bizhourInfo']
    n_link = load['result']['place']['list'][idx]['id']
    website = load['result']['place']['list'][idx]['homePage']

    data_frame.append([i+22543, df['store_addr'][i][:2], store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website])
    dataset = pd.DataFrame(data_frame, columns=['store_id', 'region', 'store_name', 'store_x', 'store_y', 'store_addr', 'store_addr_new', 'store_tel', 'open_hours', 'n_link', 'website'])
    dataset.to_csv('naver_store_info_time.csv', encoding='UTF-8', index=False)



import requests
import json
import pandas as pd
import time
import random

df = pd.read_csv('storeInfo_1.csv')

count = int(len(df) / 100) + 2
num_100 = -100

data_frame = []

for i in range(len(df)):
    time.sleep(np.random.randint(0, 4))
    df['new_name'] = df['store_name'][i] + ' ' + df['store_addr'][i][:12]
    new_name = df['new_name'][i]

    headers = {
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
               'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; _ga=GA1.2.878040348.1627623526; ASID=dc5f3dbd0000017bc9a08e5f0000005a; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; BMR=s=1635143616649&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dmck0903%26logNo%3D221442957432&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hUpiasp0JywssLOingosssssthC-510028; NID_SES=AAABpbD2qjHEUIH3pWB4k7ykWkstFCWkjxSXmzGoQA6z5h2HqI5xJKRYWq3L1In+Id8MLlQkomzzt4MoE26CuvOcQ4xaL12x6Xj6jbavekPWZhilepZfZkmlLJDpHI1mxWu3QJPFb4dltRh4ZuFMNpsy149f2enHKaQv5VxOwUaunoEz4A6/VHB8lAlR3US2J1bdWvnhx0YcjtTGPJwYad32ygfxSxNDwLI57+StZkeTh+hXyTQPDadd5fo7FS7g6RwHf3Xo999b8ub9F43Z9u0Ua+5D9+qxdvZReRVdNVRsR45CvAG/poMR2XAw0bj8vSgHh5dx62dFZKB763UKFPTm+l8/APzys2yvohX/nbjbALdv43XO/nQVoSjjpBYrfTni4jG5OvjFkPCqJAFP6kNhsrqGOFnc7BSDlAvSrnutBgLwrnUvDFn4Lnbdou3Vxx3m9KUflIpitWBxqHCYg7c4iAl7rVsn9b7iZm8HRa/GxG8JiXIZ7iJZ+zlBunEM2nQRgGN0kkjWwawfZFynjVqkcGVM02fxavo4jr9Z0AkMcGs+EzYdJmEHTxv9NzE4QHY9gA==; csrf_token=0462579b6db64a53558dd357d5d0f718c775ca6ca9ee0a51f671bfc170779510819d3335dabf0700e10fd6a8a79b8a5ccff05683e8c47095049a248ab522e86a; page_uid=f332993b-0836-4b3c-86a2-821516a4cc7b',
               }

    params = (
                ('query', new_name),
                ('page', '1'),
                ('displayCount', '20'),
            )
    response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
    load = json.loads(response.text)

    try:
        try:
            try:
                csv_addr = df['store_addr'][i][:12]

                for idx in range(len(load['result']['place']['list'])):
                    store_addr = load['result']['place']['list'][idx]['address'][:12]

                    if store_addr == csv_addr:
                        store_info(idx)
                        to_csv(i, idx)
                        break
                    elif store_addr[:15] == csv_addr[:15]:
                        store_info(idx)
                        to_csv(i, idx)
                        break
                    elif store_addr[:7] == csv_addr[:7]:
                        store_info(idx)
                        to_csv(i, idx)
                        break
                    elif store_addr[:10] == csv_addr[:10]:
                        store_info(idx)
                        to_csv(i, idx)
                        break

            except:
                new_name = df['store_name'][i] + ' ' + df['store_addr'][i]
                params = (
                    ('query', new_name),
                    ('page', '1'),
                    ('displayCount', '20'),
                )
                response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
                load = json.loads(response.text)
                store_info(idx)
                to_csv(i, idx)

        except:
            new_name = df['store_name'][i][:8]
            params = (
                ('query', new_name),
                ('page', '1'),
                ('displayCount', '20'),
            )
            response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
            load = json.loads(response.text)

            csv_addr = df['store_addr'][i][:12]
            web_name = df['store_name'][i] + ' ' + df['store_addr'][i]

            for idx in range(len(load['result']['place']['list'])):
                store_addr = load['result']['place']['list'][idx]['address'][:12]


                if store_addr == csv_addr:
                    store_info(idx)
                    to_csv(i, idx)
                    break
                elif store_addr[:15] == csv_addr[:15]:
                    store_info(idx)
                    to_csv(i, idx)
                    break
    except:
        data_frame.append('')



