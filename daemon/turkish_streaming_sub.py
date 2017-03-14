from model.authentication import *
from config.options import *

import json
import redis
import time

from pymongo import MongoClient


class RedisSubscribeListener(object):
    def __init__(self):
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client[MONGODB_DBNAME]
        self.tr_tweets = db.tr_tweets
        self.tr_tweets.delete_many({})

        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe([TR_TWEETS_CHANNEL])
        self.last_sec = 0
        self.counter = 0
        self.unique_counter = 0

    def run(self):
        for item in self.pubsub.listen():
            try:
                tweet = json.loads(item['data'].decode())
                start = int(time.time())
                print(tweet["id_str"]+" : "+tweet["text"])
                if self.last_sec == start:
                    self.counter += 1
                else:
                    self.counter = 1
                    self.unique_counter = 1
                    self.last_sec = start
                if self.redis_client.exists(tweet['id_str']):
                    pass
                else:
                    self.unique_counter += 1
                    self.redis_client.setex(tweet['id_str'], True, 60)
                    self.tr_tweets.insert_one(tweet)
                    # print("%s : %s" % (tweet['id'], tweet['text']))

            except Exception as e:
                print(e)
                pass


def start():
    while True:
        try:
            redis_client = RedisSubscribeListener()
            redis_client.run()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    start()
