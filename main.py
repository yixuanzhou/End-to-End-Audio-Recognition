#!/usr/bin/python
# -*- coding: UTF-8 -*-
from audio_filter import array2list, audiofilter, read_segment_points, read_seg_points
from audio_segmenter import audio_segment
from audio_recognition import getToken, getText
#from pyAudioAnalysis import audioSegmentation as aS
from pythrift import *

#ffmpeg -i http://rs.ajmide.com/c_3/3.m3u8 -ab 16k -ar 16000 -ac 1 c3_0629.wav

if __name__ == "__main__":
	'''[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("0629-600.wav", "./knnMusicGenre2",\
					           		  "knn", False, './audiofiles/c3_0629.segments')

	flags = array2list(flagsInd)
	print flags'''
	flags = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	audio_step0, result = audiofilter(flags)
	#seg_points = read_segment_points(audio_step0, 8)
	seg_points = read_seg_points(audio_step0, 8)
	#print seg_points
	#audio_segment('0629-600.wav', seg_points)
	token_url = "https://openapi.baidu.com/oauth/2.0/token"
	upvoice_url = 'http://vop.baidu.com/server_api'
	api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"
	api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
	token_str = getToken(token_url, api_key, api_secert)
	cu_id = "9c:4e:36:b9:d6:28"

	ht = HBaseAji(table='test5')
	typename = {0: 'music', 1: 'speech'}
    #print(getText("c3_0629_392_399.wav", token_str, cu_id, upvoice_url))

	for index, seg_point in enumerate(seg_points):
		__type, start, end = seg_point[0], seg_point[1], seg_point[2]
		#print __type, start, end
		if __type == 1:
			filename = "./segs/c3_0629_%s_%s.wav" % (start, end)
			#print filename
		#signal = open(filename, "rb").read()
		#rate = 16000
		#recognize(signal, rate, token)
		#print '%ss to %ss' %(start, end), getText(filename, token_str, cu_id, upvoice_url)
			text = getText(filename, token_str, cu_id, upvoice_url).encode('utf-8')
			print(text)
		else:
			text = 'None'
		#['m3u8', 'start_time', 'end_time', 'type', 'content']
		try:
			ht.put(filename, '0', filename, __type, typename[__type], text)
			print(ht.getRow(filename))
		except Exception as e:
			print(e)
			continue
		'''with open("segs.txt", "a") as f:
			f.write('%ss to %ss %s\n' %(start, end, text))'''
	#print ht.getRow(rowkey)

	#for i in ht.getRows([rowkey] * 4):
	#	print i
	tl = ht.scanWithKeyword('上海')
	print tl
	'''scan = Hbase.TScan()
	scan.columns = ['content:0']
	scan.filterString = "ValueFilter(=,'substring:上海')"
	t = ht.client.scannerOpenWithScan('test5', scan, None)
	result = ht.client.scannerGetList(t, 100)'''
	
	#print str(result).decode('utf-8')