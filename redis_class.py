import redis

class Redis:
    def __init__(self,host,port,id):
        self.host=host
        self.port=port
        self.id=id
        self.connection=redis.Redis(host=self.host,port=self.port,decode_responses=True)

class RedisPublish(Redis):
    def __init__(self,host,port,id):
        super().__init__(host,port,id)
    def Redis_publish(self,message):
        self.connection.publish(self.id,message)

class RedisSubscribe(Redis):
    def __init__(self,host,port,id):
        super().__init__(host,port,id)

    def Redis_subscribe(self):
        subscriber=self.connection.pubsub()
        subscriber.subscribe(self.id)
        return subscriber.listen()
