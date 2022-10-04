import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
import psycopg2
from data.conn import connRailwayHost,connRailwayDatabase,connRailwayPort,connRailwayUser,connRailwayPassword

# Below are two ways of scraping using the Python Wrapper.
# Comment or uncomment as you need. If you currently run the script as is it will scrape both queries
# then output two different csv files.

# Query by username
# Setting variables to be used below
maxTweets = 2000000

# Creating list to append tweet data to
tweets_list1 = []
t0= time.time()

#insertion in database
def dbConnect(tweetid,username,isverified,followersCount,friendsCount,content,replyCount,retweetCount,likeCount,quoteCount,date):
    conn = psycopg2.connect(host=connRailwayHost,database=connRailwayDatabase,port=connRailwayPort,user=connRailwayUser,password=connRailwayPassword)
    cur = conn.cursor()

    # insert tweet information
    command = '''INSERT INTO twitterarchive (tweetid,username,isverified,followersCount,friendsCount,content,replyCount,retweetCount,likeCount,quoteCount,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    try:
        cur.execute(command,(tweetid,username,isverified,followersCount,friendsCount,content,replyCount,retweetCount,likeCount,quoteCount,date))
    except Exception as e:
        print (e.message)
        cur = conn.cursor()
    conn.commit()
    
    # Disconnect
    cur.close()
    conn.close()

# Using TwitterSearchScraper to scrape data 
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('(amazon) lang:en until:2010-09-30 since:2002-01-01').get_items()):
    if i>maxTweets:
        break
    dbConnect(tweet.id,tweet.user.username, tweet.user.verified, tweet.user.followersCount, tweet.user.friendsCount, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount,tweet.date)
    # tweets_list1.append([tweet.user.username, tweet.user.verified, tweet.user.followersCount, tweet.user.friendsCount, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount])

# df = pd.DataFrame(tweets_list1, columns=['Username', 'isVerified', 'followersCount', 'friendsCount', 'Tweet', 'replyCount', 'retweetCount', 'likeCount', 'quoteCount'])

# df.to_excel(r'Amazon2010.xlsx', sheet_name='2M Tweets', index = False)
