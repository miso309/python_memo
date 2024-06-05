import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sched, time, datetime
import os

def get_latest_ep():  # 話数を取得
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # GUIを開かないモードで動作させる
    driver = webdriver.Chrome(options=options)
    load_url = "https://comic-mangashelf.com/category/netabare"
    driver.get(load_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    latest_ep = ""
    for element in soup.find_all("h2"):  # すべてのaタグを検索
        if "最終話" in element.text and "結末" in element.text:  # 要素を文字列化し、話数を抽出
            latest_ep = element.text
            break
    driver.quit()
    return latest_ep

def log_check(content):  # 最新話かどうか判定
    logfile_name = "netabare_log.txt"
    if not os.path.exists(logfile_name):  # ログファイルの存在を確認
        with open(logfile_name, 'w', encoding='utf-8') as file:  # なければ作る
            file.write("")
    with open(logfile_name, 'r', encoding='utf-8') as file:  # 読み取りでファイルを開く
        if file.readline().strip() == content:
            return False
    with open(logfile_name, 'w', encoding='utf-8') as file:  # 更新のために書き込む
        file.write(content)
    return True

def send_line(text):  # ライン送信
    url = 'https://notify-api.line.me/api/notify'
    token = os.getenv("LINE_NOTIFY_TOKEN")  # 環境変数からトークンを取得
    if not token:
        print("LINE token not found. Please set the LINE_NOTIFY_TOKEN environment variable.")
        return
    headers = {'Authorization': 'Bearer ' + token}
    message = f"ネタバレ・感想{text}が更新されました"
    payload = {'message': message}
    try:
        p = requests.post(url, headers=headers, data=payload, timeout=10)
        print(p)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    def periodic_check():
        print(f"Checking at {datetime.datetime.now()}")
        try:
            latest_episode = get_latest_ep()
            if log_check(latest_episode):
                send_line(latest_episode)
        except Exception as e:
            print(f"Error during check: {e}")
        scheduler.enter(1800, 1, periodic_check)  # 30分ごとにチェック
    scheduler.enter(1, 1, periodic_check)  # 最初のチェックを開始
    scheduler.run()