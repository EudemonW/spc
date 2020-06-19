import os

from django.core import serializers
from django.http import HttpResponse
from spcapi.model.dbcommon import dbcommon
from spcapi.model.spcSource import spcSource
import json
import threading
from Server.spcapi.spcapi.model.dataProcess import dataCompute, dataProcess
from Server.spcapi.spcapi.model.spctest import create


class api():
    def __init__(self):
        self.mdb = dbcommon()

        pass

    def saveOriLost(request):
        req = {}
        try:
            spcSource().saveOri(request.GET)
            t = threading.Thread(target=dataCompute)
            t.start()
            req["code"] = 0
            req["msg"] = "save ok"
        except Exception as ex:
            print(ex)
            req["code"] = False
            req["msg"] = "save failure"
        return HttpResponse(json.dumps(req))

    def saveUpdLost(request):
        req = {}
        try:
            spcSource().saveUpd(request.GET)
            req["code"] = 0
            req["msg"] = "update ok"
        except Exception as ex:
            print(ex)
            req["code"] = False
            req["msg"] = "save failure"
        return HttpResponse(json.dumps(req))

    def getDevice(request):
        no = str(request.GET["no"])
        print(no)
        result = {}
        jsonData = []
        try:
            path = r"../spcapi/static/device/{no}.txt".format(no=no)
            f = open(path, "r")
            jsonData = f.read()
            result["success"] = True
            result["data"] = jsonData
            print(result)
            f.close()
        except:
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
                f = open(r"../spcapi/static/device/{no}.txt".format(no=no), "w")
                f.write(jsonData)
                f.close()
                result["success"] = True
                result["data"] = jsonData
        return HttpResponse(json.dumps(result))
