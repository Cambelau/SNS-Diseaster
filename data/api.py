# from conn import conn
import pandas as pd
import pathlib
import psycopg2

# DB_FILE = '/app/tweets.sqlite'

def DbConnect(query):
    
    # conn = psycopg2.connect(host="localhost",database="TwitterDB",port=5432,user="postgres",password="matthieu")
    conn = psycopg2.connect(host="dpg-ccr13n9a6gdlc0agf37g-a.oregon-postgres.render.com",database="twitterdb",port=5432,user="twitterdb_user",password="Voe2ktiDqONML8Lj9QvfkaH6gHK8tvOQ")

    curr = conn.cursor()
    
    curr.execute(query)
    
    rows = curr.fetchall()
    
    return rows


    
def get_tweet_data():
    # Create 
    data_tweet = DbConnect("SELECT User_Id, Tweet_Id, Tweet FROM TwitterTweet;")

    df_tweet = pd.DataFrame(columns=['User_Id','Tweet_Id','text'])

    for data in data_tweet:
        index = len(df_tweet)
        df_tweet.loc[index,'User_Id'] = data[0]
        df_tweet.loc[index,'Tweet_Id'] = data[1]
        df_tweet.loc[index,'text'] = data[2]
        
    return df_tweet
