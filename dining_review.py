import requests
import datetime
from bs4 import BeautifulSoup as bs
import pandas as pd

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
            review = review.select_one('p.review_contents.btxt').text

            # # 데이터프레임에 추가해주기
            review_df_row = pd.DataFrame([[store_id, 1003, date, star_score, review]], columns=column_list)
            df = df.append(review_df_row)
    return df
