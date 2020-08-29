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
    host = 'autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'q2vGUCYoA1PgDS9EFd5L',
    database = "MainDB"
)

cur = connection.cursor()

def create_table(TableName):
    supplier_schema = """ 
    CREATE TABLE supplier (
        SupplierID INT(6) AUTO_INCREMENT,
        CompanyName VARCHAR(340) NOT NULL,
        ContactPerson VARCHAR(30) NOT NULL,
        Email VARCHAR(50),
        Phone VARCHAR(50),
        PRIMARY KEY (SupplierID)
        );
    """

    # ItemID,Name,Price,ShelfLife,OrderFrequency,SupplierID,SupplierSKU,SOH,LastUpdated,MinSOH,MaxSOH,MOQ
    stock_schema = """ 
    CREATE TABLE stock (
        ItemID INT(6) AUTO_INCREMENT , 
        Name VARCHAR(30) NOT NULL,
        Price FLOAT NOT NULL, 
        ShelfLife INT(3),
        OrderFrequency INT(3),
        SupplierID INT(6),
        SupplierSKU INT(10),
        SOH INT(5),
        LastUpdated TIMESTAMP,
        MinSOH INT(5),
        MaxSOH INT(5),
        MOQ INT(5),
        PRIMARY KEY (ItemID),

        CONSTRAINT fk_stockSupplier
        FOREIGN KEY (SupplierID) 
        REFERENCES supplier(SupplierID)


        );
    """

    order_schema = """ 
    CREATE TABLE orders (
        OrderID INT(6) UNSIGNED AUTO_INCREMENT,
        Date TIMESTAMP,
        SupplierID INT(6),
        ItemID INT(6),
        Total FLOAT,
        Status VARCHAR(40),

        PRIMARY KEY orders(OrderID),

        CONSTRAINT fk_orderSupplier
        FOREIGN KEY (SupplierID) 
        REFERENCES supplier(SupplierID),

        CONSTRAINT fk_orderItem
        FOREIGN KEY (ItemID) 
        REFERENCES stock(ItemID)

        );
    """
    if TableName.lower() == 'stock':
        cur.execute(stock_schema)
    elif TableName.lower() == 'supplier':
        cur.execute(supplier_schema)
    elif TableName.lower() == 'order':
        cur.execute(order_schema)

    connection.commit()
    print('<< CREATED TABLE >> %s << END >>'%(TableName))



def drop_table(TableName):
    sql = """drop table %s;"""%(TableName)
    cur.execute(sql)
    connection.commit()
    print('<< DROPPED TABLE >> %s << END >>'%(TableName))


#drop_table('supplier')
#drop_table('stock')
#drop_table('orders')

create_table('supplier')
create_table('stock')
create_table('order')