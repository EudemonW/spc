# import json
#
# from spcapi.model.dataProcess import dataProcess
# from spcapi.model.spctest import create
import datetime
import time

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

# list = spcSource().getNameAndMethod(10001,'A')
# print(list['process_person'].values)
# from Server.spcapi.spcapi.model.dataProcess import dataProcess
# from Server.spcapi.spcapi.model.spcSource import spcSource
# from Server.spcapi.spcapi.model.spctest import create
#
from Server.spcapi.spcapi.contr.baseContr import baseContro
from Server.spcapi.spcapi.model.dataProcess import dataProcess
from Server.spcapi.spcapi.model.spcSource import spcSource
from Server.spcapi.spcapi.model.spctest import create, get_data
import pandas as pd
from datetime import datetime

def send(df):
    for index,row in df.iterrows():
        data = {
            "device_no": row["device_no"],
            "size_type": row["size_type"],
            "change_val": row["change_val"],
            "control_up": row["control_up"],
            "control_down": row["control_down"],
            "control_center": row["control_center"],
            "timestamp": datetime.strptime(row["timestamp"], '%Y-%m-%d %H:%M:%S').timestamp(),
            "r_control_up": row["r_contro_up"],
            "r_control_down": row["r_contro_down"],
            "r_control_center": row["r_contro_center"],
            "pro1": row["prob1"],
            "pro2": row["prob2"],
            "pro3": row["prob3"],
            "pro4": row["prob4"],
            "pro5": row["prob5"],
            "pro6": row["prob6"],
            "pro7": row["prob7"],
            "pro8": row["prob8"],
        }
        print(data)
        baseContro().sendLost(data)
df = spcSource().getList(10001)
dlist = create(df, 10001)
def sendBack(dlist):
    for item in dlist:
        df_x = pd.DataFrame(item['X'])
        df_r = pd.DataFrame(item['R'])
        df_x_back = df_x[(df_x['prob1'] == 1) | (df_x['prob2'] == 1) | (df_x['prob3'] == 1) | (df_x['prob4'] == 1) | (
                df_x['prob5'] == 1) | (df_x['prob6'] == 1) | (df_x['prob7'] == 1) | (df_x['prob8'] == 1)]
        df_r_back = df_r[(df_r['prob1'] == 1) | (df_r['prob2'] == 1) | (df_r['prob3'] == 1) | (df_r['prob4'] == 1) | (
                df_r['prob5'] == 1) | (df_r['prob6'] == 1) | (df_r['prob7'] == 1) | (df_r['prob8'] == 1)]
        send(df_x_back)
        send(df_r_back)
    # print(df_x_back)
# data_x = dataProcess(dlist, 'R', 'R')
# print(data_x)
# from Server.spcapi.spcapi.contr.baseContr import baseContro
#
# baseContro().sendLost()
