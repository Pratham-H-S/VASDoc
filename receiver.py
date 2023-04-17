import redis
import time

def connect():
        connection=redis.Redis('127.0.0.1',6379,)
        subscriber=connection.pubsub()
        subscriber.subscribe(["pratham"])
        
        msg = []
        
        for message in subscriber.listen():
                msg.append(message)
                print(message,type(message))
                return msg
                
      
# connect()
