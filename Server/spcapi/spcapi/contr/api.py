import os

from django.http import HttpResponse

from spcapi.model.dataProcess import dataProcess
from spcapi.model.dbcommon import dbcommon
import pandas as pd
from spcapi.model.spcSource import spcSource
import json
import numpy as np

from spcapi.model.spctest import create

from Server.spcapi.spcapi.model.dataProcess import sendBack


class api():
    def __init__(self):
        self.mdb = dbcommon()


        pass

    def hello(request):
        no = 10001
        df = spcSource().getList(no)
        create(df,no)

    def saveOriLost(request):
        # spcSource().saveOri(request.GET)
        no = spcSource().getDeviceNo()
        for index, row in no.iterrows():
            df = spcSource().getList(row['device_no'])
            dlist = create(df, row['device_no'])
            sendBack(dlist)
        req = {}
        req["code"] = 0
        req["msg"] = "save ok"
        return HttpResponse(json.dumps(req))

    def saveUpdLost(request):
        spcSource().saveUpd(request.GET)
        req = {}
        req["code"] = 0
        req["msg"] = "update ok"
        return HttpResponse(json.dumps(req))


    def getDevice(request):
        no = request.GET["no"]
        print(no)
        df = spcSource().getList(no)
        dlist = create(df, no)
        data = []
        data_r = dataProcess(dlist, 'R', 'R')
        data_x = dataProcess(dlist, 'X', 'change_val')
        data.append(data_r)
        data.append(data_x)
        jsonData = json.dumps(data)
        # print(jsonData)
        return HttpResponse(jsonData)


    def img(request):
        no = request.GET["no"]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = base_dir+"/static/{no}.png".format(no=no)
        if os.path.exists(path):
            image_data = open(base_dir+"/static/{no}.png".format(no=no), "rb").read()
            return HttpResponse(image_data, content_type="image/png")
        return HttpResponse("can not find device")
