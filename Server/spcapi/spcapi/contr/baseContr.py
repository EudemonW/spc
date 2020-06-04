
import requests

class baseContro:
    # def __init__(self):
    #     self.mdb = dbcommon()
    #     pass

    def sendLost(self,data):
        url = 'http://172.18.23.154:9081/erp3/getExceptionInfo'
        requests.get(url=url, params=data)
