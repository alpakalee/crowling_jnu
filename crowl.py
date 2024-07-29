import pyautogui
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pyperclip

# 좌표 설정
x_win = 1403
y_win = 531
x_kakao = 1561
y_kakao = 112
x_chat = 1735
y_chat = 111

setting_date = 5

# 웹드라이버 설정
def driversetup(url):
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    return driver

# 웹페이지에서 데이터 크롤링
def get_latest_notice(driver, url_type):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    notices = soup.select('tbody tr')
    recent_notices = []
    
    if url_type == "www.sojoong" or url_type == "aicoss" or url_type == "jnu.nccoss":
        for notice in notices:
            date_td = notice.find_all('td', class_='mobileNone')[1].text.strip()
            notice_date = datetime.strptime(date_td, "%Y.%m.%d")
            if (datetime.now() - notice_date).days <= setting_date:
                title = notice.find('strong', class_='cutText').text.strip()
                link = notice.find('a')['href']
                link_id = link.split('(')[1].split(')')[0]
                recent_notices.append(f"{title} \n https://{url_type}.kr/www/notice/view/{link_id}")   
            else:
                break
    elif url_type == "eaierc":
        for notice in notices:
            date_td = notice.find('td', class_='kboard-list-date').text.strip()
            notice_date = datetime.strptime(date_td, "%Y.%m.%d")
            if (datetime.now() - notice_date).days <= setting_date:
                title = notice.find('div', class_='kboard-default-cut-strings').text.strip()
                link = notice.find('a')['href']
                full_link = f"https://eaierc.jnu.ac.kr{link}"
                recent_notices.append(f"{title}\n{full_link}")
            else:
                break

    return recent_notices

# 카카오톡으로 메시지 보내기
def send_to_kakao(messages, header):
    pyautogui.moveTo(x_win, y_win)
    pyautogui.doubleClick()
    time.sleep(15)
    pyautogui.moveTo(x_kakao, y_kakao)
    pyautogui.click()
    time.sleep(1)
    
    pyautogui.moveTo(x_chat, y_chat)
    pyautogui.doubleClick()
    time.sleep(3)
    
    pyperclip.copy(f"오늘의 알림 \n{header}")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("shift", "enter")
    time.sleep(1)
        
    for message in messages:
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("shift", "enter")
        time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

# URL 및 알림 유형 설정
urls = [
    ('https://www.sojoong.kr/www/notice/', '소중사업단', 'www.sojoong'),
    ('https://aicoss.kr/www/notice/?cate=%EC%A0%84%EB%82%A8%EB%8C%80%ED%95%99%EA%B5%90', '인혁단', 'aicoss'),
    ('https://eaierc.jnu.ac.kr/community/notice/', 'Energy+ai', 'eaierc'),
    ('https://jnu.nccoss.kr/www/notice/', '차통단', 'jnu.nccoss')
]
time.sleep(10)
for url, header, url_type in urls:
    driver = driversetup(url)
    latest_notices = get_latest_notice(driver, url_type)
    
    if latest_notices:
        send_to_kakao(latest_notices, header)
