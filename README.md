# TwitterAnalyzer
Twitter Usertimeline Crawler and Streaming API usage by Tweepy for bypassing Rate Limit

**Streaming API**
* Access configuration should be done individually (config/auth.json)
* config/options.py parameters should be changed

**Most Used Words Database**
* most_used_tr_words.db is prepared by pickle.
* It is actually a list of words which are most commonly used in Turkish language.
* If you want to filter any language, you should prepare your own database.

**Usertimeline Crawler**
* This crawler is used for bypassing 3200 limit which is set by Twitter.
* Twitter only gives last 3200 tweets.

**NoSQL**
* In order to analyze tweets MongoDB is used as a document database
