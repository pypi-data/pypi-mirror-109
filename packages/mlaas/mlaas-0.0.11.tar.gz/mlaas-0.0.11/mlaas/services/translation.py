import requests
from urllib.parse import urlencode, quote_plus

def translate(text,source_lang,target_lang):
    payload = {'target':target_lang, 'source':source_lang,'text':text}
    result = urlencode(payload, quote_via=quote_plus)
    response = requests.get(f"http://api.mlaas.me/translator/translate?{result}")
    return response.json()['translation'][0]


if __name__=='__main__':
    translate("this is a sentece",'en','fr')