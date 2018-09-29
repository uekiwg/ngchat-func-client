# coding: utf-8
"""
wavファイルの変換)
  ffmpeg  -i audio_rec_org.wav  -vn -ac 2 -ar 16000 -acodec pcm_s16le -f wav audio_rec.wav
"""
import os
import subprocess
from time import sleep
import my_log as log # ./lib/my_log.py

class MyAudio:

    def rec_wav(self, wav, rec_sec):
        log.debug("Start. wav=" + wav + ", rec_sec=" + str(rec_sec))
        if os.path.exists(wav):
            os.remove(wav)
        
        if os.name == 'nt': # Windows
            # http://www.cepstrum.co.jp/download/recplay/recplay.html
            cmd = "trec44s.exe " + wav + " " + str(rec_sec)
        else:
            cmd = "rec " + wav + " trim 0 " + str(rec_sec)
        log.info("Exec " + cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        #sleep(10)
        p.terminate();
        log.debug("End.")

