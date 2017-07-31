from audio_filter import array2list, audiofilter, read_seg_points
from audio_segmenter import audio_segment
from audio_recognition import audio2text_multiprocessing
from pyAudioAnalysis import audioSegmentation as aS
from io import StringIO
from pythrift import *

import os
import subprocess
import urlparse

from flask import Flask, make_response, jsonify, send_from_directory, request
import sys
sys.path.append('./hbase')

app = Flask(__name__)


@app.route('/music/<filename>')
def get_file(filename):
    if os.path.exists('audiofiles/' + filename):
        return send_from_directory('audiofiles', filename)
    elif os.path.exists('segs/' + filename):
        return send_from_directory('segs', filename)


@app.route('/rec_types')
def rec_types():
    rec_types_list = set()
    with open('rec_types.txt', 'r') as f:
        for t in f.readlines():
            rec_types_list.add(t)
    r = {'code': 0, 'rec_types': list(rec_types_list)}
    response = make_response(jsonify(r))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/wavfiles')
def wav_list():
    audio_dir = 'audiofiles/'
    file_names = os.listdir(audio_dir)
    resp = {'code': 0, 'files': list()}

    for file_name in file_names:
        if file_name.endswith('.wav'):
            resp['files'].append(file_name)
    response = make_response(jsonify(resp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


def seg(file_name, rec_type):
    [flagsInd, classesAll, acc, CM] = aS.mtFileClassification('audiofiles/' + file_name,
                                      "./" + rec_type + 'MusicGenre2', rec_type, False)
    print(os.getcwd())
    flags = array2list(flagsInd)
    audio_step0, _ = audiofilter(flags)
    with open(os.path.join('seg_result/', file_name + '.seg'), 'w') as f:
        for s in audio_step0:
            f.write(str(s) + '\n')
    seg_points = read_seg_points(audio_step0, 8)
    #seg_points = read_segment_points(audio_step0, 8)
    audio_segment('audiofiles/' + file_name, seg_points)
    return audio_step0, len(flagsInd)


@app.route('/m3u8_download', methods=['GET'])
def m3u8_downloader():
    request_data = request.args
    m3u8_url = request_data.get('url')
    file_name = urlparse.urlparse(m3u8_url).path.strip('/').replace('/', '_').split('.')[0] + '.wav'
    io = StringIO()
    io.write(u'ffmpeg -y -i {} -ab 16k -ar 16000 -ac 1 audiofiles/{}'.format(m3u8_url, file_name))
    cmd = io.getvalue()
    subprocess.call(cmd.split())
    resp = {"file_name": file_name, "code": 0}
    response = make_response(jsonify(resp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/audio_recognize', methods=['GET'])
def audio_rec():
    request_data = request.args
    file_name = request_data.get('file')
    rec_type = request_data.get('rec_type')
    result, duration = seg(file_name.encode('utf-8'), rec_type)
    resp = {"file_name": file_name, "code": 0, "duration": duration, "rec_result": result}
    response = make_response(jsonify(resp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/audio_to_text', methods=['GET'])
def audio2text():
    request_data = request.args
    file_name = request_data.get('file')
    result, seg_points = audio2text_multiprocessing(file_name)
    text_result = {'text': [], 'code': 0}
    for i in range(len(result)):
        r = result.get(i, 'error')
        text_result['text'].append(r)
    i = 0
    h_data = []
    ht = HBaseAji(table='wahaha')
    typename = {0: 'music', 1: 'speech'}
    for s in seg_points:
        if s[2] == 1:
            h_data.append((file_name, s[0], s[1], s[2], text_result['text'][i]))
            fn = file_name.split('.')[0] + '_' + str(s[0]) + '_' + str(s[1]) + '.wav'
            ht.put(fn, '0', s[2], typename[s[2]], text_result['text'][i].encode('utf-8'))
            i += 1
        else:
            h_data.append((file_name, s[0], s[1], s[2], ''))
            fn = file_name.split('.')[0] + '_' + str(s[0]) + '_' + str(s[1]) + '.wav'
            ht.put(fn, '0', s[2], typename[s[2]], 'None')

    response = make_response(jsonify(text_result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/search', methods=['GET'])
def scanwithkw():
    request_data = request.args
    s = urlparse.unquote(request_data.get('s'))
    ht = HBaseAji(table='wahaha')
    result = ht.scanWithKeyword(s)
    r = []
    for i in range(len(result)):
        r.append({'name': result[i].row, 'value': result[i].columns['content:0'].value})
    resp = {"code": 0, "data": r, "err_msg": 0}
    response = make_response(jsonify(resp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8216, threaded=True)
