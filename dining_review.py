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
                'authority': 'www.diningcode.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.diningcode.com/list.php?query=%EB%A7%9D%ED%96%A5%20%EB%B9%84%EB%B9%94%EA%B5%AD%EC%88%98&rn=1',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'PHPSESSID=727mo9ijuujbga17g9h9k1mmt4; dcadid=WUWRW1635068383; _fbp=fb.1.1635068388130.1712848784; _ga=GA1.2.628709873.1635068388; _gid=GA1.2.1856169200.1635068388; __gads=ID=1c33ecdc56c8d6b4-226daa67d9cc00a4:T=1635068388:RT=1635068388:S=ALNI_MbcUqA8lL5QqG75JeAAiUZCLE_2iQ; dclogid=wbe1635069453; dckeyword=%5B%22%5Cub9dd%5Cud5a5+%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cub9dd%5Cud5a5%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44+%5Cuba85%5Cub3d9%5Cuc810%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44%22%2C%22%5Cuc555%5Cub85d%5Cub9e4%5Cuc6b4%5Cud0d5%22%2C%22%5Cub9dd%5Cud5a5%5Cuce7c%5Cuad6d%5Cuc218%22%5D',
            }

            params = (
                ('rid', store_code),
            )

            response = requests.get('https://www.diningcode.com/profile.php', headers=headers, params=params)
        else :
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
                'referer': 'https://www.diningcode.com/profile.php?rid=3PnoYTI8YFb8',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'PHPSESSID=727mo9ijuujbga17g9h9k1mmt4; dcadid=WUWRW1635068383; _fbp=fb.1.1635068388130.1712848784; _ga=GA1.2.628709873.1635068388; _gid=GA1.2.1856169200.1635068388; __gads=ID=1c33ecdc56c8d6b4-226daa67d9cc00a4:T=1635068388:RT=1635068388:S=ALNI_MbcUqA8lL5QqG75JeAAiUZCLE_2iQ; dclogid=wbe1635069453; dcpopup=Y; dckeyword=%5B%22%5Cub9dd%5Cud5a5+%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cub9dd%5Cud5a5%5Cube44%5Cube54%5Cuad6d%5Cuc218%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44+%5Cuba85%5Cub3d9%5Cuc810%22%2C%22%5Cuc720%5Cuac00%5Cub124+%5Cub2ed%5Cuac08%5Cube44%22%2C%22%5Cuc555%5Cub85d%5Cub9e4%5Cuc6b4%5Cud0d5%22%2C%22%5Cub9dd%5Cud5a5%5Cuce7c%5Cuad6d%5Cuc218%22%5D; _gat_gtag_UA_46679784_1=1',
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
