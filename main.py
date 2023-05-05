from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyperclip
import platform

klas_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginForm.do"

klas_id = input("학번: ")
klas_pw = input("비밀번호: ")
naver_id = input('네이버 id: ')
naver_pw = input('네이버 pw: ')

driver = webdriver.Chrome()
driver.get(klas_url)

# 로그인
driver.find_element(By.ID, "loginId").send_keys(klas_id, Keys.TAB)
driver.find_element(By.ID, "loginPwd").send_keys(klas_pw, Keys.ENTER)

# 2초 후 진행
time.sleep(2)

klas_html = driver.page_source
klas_soup = BeautifulSoup(klas_html, 'html.parser')

# 수강 과목 리스트, 개수 저장
subjects = klas_soup.find("ul", attrs={'class': 'subjectlist listbox'}).findAll("li")
len_of_subjects = len(subjects)

# 과제들을 저장할 리스트 선언
homeworks = []
for i in range(1, len_of_subjects+1):
    # 강의 페이지로 들어감
    driver.find_element(By.XPATH, f'//*[@id="appModule"]/div/div[1]/div[2]/ul/li[{i}]/div[1]').click()

    # 강의 과제 페이지로 들어감
    driver.find_element(By.XPATH, '//*[@id="appModule"]/div[1]/div[2]/div/div[2]/div/div[2]/ul/li[2]/a').click()
    subject_name = subjects[i-1].text.split()[0]

    subjects_html = driver.page_source
    subjects_soup = BeautifulSoup(subjects_html, 'html.parser')
    # 과제들 리스트를 가져옴
    subs = subjects_soup.findAll('tbody')

    # 과제들 모두 homeworks 리스트에 (강의명+과제명, 시작일,시간, 마감일,시간) 형태로 저장
    for sub in subs[:-1]:
        print(subject_name, sub.findAll('td')[1].text, sub.findAll('td')[2].text)
        homeworks.append((subject_name + ' ' + sub.findAll('td')[1].text, sub.findAll('td')[2].text.split()[0], sub.findAll('td')[2].text.split()[1], sub.findAll('td')[2].text.split()[3], sub.findAll('td')[2].text.split()[4]))

    # 다시 메인페에지로 돌아감
    driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div[1]/a/img').click()
    time.sleep(0.5)

print(homeworks)

'''
네이버 캘린더에 일정 추가 시작
'''

calendar_url = 'https://calendar.naver.com'
driver.get(calendar_url)

# id 입력
elem_id = driver.find_element(By.ID, 'id')
elem_id.click()
time.sleep(0.1)
pyperclip.copy(naver_id)                        ################ id 입력으로 바꿔야 됨
# mac OS 일 경우 command + v 로 붙여넣기
if platform.system() == 'Darwin':
    elem_id.send_keys(Keys.COMMAND, 'v')
else:
    elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(0.1)

# pw 복사 붙여넣기
elem_pw = driver.find_element(By.ID, 'pw')
elem_pw.click()
time.sleep(0.1)
pyperclip.copy(naver_pw)
if platform.system() == 'Darwin':
    elem_pw.send_keys(Keys.COMMAND, 'v')
else:
    elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(0.1)

# 로그인 버튼 클릭
driver.find_element(By.ID, 'log.login').click()
time.sleep(1)
driver.find_element(By.ID, 'new.dontsave').click()
time.sleep(1)

# 일정 추가
for i, hw in enumerate(homeworks):
    driver.find_element(By.XPATH, '//*[@id="nav_snb"]/div/div[1]/a[1]').click()

    time.sleep(1)

    # 제목 입력
    driver.find_element(By.XPATH, '//*[@id="tx0_0"]').send_keys(hw[0])
    time.sleep(0.2)

    # 시작일 입력
    start_day = driver.find_element(By.XPATH, '//*[@id="start_date"]')
    for _ in range(10):
        start_day.send_keys(Keys.BACKSPACE)
    start_day.send_keys(hw[1])
    time.sleep(0.2)

    # 시작 시간 입력
    start_time = driver.find_element(By.XPATH, '//*[@id="_real_schedule_body"]/div[2]/div/div[3]/div[3]/div/div[3]/div[1]/input')
    for _ in range(8):
        start_time.send_keys(Keys.BACKSPACE)
    start_time.send_keys(hw[2])
    time.sleep(0.2)

    # 마감일 입력
    end_day = driver.find_element(By.XPATH, '//*[@id="end_date"]')
    for _ in range(10):
        end_day.send_keys(Keys.BACKSPACE)
    end_day.send_keys(hw[3])
    time.sleep(0.2)

    # 마감 시간 입력
    end_time = driver.find_element(By.XPATH, '//*[@id="_real_schedule_body"]/div[2]/div/div[3]/div[3]/div/div[5]/div[1]/input')
    for _ in range(8):
        end_time.send_keys(Keys.BACKSPACE)
    end_time.send_keys(hw[4])
    time.sleep(0.2)

    driver.find_element(By.XPATH, '//*[@id="_real_schedule_body"]/div[2]/div/div[7]/button[1]').click()
    driver.find_element(By.XPATH, '//*[@id="header"]/h1/a[2]').click()
    time.sleep(0.5)