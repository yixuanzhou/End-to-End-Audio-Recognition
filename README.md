# End-to-End-Audio-Recognition
# 音频数据结果可视化页面Demo文档
**现布在测试服(121.40.161.184)上，可直接访问http://121.40.161.184:8484/music\_voice.html与http://121.40.161.184:8484/search.html。**
## 服务端
###启用
**cd /home/zhouyixuan/audio2text\_api/**
**nohup python audio2text\_api.py > audio2text\_api.log &**
###接口
所有返回json的接口都必须加上跨域访问的headers，所有接口使用端口8216
##/home/zhouyixuan/audio2text\_api/audio2text\_api.py
###@app.route('/music/<filename>')
返回音频
###@app.route('/wavfiles')
获取wav文件列表
####返回格式为json包含:
code: 0代表正确，非0代表错误
err\_msg: 错误信息
files: 文件名列表(无后缀名与路径)
###@app.route('/m3u8\_download', methods=\['GET'])
下载m3u8音频流并进行转码
####返回格式为json包含:
code: 0代表正确，非0代表错误
err\_msg: 错误信息
file\_name:转码后文件名
###@app.route('/audio\_recognize', methods=\['GET'])
音频识别并返回识别结果
调用seg()方法
####返回格式为json包含:
code: 0代表正确，非0代表错误
err\_msg: 错误信息
file\_name: 文件名称(无后缀名与路径)
rec\_result: 只包含1与0的列表，代表每个8秒识别为语音还是音乐，1代表语音
###@app.route('/audio\_to\_text', methods=\['GET'])
音频转文字并返回结果
调用audio2text\_multiprocessing()方法
####返回格式为json包含:
code: 0代表正确，非0代表错误
err\_msg: 错误信息
text: 转文字结果列表，按先后顺序排列
###@app.route('/search', methods=\['GET'])
HBase关键词检索接口
###方法
##/home/zhouyixuan/audio2text\_api/audio\_segmenter.py
###audio\_segment(audio\_url, seg\_points)
###功能：
切割音频
####输入：
audio\_url: 将要进行切割的wav音频文件路径
seg\_points: 切割时间点，格式为\[\[start1, end1], \[start2, end2],...\[startn, endn]
####输出：
wav音频切割文件
##/home/zhouyixuan/audio2text\_api/audio\_filter.py
###audiofilter(flagsInd)
####功能：
音频滤波处理
####输入：
flagsInd: 一维列表，横轴为时间，纵轴为类型
####输出：
step: 滤波窗每一步的判断值
result: 完成滤波的音频时间结构 
###read\_seg\_points(audio\_step, window\_size)
####功能：
读取音频时间结构进行切割点的选取
####输入：
audio\_step: 音频时间结构
window\_size: 滤波窗大小
####输出：
time\_steps: 音频类型，切割时间点
##/home/zhouyixuan/audio2text\_api/audio\_recognition.py
###get\_token(token\_url, api\_key, api\_secret)
####功能：
获取百度语音识别所需的token
####输入：
token\_url："https://openapi.baidu.com/oauth/2.0/token"
api\_key："SrhYKqzl3SE1URnAEuZ0FKdT"
api\_secret："hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d"
####输出：
token
###get\_text(filename, token\_str, cu\_id, upvoice\_url, text\_result, num)
####功能：
返回百度语音识别转文字结果
####输入：
filename：待转文字的音频文件
token\_str：由get\_token获得的token
cu\_id：用户标识码，一般用本机mac地址
upvoice\_url：'http://vop.baidu.com/server\_api'
text\_result：转文字结果
###audio2text\_multiprocessing(file\_name)
####功能：
多线程处理
##train-model.py
###aT.featureAndTrain(\["/home/yixuan/Documents/ajim/ad","/home/yixuan/Documents/ajim/sp"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knnMusicGenre2", False)
####输入
参数一，\["/home/yixuan/Documents/ajim/ad","/home/yixuan/Documents/ajim/sp"]: 训练数据路径，需要事先进行分类，文件夹名即为类型名
参数二-五分别对应的是mtWin, mtStep, stWin, stStep
参数六，"knn"：训练类型，其他选择有svm, extratrees, gradientboosting, randomforest
参数七，"knnMusicGenre2"：模型保存文件名
最后一个参数：False代表不计算长时特征，True相反。音频切割任务只能用False
audio-classifier.py
####功能：
使用模型对音频进行分类切割\[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("./audiofiles/c3\_0629.wav", "./knnMusicGenre2", "knn", False, './audiofiles/c3\_0629.segments')
参数一，"./audiofiles/c3\_0629.wav"：音频文件路径
参数二、三：模型文件路径，模型使用方法名称
参数四： 是否给出可视化结果：若True则会给出可视化结果
参数五：标准切割点文件路径，用来比较切割准确性。 
/home/zhouyixuan/audio2text\_api/pythrift.py
###scanWithKeyword(\_\_filter)
####功能：
对传入的参数值进行搜索
####输入：
\_\_filter: 搜索词
####输出：
HBase中所有含有此关键词的记录

## 页面端
###启用
**随nginx启动**
###Html
##/data/ml\_project/music\_voice/music\_voice.html
包含js/music\_voice.js，js/jquery-3.2.1.min.js
###功能
####line32\~52:获取wav\_file\_list
调用@app.route('/wavfiles')获取wav文件列表并加入选择栏
####button 开始上传并处理
调用getRecognizedResultM3U8(m\_url)
####button 开始处理
调用getRecognizedResult(file\_name)
##/data/ml\_project/music\_voice/search.html
包含js/search.js，js/jquery-3.2.1.min.js
###Javascript
##/data/ml\_project/music\_voice/js/music\_voice.js
###getRecognizedResultM3U8(m\_url)
####功能：
调用接口进行音频下载转码，并调用下一个音频分割的方法
####输入：
m\_url: m3u8地址
####调用：
getRecognizedResult(file\_name)
###getRecognizedResult(file\_name)
####功能：
调用接口进行音频分割
####输入：
file\_name: wav文件名
####调用：
@app.route('/audio\_recognize', methods=\['GET'])
createResultTable (rec\_result, duration)
####输出：
页面显示播放器
###createResultTable (rec\_result, duration)
####功能：
生成音频切割结果的表格
####输入：
rec\_result: 识别结果
duration: 音频时长
####调用：
formatSeconds(value)
####输出：
页面显示识别结果与button 语音转文字，点击可调用getTextResult()方法，点击识别结果中的‘语音’／‘音乐’可调用playFromTo()方法
###getTextResult()
####功能：
获取所有语音转文字的结果
####调用：
@app.route('/audio\_to\_text', methods=\['GET'])
####输出：
页面显示转文字结果
###formatSeconds(value)
####功能：
格式化时间
####输入：
value: 秒数
####输出：
String：将秒数格式化为HH:mm:ss的格式
###playFromTo(stt, edt):
####功能：
使播放器从开始时间开始播放到结束时间自动停止
####输入：
stt: 开始时间
edt: 结束时间
##/data/ml\_project/music\_voice/js/search.js
###search()
####功能
获取搜索结果
####输入
无
####输出
页面表格包含有名称内容与播放器
###highLight(s)
####功能
高亮显示关键词
####输入
s: 关键词
####输出
表格内容列关键词显示红色加粗效果
