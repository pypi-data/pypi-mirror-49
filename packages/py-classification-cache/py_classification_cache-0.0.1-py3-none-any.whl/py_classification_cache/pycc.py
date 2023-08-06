from pypinyin import pinyin, lazy_pinyin, Style
import pickle
import re
import time
import os

class PCC():
    def __init__(self,cache_dir = '.ch_cache'):
        self.CACHE_DIR = cache_dir
        self.__checkCacheDir()
    
    def __checkCacheDir(self):
        if(not os.path.isdir(self.CACHE_DIR)):
            os.mkdir(self.CACHE_DIR)
            with open(self.CACHE_DIR+'/.gitignore', 'w', encoding='utf-8') as f:
                f.write("*\n!.gitignore\n")
    
    def __parseHead(self,key):
        parseResult = pinyin(key, style=Style.INITIALS, strict=False)
        parseResultHead = parseResult[0][0]
        parseResultHead = re.sub(r"[^A-Za-z|0-9]+", '', parseResultHead) #僅保留英文與數字
        if(len(parseResultHead)>1): #只取頭
            parseResultHead = parseResultHead[0]
        if(parseResultHead == ''):
            parseResultHead = '_others'
        else:
            pass
        return parseResultHead
    
    def remove(self, key):
        CACHE_DIR = self.CACHE_DIR
        parseResultHead = self.__parseHead(key)
        key = key + '.pkl'        
        try:
            os.remove(CACHE_DIR + '/' + parseResultHead + '/' + key)    
        except:
            pass

    def clearCache(self):
        top = self.CACHE_DIR
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                if name in ['.gitignore']: #file name white list
                    continue
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def save(self, key, data):
        CACHE_DIR = self.CACHE_DIR        
        parseResultHead = self.__parseHead(key)
        # 檢查資料夾存在
        if(not os.path.isdir(CACHE_DIR + '/' + parseResultHead)):
            os.mkdir(CACHE_DIR + '/' + parseResultHead)
        
        #
        key = key + '.pkl'
        with open(CACHE_DIR + '/' + parseResultHead + '/' + key , 'wb') as f:
            pickle.dump(data,f)
    
    def get(self, key):
        key = key + '.pkl'
        subDir = self.__parseHead(key)
        CACHE_DIR = self.CACHE_DIR
        try:
            with open(CACHE_DIR + '/' + subDir + '/' + key, 'rb') as f:
                data = pickle.load(f)
            return data
        except:
            return None