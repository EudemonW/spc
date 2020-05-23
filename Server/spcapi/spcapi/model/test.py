# import json
#
# from spcapi.model.dataProcess import dataProcess
# from spcapi.model.spctest import create
import datetime
import time

from spcapi.model.spcSource import spcSource
#
# df = spcSource().getList(10001)
# dlist = create(df, 10001)
# data = {}
# data_x = dataProcess(dlist,'R','R')
# data_r = dataProcess(dlist, 'X', 'change_val')
# data['x'] = data_x
# data['r'] = data_r
# jsonData = json.dumps(data)
# print(jsonData)


# data={}
# data['process_person'] = '陈卓'
# data['process_procedure'] = '别'
# data['process_time'] = datetime.datetime.now().timestamp()
# print(data['process_time'])
# data['device_no'] = '10001'
# tss1 = '2020-05-20 16:33:06'
# timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)
# data['timestamp'] = timeStamp
# spcSource().saveUpd(data)

list = spcSource().getNameAndMethod(10001,'A')
print(list['process_person'].values)