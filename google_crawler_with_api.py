import pandas as pd
import requests
import re
import json
import time
import numpy as np

# 구글 맵스에서 F12, 네트워크에서 해당 음식점 검색 후 curl 카피후 python 변환

df = pd.read_csv('store_info.csv', sep=',', encoding='utf-8')

df = df[['store_id', 'region', 'store_name', 'store_addr', 'store_addr_new']]

df['key_words'] = df['store_addr'] + ' ' + df['store_name']

dataset = []

for n, keyword in enumerate(df['key_words'].tolist()):
    headers = {
        'authority': 'www.google.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'device-memory': '8',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-client-data': 'CIq2yQEIprbJAQjBtskBCKmdygEIvNHKAQj0gcsBCOryywEI7/LLAQie+csBCLT/ywEI3ITMAQjnhMwBCLaFzAEI/4XMAQiAhswBCOCGzAEIg4jMARitqcoB',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.google.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'OGPC=19025836-2:; OTZ=6182319_20_20__20_; SID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjM-D3OKDodiA0RM5Q4T34Tg.; __Secure-1PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjXzeBW1luBJPzmSeHj2MPNw.; __Secure-3PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKj_dijG7zA6b9wAR-ksa2diQ.; HSID=A1cbJgo3cmd9o4Y37; SSID=AzGv90Vg5d1cMLl1Z; APISID=otxhKN_r3r5yzlSp/AiLBIT5EBQz_7VDFH; SAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-1PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-3PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; 1P_JAR=2021-10-25-05; NID=511=j3aN7ARLOW4WdQ7VYzqiDT2X9bgxF7bxnzvfBqzVZIMsCYTY7MhwgRdgqinmsCpuxapZMqBSWj4ovVvp5rOOTI_4qB5Ifur8HWSEm-ZFltfDYEz2sv6HCZ5Bxy5SeJF44H9PhS-c90Ugm7gdlq-2LdBJnDzOyRFj9MLaviErk8KzVPokxGpiE7QoONtxXPD6cs2Em83IAdCBtwqUfHJqX_N4YYzpdkmQIx7_1C3nUICs2CtHxwqQraGVFECd4AcWgGW5YAvD17NZzbEsU4rEG0wfTH-VcmQfsyCLkZ9HeOyMSNHWQnRX; DV=s0qLE12XtocTUAuW96t36_4OpPBfyxc; SIDCC=AJi4QfGKSMePgNPX80AmvjI9tUM_m6uR54jqZmdBfSaU-S2lchqxxLSsKr9xvQgrz8R1DO3snsA; __Secure-3PSIDCC=AJi4QfE1RS4e_Hom3SDIg2n-ZiQX2C_q0loQU8-htb-Gpbobh2b5wYkepH2360JfrndsahiRp8kd',
    }

    params = (
        ('hl', 'ko'),
    )

    store_id = n + 1
    first_query = ''
    second_query = ''
    print(f'store_id : {store_id}')
    print(keyword, end=" ")

    response = requests.get(f'https://www.google.com/maps/search/{keyword}', headers=headers, params=params)
    res_text = response.text

    # 정규표현식 작성 및 store pb값 추출
    var = re.compile('window.APP_INITIALIZATION_STATE.*?;window')
    var = var.search(res_text).group().replace('\\"', '').replace('[', '').replace(']', '').split(',')

    for idx, item in enumerate(var):
        if item[:2] == '38':
            first_query = var[idx]
            second_query = var[idx + 1]

    print(first_query, second_query)

    headers = {
        'authority': 'www.google.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'device-memory': '8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'x-client-data': 'CIq2yQEIprbJAQjBtskBCKmdygEIvNHKAQj0gcsBCOryywEI7/LLAQie+csBCLT/ywEI3ITMAQjnhMwBCLaFzAEI/4XMAQiAhswBCOCGzAEIg4jMARitqcoB',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.google.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'OGPC=19025836-2:; OTZ=6182319_20_20__20_; SID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjM-D3OKDodiA0RM5Q4T34Tg.; __Secure-1PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKjXzeBW1luBJPzmSeHj2MPNw.; __Secure-3PSID=DQit8m0i9UP43amvQDZ7JyYDGm78ZhulMqY1j5F6Pusi_OKj_dijG7zA6b9wAR-ksa2diQ.; HSID=A1cbJgo3cmd9o4Y37; SSID=AzGv90Vg5d1cMLl1Z; APISID=otxhKN_r3r5yzlSp/AiLBIT5EBQz_7VDFH; SAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-1PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; __Secure-3PAPISID=AGkxcOT4-PR5sYGS/AurMyyHA7gBpxaheo; NID=511=j3aN7ARLOW4WdQ7VYzqiDT2X9bgxF7bxnzvfBqzVZIMsCYTY7MhwgRdgqinmsCpuxapZMqBSWj4ovVvp5rOOTI_4qB5Ifur8HWSEm-ZFltfDYEz2sv6HCZ5Bxy5SeJF44H9PhS-c90Ugm7gdlq-2LdBJnDzOyRFj9MLaviErk8KzVPokxGpiE7QoONtxXPD6cs2Em83IAdCBtwqUfHJqX_N4YYzpdkmQIx7_1C3nUICs2CtHxwqQraGVFECd4AcWgGW5YAvD17NZzbEsU4rEG0wfTH-VcmQfsyCLkZ9HeOyMSNHWQnRX; 1P_JAR=2021-10-25-06; SIDCC=AJi4QfEFKPv5vpzcWPx635uf2vnq4uHXU4qpJhc_5rPbL2CQBBp3-eHUc4zQL1Y4qey3HXnayGw; __Secure-3PSIDCC=AJi4QfHigAdRZEZMitu3PSPZqg1o1f0_daQotCOgXk_3ddP9_USpRIdnpQoFxQFsTIPduOJuYjXU',
    }

    for num in range(0, 1000, 10):
        try:
            params = (
                ('authuser', '0'),
                ('hl', 'ko'),
                ('gl', 'kr'),
                ('pb',
                 f'!1m2!1y{first_query}!2y{second_query}!2m2!1i{num}!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sZ012YdKFJuW4mAWWz67ICg!7e81'))

            # f'!1m2!1y3854127467291613967!2y13313712869612169873!2m2!1i20!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1s2FF2YbeDD4aDoASR-4joAw!7e81' 가 다음 리뷰페이지의 값 규칙찾기
            # f'!1m2!1y3854127501305852349!2y8238844305192902537!2m2!1i0!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1syWR2YdAvmr_AA7fWhPgO!7e81' 는 뷰투베이커리 리뷰 pb값
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
                    pass
                else:
                    dataset.append([store_id, portal_id, review_text, score, str(date)[0:19]])
                    # print(store_id, portal_id, review_text, score, str(date)[0:19])

        except:
            print('end of docs')
            break

# save as csv
review_df = pd.DataFrame(dataset, columns=['store_id', 'portal_id', 'review', 'score', 'date'])
review_df.to_csv('review_with_api.csv')
print('dataframe saved')


# 27번째 >> 타임 스탬프
# 리뷰텍스트, 별점, 날짜 가져오기
# params에서  pb 값의 변화? >> 리뷰 다음페이지로
# 가게를 특정 > 가게의 리뷰 추출 > 해당가게의 리뷰와 해당가게를 연결


