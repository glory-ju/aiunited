import pandas as pd
import requests
import json
import time
import numpy as np
import math
import datetime

df = pd.read_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/naver_storeInfo_1.csv')

data_frame = []

for idx in range(38, 1000):

    time.sleep(np.random.randint(0, 3))

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
        'referer': 'https://pcmap.place.naver.com/restaurant/11718339/review/visitor?reviewItem=0',
        'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; ASID=dc5f3dbd0000017bc9a08e5f0000005a; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; _ga=GA1.2.878040348.1627623526; BMR=; nx_ssl=2; page_uid=hhuRiwprvOssshQnb38ssssstN0-432449; _ga_7VKFYR6RV1=GS1.1.1635832829.2.0.1635832829.60; NID_SES=AAABpxJkNbzKKebR/D3HfBhLJQxV2C0S99SKoj0Lu4OkV2Tu7pq7lfXeJL+4QSHmSFgQr7+G9RyHkEPp9k5UuRShm8htem677eWLy8x+sHMQ0r2Nz4k1M7dtCHbYlBCCwe2Ue2DStGEOD3Hl2eNLX9/Fw2pEJEpp4D1EDbQ8OnR/AgXCM57SecsqAST5n5VyQPpK6fRP1jSYN822wHF8blsxiuZnAkG9dFQP38QsP/s6fAelb6zTw8kZAKqDHGFUy5MT2rZIBr4oW+cf2ZtOxtIAziBQbDYv1QU1SpNJJ1tF54yjhl8pCIleaYd3LsbTX/f7PhsGtk/AX8nXmWE6Pffy69TILVNfl0wxZmioGNWUtfBBbJ1r8D0DyNWNC5xMDeGteRzje79o8LfCaFV0+22YgqJRe0Ut6Pt8ytVg8LAQmHsyuvcSbdqSVYK9sNypybSAePy15y58kJOra8wo7ZD10DU3bVJvTwjMgG20MA2VR5Sk4harA1dzDEIyQA0+dtUl0cGjezCAmMsv01+QM0D2cVGmFN0yByFyrWrNwGMMa4GamVqdWaAx4pVIvsrxamUpbA==',
    }

    nan_value = float(df['n_link'][idx])

    if math.isnan(nan_value) == False:
        businessid = str(int(df['n_link'][idx]))
    else:
        continue

    data = '[{"operationName":"getVisitorReviews","variables":{"input":{"businessId":"'+businessid+'","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":1,"display":100,"isPhotoUsed":false,"includeContent":true,"getAuthorInfo":true}},"query":"query getVisitorReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visitCount\\n      viewCount\\n      visited\\n      created\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      language\\n      highlightOffsets\\n      apolloCacheId\\n      translatedText\\n      businessName\\n      showBookingItemName\\n      showBookingItemOptions\\n      bookingItemName\\n      bookingItemOptions\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorReviews","variables":{"id":"11718339"},"query":"query getVisitorReviews($id: String) {\\n  visitorReviewStats(input: {businessId: $id}) {\\n    id\\n    name\\n    review {\\n      avgRating\\n      totalCount\\n      scores {\\n        count\\n        score\\n        __typename\\n      }\\n      starDistribution {\\n        count\\n        score\\n        __typename\\n      }\\n      imageReviewCount\\n      authorCount\\n      maxSingleReviewScoreCount\\n      maxScoreWithMaxCount\\n      __typename\\n    }\\n    analysis {\\n      themes {\\n        code\\n        label\\n        count\\n        __typename\\n      }\\n      menus {\\n        label\\n        count\\n        __typename\\n      }\\n      votedKeyword {\\n        totalCount\\n        reviewCount\\n        userCount\\n        details {\\n          category\\n          code\\n          displayName\\n          count\\n          previousRank\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    visitorReviewsTotal\\n    ratingReviewsTotal\\n    __typename\\n  }\\n  visitorReviewThemes(input: {businessId: $id}) {\\n    themeLists {\\n      name\\n      key\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorReviewPhotosInVisitorReviewTab","variables":{"businessId":"11718339","businessType":"restaurant","item":"0","page":1,"display":10},"query":"query getVisitorReviewPhotosInVisitorReviewTab($businessId: String!, $businessType: String, $page: Int, $display: Int, $theme: String, $item: String) {\\n  visitorReviews(input: {businessId: $businessId, businessType: $businessType, page: $page, display: $display, theme: $theme, item: $item, isPhotoUsed: true}) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visited\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      businessName\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorRatingReviews","variables":{"input":{"businessId":"11718339","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":1,"display":10,"includeContent":false,"getAuthorInfo":true},"id":"11718339"},"query":"query getVisitorRatingReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    total\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      visitCount\\n      visited\\n      originType\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      businessName\\n      status\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'
    response = requests.post('https://pcmap-api.place.naver.com/graphql', headers=headers, data=data)

    load = json.loads(response.text)
    total_review = load[0]['data']['visitorReviews']['total']
    print(idx+1, '/', total_review)

    iter_cnt = int(total_review / 100) + 2

    if total_review < 100:
        display = str(total_review)
    else:
        display = str(100)

    try:
        for page in range(1, iter_cnt):
            print('---'*30)
            data = '[{"operationName":"getVisitorReviews","variables":{"input":{"businessId":"' + businessid + '","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":' + str(page) + ',"display":'+display+',"isPhotoUsed":false,"includeContent":true,"getAuthorInfo":true}},"query":"query getVisitorReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visitCount\\n      viewCount\\n      visited\\n      created\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      language\\n      highlightOffsets\\n      apolloCacheId\\n      translatedText\\n      businessName\\n      showBookingItemName\\n      showBookingItemOptions\\n      bookingItemName\\n      bookingItemOptions\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorReviews","variables":{"id":"11718339"},"query":"query getVisitorReviews($id: String) {\\n  visitorReviewStats(input: {businessId: $id}) {\\n    id\\n    name\\n    review {\\n      avgRating\\n      totalCount\\n      scores {\\n        count\\n        score\\n        __typename\\n      }\\n      starDistribution {\\n        count\\n        score\\n        __typename\\n      }\\n      imageReviewCount\\n      authorCount\\n      maxSingleReviewScoreCount\\n      maxScoreWithMaxCount\\n      __typename\\n    }\\n    analysis {\\n      themes {\\n        code\\n        label\\n        count\\n        __typename\\n      }\\n      menus {\\n        label\\n        count\\n        __typename\\n      }\\n      votedKeyword {\\n        totalCount\\n        reviewCount\\n        userCount\\n        details {\\n          category\\n          code\\n          displayName\\n          count\\n          previousRank\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    visitorReviewsTotal\\n    ratingReviewsTotal\\n    __typename\\n  }\\n  visitorReviewThemes(input: {businessId: $id}) {\\n    themeLists {\\n      name\\n      key\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorReviewPhotosInVisitorReviewTab","variables":{"businessId":"11718339","businessType":"restaurant","item":"0","page":1,"display":10},"query":"query getVisitorReviewPhotosInVisitorReviewTab($businessId: String!, $businessType: String, $page: Int, $display: Int, $theme: String, $item: String) {\\n  visitorReviews(input: {businessId: $businessId, businessType: $businessType, page: $page, display: $display, theme: $theme, item: $item, isPhotoUsed: true}) {\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        __typename\\n      }\\n      body\\n      thumbnail\\n      media {\\n        type\\n        thumbnail\\n        __typename\\n      }\\n      tags\\n      status\\n      visited\\n      originType\\n      item {\\n        name\\n        code\\n        options\\n        __typename\\n      }\\n      businessName\\n      __typename\\n    }\\n    starDistribution {\\n      score\\n      count\\n      __typename\\n    }\\n    hideProductSelectBox\\n    total\\n    __typename\\n  }\\n}\\n"},{"operationName":"getVisitorRatingReviews","variables":{"input":{"businessId":"11718339","businessType":"restaurant","item":"0","bookingBusinessId":null,"page":1,"display":10,"includeContent":false,"getAuthorInfo":true},"id":"11718339"},"query":"query getVisitorRatingReviews($input: VisitorReviewsInput) {\\n  visitorReviews(input: $input) {\\n    total\\n    items {\\n      id\\n      rating\\n      author {\\n        id\\n        nickname\\n        from\\n        imageUrl\\n        objectId\\n        url\\n        review {\\n          totalCount\\n          imageCount\\n          avgRating\\n          __typename\\n        }\\n        theme {\\n          totalCount\\n          __typename\\n        }\\n        __typename\\n      }\\n      visitCount\\n      visited\\n      originType\\n      reply {\\n        editUrl\\n        body\\n        editedBy\\n        created\\n        replyTitle\\n        __typename\\n      }\\n      votedKeywords {\\n        code\\n        displayName\\n        __typename\\n      }\\n      businessName\\n      status\\n      userIdno\\n      isFollowing\\n      followerCount\\n      followRequested\\n      loginIdno\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'
            response = requests.post('https://pcmap-api.place.naver.com/graphql', headers=headers, data=data)

            response_json = json.loads(response.text)
            response_json = response_json[0]['data']['visitorReviews']['items']


            for index, i in enumerate(response_json):
                date = i['visited']
                if len(date) > 7:
                    date_slicing = date[:-2].split('.')
                    date_time = datetime.date(int('20' + date_slicing[0]), int(date_slicing[1]), int(date_slicing[2]))
                else:
                    date_slicing = date[:-2].split('.')
                    date_time = datetime.date(int('2021'), int(date_slicing[0]), int(date_slicing[1]))
                score = i['rating']
                review = i['body'].replace('\n', '').replace('.','')
                data_frame.append([df['store_id'][idx], 1004, date_time, score, review])

                print(index, date_time)
                print(score)
                print(review)
                time.sleep(np.random.randint(0, 2))

    except:
        if businessid == '':
            data_frame.append('NoInfo')
            pass


    dataset = pd.DataFrame(data_frame, columns=['store_id', 'portal_id', 'date', 'score', 'review'])
    dataset.to_csv('naver_1000_1.csv', encoding='UTF-8', index=False)
