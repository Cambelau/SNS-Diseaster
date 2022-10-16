import tweepy
import data.env as env

client = tweepy.Client(bearer_token=env.bearer_token_academic)

# Replace with your own search query
query = 'Apple -is:retweet lang:en'
i=0
# Replace the limit=1000 with the maximum number of Tweets you want
for tweet in tweepy.Paginator(  client.search_recent_tweets, query=query,
                                start_time = '2022-07-28T23:00:01Z',
                                end_time = '2022-08-05T00:00:01Z',
                                tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=101):
    i+=1
    print(tweet.id)
print(i)