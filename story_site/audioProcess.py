import os
import re
import utilities
import shutil

from subprocess import STDOUT, check_output, CalledProcessError

# TMP_DIR_PATH = "/Users/jonathaneidelman/Dropbox/dev_projects/story_share/storage/tmp/"
# TEST_PATH = "/Users/jonathaneidelman/Dropbox/dev_projects/story_share/story_share/story_site/audio_test/"

### Checks if the file at filePath is an audio file. If it is, it returns format of the audiofile.
### if the file at filePath is not an audio file, we return None
def check_file_format(filePath):
    try:
        output = check_output(["ffprobe", filePath], stderr=STDOUT)
    except CalledProcessError:
        return None

    matchObj = re.search(r'Input #0, ', output, re.M|re.I)

    endIdx = matchObj.end()
    output = output[endIdx:]

    matchObj = re.search(r',', output)
    startIdx = matchObj.start()

    fileFormat = output[:startIdx]

    return fileFormat



### Takes a list of file paths to audio files (of the same format),
### and concatenates all of them into a new audio file at destinationPath
def concatenate_audio_files(fnameList, destinationPath, tmpDirPath):

    if not fnameList:
        return None

    elif len(fnameList) == 1:
        shutil.copy2(fnameList[0], destinationPath)
        return destinationPath

    concatWorkFilePath = os.path.join(tmpDirPath, utilities.id_generator(size=10))
    print concatWorkFilePath

    
    with open(concatWorkFilePath, "w") as workingFile:
        for fname in fnameList:
            workingFile.write("file '" + fname + "'\n")

    os.system('ffmpeg' + ' -f ' + ' concat ' + ' -i ' + concatWorkFilePath + ' -c ' + ' copy ' + destinationPath)
    os.remove(concatWorkFilePath)

    return destinationPath




# concatenate_audio_files([TEST_PATH+"test1.mp3", TEST_PATH+"test2.mp3", TEST_PATH+"test3.mp3"], TEST_PATH + "output_test.mp3")
