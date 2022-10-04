import psycopg2

# Connection to database local
# conn = psycopg2.connect(host="localhost",database="TwitterDB",port=5432,user="postgres",password="matthieu")

# --------------------------------------------------------------- 
# Connection to database Railway
connRailwayHost="containers-us-west-70.railway.app"
connRailwayDatabase="railway"
connRailwayPort="7637"
connRailwayUser="postgres"
connRailwayPassword="v4Rnu4WDaVHtwAHfMXiY"

# conn = psycopg2.connect(host=connRailwayHost,database=connRailwayDatabase,port=connRailwayPort ,user=connRailwayUser,password=connRailwayPassword)


# conn = psycopg2.connect(host="containers-us-west-70.railway.app",database="railway",port=7637 ,user="postgres",password="v4Rnu4WDaVHtwAHfMXiY")
