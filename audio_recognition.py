# -*- coding: utf-8 -*-
import time
import requests
import json
import base64
from audio_filter import read_seg_points
from pythrift import *
from threading import Thread
threads = []


def get_token(token_url, api_key, api_secert):
    data = {'grant_type': 'client_credentials', 'client_id': api_key, 'client_secret': api_secert}
    r1 = requests.post(token_url, verify=False, data=data)
    Token = json.loads(r1.text)
    return Token['access_token']


def get_text(filename, token_str, cu_id, upvoice_url, text_result, num):
    for _ in range(3):
        try:
            data = {"format": "wav", "rate": 8000, "channel": 1, "token": token_str, "cuid": cu_id, "lan": "zh"}
            wav_fp = open(filename, 'rb')
            voice_data = wav_fp.read()
            data['len'] = len(voice_data)
            print num, data
            data['speech'] = base64.b64encode(voice_data).decode('utf-8')
            r = requests.post(upvoice_url, data=json.dumps(data))
            r = json.loads(r.text)
            if r.get('result'):
                text_result[num] = r.get('result')[0]
                print num, r.get('result')[0].decode('utf-8')
                return
            else:
                # print num, r.get('err_msg')
                if r.get('err_msg') == 'recognition error.':
                    text_result[num] = r.get('err_msg')
                    return
        except Exception as e:
            print(e)
            continue
    text_result[num] = 'error'
    return


def audio2text_multiprocessing(file_name):
    result = []
    with open('seg_result/' + file_name + '.seg', 'r') as f:
        for l in f.readlines():
            result.append(int(l))
    token_url = "https://openapi.baidu.com/oauth/2.0/token"
    upvoice_url = 'http://vop.baidu.com/server_api'
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"
    api_secret = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
    cu_id = "9c:4e:36:b9:d6:28"
    seg_points = read_seg_points(result, 8)
    text_result = dict()
    count = 0
    for s in range(0, len(seg_points), 10):
        for i, seg_point in enumerate(seg_points[s: s+10]):
            if seg_point[2] != 1:
                continue
            token_str = get_token(token_url, api_key, api_secret)
            start, end = seg_point[0], seg_point[1]
            filename = "segs/%s_%s_%s.wav" % (file_name.split('/')[-1].split('.')[0], start, end)
            t = Thread(target=get_text, args=(filename, token_str, cu_id, upvoice_url, text_result, count))
            count += 1
            threads.append(t)
            t.start()
            time.sleep(1)
        while len(threads) > 0:
            t = threads.pop()
            t.join()
    return text_result, seg_points


'''if __name__ == "__main__":
    token_url = "https://openapi.baidu.com/oauth/2.0/token" 
    upvoice_url = 'http://vop.baidu.com/server_api'
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"    
    api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
    token_str = getToken(token_url, api_key, api_secert)
    cu_id = "9c:4e:36:b9:d6:28"
    print(getText("c3_0629_392_399.wav", token_str, cu_id, upvoice_url))'''
