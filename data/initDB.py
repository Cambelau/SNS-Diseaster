from conn import conn

# tABLE creation
commands = (# Table 1
            # '''Create Table TwitterUser(User_Id BIGINT PRIMARY KEY, User_Name TEXT);''',
            # # Table 2
            # '''Create Table TwitterTweet(Tweet_Id BIGINT PRIMARY KEY,
            #                              User_Id BIGINT,
            #                              Tweet TEXT,
            #                              Retweet_Count INT,
            #                              CONSTRAINT fk_user
            #                                  FOREIGN KEY(User_Id)
            #                                      REFERENCES TwitterUser(User_Id));''',
            # # Table 3
            # '''Create Table TwitterEntity(Id SERIAL PRIMARY KEY,
            #                              Tweet_Id BIGINT,
            #                              Hashtag TEXT,
            #                              CONSTRAINT fk_user
            #                                  FOREIGN KEY(Tweet_Id)
            #                                      REFERENCES TwitterTweet(Tweet_Id));''',
            # Table 4
            '''Create Table TwitterStream(Tweet_Id BIGINT PRIMARY KEY,
                                         Author_ID BIGINT,
                                         Like_count INT,
                                        Quote_count INT,
                                        Retweet_count INT,
                                        content TEXT
                                        );''',                                    
                                            )
commandss='''Drop Table  IF EXISTS TwitterStream;'''

# Create cursor to execute SQL commands
cur = conn.cursor()
# Execute SQL commands
for command in commands:
    # Create tables
    cur.execute(command)

# cur.execute(commandss)

# Close communication with server
conn.commit()
cur.close()
conn.close()
