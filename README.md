# End-to-End-Audio-Recognition
The web has been deployed on `121.40.161.184`, one can directly access on [http://121.40.161.184:8484/music_voice.html](http://121.40.161.184:8484/music_voice.html)(for audio to text translate) and [http://121.40.161.184:8484/search.html](http://121.40.161.184:8484/search.html)(for search in database through keyword).

## Dependencies
- Python 2.x
- HBase
- For downloading m3u8 audio stream and convert to wav files:
    - [FFmpeg](http://ffmpeg.org/)
- For audio classification and segmentation tasks:
    - [PyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis)
- For segmenting an audio file (wav) into pieces:
    - [Pydub](https://github.com/jiaaro/pydub)
- For audio recognition and translate to text:
    - [Baidu speech recognition API](http://yuyin.baidu.com/asr)

## Workflow
1. Prepare audio files for training model (`train-model.py`)
1. Use pre-trained model to classify targeted audio segments (`audio-classifier.py`)
1. Filter to get optimized the audio segments (`audio_filter.py`)
1. Segment an audio file into pieces according to segment points (`audio-segmenter.py`)
1. For each audio segment, do audio to text translation (`audio_recognition.py`)
1. Save the result data in HBase (`pythrift.py`)

## Demo
![image](https://github.com/yixuanzhou/End-to-End-Audio-Recognition/raw/master/screenshots/audio2text.png)
![image](https://github.com/yixuanzhou/End-to-End-Audio-Recognition/raw/master/screenshots/search.png)