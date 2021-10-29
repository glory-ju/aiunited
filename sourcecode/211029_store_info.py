def store_info(idx):
    store = load['result']['place']['list'][idx]['name']
    store_x = load['result']['place']['list'][idx]['x']
    store_y = load['result']['place']['list'][idx]['y']
    store_addr = load['result']['place']['list'][idx]['address']
    store_addr_new = load['result']['place']['list'][idx]['roadAddress']
    store_tel = load['result']['place']['list'][idx]['tel']
    open_hours = load['result']['place']['list'][idx]['bizhourInfo']
    n_link = load['result']['place']['list'][idx]['id']
    website = 'https://map.naver.com/v5/search/' + web_name + '/place/' + str(n_link)

    print(store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website, sep='\n')
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
    website = 'https://map.naver.com/v5/search/' + web_name + '/place/' + str(n_link)

    data_frame.append([i+1, df['store_addr'][i][:2], store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website])
    dataset = pd.DataFrame(data_frame, columns=['store_id', 'region', 'store_name', 'store_x', 'store_y', 'store_addr', 'store_addr_new', 'store_tel', 'open_hours', 'n_link', 'website'])
    dataset.to_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/naver_store_info1.csv', encoding='utf-8-sig', index=False)

import requests
import json
import pandas as pd
import time

df = pd.read_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/storeInfo_1.csv')

count = int(len(df) / 100) + 2
num_100 = -10

data_frame = []

for i in range(100):
    time.sleep(1)
    df['new_name'] = df['store_name'][i] + ' ' + df['store_addr'][i][:12]
    new_name = df['new_name'][i]

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',}

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
            # store_info(idx)
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
        data_frame.append('NoInfo')
