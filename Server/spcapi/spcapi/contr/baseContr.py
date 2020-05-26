
import requests

class baseContro:
    # def __init__(self):
    #     self.mdb = dbcommon()
    #     pass

    def sendLost(self,data):
        url = 'http://127.0.0.1:8081/index/hello'
        requests.get(url=url, params=data)
