# -*- coding: UTF-8 -*-
import requests
import json
import uuid
import base64
import pymysql
import traceback
import time

import os
os.environ["PYSPARK_PYTHON"] = "python3"

from pyspark import SparkContext, SparkConf,SQLContext

def get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"                     # 自己申请的应用
    secret_key = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"            # 自己申请的应用
    data = {'grant_type': 'client_credentials', 'client_id': api_key, 'client_secret': secret_key}
    r = requests.post(url, data=data)
    token = json.loads(r.text).get("access_token")
    return token


def recognize(sig, rate, token):
    url = "http://vop.baidu.com/server_api"
    speech_length = len(sig)
    speech = base64.b64encode(sig).decode("utf-8")
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    rate = rate
    data = {
        "format": "wav",
        "lan": "zh",
        "token": token,
        "len": speech_length,
        "rate": rate,
        "speech": speech,
        "cuid": mac_address,
        "channel": 1,
    }
    data_length = len(json.dumps(data).encode("utf-8"))
    headers = {"Content-Type": "application/json",
               "Content-Length": data_length}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)

def recognize_by_url(rate, token, audio_url):
    url = "http://vop.baidu.com/server_api"
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    rate = rate
    data = {
        "format": "wav",
        "lan": "zh",
        "token": token,
        "rate": rate,
        "cuid": mac_address,
        "channel": 1,
	    "url":audio_url
    }
    data_length = len(json.dumps(data).encode("utf-8"))
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    record = json.loads(r.text)    
    audio = audio_url[audio_url.find('tmpaudio') + 9:]
    tag = audio.split('-')
    return [tag[:2]] + record['result']


def read_mysql():
	token = get_token()
	rate = 8000

	source_mysql_host = "120.27.141.126"
	source_mysql_db = "ajmide_clip"
	source_mysql_user = "clip_test"
	source_mysql_passwd = "xtxu67Mesq"
	conn = pymysql.connect(host=source_mysql_host, user=source_mysql_user,
	                       passwd=source_mysql_passwd, db=source_mysql_db, charset='utf8')
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	link_list =[]
	query_sql = "select oss_link, tag  from trans_files where verified = 1 limit 6"
	try:
		cursor.execute(query_sql)
		files = cursor.fetchall()
		for item in files:
			if True:
				path = item["oss_link"]
				#print(path)
				link_list.append(path)
				#recognize_by_url(rate, token, path)
	except:
		traceback.print_exc()
		pass
	cursor.close()
	conn.close()
	return link_list

def pyspark_mysql(sqlContext):
	sqlContext.read.format("jdbc").options(
		url="jdbc:mysql://localhost/mysql",
		driver="com.mysql.jdbc.Driver",
		dbtable="user",
		user="root",
		password=""
	).load().take(10)
	
if __name__ == "__main__":
	mode = "emr"
	t1 = time.time()

	if mode == "test":
		link_list = read_mysql()
		#print(link_list)
		token = get_token()
		#print(token)
		rate = 8000
		for path in link_list:
			recognize_by_url(rate, token, path)
	if mode == "emr":
		conf = SparkConf().setAppName("Simple App").setMaster("local")
		sc = SparkContext(conf=conf)
		link_list = read_mysql()
		token = get_token()		
		rate = 8000		
		links_data = sc.parallelize(link_list).map(lambda path: recognize_by_url(rate, token, path))
		sorted_data = links_data.sortBy(lambda x: (x[0][0],x[0][1])).map(lambda x: [x[0][0],x[1]])
		from operator import add
		result = sorted_data.map(lambda x: tuple(x)).reduceByKey(add).collect()
		print(result)

	elif mode == "url":
		a = read_mysql()
		pass

	elif mode == "local":
		filename = "two.wav"
		token = get_token()
		signal = open(filename, "rb").read()
		rate = 8000
		recognize(signal, rate, token)
		
	t2 = time.time()
	print(t2-t1)
	pass
