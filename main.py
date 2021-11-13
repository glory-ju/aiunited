import pandas as pd
from functools import reduce
from cralwer.dining.dining_store import action_dining_store_info
from cralwer.naver.naver_crawling import action_naver_store_info
from cralwer.dining.dining_review import action_dining_review_crwaler
from cralwer.naver.review_crawler import action_naver_review_crawler


if __name__ == '__main__':
    # 최초 storeinfo csv 가져오기
    df = pd.read_csv('data/siksin_info.csv', encoding='UTF-8')

    # dining_code get store_info
    store_info_dining = action_dining_store_info(df)

    # siksin get store_info

    # naver get store_info
    store_info_naver = action_naver_store_info(df)
    # google get store_info

    # combine store_info


    # dining_review_crawling
    dining_review = action_dining_review_crwaler(store_info_dining)

    # siksin review Crawling

    # naver review Crawling
    naver_review = action_naver_review_crawler(store_info_naver)
    # google review crawling

    # combine review

    # preprocessi ngmethod

    # embedding
