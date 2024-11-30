from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode

#refer to third midterm project to change variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user = "root",
            password = "root",
            port = "5011",
            database = "sakila_db"
        )
    except mysql.connector.Error:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            exit()
        else:
            print(err)
            print("ERROR: Service not available")
            exit()
        return mydb
    
    