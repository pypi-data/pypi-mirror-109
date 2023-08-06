import requests
from urllib.parse import urlencode, quote_plus
import os
import base64
import json   

def speech2text(audio_path):
    url = "https://api.mlaas.me/speech_to_text/speech_to_text"
    data = open(audio_path, 'rb').read()
    data_b64 = base64.b64encode(data).decode("utf8")
    content = {'audio_path':audio_path,'audio_data':data_b64 }

    text = requests.post(url, data = content).json()['text']
    return text



if __name__=='__main__':
    speech2text("/home/mlaas/repos/python-client/tmp/text2speech/out.wav")