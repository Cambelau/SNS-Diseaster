# from conn import conn
import pandas as pd
from conn import conn

# DB_FILE = '/app/tweets.sqlite'

def DbConnect(query):
    
    curr = conn.cursor()
    
    curr.execute(query)
    
    rows = curr.fetchall()
    
    return rows


    
def get_tweet_data():
    # Create 
    data_tweet = DbConnect("SELECT User_Id, Tweet_Id, Tweet FROM TwitterArchive;")

    df_tweet = pd.DataFrame(columns=['User_Id','Tweet_Id','text'])

    for data in data_tweet:
        index = len(df_tweet)
        df_tweet.loc[index,'User_Id'] = data[0]
        df_tweet.loc[index,'Tweet_Id'] = data[1]
        df_tweet.loc[index,'text'] = data[2]
        
    return df_tweet
