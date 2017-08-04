#!/bin/python3.6

import warnings
import sys
import requests
import json
from string import Template
from urllib.parse import urlunsplit
from datetime import datetime as dt
from datetime import timedelta as td
warnings.simplefilter("ignore", UnicodeWarning)

''' -----------------------------------------------------------------
Mastodon Toot From Template by itsumonotakumi

[Usage]
 python mastodon-toot-from-template.py [HOST] [JSON] [TEMPLATE]
  - HOST:  From instance's hostname
  - JSON:  Json data contains access_token
  - TEMPLATE: Toot body text which incluedes substitutes values "UPDATETIME"

'''

# 引数処理 ----------------------------------------------------------
HOST = sys.argv[1]
JSONDATA = sys.argv[2]
TEMPLATE = sys.argv[3]


# 処理ルーチン -------------------------------------------------------
# マストドンAPIアクセスのためのクラス by requestsライブラリ
class Mstdn:
    def __init__(self, token, scheme='https', host='pawoo.net'):
        self.scheme = scheme
        self.host = host
        self.session = requests.Session()
        headers = {'Authorization': 'Bearer ' + token['access_token']}
        self.session.headers.update(headers)

    def _build_url(self, path):
        return urlunsplit([self.scheme, self.host, path, '', ''])

    def _request(self, method, url, data=None, params=None):
        kwargs = {
            'data': data or {},
            'params': params or {}
        }
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def home_timeline(self):
        url = self._build_url('/api/v1/timelines/home')
        return self._request('get', url)

    def toot(self, status):
        url = self._build_url('/api/v1/statuses')
        return self._request('post', url, data={'status': status})


# コンテンツ取得・整形
def createContents(Template_Path):
    # アップデート日の取得
    Update_Day = (dt.now() - td(days=1)).strftime('%Y/%m/%d')

    with open(Template_Path, 'r', encoding='utf-8') as file_obj:
        html_template = Template(file_obj.read())

    return html_template.substitute({"UPDATETIME": Update_Day})


# Access Token取得
def getAccToken(Json_File):
    
    with open(Json_File) as json_obj:
        Json_str = json_obj.read()
    if Json_str is None or Json_str == '':
        raise Exception
    Json_dict = json.loads(Json_str)
    return Json_dict


# トゥート実行
def mastodon_toot(Hostname, Contents_data, Acc_Token):
    mstdn_obj = Mstdn(token=Acc_Token, host=Hostname)
    mstdn_obj.toot(Contents_data)


# メインルーチン
def main():
    # 記事の投稿チェック(保留)
    # checkWpPost()
    
    # コンテンツ取得・整形
    contents_data = createContents(TEMPLATE)
    
    # Access Token取得
    token = getAccToken(JSONDATA)

    # トゥート実行
    mastodon_toot(HOST, contents_data, token)


# メインルーチン（ダミー）
if __name__ == '__main__':
    main()
