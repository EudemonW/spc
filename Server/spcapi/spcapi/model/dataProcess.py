import json
from datetime import datetime

import pandas as pd

from spcapi.contr.baseContr import baseContr

from spcapi.model.spcSource import spcSource
from spcapi.model.spc import create

from spcapi.utils.redisUtil import redisUtil

def judgeIn(temp1,item):
    temp1['color'] = getattr(item, 'color')
    temp1['part_no'] = getattr(item, 'part_no')
    temp1['lot_no'] = getattr(item, 'lot_no')
    temp1['theory_val'] = getattr(item, 'theory_val')
    temp1['p_left'] = getattr(item, 'p_left')
    temp1['measured_val'] = getattr(item, 'measured_val')
    temp1['oper_id'] = getattr(item, 'oper_id')
    temp1['work_name'] = getattr(item, 'work_name')
    temp1['measure_time'] = getattr(item, 'measure_time')
    temp1['z_compensate'] = getattr(item, 'z_compensate')
    temp1['manufacturer'] = getattr(item, 'manufacturer')
    temp1['part_no_number'] = getattr(item, 'part_no_number')
    temp1['spec_no'] = getattr(item, 'spec_no')
    temp1['tech_oper'] = getattr(item, 'tech_oper')
    temp1['op_no'] = getattr(item, 'op_no')
    temp1['gcd'] = getattr(item, 'gcd')
    temp1['material'] = getattr(item, 'material')
    temp1['x_r'] = getattr(item, 'x_r')
def dataProcess(dlist,R_X,value,ucl,lcl,center):
    # 取出X
    # df = pd.DataFrame(dlist[0][temp])
    temp_all = []
    for ite in dlist:
        df = ite[R_X]
        df1 = []
        for item in df.itertuples():
            temp1 = {}
            # df2=[]
            temp1['x'] = getattr(item, 'measure_time')
            temp1['y'] = getattr(item, value)
            if 'type' in list(df.columns):
                temp1['type'] = getattr(item, 'type')
                temp1['name'] = getattr(item, 'name')
                temp1['method'] = getattr(item, 'method')
                temp1['process_time'] = getattr(item, 'process_time')
                judgeIn(temp1,item)
                df1.append(temp1)
            else:
                judgeIn(temp1,item)
                df1.append(temp1)
            # df2.append(getattr(item, value))
            # df2.append(getattr(item, 'timestamp'))

            # df2.append(temp1)
            # df1.append(df2)
        # df2 = df['timestamp'].values*1000
        # df2 = df2.tolist()
        temp = {}
        temp['data'] = df1
        # temp['x'] = df2
        if ite[ucl] != None:
            temp['UCL'] = ite[ucl]
            temp['LCL'] = ite[lcl]
            temp['center'] = ite[center]
        temp['size'] = ite['size_type']
        temp_all.append(temp)
    return temp_all

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
            'x_r':row['x_r']
        }
        # print(data)
        baseContr.sendLost(data)

def sendBack(dlist):
    for item in dlist:
        df_x = pd.DataFrame(item['X'])
        df_r = pd.DataFrame(item['R'])
        df_x_back = df_x[(df_x['prob1'] == 1) | (df_x['prob2'] == 1) | (df_x['prob3'] == 1) | (df_x['prob4'] == 1) | (
                df_x['prob5'] == 1) | (df_x['prob6'] == 1) | (df_x['prob7'] == 1) | (df_x['prob8'] == 1)]
        df_r_back = df_r[(df_r['prob1'] == 1) | (df_r['prob2'] == 1) | (df_r['prob3'] == 1) | (df_r['prob4'] == 1) | (
                df_r['prob5'] == 1) | (df_r['prob6'] == 1) | (df_r['prob7'] == 1) | (df_r['prob8'] == 1)]
        df_r_x_back = df_x_back[df_x_back['id']==df_r_back['id']]
        df_x_back['x_r'] = 0
        df_r_back['x_r'] = 1
        df_r_x_back['x_r'] = 2
        send(df_x_back)
        send(df_r_back)
        send(df_r_x_back)

def dataCompute():
    no = spcSource().getDeviceNo()
    for index, row in no.iterrows():
        df = spcSource().getList(row['device_no'])
        dlist = create(df, row['device_no'])
        data = []
        data_r = dataProcess(dlist, 'R', 'R', 'R_UCL', 'R_LCL', 'R_center')
        data_x = dataProcess(dlist, 'X', 'change_val', 'UCL', 'LCL', 'center')
        data.append(data_r)
        data.append(data_x)
        jsonData = json.dumps(data)
        redisUtil().setValue(no,jsonData)
        sendBack(dlist)