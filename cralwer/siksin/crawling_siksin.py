import requests as req
import pandas as pd
import json
import datetime
import re

# csv 파일 읽기
df = pd.read_csv('data/store_info.csv', encoding='euc-kr')

# header 저장
# 'siksinoauth' 갱신 필요함
def action_siksin_review_crwaler(df):
    review_columns = ['store_id', 'portal_id', 'date', 'score', 'review']
    store_review = pd.DataFrame(columns=review_columns)
    df = df.astype({'s_link': 'str'})
    df = df.astype({'store_id':'int'})
    s_link = df['s_link'].values.tolist()
    store_id = df['store_id'].values.tolist()

    headers = {
        'siksinoauth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjAsImlhdCI6MTYzNTQxMDE1MSwiZXhwIjoxNjM1NDk2NTUxLCJpc3MiOiJzaWtzaW4ifQ.zYoq5aV4Y2ZvNFAX9IRs0-5DSwFVY6dLoaBIWuBhKpA',
    }

    for s_id,link in zip(store_id, s_link):
        url = f'https://api.siksinhot.com/v1/hp/{link}/review'

        res = req.get(url, headers=headers)
        res_text = res.text
        total_review = json.loads(res_text)['data']['cnt']

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
                review = json.loads(i)
                timestamp = review['writeDt']
                storyContent = review['storyContents'].replace('\n', '').replace('\r', '')
                scr = review['score']
                date_time = datetime.datetime.fromtimestamp(timestamp/1000).date()

                store_review = store_review.append(pd.DataFrame([[s_id, 1001, date_time,
                                                                 scr, storyContent]], columns=review_columns))

    return store_review



def action_siksin_store_info(df):
    df = df.astype({'s_link':'str'})
    df = df.astype({'store_id':'int'})
    s_link = df['s_link'].values.tolist()
    store_id = df['store_id'].values.tolist()
    store_name = df['store_name'].values.tolist()

    for idx, (s_id, link, name) in enumerate(zip(store_id, s_link, store_name)):

        if df.iloc[idx][:].isnull().values.any() == True:

            headers = {
                'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'cookie': 'lang=ko; dable_uid=87785282.1623807812548; __gads=ID=7e4bf84be73bed3d-226037bfd2cc0027:T=1634893699:RT=1634893699:S=ALNI_MYAhM54Ffr67Y30HAdRCrm1Asyywg; _gid=GA1.2.1828807244.1635322615; _ga=GA1.2.686690300.1634892536; _ga_BWRRE5S41P=GS1.1.1635407673.37.1.1635416292.20',
            }

            url = f'https://www.siksinhot.com/P/{link}'
            res = req.get(url, headers=headers)
            res_text = res.text
            print(s_id)

            var = re.compile('{"pid":.*?"}')
            info = var.findall(res_text)
            info_json = json.loads(info[1])
            region = info_json['upHpAreaTitle']
            lat = info_json['lat']
            lng = info_json['lng']
            addr = info_json['addr']
            addr2 = info_json['addr2']
            phone = info_json['phone']
            homepage = info_json['homepage']

            try:
                var2 = re.compile('{"oprtCode":.*?}')
                open_hours = var2.search(res_text).group()
                opn_hrs_json = json.loads(open_hours)
                weekbit = opn_hrs_json['weekBit']

                week = '월화수목금토일'
                for day, i in enumerate(weekbit):
                    if i == '0':
                        week = week.replace(week[day], ' ')
                    elif i == '1':
                        continue

                week = week.replace(' ', '')
                opn_hrs = week + ' ' + opn_hrs_json['startTm'] + ' ' + opn_hrs_json['endTm']

            except:
                opn_hrs = ''

            df.iloc[idx] = (s_id, region, name, lat, lng, addr, addr2, phone, opn_hrs, homepage, link)

        else:
            pass

    return df

# store_hrs.to_csv('siksin_info.csv', encoding='utf-8-sig', index=False)


# store_review.to_csv('siksin_review2.csv', encoding='utf-8-sig', index=False)