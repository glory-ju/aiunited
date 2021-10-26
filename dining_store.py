import requests
from bs4 import BeautifulSoup as bs
import dining_review as dining_review
import pandas as pd
import numpy as np
import time

def find_store_and_get_review(store_id, store_name, find_addr, store_review):
    page = 0

    # 찾고자 하는 스토어 찾았는지 확인하는 bool type 변수
    target_find = False

    while True:
        page += 1
        if page == 1:
            headers = {
                'authority': 'www.diningcode.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'PHPSESSID=727mo9ijuujbga17g9h9k1mmt4; dcadid=WUWRW1635068383; _fbp=fb.1.1635068388130.1712848784; _ga=GA1.2.628709873.1635068388; _gid=GA1.2.1856169200.1635068388; __gads=ID=1c33ecdc56c8d6b4-226daa67d9cc00a4:T=1635068388:RT=1635068388:S=ALNI_MbcUqA8lL5QqG75JeAAiUZCLE_2iQ; dclogid=wbe1635069453; dckeyword=%5B%22%5Cub9dd%5Cud5a5+%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cub9dd%5Cud5a5%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44+%5Cuba85%5Cub3d9%5Cuc810%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44%22%2C%22%5Cuc555%5Cub85d%5Cub9e4%5Cuc6b4%5Cud0d5%22%2C%22%5Cub9dd%5Cud5a5%5Cuce7c%5Cuad6d%5Cuc218%22%5D',
            }

            params = (
                ('query', store_name),
                ('rn', '1'),
            )

            response = requests.get('https://www.diningcode.com/list.php', headers=headers, params=params)
        else:
            headers = {
                'authority': 'www.diningcode.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                'sec-ch-ua-platform': '"macOS"',
                'origin': 'https://www.diningcode.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.diningcode.com/list.php?query=%EB%A7%9D%ED%96%A5%20%EB%B9%84%EB%B9%94%EA%B5%AD%EC%88%98&rn=1',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'PHPSESSID=727mo9ijuujbga17g9h9k1mmt4; dcadid=WUWRW1635068383; _fbp=fb.1.1635068388130.1712848784; _ga=GA1.2.628709873.1635068388; _gid=GA1.2.1856169200.1635068388; __gads=ID=1c33ecdc56c8d6b4-226daa67d9cc00a4:T=1635068388:RT=1635068388:S=ALNI_MbcUqA8lL5QqG75JeAAiUZCLE_2iQ; dclogid=wbe1635069453; dcpopup=Y; dckeyword=%5B%22%5Cub9dd%5Cud5a5+%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cub9dd%5Cud5a5%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44+%5Cuba85%5Cub3d9%5Cuc810%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44%22%2C%22%5Cuc555%5Cub85d%5Cub9e4%5Cuc6b4%5Cud0d5%22%2C%22%5Cub9dd%5Cud5a5%5Cuce7c%5Cuad6d%5Cuc218%22%5D; _gat_gtag_UA_46679784_1=1',
            }

            data = {
                'type': '',
                'query': store_name,
                'lat': '',
                'lng': '',
                'dis': '',
                'page': page,
                'chunk': '5',
                'rn': '1'
            }
            response = requests.post('https://www.diningcode.com/2018/ajax/list.php', headers=headers, data=data)
        soup = bs(response.text, 'html.parser')

        # api로 가져온 스토어 리스트 확인
        store_list = soup.select('a.blink')

        # 더 이상 가져올 스토어 목록이 없으면 브레이크
        if len(store_list) == 0:
            print(store_name + ' 못찾음')
            # print(find_addr)
            break

        for store_imp in store_list:
            # 지역명 삭제
            loca = store_imp.select_one('span.ctxt i.loca')
            try:
                loca.replaceWith('')
            except:
                pass

            addr = store_imp.select('span.ctxt')[1].text
            addr_str_list = addr.split(' ')

            # 주소 잘못된 곳이 많아 동까지만 같은지 검색
            request_addr = ' '.join(addr_str_list[:3])

            # 서울'특별'시 누락으로 주소매칭 안되는 부분있어서 추가하고 검색
            if addr_str_list[0] == '서울시':
                addr_str_list[0] = '서울특별시'

            request_addr_1 = ' '.join(addr_str_list[:3])

            if find_addr == request_addr or find_addr == request_addr_1:
                # 찾는 주소와 요청 주소가 같으면 스토어 아이디 검색
                store_code = str(store_imp).split('rid=')[1].split('"')[0]

                store_review = dining_review.get_review(store_id, store_code, store_review)
                target_find = True
                # 같은 가게 찾으면 for문 탈출
                break
        # 해당 스토어를 찾아 리뷰를 가져왔으면 while문 나오기
        if target_find == True:
            break

    return store_review


# csv 파일 데이터프레임화
df = pd.read_csv('data/store_info.csv', encoding='UTF-8')

# 결과 데이터 프레임
column_list = ['store_id', 'portal_id', 'date', 'score', 'review']
store_review = pd.DataFrame(columns=column_list)

# 10개 되면 시간지연하기위해 변수 선언
idx = 0

# 검색이름, 주소 리스트화시켜 loop 진입
for store_name, find_addr, store_id in zip(df['store_name'].tolist(), df['store_addr'].tolist(), df['store_id'].tolist()):
    # 상세주소 미스매치를 줄이기 위한 전처리
    addr_str_list = find_addr.split(' ')

    # 주소 잘못된 곳이 많아 동까지만 같은지 검색
    find_addr = ' '.join(addr_str_list[:3])
    idx += 1
    if idx % 9 == 0:
        time.sleep(60)
    store_review = find_store_and_get_review(store_id, store_name, find_addr, store_review)

# csv 파일변환
store_review.to_csv('diningcode_review1.csv', encoding='UTF-8', index=False)