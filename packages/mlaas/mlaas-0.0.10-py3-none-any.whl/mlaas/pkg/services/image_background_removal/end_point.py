import requests
from urllib.parse import urlencode, quote_plus
import os
import base64
import json   

def background_removal(img_path,output_path):
    # url = "https://api.mlaas.me/background_removal/background_removal"
    url = "http://127.0.0.1:5001/background_removal/background_removal"
    data = open(img_path, 'rb').read()
    data_b64 = base64.b64encode(data).decode("utf8")
    is_video = img_path[-3:] not in ['png','jpg']
    content = {'img_path':img_path,'img_data':data_b64,'is_video':str(is_video).lower() }

    background_free_img = requests.post(url, data = content).json()['data']
    content_bytes = base64.b64decode(background_free_img.encode('utf-8'))
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    open(output_path, 'wb').write(content_bytes)
    return 


if __name__=='__main__':
    background_removal("/home/mlaas/repos/python-client/tmp/image_background_removal/20210603073725_Trim_Trim.mp4",output_path='tmp/background_removal/out.mp4')