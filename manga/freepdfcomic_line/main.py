import requests
from bs4 import BeautifulSoup
import os

def get_latest_ep():
    # 話数を取得
    load_url = "https://freepdfcomic.com/"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    
    def should_exclude(link):
        # href属性がページ番号や特定のパターンを含む場合は除外
        href = link.get('href', '')
        if any(pattern in href for pattern in ['/page/', '/listed', '/cdn-cgi/l/email-protection']):
            return True
        # 特定のクラス名を持つリンクを除外
        if 'page-numbers' in link.get('class', []) or 'more-link' in link.get('class', []):
            return True
        # 特定のテキスト内容を持つリンクを除外
        text = link.get_text().strip()
        if text in ["Free PDF Comic"]:
            return True
        return False
    
    latest_ep = None
    latest_url = None
    latest_image_url = None

    for link in soup.find_all("a"):
        for span in link.find_all("span", class_="screen-reader-text"):
            span.decompose()
        if not should_exclude(link):
            text = link.get_text().strip()
            if text and text != "続きを読む":
                latest_ep = text
                latest_url = link.get('href')
                if link.find('img'):
                    latest_image_url = link.find('img').get('src')
                break
    return latest_ep, latest_url, latest_image_url

def try_encodings(file_path, encodings=['utf-8', 'latin-1', 'cp1252']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read().strip()
        except UnicodeDecodeError:
            continue
    return ""

def log_check(content):
    # 最新話かどうか判定
    logfile_name = "comic_log.txt"
    if not os.path.exists(logfile_name):
        with open(logfile_name, 'w', encoding='utf-8') as file:
            file.write("")
    
    logged_content = try_encodings(logfile_name)
    
    if logged_content == content:
        return False
    else:
        with open(logfile_name, 'w', encoding='utf-8') as file:
            file.write(content)
        return True

def send_line(text, url, image_url):
    # ライン送信
    api_url = 'https://notify-api.line.me/api/notify'
    token = "L3c2i88EaQ2DUwpUTXm88o3M5KHnb3GrfJz1piaNX3N"  # ここにトークンを貼り付けてください
    headers = {'Authorization': 'Bearer ' + token}
    message = f"Free PDF Comic {text} が更新されました\n{url}"
    payload = {'message': message}
    if image_url:
        payload['imageThumbnail'] = image_url
        payload['imageFullsize'] = image_url
    response = requests.post(api_url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    latest_episode, latest_url, latest_image_url = get_latest_ep()
    if latest_episode and log_check(latest_episode):
        send_line(latest_episode, latest_url, latest_image_url)