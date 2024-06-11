import requests
from bs4 import BeautifulSoup
import os

URL = 'https://freepdfcomic.com/'
LOG_FILE_NAME = 'comic_log.txt'
LINE_NOTIFY_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'

# ウェブページを取得して解析
def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

# タイトルとURLの抽出
def extract_titles_and_urls(soup):
    titles, urls = [], []
    for item in soup.find_all('h3', class_='entry-title'):
        a_tag = item.find('a')
        if a_tag:
            titles.append(a_tag.text.strip())
            urls.append(a_tag['href'])
    return titles, urls

# ファイルを複数のエンコーディングで読み込む
def try_encodings(file_path, encodings=['utf-8', 'latin1', 'cp1252']):
    for encoding in encodings:
        try:
            with open(file_path, encoding=encoding) as file:
                return file.read().strip()
        except Exception:
            continue
    return ""

# コンテンツが既にログに記録されているかチェック
def log_check(content, logfile_name='comic_log.txt'):
    if not os.path.exists(logfile_name):
        return True
    logged_content = try_encodings(logfile_name)
    return content not in logged_content.split('\n')

# ログファイルを更新
def update_log(content, logfile_name='comic_log.txt'):
    with open(logfile_name, 'a', encoding='utf-8') as file:
        file.write(content + '\n')

# LINEで通知を送信
def send_line(text, url, image_url=None):
    api_url = 'https://notify-api.line.me/api/notify'
    token = "YOUR_LINE_NOTIFY_TOKEN"
    headers = {'Authorization': 'Bearer ' + token}
    message = f"FreePDFComic {text} が更新されました\n{url}"
    payload = {'message': message}
    if image_url:
        payload.update({'imageThumbnail': image_url, 'imageFullsize': image_url})
    response = requests.post(api_url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)

# メイン処理
def main():
    soup = fetch_webpage(URL)
    titles, urls = extract_titles_and_urls(soup)
    
    if titles and urls:
        latest_ep = titles[0]
        latest_url = urls[0]

        if log_check(latest_ep):
            send_line(latest_ep, latest_url)
            update_log(latest_ep)

if __name__ == "__main__":
    main()
