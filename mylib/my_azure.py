# coding: utf-8
"""
Speech to Text API の検証方法)
# 認証トークンの取得
curl -v -X POST 
 "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
 -H "Content-type: application/x-www-form-urlencoded"
 -H "Content-Length: 0"
 -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY"
 > token
# Speech to Textの呼び出し
curl -X POST "https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-JP&local=ja-JP"
 -H "Transfer-Encoding: chunked"
 -H "Authorization: `cat token`"
 -H 'Content-type: audio/wav; codec="audio/pcm";  samplerate=44100'
 --data-binary @tmp/audio_rec.wav

"""
import os
import requests
import urllib
import my_log as log # ./lib/my_log.py

class MyAzure(object):

    """
    コンストラクタ。
    
    Parameters
    ----------
    config : dict
        Speech API(旧 Bing Speech Service)へ接続するための情報
    """
    def __init__(self, config):
        self.config = config

    """
    音声ファイルをテキスト変換する。
    
    Parameters
    ----------
    wav : string
        録音してBeing Speech To Text へ送信する音声ファイル
    
    Returns
    ----------
    text : string
        変換結果
    """
    def wav_to_text(self, wav):
        log.debug("Start. wav=" + wav)
        
        # wavファイルを読み込む
        with open(wav, 'rb') as infile:
            raw_data = infile.read()
        
        # 認証トークンを取得
        token = self._authorize()
        
        # Speech to Textを呼び出す
        text  = self._speech_to_text(raw_data, token)
        
        log.debug("End. return " + text)
        return text

    def _authorize(self):
        log.debug("Start.")
        url = self.config["authURL"]
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Content-Length": "0",
            "Ocp-Apim-Subscription-Key": self.config["apiKey"]
        }
        
        log.info("Request -------------\n  url=" + url + "\n  headers=" + str(headers))
        response = requests.post(url, headers=headers)

        if not response.ok:
            log.debug("Response NG")
            response.raise_for_status()

        log.info("Response OK")
        log.debug("End.")
        return response.text

    def _speech_to_text(self, raw_data, token, lang="ja-JP", samplerate=16000):
        log.debug("Start.")

        # Bing Speech API呼び出し
        url =  self.config["wav2textURL"] + "?" + urllib.parse.urlencode({
           "language": lang
        })
        headers = {
           "Content-type": "audio/wav; codec=audio/pcm; samplerate={0}".format(samplerate),
           #"Transfer-Encoding": "chunked",
           "Authorization": "Bearer " + token 
        }
        log.info("Request -------------\n  url=" + url + "\n  headers=" + str(headers))
        response = requests.post(url, data=raw_data, headers=headers)
        if not response.ok:
            raise response.raise_for_status()

        # 文字化け対策のためutf-8で処理する
        response.encoding = "utf-8"
        log.info("Response ------------\n  " + response.text)

        json = response.json();
        if ("Success" != json["RecognitionStatus"]):
            log.warn(json["RecognitionStatus"] + "が発生しました。")
            return ""
        result = response.json()["DisplayText"]

        print("End.")
        return result
