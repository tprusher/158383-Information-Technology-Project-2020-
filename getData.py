import pymysql
import openpyxl
import pandas as pd

# connection = pymysql.connect(
#     host = 'autostockordering.co7conkey36s.us-east-1.rds.amazonaws.com',
#     port = 3306,
#     user = 'adminTom',
#     password = 'XXHnW0lpK1jKaDujJaQA',
#     database = "Supplier"
# )

connection = pymysql.connect(
    host = 'autostockordering.cwhehy370roy.ap-southeast-2.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'TM1ZtaKUOw9EHthjUEYt',
    database = "MainDB"
)


cur = connection.cursor()

def get_data(TableName):
    sql = """select * from %s;"""%(TableName)
    print("<< RUNNING SQL:\n%s\n>>"%(sql))
    table_data = pd.read_sql(sql, con=connection)   
    write_to_excel(table_data)
    print("<< TABLE DATA >>")
    print(table_data)


def write_to_excel(dataSet): 
    dataSet.to_excel (r'/Users/tprusher/Documents/Coding/158383-Information-Technology-Project-2020-/DataSet.xlsx',
     index = False, header=True, sheet_name='Tom_Data_Export')


get_data('supplier')