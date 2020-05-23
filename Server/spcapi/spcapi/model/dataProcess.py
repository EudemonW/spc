import pandas as pd

def dataProcess(dlist,R_X,value):
    # 取出X
    # df = pd.DataFrame(dlist[0][temp])
    df1 = []
    df = dlist[0][R_X]
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
    temp['UCL'] = dlist[0]['UCL']
    temp['LCL'] = dlist[0]['LCL']
    temp['center'] = dlist[0]['center']
    return temp