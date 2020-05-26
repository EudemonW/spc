import json

from Server.spcapi.spcapi.model.spcSource import spcSource

import pandas as pd
# df = spcSource().getList(10001)
# dlist = create(df, 10001)
# df = dlist[0]['R']
# data = []
# for item in df.itertuples():
#     temp = {}
#     temp['y'] = getattr(item, 'R')
#     temp['color'] = getattr(item, 'color')
#     data.append(temp)
# print(data)
list = spcSource().getDeviceNo()
print(list)
