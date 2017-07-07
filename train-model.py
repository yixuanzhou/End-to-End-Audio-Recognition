from pyAudioAnalysis import audioTrainTest as aT
#aT.featureAndTrain(["/home/yixuan/Documents/test/ad","/home/yixuan/Documents/test/speech"],1.0, 1.0,aT.shortTermWindow, aT.shortTermStep, "svm", "svmMusicGenre2", False)
aT.featureAndTrain(["/home/yixuan/Documents/ajim/ad","/home/yixuan/Documents/ajim/sp"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knnMusicGenre2", False)
#aT.featureAndTrain(["/home/yixuan/Documents/test/ad","/home/yixuan/Documents/test/speech"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "extratrees", "etMusicGenre2", False)
#aT.featureAndTrain(["/home/yixuan/Documents/test/ad","/home/yixuan/Documents/test/speech"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "gradientboosting", "gbMusicGenre2", False)
#aT.featureAndTrain(["/home/yixuan/Documents/test/ad","/home/yixuan/Documents/test/speech"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest", "rfMusicGenre2", False)