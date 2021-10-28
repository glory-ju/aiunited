import requests as req
import pandas as pd
import json
import datetime
import re


# csv 파일 읽기
df = pd.read_csv('data/store_info.csv', encoding='utf-8')
df = df.astype({'s_link':'str'})

# 크롤링한 데이터 저장할 데이터프레임 생성
review_columns = ['store_id','portal_id','date', 'score','review']
store_review = pd.DataFrame(columns=review_columns)

s_link = df['s_link'].values.tolist()
store_id = df['store_id'].values.tolist()


headers = {
    'authority': 'api.siksinhot.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'siksinoauth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjAsImlhdCI6MTYzNTQxMDE1MSwiZXhwIjoxNjM1NDk2NTUxLCJpc3MiOiJzaWtzaW4ifQ.zYoq5aV4Y2ZvNFAX9IRs0-5DSwFVY6dLoaBIWuBhKpA',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.siksinhot.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.siksinhot.com/',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

for s_id,link in zip(store_id, s_link):
    url = f'https://api.siksinhot.com/v1/hp/{link}/review'

    res = req.get(url, headers=headers)
    res_text = res.text
    total_review = int(res_text.split('"cnt":')[1].split(',')[0])


    if total_review == 0:
        pass
    else:
        params = (
            ('idx', '0'),
            ('limit', total_review),
            ('sort', 'T'),
        )

        response = req.get(url, headers=headers, params=params)
        res_text2 = response.text


        var = re.compile('{"tid":.*?]}')
        reviews = var.findall(res_text2)

        for idx, i in enumerate(reviews):
            reviews[idx] = json.loads(i)
            timestamp = reviews[idx]['writeDt']
            storyContent = reviews[idx]['storyContents'].replace('\n', '').replace('\r', '')
            scr = reviews[idx]['score']
            date_time = datetime.datetime.fromtimestamp(timestamp/1000).date()

            store_review = store_review.append(pd.DataFrame([[int(s_id), 1001, date_time,
                                                             scr, storyContent]], columns=review_columns))


print(store_review.iloc[0, :])
# store_review.to_csv('siksin_review2.csv', encoding='utf-8-sig', index=False)

