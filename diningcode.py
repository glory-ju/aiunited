import pandas as pd
import ssl
import time
from selenium import webdriver

# 셀레니움 설정
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/Users/imseunghyo/dev/chromedriver')

# CERTIFICATE_VERIFY_FAILED 에러 수정
context = ssl._create_unverified_context()

# csv 파일 데이터프레임화
df = pd.read_csv('data/store_info.csv', encoding='UTF-8')

# base url
base_url = 'https://www.diningcode.com/profile.php?rid='

# 결과 데이터 프레임
column_list = ['store_id', 'portal_id', 'date', 'score', 'review']
store_review = pd.DataFrame(columns=column_list)

# url 딕셔너리
url_dict = {}
for index, d_link in zip(df['store_id'], df['d_link']):
    #nan 아닐시에만 딕셔너리에 추가
    if type(d_link) != float:
        url_dict[index] = d_link

for store_id in url_dict.keys():
    # request url 완성하기
    request_url = base_url + url_dict.get(store_id)

    # 페이지 이동
    driver.get(request_url)

    # 다음버튼 안나올 때 까지 더보기 버튼 클릭
    while True:
        try:
            time.sleep(2)
            driver.find_element_by_id('div_more_review').click()
        except NoSuchElementException:
            break

    time.sleep(1)

    # 댓글 전체를 감싸는 div 가져오기
    review_divs = driver.find_elements_by_css_selector('#div_review > div')

    # 댓글별로 loop 시작
    for el in review_divs:
        # 별점
        star = el.find_element_by_css_selector('p.person-grade > span.star-date > i.star > i')
        star_score_style_attribte = star.get_attribute('style')
        # 별점 전처리
        # 1. width 값만 꺼내기
        star_score_by_per = float(star_score_style_attribte.split('%')[0][-2:])
        # 2. 별점계산
        star_score = star_score_by_per / 20
        # 작성일시
        date = el.find_element_by_css_selector('p.person-grade > span.star-date > i.date').text
        # 리뷰
        review = el.find_element_by_css_selector('p.review_contents.btxt').text

        # 데이터프레임에 추가해주기
        review_df_row = pd.DataFrame([[store_id, 1003, date, star_score, review]], columns=column_list)
        store_review = store_review.append(review_df_row)

# csv 파일변환
store_review.to_csv('diningcode_review.csv', encoding='UTF-8', index=False)

# 웹 드라이버 종료
driver.quit()
