

import pymysql
import openpyxl
import pandas as pd




connection = pymysql.connect(
    host = 'autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'q2vGUCYoA1PgDS9EFd5L',
    database = "MainDB"
)

cur = connection.cursor()




sql = """

UPDATE stock SET ProductName = 'FANTA 1.0', Price = 123 , ShelfLife = 456, SupplierSKU = 789 WHERE ItemID = 10 
"""


cur.execute(sql)
connection.commit()






def get_data(TableName):
    sql = """select * from stock WHERE ItemID = 10;"""

    table_data = pd.read_sql(sql, con=connection)   
    #write_to_excel(table_data)

    print("<< TABLE DATA >>")
    print(table_data)


def write_to_excel(dataSet): 
    dataSet.to_excel (r'/Users/tprusher/Documents/Coding/158383-Information-Technology-Project-2020-/DataSet.xlsx',
     index = False, header=True, sheet_name='Data_Export')


get_data('order_detail')