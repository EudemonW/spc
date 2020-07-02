import json

import requests
from django.http import HttpResponse


class baseContr:
    # def __init__(self):
    #     self.mdb = dbcommon()
    #     pass

    def sendLost(self,data):
        url = 'http://172.18.23.154:9081/erp3/getExceptionInfo'
        requests.get(url=url, params=data)

    def response(code=0, msg=""):
        return HttpResponse(json.dumps({"code": code, "msg": msg}))

    def error(msg=""):
        return baseContr.response(code=1, msg=msg)

    def ok(msg=""):
        return baseContr.response(code=0, msg=msg)

