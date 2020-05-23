from spcapi.model.dbcommon import dbcommon
import requests

class baseContro:
    def __init__(self):
        self.mdb = dbcommon()
        pass

    def sendLost(self):
        url = ''
        data = {
        }
        requests.post(url=url, data=data)