import requests
import pandas as pd
import json

df = pd.read_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/store_info.csv', encoding='euc-kr')
id_list = []
data_frame = []

df = df[['store_id', 'region', 'store_name', 'store_addr', 'store_addr_new']]
df['key_words'] = df['store_name'] + ' ' + df['store_addr']

for idx in range(len(df['key_words'])):
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
        'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; _ga=GA1.2.878040348.1627623526; ASID=dc5f3dbd0000017bc9a08e5f0000005a; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; BMR=s=1635143616649&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dmck0903%26logNo%3D221442957432&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hUkvElprvxsssgoJ2/hssssssQs-198217; NID_SES=AAABqmUW7xLj2yVLNCxB5g8ND5JruVzMq00CfVx+6aNGEDWNwA/kDK3sOgNNmUNHf05i9d9dpXWMVmsrt01jIK/VuwbXGbQPeB2XgU0Uu5P0fXEhXMjNnXIjdS89JLV4jf1aGk/68uIzdQHFEVnvU7Mom0ttwfRCTkWUdh4RykauW4UgKpmaE+Xn0p+u6FAfBvnH0IwkmQixu2n2QZgIij4e6/I4NNEjJzVekMKb3EKNH/sKEAo8fYwnSk7sTc9mI1CVwIE0+IfVSUZZ+ymkprp17yrNFIKjb/hIX2alGN4esV4KvE0oDiVPpKZ02LUMWe31GiNu+6NCjhG+XBR8GdRNKgeMjuUDrF2CkrLmAEqn1l3qdFCPsKq9naoWk+OZ3WRsb2hAaI0p6fT93AJXc1cz8t+nx/sXKVPOV32l25qHwzf0JRw/7tIUr1zEJAi0x7h93hOrekEq3kqgpbzHGUWBwm2+NHhN6aQDNDHT/WDnpFKGmoMXz4EdaAMmYkL70nFIjDuQMnjg21ww7bHGCAy/K2xTlgxT0kKXYevhZ9W5SsG2N7i/wuyGklFS7qQqWVWR0w==; page_uid=f8c80504-8a37-4e84-875b-e0d80c6aa761; csrf_token=aa77e25a00fdcf4ca22bfa830129e2efc775ca6ca9ee0a51f671bfc170779510819d3335dabf0700e10fd6a8a79b8a5ccff05683e8c47095049a248ab522e86a',
    }

    params = (
        ('caller', 'pcweb'),
        ('query', df['key_words'][idx]),
        ('type', 'all'),
        ('searchCoord', '127.10516880000041;38.023804000000084'),
        ('page', '1'),
        ('displayCount', '20'),
        ('isPlaceRecommendationReplace', 'true'),
        ('lang', 'ko'),
    )

    try:
        response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
        json_load = json.loads(response.text)

        try:
            id_list.append(int(json_load['result']['place']['list'][0]['id']))
        except:
            id_list.append(int(json_load['id']))

    except:
        id_list.append('None')

    print(id_list)
    print()
    print()

    headers = {
        'authority': 'pcmap-api.place.naver.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': '*/*',
        'content-type': 'application/json',
        'accept-language': 'ko',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://pcmap.place.naver.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pcmap.place.naver.com/restaurant/12024487/review/visitor',
        'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; _ga=GA1.2.878040348.1627623526; ASID=dc5f3dbd0000017bc9a08e5f0000005a; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; BMR=s=1635143616649&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dmck0903%26logNo%3D221442957432&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hUkvElprvxsssgoJ2/hssssssQs-198217; NID_SES=AAABqUdy5qaJkQVgUDBimF9DLBoPCdSxBkJZsVo8hsnxMow89EYkUgvT7hBLsUV8g6xDHKSGZsbUAB77oXk9eMmAl7z8F0nt5lT2FTTIjOQhr2AIBuT7reuiaJ6vqR4AlfGBEUFYiGexgDOu8hDBWDU4owril4TzsNA6VhjAvfcFb5ingrY61nTJ6zZEJ7VwivEqB9zRmJZmbVEk9JQEm/i0AA0cupij+6bpNzuETupLRWAne2uI70+qf56ove0W4PZe7vf1Uw0LPleWAQRdQUbHvHstgH170kk/tqTmCk/KGQejtqjL7R0+1ob+73zPcKXbrVGYeRFyOPU4znAJTA3yh/kiALcssR8KsBi8bNRmIDHUK4hyMxrqxOMDbwbXVHtOAmjpzcK3kYWmirCGRJZpdeu1a9mZChOpTWlxSBLxNt64z/QmEOfQgKlMyw1QZb90wGOvgv5NRVmj7b/6VY+gI5ITpXtLsfjKj7giR5kLBrYnjs0/2U/v7XXLsTP1AgM9zQROQJhZEtCLe9z2NkTv2j54A1dIQ48bGlsrrZ3CpC0ExvrASCYcGOjYNmDb5Q7C8Q==',
    }

    businessid = str(id_list[idx])
    page = 0

    data = '[{"operationName":"getVisitorReviews","variables":{"input":{"businessId":"'+ businessid +'","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":' + str(page) +',"display":100,"isPhotoUsed":false,"includeContent":true,"getAuthorInfo":true},"id":"12024487"},"query":"query getVisitorReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visitCount\\n      viewCount\\n      visited\\n      created\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      language\\n      highlightOffsets\\n      apolloCacheId\\n      translatedText\\n      businessName\\n      showBookingItemName\\n      showBookingItemOptions\\n      bookingItemName\\n      bookingItemOptions\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"}]'
    response = requests.post('https://pcmap-api.place.naver.com/graphql', headers=headers, data=data)

    slicing = json.loads(response.text)
    total_review = slicing[0]['data']['visitorReviews']['total']
    iter_cnt = int(total_review / 100) + 2

    if total_review < 100:
        display = str(total_review)
    else:
        display = str(100)
    try:
        for page in range(iter_cnt):
            data = '[{"operationName":"getVisitorReviews","variables":{"input":{"businessId":"' + businessid + '","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":' + str(page) + ',"display":'+ display +',"isPhotoUsed":false,"includeContent":true,"getAuthorInfo":true},"id":"12024487"},"query":"query getVisitorReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visitCount\\n      viewCount\\n      visited\\n      created\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      language\\n      highlightOffsets\\n      apolloCacheId\\n      translatedText\\n      businessName\\n      showBookingItemName\\n      showBookingItemOptions\\n      bookingItemName\\n      bookingItemOptions\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"}]'
            response = requests.post('https://pcmap-api.place.naver.com/graphql', headers=headers, data=data)
            response_json = json.loads(response.text)
            response_json = response_json[0]['data']['visitorReviews']['items']
            print(total_review)

            for index, i in enumerate(response_json):
                # date = i['created']
                # score = i['rating']
                # review = i['body'].replace('\n','')
                # data_frame.append([idx+1, 1004, date, score, review])
                print(index, i['visited'])
                print(i['rating'])
                print(i['body'].replace('\n', ''))


            # try:
            #
            #     for i in range(total_review):
            #         store_id_list = idx+1
            #         portal_id = 1004
            #         date_list = response_json[0]['data']['visitorReviews']['items'][i]['created']
            #         score_list = response_json[0]['data']['visitorReviews']['items'][i]['rating']
            #         review_list = response_json[0]['data']['visitorReviews']['items'][i]['body'].replace('\n', '')
            #
            #         data_frame.append([store_id_list, portal_id, date_list, score_list, review_list])
            #
            #         print(date_list)
            #         print(score_list)
            #         print(review_list)
            #
            # except:
            #     print('noreview')

        # for i in range(page):
        #     if businessid == 'None':
        #         pass
        #     else:
        #         # data_sliced = data.replace(data[74:82], f'{businessid}').replace(data[155:156], f'{i+1}')
        #         data_sliced = data.replace(data[74:82], f'{businessid}')
        #         # print(data_sliced)
        #
        #         response = requests.post('https://pcmap-api.place.naver.com/graphql', headers=headers, data=data_sliced)
        #         # print(response.text)
        #         slicing = json.loads(response.text)
        #         # print(slicing)
        #         total_review = slicing[0]['data']['visitorReviews']['total']
        #
        #         # data2 = json.loads(data)
        #         # data2[0]['variables']['input']['display'] = total_review
        #         # print(response.text)
        #         # print(total_review)
        #
        #
        #         try:
        #
        #             for i in range(total_review):
        #                 store_id_list = idx+1
        #                 portal_id = 1004
        #                 date_list = slicing[0]['data']['visitorReviews']['items'][i]['created']
        #                 score_list = slicing[0]['data']['visitorReviews']['items'][i]['rating']
        #                 review_list = slicing[0]['data']['visitorReviews']['items'][i]['body'].replace('\n', '')
        #
        #                 data_frame.append([store_id_list, portal_id, date_list, score_list, review_list])
        #
        #                 print(date_list)
        #                 print(score_list)
        #                 print(review_list)
        #
        #         except:
        #             print('noreview')

    except:
        if businessid == 'None':
            pass
dataset = pd.DataFrame(data_frame, columns=['store_id','portal_id','date','score','review'])
dataset.to_csv('naver_crawling.csv', encoding='utf-8-sig', index=False)

