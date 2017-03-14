from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from model.authentication import *
from config.options import *

import pickle
import json
import redis


class TurkishTweetsListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def on_data(self, data):
        tweet = json.loads(data)

        if ('id' in tweet) and ('text' in tweet):
            # if ('retweeted' in tweet) and (tweet['retweeted'] is True):
            #    pass
            # elif tweet['text'].startswith('RT @') is False:
            # print("%s : %s" % (tweet['id'], tweet['text']))
            # self.tr_tweets.insert_one(tweet)
            self.redis_client.publish(TR_TWEETS_CHANNEL, data)

        return True

    def on_error(self, status):
        print(status)

    def on_limit(self, track):
        """Prints any limit notice to the console but doesn't halt.
        Limit notices indicate that additional tweets matched a filter,
        however they were above an artificial limit placed on the stream
        and were not sent. The value of 'track' indicates how many tweets
        in total matched the filter but were not sent since the stream
        was opened.
        """
        print(track)


def start():
    most_used_words = pickle.load(open(MOST_USED_WORDS_DB, "rb"))
    most_used_400_words = [".", ",", "?", "!", ";"] + most_used_words[:395]

    # This handles Twitter authetification and the connection to Twitter Streaming API
    accounts = get_accounts()
    index = 1
    while True:
        try:
            auth = OAuthHandler(accounts[index].consumer_key, accounts[index].consumer_secret)
            auth.set_access_token(accounts[index].access_token, accounts[index].access_token_secret)
            listener = TurkishTweetsListener()
            stream = Stream(auth, listener)
            if STREAMING_MODE == "track":
                stream.filter(track=most_used_400_words, languages=["tr"])
            elif STREAMING_MODE == "follow":
                stream.filter(follow=FOLLOWING)
            elif STREAMING_MODE == "mixed":
                stream.filter(track=most_used_400_words, follow=FOLLOWING)
            else:
                print("STREAMING MODE track ya da folllow olabilir.")
                break
        except KeyboardInterrupt:
            stream.disconnect()
            break
        except Exception as e:
            print(e)
            index += 1
            index %= len(accounts)
            # switch alternative account
            continue


if __name__ == '__main__':
    start()
