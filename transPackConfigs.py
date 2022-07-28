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