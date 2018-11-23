#! /usr/bin/python
# -*- coding: utf-8 -*-

# -*- author: lianxue.aho -*-

import os
import os.path
import pickle


def pngquantPicture(file):
    
    os.system("pngquant -f --ext .png --quality 50-80 \"" + file + "\"")
    filesize = os.path.getsize(file)
    dict = {file: filesize}
#    print dict
    return dict;


def dumpStorageImageInfo(imageInfoList):
    
    output = open('storageImageInfo.pkl','wb')
    pickle.dump(imageInfoList, output)
#    print imageInfoList
    output.close()


def loadStorageImageInfo():
    
    if os.path.isfile('storageImageInfo.pkl'):
       pkl_file = open('storageImageInfo.pkl', 'rb')
       imageInfoListStorage = pickle.load(pkl_file)
#       print imageInfoListStorage
       pkl_file.close()
       return imageInfoListStorage


def compareFileSize(imageInfoListStorage, file):
    
    oldImage = 0
    for index, imageInfoDict in enumerate(imageInfoListStorage):
        if file in imageInfoDict:
           oldImage = 1
           fileSizeOld = imageInfoDict[file]
           fileSizeNew = os.path.getsize(file)
           if fileSizeOld == fileSizeNew:
#              print 'image size equal to'
              return
           elif fileSizeOld < fileSizeNew:
              dict = pngquantPicture(file)
              imageInfoListStorage[index] = dict
              dumpStorageImageInfo(imageInfoListStorage)
#              print 'pngquant picture update storage'
              return
           elif fileSizeOld > fileSizeNew:
              imageInfoListStorage[index] = {file: fileSizeNew}
              dumpStorageImageInfo(imageInfoListStorage)
#              print 'update fileSize update storage'

    return oldImage



def compress(path):
    
    imageInfoList = []

    imageInfoListStorage = loadStorageImageInfo();

    for dir_path, dir_names, file_names in os.walk(path):
        file_names = filter(lambda file_name: file_name[-4:] == '.png', file_names)
        file_names = map(lambda file_name: os.path.join(dir_path, file_name), file_names)
        
        for file in file_names:
            print file
            if imageInfoListStorage:
               oldImage = compareFileSize(imageInfoListStorage, file)
#               print 'image are stored, not have to add picture'
               if oldImage == 0:
                  dict = pngquantPicture(file)
                  imageInfoListStorage.append(dict)
#                  print 'image are stored, have to add picture'
            else:
               dict = pngquantPicture(file)
               imageInfoList.append(dict)
#               print 'no image stored, have to add picure'

                
    if imageInfoListStorage:
       dumpStorageImageInfo(imageInfoListStorage)
#       print 'update storage picture'
    elif imageInfoList:
       dumpStorageImageInfo(imageInfoList)
#       print 'add storage picture'

if __name__ == '__main__':
    compress(os.getcwd())
