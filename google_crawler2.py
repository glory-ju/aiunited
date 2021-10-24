"""
coding : utf-8
author : jihnkim

*-- Google Maps Crawler --*

"""
# import modules
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from Bs4Utils import StaticCrawler

# preprocessing
df = pd.read_csv('store_info.csv', sep=',', encoding='utf-8')

df = df[['store_id', 'region', 'store_name', 'store_addr', 'store_addr_new']]

df['key_words'] = df['store_addr'] + ' ' + df['store_name']

# crawl with selenium webdriver for dynamic crawling
service = Service('C:/Users/sysan/PycharmProjects/aiunited/ex_crawldata/chromedriver.exe')
driver = webdriver.Chrome(service= service)

data = []

for i, keyword in enumerate(df['key_words'].tolist()):
    print(i)
    print(keyword, end=" ")

    try:
        search_url = f'https://www.google.com/maps/search/{keyword}'
        driver.get(search_url)
        driver.implicitly_wait(5)

        review_btn = driver.find_element(By.CSS_SELECTOR,
                                         "#pane > div > div.widget-pane-content.cYB2Ge-oHo7ed > div > div > div.x3AX1-LfntMc-header-title > div.x3AX1-LfntMc-header-title-ma6Yeb-haAclf > div.x3AX1-LfntMc-header-title-ij8cu > div.x3AX1-LfntMc-header-title-ij8cu-haAclf > div > div.gm2-body-2.h0ySl-wcwwM-RWgCYc > span:nth-child(3) > span > span:nth-child(1) > span.OAO0-ZEhYpd-vJ7A6b.OAO0-ZEhYpd-vJ7A6b-qnnXGd > span:nth-child(1) > button")
        review_btn.click()
        time.sleep(3)

        # infinite scroll ** 수정필요(스크롤 다운은 안되고.. action으로는 페이지가 안넘어감)
        # for n in range(1, 10000):
        #     n += 29
        #     element = driver.find_element(By.XPATH,
        #                                   f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[9]/div[30]')
        #     actions = ActionChains(driver).move_to_element(element)
        #     actions.perform()
        #     time.sleep(3)

        try:
            try:
                for j in range(1, 10000):
                    # user id
                    idx = (3 * j) - 2  # what's idx mean? XPath에서 특정 디비젼 인덱스가 공차가 3인 등차수열임
                    user_id = driver.find_element(By.XPATH,
                                                  f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[9]/div[{idx}]/div/div[3]/div[2]/div/div/a/div[1]/span').text
                    # review text
                    review_txt = driver.find_element(By.XPATH,
                                                     f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[9]/div[{idx}]/div/div[3]/div[3]/div[2]/span[2]').text

                    # rate
                    star_score = driver.find_element(By.XPATH,
                                                     f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[9]/div[{idx}]/div/div[3]/div[3]/div[1]/span[2]')
                    star_score = star_score.get_attribute('aria-label')  # 구글 별점은 text 형식이 아니여서 속성값을 불러옴

                    # save as list
                    data.append([i + 1, 1002, user_id, review_txt, int(star_score[4])])

            except:
                try:
                    for k in range(1, 10000):
                        idx = (3 * k) - 2
                        user_id = driver.find_element(By.XPATH,
                                                      f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[8]/div[{idx}]/div/div[3]/div[2]/div/div/a/div[1]/span').text
                        # review text
                        review_txt = driver.find_element(By.XPATH,
                                                         f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[8]/div[{idx}]/div/div[3]/div[3]/div[2]/span[2]').text

                        # rate
                        star_score = driver.find_element(By.XPATH,
                                                         f'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[8]/div[{idx}]/div/div[3]/div[3]/div[1]/span[2]')
                        star_score = star_score.get_attribute('aria-label')  # 구글 별점은 text 형식이 아니여서 속성값을 불러옴

                        # save as list
                        data.append([i + 1, 1002, user_id, review_txt, int(star_score[4])])

                except:
                    print('end of docs')

        except:
            print('end of docs')


    except Exception as e1:
        print('No info')
        data.append([i+1, 1002, 'No info', 'No info', 'No info'])

driver.quit()
print(data)

# save as csv
review_df = pd.DataFrame(data, columns=['store_id', 'portal_id', 'user_id', 'review', 'score'])
review_df.to_csv('reviews.csv')
print('dataframe saved')