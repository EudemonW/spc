from datetime import datetime

import pandas as pd

from Server.spcapi.spcapi.contr.baseContr import baseContro


def dataProcess(dlist,R_X,value):
    # 取出X
    # df = pd.DataFrame(dlist[0][temp])
    temp_all = []
    for ite in dlist:
        df = ite[R_X]
        df1 = []
        for item in df.itertuples():
            temp1 = {}
            temp1['y'] = getattr(item, value)
            temp1['color'] = getattr(item, 'color')
            temp1['name'] = getattr(item, 'name')
            temp1['method'] = getattr(item, 'method')
            df1.append(temp1)
        df2 = df['timestamp'].values
        df2 = df2.tolist()
        temp = {}
        temp['y'] = df1
        temp['x'] = df2
        temp['UCL'] = ite['UCL']
        temp['LCL'] = ite['LCL']
        temp['center'] = ite['center']
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
        }
        print(data)
        baseContro().sendLost(data)

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