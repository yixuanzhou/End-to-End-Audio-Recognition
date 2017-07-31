from pyAudioAnalysis import audioSegmentation as aS
[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("./audiofiles/c3_0629.wav", "./knnMusicGenre2", "knn", False, './audiofiles/c3_0629.segments')
