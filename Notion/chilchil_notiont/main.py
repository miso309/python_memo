from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def addContent(title, date, link, token, databaseId, category, genre, note):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    notionUrl = 'https://api.notion.com/v1/pages'
    addData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "名前": {
                "title": [
                    {
                        "text": {"content": title}
                    }
                ]
            },
            "分類": {
                "multi_select": [{"name": category}]
            },
            "ジャンル": {
                "multi_select": [{"name": genre}]
            },
            "URL": {"url": link},
            "メモ": {
                "rich_text": [
                    {"text": {"content": note}}
                ]
            }
        }
    }
    data = json.dumps(addData)
    response = requests.post(notionUrl, headers=headers, data=data)
    print(response.status_code, response.text)

def job(url, token, databaseId, category, genre, note):
    chrome_options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        browser.get(url)
        elem_search_keywords = browser.find_element(By.ID, 'ID')
        elem_search_keywords.send_keys('検索したい本のタイトル')

        elem_search_btm = browser.find_element(By.CLASS_NAME, 'Class')
        elem_search_btm.click()

        browser.implicitly_wait(5)

        first_link = browser.find_element(By.CLASS_NAME, 'Class').find_element(By.TAG_NAME, 'Tag')
        first_link.click()

        time.sleep(1)

        title = browser.find_element(By.CLASS_NAME, 'Class').text
        link = browser.current_url

        addContent(title, datetime.datetime.now().isoformat(), link, token, databaseId, category, genre, note)
    finally:
        browser.quit()

if __name__ == "__main__":
    token = os.getenv("NOTION_TOKEN")
    databaseId = os.getenv("DATABASE_ID")
    category = "ここにタグを入力"
    genre = "ここにタグを入力"
    note = "ここにメモを入力"
    url = 'ここにURLを添付する'
    job(url, token, databaseId, category, genre, note)
