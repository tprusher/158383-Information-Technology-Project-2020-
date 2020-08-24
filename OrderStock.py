

"""
Goal: 
1. Will need to query RDS MySQL DB -- COMPLETE
2. Perform Calculations off the back of that to determine whether or not a PO should be raised.. 
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

# Goal 1 (Get Data): 
def get_data():
    sql = """select * from stock;"""
    print("<< RUNNING SQL:\n%s\n>>"%(sql))
    table_data = pd.read_sql(sql, con=connection)   

    print("<< TABLE DATA >>")
    print(table_data)

    

