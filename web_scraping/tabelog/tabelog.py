import requests
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Googleスプレッドシートの認証情報ファイルのパス
CREDENTIALS_FILE = 'path/to/your/credentials.json'  # 実際のパスに置き換えてください

# 認証に必要なスコープ（権限）
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']

# 対象のGoogleスプレッドシートのキー
SHEET_KEY = 'your_spreadsheet_key'  # 実際のスプレッドシートキーに置き換えてください

# 使用するシートの名前
SHEET_NAME = '食べログ'

# Googleスプレッドシートへの認証
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
gc = gspread.authorize(credentials)

# スプレッドシートのキーを使用してスプレッドシートを開く
spreadsheet = gc.open_by_key(SHEET_KEY)

# 新規ワークシートを作成（存在する場合は上書きするために削除）
try:
    worksheet = spreadsheet.worksheet(SHEET_NAME)
    spreadsheet.del_worksheet(worksheet)
except gspread.exceptions.WorksheetNotFound:
    pass
worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows="1000", cols="20")

# ベースURL（例：東京のレストラン）
base_url = 'https://tabelog.com/tokyo/A1301/A130101/'

# レストランの情報を格納するリスト
restaurants = []

# 1ページ目から60ページ目までのデータを取得
for page in range(1, 61):
    # ページに応じたURLを設定
    url = base_url if page == 1 else f'{base_url}rstLst/{page}/'
    
    response = requests.get(url)
    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # レストラン情報の取得
    restaurant_elements = soup.select('.list-rst__rst-name-target')
    if not restaurant_elements:
        continue

    for restaurant in restaurant_elements:
        name = restaurant.get_text(strip=True)
        link = restaurant['href']
        
        # 詳細ページのコンテンツを取得
        detail_response = requests.get(link)
        if detail_response.status_code != 200:
            continue

        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
        
        # 評価
        rating_element = detail_soup.select_one('.rdheader-rating__score-val-dtl')
        if not rating_element:
            continue
        rating = rating_element.get_text(strip=True)
        
        # 住所
        address_element = detail_soup.select_one('.rstinfo-table__address')
        if not address_element:
            continue
        address = address_element.get_text(strip=True)
        
        restaurants.append([name, rating, address])
    
    # サーバーに負荷をかけないためにスリープを挟む
    time.sleep(2)

# スプレッドシートにデータを書き込む
worksheet.append_row(['レストラン名', '評価', '住所'])  # ヘッダーを追加

# 一括で書き込み
worksheet.append_rows(restaurants)
