#필요한 라이브러리 로딩
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

#2.크롬부라우저 옵션 정의
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

#3. 크롬 웹드라이브 크롬부라우저 객체 생성
#방법1 자동으로 다운로드(현재 크롬 브라우저 버전에 맞게)
# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())

#방법2. 방법1이 안될 때 메뉴얼하게 다운로드 받아서 지정해야 함.
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/
#메뉴얼하게 지정하는 방법
service = Service("chromedriver_142/chromedriver.exe")

#크롬 부라우저 객체 생성됨, chrome은 브라우저 객체 식별자
chrome = webdriver.Chrome(service=service, options=options) 

#4. 데이터 수집할 웹 주소
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

chrome.get(url)

#지정한 요소가 브라우저에 로딩될 떄까지 기다림, 최대 10초
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

#5. 데이터 수집할 부분에 대한 검색 액션 수행
try:
    ## 한국 영화만 선택, 해외 체크박스 해제 액션
    #셀렉터 지정방법
    # ul.list_idx li input#repNationNoKor 또는 
    # ul.list_idx li label[for='repNationNoKor']
    # find(wait, "셀렉터")
    # 지정 셀렉터 요소가 로딩될 때까지 기다리고, 로딩되면 요소 리턴
    #로딩된 요소 클릭
    ele = find(wait, " ul.list_idx li label[for='repNationNoKor']")
    ele.click()

    #조회버튼 로딩되면 클릭하기
    btn = find(wait, " .wrap_btn button.btn_blue")
    btn.click()

    #조회된 데이터에서 필요한 데이터 수집
    #각 영화 데이터를 list로 추출(tbody tr을 목록으로 추출)
    time.sleep(5) #크롤링할 데이터 요소가 로딩될 때까지 잠시 기다리기
    #"table.tbl.comm tbody tr" 해당 셀렉터의 모든 요소를 추출함
    items =chrome.find_elements(By.CSS_SELECTOR, "table.tbl_comm tbody tr")
    # print(items)
    movie_list= []
    print("영화명 | 개봉일 | 예매매출액 | 예매관객수")
    for item in items:
        # 하나의 tr 안에서 td가 두번째인 요소의 텍스트 추출
        title = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        #open_date가 없는 경우 처리
        if not open_date:
            open_date = "-"
        ticket_sales  = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        sale_audience = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
        # print(f"{title} | {open_date} | {ticket_sales } | {sale_audience}")
        movie_list.append([title, open_date, ticket_sales, sale_audience])
        print(movie_list)
except Exception as e:
    print("d오류", e)

# print("-"*30)
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료

#파일로 저장하기(csv)
#현재 날짜/시간 가져오기
from datetime import datetime
import os
import csv
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H")

# 폴더 / 파일명 설정
folder = "movie_datas"
filename = f"movie_{timestamp}.csv"
# "movie_datas"/movie_25-11-21-12
filepath = os.path.join(folder, filename) 


# 폴더 자동생성 
os.makedirs(folder, exist_ok=True)

# 3. CSV 파일 저장(2차원 리스트여야함)
with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    #print("영화명 | 개봉일 | 예매매출액 | 예매관객수")
    #1ck원 리스트 저장
    writer.writerow(["영화명", "개봉일", "예매매출액","예매관객수"])
    #2자원 list로 만들어서 저장(수집한 데이터)
    writer.writerows(movie_list)

print(f"저장 완료: {filename}")