import mysql.connector
import time
import datetime
import os.path as path
import sys
import numpy as np

# Relative import for the database package
sys.path.append( path.abspath(path.join(__file__ ,"../../../database")))
from mysql_credentials import host, user, password, database

def get_conn():
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

conn = get_conn()
cursor = conn.cursor()

cursor.execute("SELECT num_words,sentence_length,prediction_time from PredictionLog")

data = cursor.fetchall()
data = np.array(data).astype(np.float32)

# TODO: Train linear regression model

cursor.close()
conn.close()
plt.show()
