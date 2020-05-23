import json

from spcapi.model.spcSource import spcSource
from spcapi.model.spctest import get_data, create
import pandas as pd
df = spcSource().getList(10001)
dlist = create(df, 10001)
df = dlist[0]['R']
data = []
for item in df.itertuples():
    temp = {}
    temp['y'] = getattr(item, 'R')
    temp['color'] = getattr(item, 'color')
    data.append(temp)
print(data)
