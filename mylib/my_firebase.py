# coding: utf-8
"""
"""
import os
import pyrebase # sudo pip3 install pyrebase

import requests
import urllib
import my_log as log # ./lib/my_log.py

class MyFirebase:

    """
    コンストラクタ。
    
    Parameters
    ----------
    config : dict
        Firebaseへ接続するための情報
    """
    def __init__(self, config):
        self.config = config
        self.firebase = pyrebase.initialize_app(config)

    def add_comment(self, text):
        log.debug("Start. text=" + text)
        
        auth = self.firebase.auth()
        user = auth.sign_in_with_email_and_password(self.config["email"], self.config["password"])
        print(user)

        # Firebase Functions呼び出し
        url =  self.config["addCommentURL"]
        headers = {
           "Authorization": "Bearer " + user["idToken"]
        }
        data = {
            "email": self.config["email"],
            "content": text
        }
        log.info("Request -------------\n  url=" + url + "\n  headers=" + str(headers) + "\n  data=" + str(data))
        response = requests.post(url, data=data, headers=headers)
        if not response.ok:
            raise response.raise_for_status()
            
        # 文字化け対策のためutf-8で処理する
        response.encoding = "utf-8"
        log.info("Response ------------\n  " + response.text)

        
        log.debug("End.")
