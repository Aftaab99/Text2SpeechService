import mysql.connector
import time
import datetime
import os.path as path
import sys
import numpy as np
from sklearn.linear_model import LinearRegression

# Relative import for the database package
sys.path.append( path.abspath(path.join(__file__ ,"../../../database")))
from mysql_credentials import host, user, password, database

def get_conn():
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

conn = get_conn()
cursor = conn.cursor()

cursor.execute("""SELECT 
            c.n_cpu, c.ram, c.gpuavailable, p.num_words, p.sentence_length, p.prediction_time 
            from Configuration c INNER JOIN PredictionLog p 
            ON c.server_id=p.server_id""")

data = cursor.fetchall()
data = np.array(data).astype(np.float32)

x = data[:, :-1]
y = data[:, -1]
print('X shape={}'.format(x.shape))
print('Y shape={}'.format(y.shape))
model = LinearRegression()
model.fit(x, y)

print('Coefficients are={}. Intercept={}('.format(model.coef_, model.intercept_))

cursor.close()
conn.close()
