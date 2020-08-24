


"""
 Goal is to: 
 
 1. Create a function which creates the schema for the tables we will store the data in. 
 2. Create a function to insert data/rows into this table

"""

import pymysql
import pandas as pd

connection = pymysql.connect(
    host = 'autostockordering.co7conkey36s.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'adminTom',
    password = 'XXHnW0lpK1jKaDujJaQA',
    database = "Supplier"
)

cur = connection.cursor()

def create_table():
    schema = """ 
    CREATE TABLE supplier (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        CompanyName VARCHAR(340) NOT NULL,
        ContactPerson VARCHAR(30) NOT NULL,
        Email VARCHAR(50),
        Phone VARCHAR(50)
        );
    """
   
    cur.execute(schema)
    connection.commit()
    print('<< TABLE CREATED >>')

    #insert_data()

def drop_table():
    sql = """drop table supplier;"""
    cur.execute(sql)
    connection.commit()
    print('<< TABLE DROPPED >>')



def insert_data():
    schema = """
        INSERT INTO supplier (CompanyName, ContactPerson, Email, Phone)
        VALUES ('Test Company 3', 'Company Admin 3', 'test3@Company.co.nz','09 123 45 90');
    """
    cur.execute(schema)
    connection.commit()
    print('<< DATA INSERTED >>')

def get_data():
    sql = """select * from supplier;"""
    print("<< RUNNING SQL:\n%s\n>>"%(sql))
    table_data = pd.read_sql(sql, con=connection)   

    print("<< TABLE DATA >>")
    print(table_data)


#create_table()
#insert_data()
get_data()

#drop_table()