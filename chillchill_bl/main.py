import os
from pprint import pprint
from notion_client import Client

notion = Client(auth=os.environ['NOTION_TOKEN'])

db = notion.databases.query(
    **{
        'database_id' : '109b95efe848472a8827991e21e6dbec'  # データベースID
       }
)
pprint(db)