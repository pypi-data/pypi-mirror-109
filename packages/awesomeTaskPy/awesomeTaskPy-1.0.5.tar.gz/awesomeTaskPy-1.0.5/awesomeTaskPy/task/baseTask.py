import importlib
import context.context
import time


class baseTask():
    __taskInfo = None
    __loger = None
    __modulePath = None
    __startAt = None
    __startAtTime = None

    def __now(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __nowInt(self):
        return int(time.time())

    def __init__(self, taskInfo, modulePath):
        self.__taskInfo = taskInfo
        self.__modulePath = modulePath
        self.__startAt = self.__now()
        self.__startAtTime = self.__nowInt()
        try:
            res = self.__run()
            output = {
                "startAt": self.__startAt,
                "endAt": self.__now(),
                "runTime": self.__nowInt() - self.__startAtTime,
                "result": res,
                "error":None
            }
            # 回调返回值并且情况缓冲的日志
            context.context.getContext().getLoger().writeRes(output).flushTmpLog()
        except Exception as e:
            output = {
                "startAt": self.__startAt,
                "endAt": self.__now(),
                "runTime": self.__nowInt() - self.__startAtTime,
                "result": None,
                "error": e
            }
            # 回调返回值并且情况缓冲的日志
            context.context.getContext().getLoger().writeRes(output).flushTmpLog()
    def log(self, message):
        return context.context.getContext().getLoger().write(message)

    # 具体的代码实现逻辑
    def __run(self):
        input = self.__taskInfo['input']
        res = importlib.import_module(self.__modulePath).run(*input)
        return res
