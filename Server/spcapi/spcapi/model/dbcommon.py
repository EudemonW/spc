from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import sessionmaker
import pymysql
class dbcommon():
        def __init__(self):
            self.engine = create_engine('mysql+pymysql://root:root@localhost:3306/spc')
            self.engine.connect()
            self.session = sessionmaker(self.engine)()

        def readQuery(self, sql):
            return pd.read_sql_query(sql, self.engine)

        def execute(self, sql):
            self.session.execute(sql)
            return self.session.commit()
