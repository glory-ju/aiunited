import pandas as pd
import requests
import re
import json
import time
import numpy as np
from tqdm import tqdm

# 구글 맵스에서 F12, 네트워크에서 해당 음식점 검색 후 curl 카피후 python 변환

df = pd.read_csv('storeInfo_1.csv', sep=',', encoding='utf-8')
df = df.iloc[0:100, :]

df['key_words'] = df['store_addr'] + ' ' + df['store_name']

review_dataset = []
store_info_dataset = []

for n, keyword in tqdm(enumerate(df['key_words'].tolist())):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    }

    params = (
        ('hl', 'ko'),
    )

    store_id = df.loc[n]['store_id']
    first_query = ''
    second_query = ''
    review_cnt = 0

    website = ''
    g_link = f'https://www.google.com/maps/search/{keyword}'

    print(f'store_id : {store_id}')
    # print(keyword, end=" ")

    response = requests.get(f'https://www.google.com/maps/search/{keyword}', headers=headers, params=params)
    res_text = response.text

    # 정규표현식 작성 및 store pb값 추출
    var = re.compile('window.APP_INITIALIZATION_STATE.*?;window')
    var = var.search(res_text).group().replace('\\"', '').replace('[', '').replace(']', '').split(',')

    try:
        for idx, item in enumerate(var):
            if item[:3] == '리뷰 ':
                review_cnt = var[idx]
                review_cnt = review_cnt.replace('리뷰 ', '').replace('개', '')

                if var[idx + 1] != 'null':
                    review_cnt = var[idx] + var[idx + 1]
                    review_cnt = review_cnt.replace('리뷰 ', '').replace('개', '')

            if item[:3] == '385':
                first_query = var[idx]
                second_query = var[idx + 1]
                break

    except:
        print('No result')
        continue

    # print(first_query, second_query, review_cnt, website, g_link)
    store_info_dataset.append([store_id, website, g_link])


    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        }

    for num in range(0, int(review_cnt), 10):
        try:
            params = (
                ('authuser', '0'),
                ('hl', 'ko'),
                ('gl', 'kr'),
                ('pb',
                 f'!1m2!1y{first_query}!2y{second_query}!2m2!1i{num}!2i10!3e2!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sZ012YdKFJuW4mAWWz67ICg!7e81'))

            response = requests.get('https://www.google.com/maps/preview/review/listentitiesreviews', headers=headers,
                                    params=params)
            res_text = response.text
            res_text = res_text.replace(")]}'", "")

            # json으로 load
            info_json = json.loads(res_text)

            for i in info_json[2]:
                portal_id = 1002
                review_text = i[3]
                score = i[4]
                date = pd.to_datetime(f'{i[27]}', unit='ms')

                if review_text == None:
                    continue
                else:
                    review_dataset.append([store_id, portal_id, review_text, score, str(date)[0:10]])

        except:
            print('end of docs')
            break

# save as csv (store info)
info_df = pd.DataFrame(store_info_dataset, columns=['store_id', 'website', 'g_link'])
info_df.to_csv('google_info_15.csv')
print('info saved')


# save as csv (review)
review_df = pd.DataFrame(review_dataset, columns=['store_id', 'portal_id', 'review', 'score', 'date'])
review_df.to_csv('google_review_15.csv')
print('review saved')

