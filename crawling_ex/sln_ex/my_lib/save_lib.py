from datetime import datetime
import os
import csv

#데이터 저장 함수 정의부
def save_datas(data_keyword, head, movie_lists):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H")

    # 폴더 / 파일명 설정
    folder = f"{data_keyword}_datas"
    filename = f"{data_keyword}_{timestamp}.csv"
    # "movie_datas"/movie_25-11-21-12
    filepath = os.path.join(folder, filename) 


    # 폴더 자동생성 
    os.makedirs(folder, exist_ok=True)

    # 3. CSV 파일 저장(2차원 리스트여야함)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #print("영화명 | 개봉일 | 예매매출액 | 예매관객수")
        #1ck원 리스트 저장
        writer.writerow(head)
        #2자원 list로 만들어서 저장(수집한 데이터)
        writer.writerows(movie_lists)

    print("csv 저장 완료" ,filepath)