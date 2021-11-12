import requests
import datetime
from bs4 import BeautifulSoup as bs
import pandas as pd
import utils.str_func as str_func

'''
    @ Author : seunghyo
    @ method : 리부 데이터 크롤링
    @ parameter : 
        1. store_id = 음식점 id
        2. store_code = diningcode 음식점 고유 code
        3. df = 리뷰 데이터 프레임 
    @ info 
        1. 매개변수로 전달된 store_code로 리뷰 api 요청
        2. 리뷰, 평점, 작성일자 추가해서 데이터프레임에 저장
        3. 저장된 데이터프레임 리턴
'''
def get_review(store_id, store_code, df):
    column_list = ['store_id', 'portal_id', 'date', 'score', 'review']
    page = 0

    while True:
        page += 1
        if page == 1:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            }

            params = (
                ('rid', store_code),
            )

            response = requests.get('https://www.diningcode.com/profile.php', headers=headers, params=params)
        else :
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            }

            data = {
                'mode': 'LIST',
                'type': 'profile',
                'v_rid': store_code,
                'page': page,
                'rows': '5'
            }
            response = requests.post('https://www.diningcode.com/2018/ajax/review.php', headers=headers, data=data)

        soup = bs(response.text, 'html.parser')

        if soup.text == '':
            break

        # 댓글 전체를 감싸는 div 가져오기
        review_divs = soup.select('.latter-graph')
        for review in review_divs:
            # 별점
            star = review.select_one('p.person-grade > span.star-date > i.star > i')
            star_score_style_attribte = star['style']
            # 별점 전처리
            # 1. width 값만 꺼내기
            star_score_by_per = float(star_score_style_attribte.split('%')[0].split(':')[1])
            # 2. 별점계산
            star_score = star_score_by_per / 20

            # 작성일시
            date = review.select_one('p.person-grade > span.star-date > i.date').text
            if date.find('년') != 4:
                dt_now = datetime.datetime.now()
                date = str(dt_now.year) + '년 ' + date

            # 리뷰
            try:
                review = review.select_one('p.review_contents.btxt').text
            except:
                review = ''
            # date format
            date = str_func.dateFormat(date)
            # # 데이터프레임에 추가해주기
            review_df_row = pd.DataFrame([[store_id, 1003, date, star_score, review]], columns=column_list)
            df = df.append(review_df_row)
    return df

'''
    @ Author : seunghyo
    @ method : 리부 크롤링 실행
    @ parameter : 
        1. store_id = 음식점 id
        2. store_code = diningcode 음식점 고유 code
        3. df = dining d_link가 포함된 store_info data_frame
    @ info 
        1. 매개변수로 전달된 store_code로 리뷰 api 요청
        2. 리뷰, 평점, 작성일자 추가해서 데이터프레임에 저장
        3. 저장된 데이터프레임 리턴
'''
def action_dining_review_crwaler(df):
    # 결과 데이터 프레임
    column_list = ['store_id', 'portal_id', 'date', 'score', 'review']
    dining_review = pd.DataFrame(columns=column_list)
    idx = 0
    # 검색이름, 주소 리스트화시켜 loop 진입
    for store_code, store_id in zip(df['d_link'].tolist(), df['store_id'].tolist()):
        if not pd.isna(store_code):
            store_review = get_review(store_id, store_code, store_review)
        # print(idx)
        # idx += 1
    return dining_review