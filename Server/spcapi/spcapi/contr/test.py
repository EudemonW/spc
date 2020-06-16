import json

from Server.spcapi.spcapi.model.dataProcess import dataProcess
from Server.spcapi.spcapi.model.spcSource import spcSource
from Server.spcapi.spcapi.model.spctest import create

no = 100
df = spcSource().getList(no)
# print(df)
print(df.shape[0])