import requests as req
import pandas as pd
import json
import datetime
import re


# csv 파일 읽기
df = pd.read_csv('data/store_info.csv', encoding='utf-8')


# header 저장
# 'siksinoauth' 갱신 필요함
def get_review(df):
    review_columns = ['store_id', 'portal_id', 'date', 'score', 'review']
    store_review = pd.DataFrame(columns=review_columns)
    df = df.astype({'s_link': 'str'})
    s_link = df['s_link'].values.tolist()
    store_id = df['store_id'].values.tolist()

    headers = {
        # 'authority': 'api.siksinhot.com',
        # 'pragma': 'no-cache',
        # 'cache-control': 'no-cache',
        # 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        # 'accept': 'application/json, text/plain, */*',
        'siksinoauth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjAsImlhdCI6MTYzNTQxMDE1MSwiZXhwIjoxNjM1NDk2NTUxLCJpc3MiOiJzaWtzaW4ifQ.zYoq5aV4Y2ZvNFAX9IRs0-5DSwFVY6dLoaBIWuBhKpA',
        # 'sec-ch-ua-mobile': '?0',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'origin': 'https://www.siksinhot.com',
        # 'sec-fetch-site': 'same-site',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-dest': 'empty',
        # 'referer': 'https://www.siksinhot.com/',
        # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }


    #
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
    return store_review


def get_opn_hrs(df):
    store_columns = ['store_id', 'open_hours']
    store_hrs = pd.DataFrame(columns=store_columns)
    s_link = df['s_link'].values.tolist()
    store_id = df['store_id'].values.tolist()
    for s_id,link in zip(store_id, s_link):
        try:
            headers = {
                'authority': 'www.siksinhot.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.siksinhot.com/',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'lang=ko; dable_uid=87785282.1623807812548; __gads=ID=7e4bf84be73bed3d-226037bfd2cc0027:T=1634893699:RT=1634893699:S=ALNI_MYAhM54Ffr67Y30HAdRCrm1Asyywg; _gid=GA1.2.1828807244.1635322615; _ga=GA1.2.686690300.1634892536; _ga_BWRRE5S41P=GS1.1.1635407673.37.1.1635416292.20',
            }

            url = f'https://www.siksinhot.com/P/{link}'
            res = req.get(url, headers=headers)
            res_text = res.text

            var = re.compile('매장 영업시간.*?</label>')
            open_hours = var.search(res_text).group()
            opn_hrs = open_hours[-21:-8]
            store_hrs = store_hrs.append(pd.DataFrame([[int(s_id), opn_hrs]], columns=hrs_columns))
        except:
            store_hrs = store_hrs.append(pd.DataFrame([[int(s_id)]], columns=hrs_columns))
    return store_hrs

# store_hrs.to_csv('siksin_info.csv', encoding='utf-8-sig', index=False)


# store_review.to_csv('siksin_review2.csv', encoding='utf-8-sig', index=False)
