
import os
import base64
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.conf import settings
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="cdcol"
    )

def query(sql):

    print(sql)
    # print(val)
    mycursor = mydb.cursor()

    mycursor.execute(str(sql))

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    return True

def getquery(qe):
    print(qe)

    mycursor = mydb.cursor(dictionary=True)

    # mycursor.execute(sql, val)
    mycursor.execute(qe)

    myresult = mycursor.fetchall()

    # for x in myresult:
    #     print(x)
    print(myresult)
    return list(myresult)

def authentication_check (request): 
    user_password = []   
    if request.META.has_key("HTTP_AUTHORIZATION"):
        encoded_user_password =  request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_password  = base64.b64decode(encoded_user_password).split(":")
        user_name = user_password[0]
        password = user_password[1]
    return user_password



