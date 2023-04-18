import redis
import time

def connect():
        connection=redis.Redis('127.0.0.1',6379,decode_responses=True)
        subscriber=connection.pubsub()
        subscriber.subscribe("pratham")
        for message in subscriber.listen():
                yield message
      
# connect()
