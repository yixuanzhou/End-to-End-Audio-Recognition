def audiofilter(flagsInd, classnum):
	'''Filtering the audio signal'''
	window_size = 8
	i = 0
	step, result = [], []
	length = len(flagsInd)
	classn = [0] * classnum
	while i < length / window_size:
		window = flagsInd[i*window_size:(i+1)*window_size]
		for flag in window:
			class6[int(flag)] += 1
		v = class6.index(max(classn))
		result += [v] * window_size
		step += [v]
		classn = [0] * classnum
		i += 1	
	return step, result


def array2list(flag):
    r = flag.tolist()
    return r


def read_seg_points(audio_step, window_size):
    time_steps, seg_points = [], []
    flag = audio_step[0]
    count = 1
    max_step = 7
    time_stamp = 0
    for i in range(1,len(audio_step)):
        if audio_step[i] == flag and count < max_step:
            count += 1
        else:		
            time_steps.append([time_stamp,time_stamp+window_size*count, flag])
            flag = audio_step[i]
            time_stamp += window_size * count		
            count = 1
    time_steps.append([time_stamp,time_stamp+window_size*count, flag])
    return time_steps
    '''for step in time_steps:
        if step[0] == 1:
            seg_points.append(step[1:])
    return seg_points'''


def read_segment_points(audio_step, window_size):
    seg_points = []
    for index, step in enumerate(audio_step):
        if step == 1:
            seg_points.append([index * window_size, (index + 1) * window_size - 1])
    return seg_points

# flag = '0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1'
# audio_step0, _ = audio_filter(str2list(flag))
# print read_segment_points(audio_step0, 8)
