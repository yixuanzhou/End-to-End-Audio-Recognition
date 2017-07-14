# -*- coding: UTF-8 -*-
import requests
import json
import base64

def getToken(token_url, api_key, api_secert):
    data={'grant_type':'client_credentials','client_id':api_key,'client_secret':api_secert}
    r=requests.post(token_url,data=data)
    Token=json.loads(r.text)
    return Token['access_token']

def getText(filename, token_str, cu_id, upvoice_url):    
    data = {"format":"wav","rate":16000, "channel":1,"token":token_str,"cuid":cu_id,"lan":"zh"}
    wav_fp = open(filename,'rb')
    voice_data = wav_fp.read()
    data['len'] = len(voice_data)
    data['speech'] = base64.b64encode(voice_data).decode('utf-8')
    post_data = json.dumps(data)    
    r = requests.post(upvoice_url, data=bytes(post_data))
    r = json.loads(r.text)
    #start = r.text.find('result')
    #end = r.text.find('sn')
    #r = requests.post(upvoice_url, data=json.dumps(data))
    return r.get('result')
    #return r.text[start+8:end-2]
    #return r.text


'''if __name__ == "__main__":
    token_url = "https://openapi.baidu.com/oauth/2.0/token" 
    upvoice_url = 'http://vop.baidu.com/server_api'
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"    
    api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
    token_str = getToken(token_url, api_key, api_secert)
    cu_id = "9c:4e:36:b9:d6:28"
    print(getText("c3_0629_392_399.wav", token_str, cu_id, upvoice_url))'''
