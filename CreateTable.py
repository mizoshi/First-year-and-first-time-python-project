import sqlite3

conn = sqlite3.connect ('userdata.db')
c = conn.cursor()
c.execute ('''CREATE TABLE userdata(ID integer PRIMARY KEY AUTOINCREMENT,USERNAME varchar(30) NOT NULL,
    PASSWORD varchar(30) NOT NULL,
    NAME varchar(50) NOT NULL,
    LAST_NAME varchar(50) NOT NULL,
    Email varchar(255) NOT NULL)''')
conn.commit()

conn = sqlite3.connect ('itemlist.db')
c = conn.cursor()
c.execute ('''CREATE TABLE itemlist(ID integer PRIMARY KEY AUTOINCREMENT,pdtname varchar(255) NOT NULL,
    price varchar(30) NOT NULL)''')
conn.commit()

conn = sqlite3.connect ('tranclog.db')
c = conn.cursor()
c.execute ('''CREATE TABLE TransactionLog(NO integer PRIMARY KEY AUTOINCREMENT,Username varchar(50) NOT NULL,
    Name varchar(50) NOT NULL,
    Last_Name varchar(50) NOT NULL,
    Email varchar(255) NOT NULL,
    Address varchar(255) NOT NULL,
    ZipCode varchar(5) NOT NULL,
    Phone varchar(10) NOT NULL,
    ProductID TEXT,
    TotalPrice varchar(30) NOT NULL)''')
conn.commit()
c.close
