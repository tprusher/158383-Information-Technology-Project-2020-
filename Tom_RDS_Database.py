


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

def create_table(TableName):
    supplier_schema = """ 
    CREATE TABLE supplier (
        SupplierID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        CompanyName VARCHAR(340) NOT NULL,
        ContactPerson VARCHAR(30) NOT NULL,
        Email VARCHAR(50),
        Phone VARCHAR(50)
        );
    """
    # ItemID,Name,Price,ShelfLife,OrderFrequency,SupplierID,SupplierSKU,SOH,LastUpdated,MinSOH,MaxSOH,MOQ
    stock_schema = """ 
    CREATE TABLE stock (
        ItemID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
        Name VARCHAR(30) NOT NULL,
        Price FLOAT NOT NULL, 
        ShelfLife INT(3),
        OrderFrequency INT(3),
        SupplierID INT(10),
        SupplierSKU INT(10),
        SOH INT(5),
        LastUpdated TIMESTAMP,
        MinSOH INT(5),
        MaxSOH INT(5),
        MOQ INT(5)
        );
    """
    if TableName.lower() == 'stock':
        cur.execute(stock_schema)
    elif TableName.lower() == 'supplier':
        cur.execute(supplier_schema)

    connection.commit()
    print('<< CREATED TABLE >>\n\t %s \n<< END >>'%(TableName))

    #insert_data()

def drop_table(TableName):
    sql = """drop table %s;"""%(TableName)
    cur.execute(sql)
    connection.commit()
    print('<< DROPPED TABLE >>\n\t %s \n<< END >>'%(TableName))


def insert_supplier_data():
    schema = """
        INSERT INTO supplier (CompanyName, ContactPerson, Email, Phone)
        VALUES ('Test Company 3', 'Company Admin 3', 'test3@Company.co.nz','09 123 45 90');
    """
    cur.execute(schema)
    connection.commit()
    print('<< DATA INSERTED >>')

def insert_stock_data(): 
    csvFile = pd.read_csv('Stock_Import_File.csv') 


    for index, row in csvFile.iterrows():
       # print((row['Name'], row['Price'],row['ShelfLife'],row['OrderFrequency'],row['SupplierID'],row['SupplierSKU'],row['SOH'], row['MinSOH'],row['MaxSOH'],row['MOQ']))

        insert_sql = """ INSERT INTO stock (Name,Price,ShelfLife,OrderFrequency,SupplierID,SupplierSKU,SOH,LastUpdated,MinSOH,MaxSOH,MOQ)
                          VALUES ('%s', %s, %s, %s, %s, %s, %s, current_timestamp(), %s, %s , %s);
                      """%(row['Name'], row['Price'],row['ShelfLife'],row['OrderFrequency'],row['SupplierID'],row['SupplierSKU'],row['SOH'], row['MinSOH'],row['MaxSOH'],row['MOQ'])
      
        update_sql = """ UPDATE stock 
                       SET 
                            Name = '%s',
                            Price = %s,
                            ShelfLife = %s,
                            OrderFrequency = %s,
                            SOH = %s,
                            LastUpdated = current_timestamp(),
                            MinSOH = %s,
                            MaxSOH = %s,
                            MOQ = %s

                       Where
                        SupplierSKU = %s
                        and SupplierID = %s
                        ; 
                      """%(row['Name'], row['Price'],row['ShelfLife'],row['OrderFrequency'],row['SOH'],row['MinSOH'],row['MaxSOH'],row['MOQ'],row['SupplierSKU'], row['SupplierID'])
          
        product_list = products_in_stock(row['SupplierID'])

        if row['SupplierSKU'] in product_list:
            print('SKU', row['SupplierSKU'], 'LIST:', product_list) 
            sql = update_sql
        else: 
            sql = insert_sql

        print('Running NOW >>', sql)

        cur.execute(sql)
        connection.commit()

def products_in_stock(supplierID): 
    unique_productKeys = """ Select distinct SupplierSKU from stock s where s.SupplierID = '%s';"""%(supplierID)
    print("<< RUNNING SQL:\n%s\n>>"%(unique_productKeys))

    table_data = pd.read_sql(unique_productKeys, con=connection)   

    print("<< TABLE DATA >>")
    #print(table_data)
    my_list = []

    for index, row in table_data.iterrows():
        my_list.append(row['SupplierSKU'])

    return my_list

def get_data():
    sql = """select * from stock;"""
    print("<< RUNNING SQL:\n%s\n>>"%(sql))
    table_data = pd.read_sql(sql, con=connection)   

    print("<< TABLE DATA >>")
    print(table_data)

drop_table('stock')
create_table('stock')

insert_stock_data()


get_data()

# products_in_stock()


