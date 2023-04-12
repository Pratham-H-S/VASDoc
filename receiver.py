import redis
import time


connection=redis.Redis('127.0.0.1',6379,)
subscriber=connection.pubsub()
subscriber.subscribe(["pratham"])
for message in subscriber.listen():
        
        print(message,type(message))