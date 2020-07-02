import os
import time

from django.core import serializers
from django.http import HttpResponse
from spcapi.model.dbcommon import dbcommon
from spcapi.model.spcSource import spcSource
import json
import threading
from spcapi.model.dataProcess import dataCompute, dataProcess
from spcapi.model.spc import create
from dwebsocket.decorators import accept_websocket
from spcapi.contr.baseContr import baseContr

from spcapi.utils.redisUtil import redisUtil


class api():
    def __init__(self):
        self.mdb = dbcommon()

        pass

    def saveOriLost(request):
        try:
            spcSource().saveOri(request.GET)
            t = threading.Thread(target=dataCompute)
            t.start()
            return baseContr.ok("save ok")
        except Exception as ex:
            print(ex)
            return baseContr.error("save failure")

    def saveUpdLost(request):
        try:
            spcSource().saveUpd(request.GET)
            # t = threading.Thread(target=dataCompute)
            # t.start()
            return baseContr.ok("update ok")
        except Exception as ex:
            print(ex)
            return baseContr.error("update failure")

    @accept_websocket
    def getDevice(request):
        if request.is_websocket():
            # print(request.websocket)
            # print("==============================")
            for message in request.websocket:
                print(isinstance(message, ))
                message = message.decode()
                # print(message)
                while True:
                    # no = str(request.GET["no"])
                    no = message
                    print(no)
                    result = {}
                    jsonData = []
                    jsonData = redisUtil().getValue(no)
                    if jsonData !=None:
                        result["success"] = True
                        result["data"] = jsonData
                        print(result)
                    else:
                        df = spcSource().getList(no)
                        if (df.shape[0] == 0):
                            result["success"] = False
                            result["msg"] = "输入编号有误，请重新输入"
                        else:
                            dlist = create(df, no)
                            data = []
                            data_r = dataProcess(dlist, 'R', 'R', 'R_UCL', 'R_LCL', 'R_center')
                            data_x = dataProcess(dlist, 'X', 'change_val', 'UCL', 'LCL', 'center')
                            data.append(data_r)
                            data.append(data_x)
                            jsonData = json.dumps(data)
                            redisUtil().setValue(no, jsonData)
                            result["success"] = True
                            result["data"] = jsonData
                    data = json.dumps(result)
                    result = data.encode('utf-8')
                    request.websocket.send(result)
                    # 检查一次
                    time.sleep(600)
        else:
            return HttpResponse('wrong request')






