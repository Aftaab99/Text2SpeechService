import os.path as path
import sys
import mysql.connector

# Relative import for the database package
sys.path.append( path.abspath(path.join(__file__ ,"../../../database")))
from mysql_credentials import host, user, password, database

def get_config():
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    q_get_config = "SELECT server_id, n_cpu, ram, gpu_available from Configuration"
    cursor = conn.cursor()

    cursor.execute(q_get_config)
    config = {}
    for (sid, ncpu, ram, hasgpu) in cursor:
        config[sid] = {'n_cpu': ncpu, 'ram': ram, 'gpu_available': hasgpu}
    cursor.close()
    conn.close()
    return config