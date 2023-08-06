import requests
from urllib.parse import urlencode, quote_plus
import os

def text2speech(text,output_path='tmp/text2speech/out.wav'):
    payload = {'text':text}
    encoded = urlencode(payload, quote_via=quote_plus)
    response = requests.get(f"https://api.mlaas.me/text_to_speech/text_to_speech?{encoded}",timeout=5)
    storage_path = response.json()['storage_path']
    content = requests.get(storage_path, allow_redirects=True).content

    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    open(output_path, 'wb').write(content)
    return output_path



if __name__=='__main__':
    text2speech("this is a sentece")