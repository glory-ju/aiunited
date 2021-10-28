'''
    @ Author : jihnkim
    @ method : df read, save 관련 func
'''

import os
import csv
import pandas as pd

# 크롤링 할 데이터 파일을 불러오는 함수
def read_csv(file_name):
    df = pd.read_csv(f'{file_name}', sep=',', encoding='utf-8')

    df = df[
        ['store_id', 'region', 'store_name', 'store_addr', 'store_addr_new', 's_link', 'g_link', 'd_link', 'n_link']
    ]

    df['key_words'] = df['store_addr'] + ' ' + df['store_name']

    return df

# 수집된 데이터 리스트를 csv 에 저장하는 함수
def write_csv(df):
    review_df = pd.DataFrame(df, columns=['store_id', 'portal_id', 'review', 'score', 'date'])
    review_df.to_csv('review_data.csv')
    print('data saved')

# 컬럼 소팅
def data_sorting(df1, df2, df3, df4):
    sorted_data_list = []
    df_list = [df1, df2, df3, df4]

    for idx, df in enumerate(df_list):
        df = df['store_id', 'portal_id', 'review', 'score', 'date']
        sorted_data_list.append(df)

    return sorted_data_list

# 다이닝코드, 구글, 네이버, 식신에서 크롤링한 리뷰데이터를 한 df로 합치기
def merge_data_to_csv(diningcode_df, google_df, naver_df, siksin_df):
    all_data_df = pd.concat(data_sorting(diningcode_df, google_df, naver_df, siksin_df))

    return all_data_df