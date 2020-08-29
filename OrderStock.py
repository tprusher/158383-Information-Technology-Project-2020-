

"""
Goal: 
1. Will need to query RDS MySQL DB -- COMPLETE
2. Perform Calculations off the back of that to determine whether or not a PO should be raised.. 
"""


import pymysql
import pandas as pd

connection = pymysql.connect(
    host = 'autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'q2vGUCYoA1PgDS9EFd5L',
    database = "MainDB"
)

cur = connection.cursor()

# Goal 1 (Get Data): 
def get_data():

    supplier_count = """ select distinct s.supplierID as suppl from supplier s join stock s2 on s.supplierId = s2.supplierid where s2.SOH <= s2.MinSOH  ;"""
    supplier_result = pd.read_sql(supplier_count, con=connection)   
    
    for index, row in supplier_result.iterrows():
        supplier_filter = row['suppl']

        sql = """
            select 
                st.supplierid as supplierid,
                su.CompanyName as CompanyName,
                st.ItemID as ItemID,
                st.Name,
                st.Price,
                st.ShelfLife,
                st.OrderFrequency,
                st.SupplierSKU,
                st.SOH,
                st.LastUpdated,
                st.MinSOH,
                st.MaxSOH,
                st.MOQ    
        
            from 
                stock st
                join supplier su on st.supplierid = su.supplierid 
            
            where SOH <= MinSOH and st.supplierId = %s;"""%(supplier_filter)
        table_data = pd.read_sql(sql, con=connection)   
        
        z = (table_data.CompanyName.unique())
        print(table_data)   
        
        
        table_data.to_excel ('/Users/tprusher/Documents/Coding/158383-Information-Technology-Project-2020-/'+'%s.xlsx'%(z[0]),
                    index = False, header=True, sheet_name='Sheet1')

        print('NEW SUPPLIER BREAK')

        # ItemID,Name,Price,ShelfLife,OrderFrequency,SupplierID,SupplierSKU,SOH,LastUpdated,MinSOH,MaxSOH,MOQ
       # for index, row in table_data.iterrows():
            #print('RAISE ORDER |', row['ItemID'], row['Name'], row['SOH'], row['MinSOH'])
            
       # print( row['CompanyName'],row['ItemID'], row['Name'],  row['SupplierSKU'], row['SOH'], row['MinSOH'], row['MaxSOH'], row['MOQ'])

get_data()