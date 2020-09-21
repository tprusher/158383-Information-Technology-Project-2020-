







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




sql = 'UPDATE stock SET ProductName ="Fanta TEST", Price = 123, ShelfLife = 123, SupplierSKU =123 WHERE SupplierID =1 AND ItemID =10;'


cur.execute(sql)
connection.commit()






sql = 'UPDATE stock SET ProductName ="Fanta TEST", Price = 123, ShelfLife = 123, SupplierSKU =123 WHERE SupplierID =1 AND ItemID =10;'