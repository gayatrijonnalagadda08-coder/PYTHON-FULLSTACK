import random
import pymysql
from db import getConnection
def generateAccNo():
    while True:
        accno = random.randint(1000000000,9999999999)
        conn  = getConnection()
        cmd = conn.cursor(pymysql.cursors.DictCursor)
        cmd.execute("SELECT * FROM CUSTOMER WHERE accno=%s",(accno,)) 
        res =  cmd.fetchone() #if accno not their you will get none
        conn.close()
        if res == None:
            return accno

print(generateAccNo())
def generateTransactionId():
    while True:
        accno = random.randint(1000000000,9999999999)
        conn  = getConnection()
        cmd = conn.cursor(pymysql.cursors.DictCursor)
        cmd.execute("SELECT * FROM CUSTOMER WHERE TransactionId=%s",(accno,)) 
        res =  cmd.fetchone() #if accno not their you will get none
        conn.close()
        if res == None:
            return accno
print(generateTransactionId())
