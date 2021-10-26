import requests
from bs4 import BeautifulSoup as bs
import dining_review as dining_review
import pandas as pd

def find_store_and_get_review(store_id, store_name, find_addr, store_review):
    page = 0

    # 찾고자 하는 스토어 찾았는지 확인하는 bool type 변수
    target_find = False

    while True:

        page += 1
        if page == 1:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
          }

            params = (
                ('query', store_name),
                ('rn', '1'),
            )

            response = requests.get('https://www.diningcode.com/list.php', headers=headers, params=params)
        else:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
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

        # 더 이상 가져올 스토어 목록이 없거나 page가 10개를 넘어가면 브레이크
        if len(store_list) == 0 or page > 10:
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
    print(store_name + '크롤링 끝')
    return store_review


# csv 파일 데이터프레임화
df = pd.read_csv('data/store_info.csv', encoding='UTF-8')

# 결과 데이터 프레임
column_list = ['store_id', 'portal_id', 'date', 'score', 'review']
store_review = pd.DataFrame(columns=column_list)

# 검색이름, 주소 리스트화시켜 loop 진입
for store_name, find_addr, store_id in zip(df['store_name'].tolist(), df['store_addr'].tolist(), df['store_id'].tolist()):
    # 상세주소 미스매치를 줄이기 위한 전처리
    addr_str_list = find_addr.split(' ')

    # 주소 잘못된 곳이 많아 동까지만 같은지 검색
    find_addr = ' '.join(addr_str_list[:3])
    store_review = find_store_and_get_review(store_id, store_name, find_addr, store_review)

# csv 파일변환
store_review.to_csv('diningcode_review1.csv', encoding='UTF-8', index=False)