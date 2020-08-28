
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
    csvFile = pd.read_csv('Supplier_Import_File.csv') 

    table_data = pd.read_sql("""select distinct CompanyName from supplier;""", con=connection)

    supplier_list = []
    
    for index, row in table_data.iterrows():
        supplier_list.append(row['CompanyName'])

    print(supplier_list)

    for index, row in csvFile.iterrows():
        insert_schema = """
            INSERT INTO supplier (CompanyName, ContactPerson, Email, Phone)
            VALUES ('%s', '%s', '%s','%s');
            """%(row['CompanyName'], row['ContactPerson'], row['Email'], row['Phone'])

        update_schema = """
            UPDATE supplier 
                CompanyName = %s,
                ContactPerson = %s, 
                Email = %s, 
                Phone = %s
            WHERE
                CompanyName = %s  
            ;
            """%(row['CompanyName'], row['ContactPerson'], row['Email'], row['Phone'], row['CompanyName'])

        if row['CompanyName'] in supplier_list:
            print('SKU', row['SupplierSKU'], 'LIST:', supplier_list) 
            sql = update_schema
            print(sql)
        elif row['CompanyName'] == 'nan':
            pass
        else: 
            sql = insert_schema
            print(sql)
        
        cur.execute(sql)
        connection.commit()
        #print('<< DATA INSERTED >>')


def delete_data(TableName):
    sql = 'Delete from %s where 1=1;'%(TableName)
    cur.execute(sql)
    connection.commit()  
    query = 'Select * from %s'%(TableName)
    table_data = pd.read_sql(query, con=connection)
    cur.execute(query)
    connection.commit()
    print(table_data)


#delete_data('supplier')

insert_supplier_data()



 