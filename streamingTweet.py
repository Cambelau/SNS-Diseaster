from data.env import bearer_token
import pandas as pd
import requests
import json
import psycopg2
from data.conn import connRailwayHost,connRailwayDatabase,connRailwayPort,connRailwayUser,connRailwayPassword

# print json ligne 140
# ligne 111 pour la sauvegarde en DB
# ligne 102 pour les valeurs requetées
# ligne 82 pour les rules de la requete api

# conn = psycopg2.connect(host="containers-us-west-70.railway.app",database="railway",port=7637 ,user="postgres",password="v4Rnu4WDaVHtwAHfMXiY")

def dbConnect(tweet_id, author_id, like_count, quote_count,retweet_count,content):
    conn = psycopg2.connect(host=connRailwayHost,database=connRailwayDatabase,port=connRailwayPort,user=connRailwayUser,password=connRailwayPassword)
    cur = conn.cursor()

    # insert tweet information
    command = '''INSERT INTO twitterstream (tweet_id, author_id, like_count, quote_count, retweet_count,content) VALUES (%s,%s,%s,%s,%s,%s);'''
    try:
        cur.execute(command,(tweet_id, author_id, like_count, quote_count,retweet_count,content))
    except Exception as e:
        print (e.message)
        cur = conn.cursor()
    # Commit changes
    conn.commit()
    
    # Disconnect
    cur.close()
    conn.close()
    
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "amazon lang:en -is:retweet"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream"+"?tweet.fields=lang,attachments,author_id,created_at,public_metrics,source", auth=bearer_oauth, stream=True,  
        )
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            # retweet_count=int(json_response['data']['public_metrics']['like_count'])
            # like_count=int(json_response['data']['public_metrics']['quote_count'])
            # quote_count=int(json_response['data']['public_metrics']['retweet_count'])
            tweet_id =json_response['data']['id']
            author_id = json_response['data']['author_id']
            retweet_count=int(json_response['data']['public_metrics']['like_count'])
            like_count=0
            quote_count=0
            lang=json_response['data']['lang']
            content= json_response['data']['text']
            # If tweet is not a retweet and tweet is in English
            if  lang=="en":
                # Connect to database
                dbConnect(tweet_id, author_id, like_count, quote_count,retweet_count,content)
            
def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)
    
main()