from audio_filter import array2list, audiofilter, read_segment_points, read_seg_points
from audio_segmenter import audio_segment
#from audio_recognition import getToken, getText
from urllib_post import getToken, getText
from pyAudioAnalysis import audioSegmentation as aS

#ffmpeg -i http://rs.ajmide.com/c_3/3.m3u8 -ab 16k -ar 16000 -ac 1 c3_0629.wav

if __name__ == "__main__":
	[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("0629-600.wav", "./knnMusicGenre2",\
					           		  "knn", False, './audiofiles/c3_0629.segments')
	flags = array2list(flagsInd)
	audio_step0, _ = audiofilter(flags)
	print audio_step0
	#seg_points = read_segment_points(audio_step0, 8)
	seg_points = read_seg_points(audio_step0, 8)
	print seg_points
	#audio_segment('0629-600.wav', seg_points)
	token_url = "https://openapi.baidu.com/oauth/2.0/token" 
	upvoice_url = 'http://vop.baidu.com/server_api'
	api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"    
	api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
	token_str = getToken(token_url, api_key, api_secert)
	cu_id = "9c:4e:36:b9:d6:28"
    #print(getText("c3_0629_392_399.wav", token_str, cu_id, upvoice_url))

	for seg_point in seg_points:
		start, end = seg_point[0], seg_point[1]
		filename = "./segs/c3_0629_%s_%s.wav" % (start, end)
		#signal = open(filename, "rb").read()
		#rate = 16000
		#recognize(signal, rate, token)
		print '%ss to %ss' %(start, end), getText(filename, token_str, cu_id, upvoice_url)