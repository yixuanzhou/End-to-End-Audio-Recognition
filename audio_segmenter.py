from pydub import AudioSegment
import logging
logging.basicConfig(level=logging.INFO)

def min2sec(minutes):
	time = minutes.split(':')	
	minute = int(time[0])
	second = int(time[1])
	return minute * 60 + second

def start2end(seg_points):
	result = []
	for seg_point in seg_points:
		start, end = min2sec(seg_point[0]), min2sec(seg_point[1])
		result.append([start, end])
	return result

seg_points0 = [[15, 50], [371, 600], [657, 900], [1121, 1365], 
              [1414, 1800], [2036, 2230], [2292, 2700], [2828, 3138]] # c21_0625 music segment points

seg_points1 = [[0, 14], [51, 370], [601, 656], [901, 1120], 
              [1366, 1413], [1801, 2035], [2231, 2291], [2701, 2827]] # c21_0625 speech segment points

seg_points2 = [[0,25],[320,569],[620,875],[1080,1330],[1398,1775],[1989,2264],[2295,2675],
			   [2838,3093],[3143,3570]] # c21_0624 music segment points

seg_points3 = [[25,320],[569,620],[875,1080],[1330,1398],[1775,1989],[2264,2295],
			   [2675,2838],[3093,3143],[3570,3600]] # c21_0624 speech segment points

seg_points4 = [[0,215],[915,1050],[1735,1968],[2705,2853],[3510,3599]] # c3_0626 ad

seg_points5 = [[215,915],[1050,1735],[1968,2705],[2853,3510]] # c3_0626 speech

seg_points6 = [[0,210],[895,1040],[1800,1955],[2692,2850],[3530,3600]] # c3_0627 ad

seg_points7 = [[210,895],[1040,1800],[1955,2692],[2850,3530]] # c3_0627 speech

seg_points8 = [[0,163],[902,1048],[1793,1980],[2687,2840],[3532,3600]] # c3_0628 ad

seg_points9 = [[163,902],[1048,1793],[1980,2687],[2840,3532]] # c3_0628 sp

seg_points10 = [[300,600]]


def audio_segment(audio_url, seg_points):
	logging.info("Loading file")
	# loading audio file
	audio = AudioSegment.from_wav(audio_url)
	# total length of the audio file
	duration = len(audio) / 1000
	count = 0
	logging.info("Audio duration: %s s" %(duration))
	for seg_point in seg_points:
		start, end = seg_point[0], seg_point[1]
		logging.info("Begin segmenting: from %s to %s" %(start, end))
		filename = "c3_0629_%s_%s.wav" % (start, end)
		#filename = "0629-%s.wav" %(count)
		filepath = './segs/'
		segmented_audio = audio[int(start * 1000): int(end * 1000)]
		segmented_audio.export(filepath + filename, format="wav")
		count += 1
	logging.info("Completed segmentation!")

#audio_segment('./audiofiles/c3_0629.wav', seg_points10)