import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from cralwer.dining import dining_review
import pandas as pd

'''
    @ Author : seunghyo
    @ method : store 검색 후 리뷰 데이터 리턴
    @ parameter : 
        1. store_id = 음식점 id
        2. store_name = 음식점명
        3. find_addr = 찾는 음식점 주소
        4. df = 리턴 데이터프레임 데이터프레임
        5. what = store info를 검색할 것인지, store review를 검색할 것인지 
    @ info 
        1. 매개변수로 전달된 음식점 및 찾는주소와 api response로 반환된 음식점 리스트에서 매칭되는 음식점 탐색
        2. 해당 음식점 html 파싱하여 리뷰 가져오는 메서드로 연결
        3. 리뷰 가져와서 데이터프레임에 저장 후 데이터프레임 리턴
'''
def find_store_and_get_review_and_info(store_id, store_name, find_addr, df, what):
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

                # what에 따라 분기
                if what == 'review':
                    df = dining_review.get_review(store_id, store_code, df)
                else:
                    df = get_store_info(store_id, store_code, df)
                target_find = True
                # 같은 가게 찾으면 for문 탈출
                break
        # 해당 스토어를 찾아 리뷰를 가져왔으면 while문 나오기
        if target_find == True:
            break
    # print(store_name + '크롤링 끝')
    return df

'''
    @ Author : seunghyo
    @ method : store_info 누락데이터 확인 및 변경 시 추가
    @ parameter : 
        1 store_id = 음식점 id
        2 store_name = 음식점명
        3 store_info = store_info dateframe 한 개의 행(row)
    @ info
        
'''
def get_store_info(store_id, store_code, df):
    # 데이터프레임 인덱스 설정

    column_list = ['region', 'store_name', 'store_x', 'store_y', 'store_addr', 'store_addr_new', 'store_tel',	'open_hours', 'website', 's_link', 'd_link']
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    params = (
        ('rid', store_code),
    )

    response = requests.get('https://www.diningcode.com/profile.php', headers=headers, params=params)

    soup = bs(response.text, 'html.parser')
    try:
        # 영업장 주소 가져오기
        store_addr = soup.select_one('.basic-info li').text
    except:
        store_addr = ''
    try:
        # 전화번호 가져오기
        tel = soup.select_one('.basic-info li.tel').text
    except:
        tel = ''
    try:
        # 영업시간 가져오기
        work_hours = soup.select_one('.busi-hours ul li p.r-txt').text
    except:
        work_hours = ''
    row_df = pd.DataFrame([df], columns=column_list)
    # info 데이터 적용
    row_df['open_hours'] = work_hours
    row_df['store_tel'] = tel
    row_df['d_link'] = store_code
    row_df['store_addr'] = store_addr


    # 행 리턴
    return row_df


'''
    @ Author : seunghyo
    @ method : dining_code store_info 크롤링 실행부
    @ parameter : 
        1 df = 사전에 조사한 store_info.csv to 데이터프레임
'''
def action_dining_store_info(df):
    # index 재설정
    df.set_index('store_id', inplace=True)
    idx = 0

    # column 딕셔너리 추가
    column_dict = {}
    for idx, column in enumerate(df):
        column_dict[column] = idx

    df['d_link'] = ''
    for index, row in zip(df.index.tolist(), df.values.tolist()):
        # store_name. id, addr 추출
        store_name = row[column_dict['store_name']]
        store_addr = row[column_dict['store_addr']]
        store_id = index
        # 상세주소 미스매치를 줄이기 위한 전처리
        addr_str_list = store_addr.split(' ')

        # 주소 잘못된 곳이 많아 동까지만 같은지 검색
        find_addr = ' '.join(addr_str_list[:3])
        try:
            make_df = find_store_and_get_review_and_info(store_id, store_name, find_addr, row, 'info').iloc[0]
            df.loc[store_id] = make_df
        except:
            pass
        idx += 1
        print(idx)
    df.to_csv('data/store_info_dining.csv', encoding='UTF-8')
    return df
