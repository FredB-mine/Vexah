import time
from hashlib import md5
from json import loads
from random import randint
from parse import compile
from typing import Any
from loguru import logger

from requests_html import HTMLSession
from ttkbootstrap import *
import warnings
warnings.filterwarnings("ignore")

class Configs:
    __name__ = "Configs"
    class logConfigs:
        needConsoleOutPut   = False
        needFileOutPut      = True
        loglevel            = "DEBUG"
        fileName            = "translateLog.log"
        fileEncoding        = "utf-8"

    class timeConfigs:
        timeFormat          = "%Y-%m-%d [%H:%M:%S] "
        timeZone            = "Asia/Shanghai"

    class SSHConfigs:
        host                = "192.168.31.100"
        port                = "22"
        username            = "root"
        password            = "20091126"

class Main:
    global to_translate_text
    global translated_result
    global fileRoute
    translated_result = str()
    def getNowTime() -> str:
        return time.strftime(
            Configs.timeConfigs.timeFormat, time.localtime()
        )

    def writeLog(self, data: Any, logType:str = "INFO") -> None:
        logObject = open(
            Configs.logConfigs.fileName, "a" ,
            encoding = Configs.logConfigs.fileEncoding
        )
        funcMap = {
            "INFO":     logger.info,
            "DEBUG":    logger.debug,
            "ERROR":    logger.error,
            "CRITICAL": logger.critical,
            "WARNING":  logger.warning,
            "SUCCESS":  logger.success,
            "TRACE":    logger.trace
        }
        toUseFunc  = funcMap[logType]
        listTypeEg = type([])
        strTypeEg  = type('')
        if type(data) == listTypeEg: 
            for item in data:
                item = item.replace("\n", "")
                if (Configs.logConfigs.needFileOutPut):
                    logObject.write(
                        Main.getNowTime() + str(item) + '\n'
                    )
                if (Configs.logConfigs.needConsoleOutPut):
                    toUseFunc(str(item))
            logObject.close()
            return

        if type(data) == strTypeEg:
            data = data.replace("\n", "")
            if (Configs.logConfigs.needFileOutPut):
                logObject.write(Main.getNowTime() + data + '\n')
            if (Configs.logConfigs.needConsoleOutPut):
                toUseFunc(data)
            logObject.close()
            return

        else:
            logObject.close()
            Main.writeLog(Main,"Error: logType is not supported", "ERROR")
            raise TypeError("Data type not supported")

    sep = '-----------------------------------------------------'

    @ logger.catch(level="WARNING")
    def translate(self, to_translate_text, from_language, to_language) -> str:
        '''
            调用百度翻译API的翻译函数
            param: args: 回调参数
            return: None
        '''
        # 初始化为合成url需要的参数
        q        = to_translate_text
        _from    = self.lang_map[from_language]
        _to      = self.lang_map[to_language]
        appid    = '20220602001236448'
        key      = 'GtVUOpsUvCgfxjXsQ1iC'
        salt     = randint(1, 65536)
        sign     = appid + q + str(salt) + key
        sign     = md5(sign.encode('utf-8')).hexdigest()
        Outputs  = (
            "就不告诉你|" + q + str(salt) + "|就不告诉你"
        )
        finalUrl = (
            'http://api.fanyi.baidu.com/api/trans/vip/translate' +\
            '?q='     + to_translate_text +\
            '&from='  + _from             +\
            '&to='    + _to               +\
            '&appid=' + appid             +\
            '&salt='  + str(salt)         +\
            '&sign='  + sign              
        )
        if q == "": #特判为空的情况
            self.writeLog("输入为空,正在退出")
            self.writeLog(self.sep)
            return
        # 输出日志
        self.writeLog("起始语言 %s"              % _from)
        self.writeLog("目标语言 %s"              % _to)
        self.writeLog("Dr.Alfred注册的appid: %s" % "就不告诉你")
        self.writeLog("Dr.Alfred注册的key: %s"   % "就不告诉你")
        self.writeLog("随机数: %s"               % salt)
        self.writeLog("求得的数字签名: %s"        % Outputs)
        self.writeLog("MD5加密后的数字签名: %s"   % sign)
        self.writeLog("最终调用api的url: %s"     % finalUrl)
        # 初始化实例对象
        Session = HTMLSession()
        # 请求头
        request_header = {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/102.0.5005.63 Safari/537.36"
            ),
            "content-type": "text/html; charset=UTF-8"
        }
        # 请求api(GET)
        json_text = Session.get(
            finalUrl, headers = request_header
        ).html.text
        # 解析json
        self.writeLog("获取到的json数据: %s" % json_text)
        json_text = loads(json_text)
        try:
            translated_result = json_text['trans_result'][0]['dst']
        except Exception:
            self.writeLog("使用频率过高")
            return
        self.writeLog("翻译结果: %s" % translated_result)
        # 展示结果
        self.writeLog(self.sep)
        return translated_result

    @ classmethod
    def initLangMap(self) -> None:
        '''
            初始化语言映射表
            param: None
            return: None
        '''
        self.lang_map = {}
        self.lang_map['自动检测'] = 'auto'
        self.lang_map['中文'] = 'zh'
        self.lang_map['英语'] = 'en'
        self.lang_map['粤语'] = 'yue'
        self.lang_map['文言文'] = 'wyw'
        self.lang_map['日语'] = 'jp'
        self.lang_map['韩语'] = 'kor'
        self.lang_map['法语'] = 'fra'
        self.lang_map['西班牙语'] = 'spa'
        self.lang_map['泰语'] = 'th'
        self.lang_map['阿拉伯语'] = 'ara'
        self.lang_map['俄语'] = 'ru'
        self.lang_map['葡萄牙语'] = 'pt'
        self.lang_map['德语'] = 'de'
        self.lang_map['意大利语'] = 'it'
        self.lang_map['希腊语'] = 'el'
        self.lang_map['荷兰语'] = 'nl'
        self.lang_map['波兰语'] = 'pl'
        self.lang_map['保加利亚语'] = 'bul'
        self.lang_map['爱沙尼亚语'] = 'est'
        self.lang_map['丹麦语'] = 'dan'
        self.lang_map['芬兰语'] = 'fin'
        self.lang_map['捷克语'] = 'cs'
        self.lang_map['罗马尼亚语'] = 'rom'
        self.lang_map['斯洛文尼亚语'] = 'slo'
        self.lang_map['瑞典语'] = 'swe'
        self.lang_map['匈牙利语'] = 'hu'
        self.lang_map['繁体中文'] = 'cht'
        self.lang_map['越南语'] = 'vie'

    @ classmethod
    def getNowTime(self) -> str:
        ''' 
            获取当前时间. 
            param: None
            return: str
        '''
        return time.strftime("%Y-%m-%d [%H:%M:%S] ", time.localtime())

    def __init__(self) -> None:
        self.initLangMap()
        pass
    

if __name__ == '__main__':
    cls = Main()   
    fileName = input("请输入文件名: ")
    file = open(fileName, "r", encoding="shift-jis")
    rs = compile("{}; {}")
    rs2 = compile("; {}")
    printCache = []
    for line in file.readlines():
        result = rs.parse(line)
        result2 = rs2.parse(line)
        if (result is not None):
            tp = result[0]+'; '+cls.translate(result[1],"自动检测","中文")
            printCache.append(tp + '\n')
            print(tp)
            time.sleep(2)
        elif (result2 is not None):
            tp = '; '+cls.translate(result2[0],"自动检测","中文")
            printCache.append(tp + '\n')
            print(tp)
            time.sleep(2)
        else:
            printCache.append(line)
            print(line,end = "")    
    file.close()
    save = input("是否保存结果? (y/n) ")
    if save != 'N' and save != 'n':
        fileName = input("请输入文件名: ")
        file = open(fileName,'w',encoding='utf-8')
        file.writelines(printCache)
        file.close()
    else:
        exit()
