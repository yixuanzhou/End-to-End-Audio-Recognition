from audio_filter import array2list, audiofilter, read_segment_points
from audio_segmenter import audio_segment
from audio_recognition import getToken, getText
from pyAudioAnalysis import audioSegmentation as aS

from io import StringIO
import os

from flask import Flask, make_response, jsonify
app = Flask(__name__)

@app.route('/audiourl/<url>')
def ffmpeg(url):
    #ffmpeg -i http://rs.ajmide.com/c_3/3.m3u8 -ab 16k -ar 16000 -ac 1 c3_0629.wav
    string_io = StringIO()
    try:
        string_io.write("ffmpeg -i %s -ab 16k -ar 16000 -ac 1 %s" % (audiourl, filename)) 
        cmd = string_io.getvalue()
        subprocess.call(cmd.split())
    except Exception as e:
        return

@app.route('/wavfiles')
def wavlist():
	dir = '/home/zhouyixuan/ajim'
	try:
		filenames = os.listdir(dir)
		resp = {}
		resp['code'] = 0
		resp['files'] = []
		for filename in filenames:
			if filename.endswith('.wav'):
				resp['files'].append(filename)
		return make_response(jsonify(resp))
	except Exception as e:
		return 'Error'

@app.route('/models')
def seg(models):
    [flagsInd, classesAll, acc, CM] = aS.mtFileClassification(wav, "./knnMusicGenre2",\
                                      "knn", True, './audiofiles/c3_0629.segments')
    flags = array2list(flagsInd)
    audio_step0, _ = audiofilter(flags)
    seg_points = read_segment_points(audio_step0, 8)
    #audio_segment('0629-600.wav', seg_points)

@app.route('/<audiofile>')
def audio2text(audiofile):
    token_url = "https://openapi.baidu.com/oauth/2.0/token"
    upvoice_url = 'http://vop.baidu.com/server_api'
    api_key = "SrhYKqzl3SE1URnAEuZ0FKdT"
    api_secert = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
    token_str = getToken(token_url, api_key, api_secert)
    cu_id = "9c:4e:36:b9:d6:28"
    #print(getText("c3_0629_392_399.wav", token_str, cu_id, upvoice_url))
    '''for seg_point in seg_points:
        start, end = seg_point[0], seg_point[1]
        filename = "c3_0629_%s_%s.wav" % (start, end)'''
        #signal = open(filename, "rb").read()
        #rate = 16000
        #recognize(signal, rate, token)
        #print filename[:-4], getText(filename, token_str, cu_id, upvoice_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8215)
