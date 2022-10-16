import string
import requests
import os
import json
import data.env as env
import time
import psycopg2
from data.conn import connRailwayHost,connRailwayDatabase,connRailwayPort,connRailwayUser,connRailwayPassword

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = env.bearer_token_academic

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'Bank of America  -is:retweet -is:quote -is:reply',
                'start_time' :'2022-09-01T00:00:00Z',
                'end_time' :'2022-09-03T00:00:00Z',
                'tweet.fields': 'author_id,lang,public_metrics,created_at',
                'max_results' : '100' ,
                }

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# def main():
#     json_response= connect_to_endpoint(search_url, query_params)
#     tweets_list1.append(json_response);
#     print(len(tweets_list1))
#     # print(json.dumps(json_response, indent=4, sort_keys=True))
    
tweets_list1 = []

def paginateTweet():
    json_response = connect_to_endpoint(search_url, query_params)
    jsonToDb(json_response);
    print("Adding tweet to db...")
    
    while ("next_token" in json.dumps(json_response)):
        print("Adding tweet to db...")
        time.sleep(1)# to dodge 'too many request'
        query_params_next = query_params
        query_params_next["next_token"]=json_response["meta"]["next_token"]
        json_response = connect_to_endpoint(search_url, query_params_next)
        jsonToDb(json_response);



def dbConnect(tweet_id, author_id, like_count, quote_count,retweet_count,content,created_at):
    conn = psycopg2.connect(host=connRailwayHost,database=connRailwayDatabase,port=connRailwayPort,user=connRailwayUser,password=connRailwayPassword)
    cur = conn.cursor()

    # insert tweet information
    command = ''' INSERT INTO twitterstream (tweet_id, author_id, like_count, quote_count, retweet_count,content,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s) ;'''
    try:
        cur.execute(command,(tweet_id, author_id, like_count, quote_count,retweet_count,content,created_at))
    except Exception as e:
        print (e)
        cur = conn.cursor()
    # Commit changes
    conn.commit()
    
    # Disconnect
    cur.close()
    conn.close()

def jsonToDb(json_response):
    for tweet in json_response['data']:
        tweet_id =tweet['id']
        author_id = tweet['author_id']
        retweet_count=int(tweet['public_metrics']['like_count'])
        like_count=int(tweet['public_metrics']['quote_count'])
        quote_count=int(tweet['public_metrics']['retweet_count'])
        created_at= tweet['created_at']
        lang=tweet['lang']
        content= tweet['text']
        # If tweet is in English
        if  lang=="en":
            # Connect to database
            dbConnect(tweet_id, author_id, like_count, quote_count,retweet_count,content,created_at)
            
        
if __name__ == "__main__":
    paginateTweet()