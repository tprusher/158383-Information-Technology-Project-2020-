
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

def insert_supplier_data():
    schema = """
        INSERT INTO supplier (CompanyName, ContactPerson, Email, Phone)
        VALUES ('Test Company 3', 'Company Admin 3', 'test3@Company.co.nz','09 123 45 90');
    """
    cur.execute(schema)
    connection.commit()
    print('<< DATA INSERTED >>')

insert_stock_data()