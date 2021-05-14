import mysql.connector
import time
import datetime
import os.path as path
import sys
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from database.mysql_credentials import host, user, password, database

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

train, test = train_test_split(data, test_size=0.2, random_state=5)
x_train = train[:, :-1]
y_train = train[:, -1]

x_test = test[:, :-1]
y_test = test[:, -1]

model = Lasso(alpha=0.125)
model.fit(x_train, y_train)

print('MSE score is {}'.format(mean_squared_error(y_test, model.predict(x_test))))

print('Coefficients are={}. Intercept={}('.format(model.coef_, model.intercept_))

cursor.close()
conn.close()
