
'''
    @ Author : seunghyo
    @ method : 날짜형식 YYYY년 MM월 dd일 -> yyyy-mm-dd로 포맷팅
'''
def dateFormat(str):
    date_list = str.split(' ')

    # 입력 잘못들어왔을 시 return
    if len(date_list) != 3:
        return False

    for index, date in enumerate(date_list):
        date_list[index] = date[:-1]

    return_date = '-'.join(date_list)
    return return_date
