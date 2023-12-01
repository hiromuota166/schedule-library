from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from linetest import send_line_notify
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

def run():
    options = Options()
    options.headless = False  # ヘッドレスモード True=非表示, False=表示
    driver = webdriver.Chrome(options=options)

    # メールアドレスとパスワードの指定
    USERNAME = os.getenv("USERNAME")
    PASS = os.getenv("PASS")

    # ブラウザを起動
    driver.get(
        "https://sso.ritsumei.ac.jp/siteminderagent/forms/login.fcc?SMQUERYDATA=-SM-ggOZBHQthWXvF%2fdsaXkETfrsYH5KjtctGsFHSGU6fZZaFsaM7ohaNPYzLO60ZVw3n37DTrKSTZlTVh%2b2%2bVLjiTakjJR4E8mRLliTcTKLOyMshMnVjH4DGhC41piha%2b0zTtyn44IgYdNFoB%2fckwBcG57oIgd0tK%2bhahFd3fjcOC7jVZGHdvAPwAxMhd63UB%2fP5Sf3ifb0VoHah8wjW5lFHXeE4LFv5LU30Vp69FpWXD0Gz330inCGiBaLiFGJjIuh%2bX65Fr7%2fud%2fUHKCFNEOY9NJFxDsG57euGeWU2P2K5%2fLGjX1dbvdI1jPfnElE3cFPDAjlpua9iCUC293%2bhFZ%2fCSrzm0TDOPFXrFBsOsB5FceE3Aa8fUiAxGGBfKd3RCGUDLW%2buuCA26R5LERwbfYTvmK8gB2olS%2fs"
    )
    time.sleep(2)  # 2秒待機

    # ログイン情報を入力する
    search_name = driver.find_element_by_name("USER")
    search_pass = driver.find_element_by_name("PASSWORD")
    search_btn = driver.find_element_by_id("Submit")
    search_name.send_keys(USERNAME)
    search_pass.send_keys(PASS)
    search_btn.click()
    time.sleep(2)  # 2秒待機

    # 利用予定教室の情報を取得
    soup = BeautifulSoup(driver.page_source, "html.parser")

    #もし教室が取れていたら
    if soup.find(class_="user_rsv"):
        tag = soup.find(href=re.compile("void"))
        tag_text = tag.text.strip()

        cleaned_text = ' '.join(tag_text.split())
        date_text = cleaned_text.replace(' ( ', ' ').replace(' )', '').replace('～', '～')
        date_text = f"日時:{date_text}"

        text_after_a = tag.next_sibling.strip()
        lines = [line.strip() for line in text_after_a.split('\n') if line.strip()]
        formatted_text = '教室が取れました。\n' + '\n'.join(lines)+ '\n' + date_text
        send_line_notify(formatted_text)
    else:
        print("教室はまだ取れていません。")

if __name__ == "__main__":
    run()
