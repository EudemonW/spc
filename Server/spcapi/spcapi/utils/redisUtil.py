from redis import StrictRedis

class redisUtil:


    def __init__(self):
        self.redis = StrictRedis(host='localhost', port=6379, db=0)

    def setValue(self,key,value):
        self.redis.set(key, value)

    def getValue(self,key):
        result = self.redis.get(key)
        if(result==None):
            return result;
        return self.redis.get(key).decode()

    def getDbSize(self):
        return self.redis.dbsize()

    def updateAndReturn(self,key,value):
        return self.redis.getset(key,value)

    def delete(self,key):
        return self.redis.delete(key)
