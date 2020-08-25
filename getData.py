import pymysql
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
def get_data():
    sql = """select * from supplier;"""
    print("<< RUNNING SQL:\n%s\n>>"%(sql))
    table_data = pd.read_sql(sql, con=connection)   

    print("<< TABLE DATA >>")
    print(table_data)



get_data()