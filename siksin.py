from selenium import webdriver
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# csv 파일 읽기
df = pd.read_csv('data/store_info.csv', encoding='utf-8')
df = df.astype({'s_link':'str'})
# print(df['s_link'])
# for col in df.columns:
# 	print(col)

# 크롤링한 데이터 저장할 데이터프레임 생성
review_columns = ['store_id','portal_id','score','review']
store_review = pd.DataFrame(columns=review_columns)

# s_link를 이용하여 쿼리문을 통해 페이지 접속
driver = webdriver.Chrome('C:/Users/hy949/PycharmProjects/chromedriver_win32/chromedriver.exe')
url = 'https://www.siksinhot.com/P/'
s_link = df['s_link'].values.tolist()
store_id = df['store_id'].values.tolist()

for s_id,link in zip(store_id, s_link):
    base_url = url + quote_plus(link)

    driver.get(base_url)
    time.sleep(1)

    # 전체 리뷰 수
    review_cnt = int(driver.find_element_by_css_selector("#siksin_review > div.txt_total > ul > li > span").text.replace(',', ''))
    print(review_cnt)

    # btn_cnt = (review_cnt-10)//5
    # # review_cnt = soup.select('#siksin_review > div.txt_total > ul > li > span')[0].get_text()
    # # print(review_cnt)
    # # btn_cnt = (int(review_cnt) - 10)
    # # print(btn_cnt)
    #
    #
    # k=0
    # while k <= btn_cnt:
    #     try:
    #         # driver.find_element_by_css_selector('#siksin_review > div.rList > a > span').click()
    #         btn_sMore = driver.find_element_by_class_name('btn_sMore')
    #         btn_sMore.click()
    #         time.sleep(1)
    #         k = k+1
    #
    #     except:
    #         break

    # 더보기 버튼이 없어질 때까지 클릭
    while True:
        try:
            driver.find_element_by_css_selector('#siksin_review > div.rList > a').click()
            time.sleep(1)
        except NoSuchElementException:
            break

    # 리뷰,평가 점수 추출
    soup = bs(driver.page_source, 'html.parser')
    reviews = soup.select('#siksin_review > div.rList > ul > li > div > div.cnt > div.score_story > p')
    scores = soup.select('#siksin_review > div.rList > ul > li > div > div.cnt > div.score_story > div > span > strong')
    for idx,review in enumerate(reviews):
        reviews[idx] = review.text.replace('\n',' ').replace('\r', '')
    for idx,score in enumerate(scores):
        scores[idx] = score.text

    # 추출한 데이터 데이터 프레임에 병합
    for i in range(review_cnt):
        store_review = store_review.append(pd.DataFrame([[s_id, 1001, scores[i], reviews[i]]], columns=review_columns))



    print(reviews)
    print(scores)

# 데이터 프레임 utf-8로 인코딩하여 csv파일로 저장
store_review.to_csv('siksin_review.csv', encoding='utf-8-sig', index=False)

# 웹드라이버 종료
driver.quit()