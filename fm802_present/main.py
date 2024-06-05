import tweepy
from datetime import datetime, timezone
import pytz
import pandas as pd
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーとトークンを取得
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Tweepyクライアントを初期化
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

search_word = 'マーケティング'
item_number = 50

# ツイートを検索
response = client.search_recent_tweets(query=search_word, tweet_fields=['created_at', 'public_metrics', 'author_id'], max_results=item_number)

# 関数: UTCをJSTに変換する
def change_time_JST(u_time):
    utc_time = datetime(u_time.year, u_time.month, u_time.day, u_time.hour, u_time.minute, u_time.second, tzinfo=timezone.utc)
    jst_time = utc_time.astimezone(pytz.timezone('Asia/Tokyo'))
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

# 取得したデータから必要な情報を取り出す
tw_data = []

for tweet in response.data:
    tweet_time = change_time_JST(tweet.created_at)
    tw_data.append([
        tweet.id,
        tweet_time,
        tweet.text,
        tweet.public_metrics['like_count'],
        tweet.public_metrics['retweet_count'],
        tweet.author_id,
        # ここでユーザー情報を取得する必要がある場合、追加のAPI呼び出しが必要になります
    ])

# DataFrameに変換
labels = [
    'ツイートID',
    'ツイート時刻',
    'ツイート本文',
    'いいね数',
    'リツイート数',
    'ユーザーID'
]

df = pd.DataFrame(tw_data, columns=labels)

# CSVファイルに出力
file_name = 'tw_data.csv'
df.to_csv(file_name, encoding='utf-8-sig', index=False)

print("データがCSVファイルに保存されました:", file_name)
