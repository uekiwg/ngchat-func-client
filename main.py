# coding: utf-8

"""
事前準備)
・Azure Speech Servicesのトライアルを有効化し、エンドポイント、キーを取得する。
　https://docs.microsoft.com/ja-jp/azure/cognitive-services/

・config_azure.json へエンドポイント、キーを設定する。

・config_firebase.json へAPIキー、認証メールアドレス(Firebaseアカウント)、FunctionsのURLを設定する。

起動方法)
  python3 main.py
  
"""
import sys
import json
import requests
sys.path.append("./mylib")
import my_log as log# ./lib/my_log.py
import my_audio     # ./lib/my_audio.py
import my_azure     # ./lib/my_azure.py
import my_firebase  # ./lib/my_firebase.py

# Azure, Firebase への接続情報をロード
with open('./config_azure.json')    as f: config_azure = json.load(f)
with open('./config_firebase.json') as f: config_firebase = json.load(f)

# 録音してBeing Speech To Text へ送信する音声ファイル
wav = "./tmp/audio_rec.wav"
#wav = "./tmp/ohayo.wav"

# 録音時間(秒)
rec_sec = 5

audio = my_audio.MyAudio()
azure = my_azure.MyAzure(config_azure)
fbase = my_firebase.MyFirebase(config_firebase)

while True:
    print("「終了」と話すとプログラムを終了します。")
    print("Enter実行後、" + str(rec_sec) + "秒以内で何か話してください！")
    line = sys.stdin.readline().strip()

    audio.rec_wav(wav, rec_sec)
    text = azure.wav_to_text(wav)

    fbase.add_comment(text)

    if ("終了" == text):
        break