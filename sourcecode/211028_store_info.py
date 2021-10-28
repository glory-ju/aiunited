import requests
import json
import pandas as pd
from bs4 import BeautifulSoup as bs

df = pd.read_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/storeInfo_1.csv')
# df['new_name'] = df['store_name']+' '+df['store_addr']
data_frame = []

for i in range(len(df)):
    df['new_name'] = df['store_name'] + ' ' + df['store_addr'][i][:10]
    try:
        store_name = df['new_name'][i]

        headers = {
            'authority': 'map.naver.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'content-type': 'application/json',
            'accept': 'application/json, text/plain, */*',
            'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://map.naver.com/',
            'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; _ga=GA1.2.878040348.1627623526; ASID=dc5f3dbd0000017bc9a08e5f0000005a; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; BMR=s=1635143616649&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dmck0903%26logNo%3D221442957432&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hUB9Uwp0Jywss57kc14ssssssGs-143163; NID_SES=AAABpADrHg1mPOsff2KN9ndSw2cZacxbh8H6dvok+TOzGB8+HAZ5GvpnJ8OIRooBsKwOURNsY4hhvv1Y4JJQnddF1IgRMrYopHzbbYGgc2s1jUUk5we5R5mN/w31U3j3cFG372de/8R/BeGp/CvoNH3/5I5BOHrD76diOaI8vus755m9AlC7rnHx/uWXhK5p7ptjqON2l2HVKCxxM7lhlLuHwrF+/4czqHwhL3TuKuElyWyNguqaHYMcib9QJgFGrLG7Aqclaj7s3hHFZ0u0WCHo3nJjgcfeJVrLpY2EaJcW3IX7lhHQQHIweFN39aEuSyPt1g8/nO8hJaskqu6g0XxGInzN1baJSmtoHeubWZsSRYOymqeExQ888fTPviqUcZsJzwvgxuw9Jykdv+Rt0lcxbAnAAkM7Mu9TbYH+Z6sCTuoeAwJwnrTj7QGS4EGnknbSzd+3y5KaFJVd4zbvN0Bi1UqQ8LjsP9INuPSvqAeRF5WHr9JlGHFmCVb8tDzhzbB4PRfnvwy4TAQ14pwgA4LSv7rdVZ4uNlR2/jDmLS17KZpCEKNn/Aws0hAX5RMv/ZNPBg==; csrf_token=106dc856ba2889ea34493a7389c26602c775ca6ca9ee0a51f671bfc170779510819d3335dabf0700e10fd6a8a79b8a5ccff05683e8c47095049a248ab522e86a; page_uid=ccdeb73c-3c2c-470f-a1c4-688a3e0c064c',
        }

        params = (
            ('caller', 'pcweb'),
            ('query', store_name),
            ('type', 'all'),
            ('page', '1'),
            ('displayCount', '20'),
            ('isPlaceRecommendationReplace', 'true'),
            ('lang', 'ko'),
        )

        response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
        print(response.text)

        soup = bs(response.text, 'html.parser')

        store_list = soup.select('')

        json_loads = json.loads(response.text)
        store = json_loads['result']['place']['list'][0]['name']
        store_x = json_loads['result']['place']['list'][0]['x']
        store_y = json_loads['result']['place']['list'][0]['y']
        store_addr = json_loads['result']['place']['list'][0]['address']
        store_addr_new = json_loads['result']['place']['list'][0]['roadAddress']
        store_tel = json_loads['result']['place']['list'][0]['tel']
        open_hours = json_loads['result']['place']['list'][0]['bizhourInfo']
        n_link = json_loads['result']['place']['list'][0]['id']
        website = 'https://map.naver.com/v5/search/'+ store_name + '/place/' + str(n_link)

        print(store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website, sep='\n')
        print()
        data_frame.append([store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website])
    except:
        print('None')

df1 = pd.DataFrame(data_frame, columns=[store, store_x, store_y, store_addr, store_addr_new, store_tel, open_hours, n_link, website])
df1.to_csv('fuck.csv', encoding='utf-8-sig', index=False)