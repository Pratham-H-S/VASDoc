import redis
import time


connection=redis.Redis('127.0.0.1',6379,)
subscriber=connection.pubsub()
subscriber.subscribe(["pratham1"])
for message in subscriber.listen():
        time.sleep(3)
        print(message,type(message))