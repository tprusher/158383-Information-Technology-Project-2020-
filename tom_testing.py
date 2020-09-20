#!/usr/bin/env python
# -*- coding: utf-8 -*- 


"""
Goal: 
1. Will need to query RDS MySQL DB -- COMPLETE
2. Perform Calculations off the back of that to determine whether or not a PO should be raised.. 
"""


import pymysql
import pandas as pd
from datetime import datetime
import time 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, sys

#import pdfkit as pdf
#import weasyprint as w

connection = pymysql.connect(
    host = 'autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'admin_Tom',
    password = 'q2vGUCYoA1PgDS9EFd5L',
    database = "MainDB"
)

cur = connection.cursor()

def get_data():

    supplier_count = """ select distinct s.supplierID as suppl from supplier s join stock s2 on s.supplierId = s2.supplierid where s2.SOH <= s2.MinSOH  ;"""
    supplier_result = pd.read_sql(supplier_count, con=connection)   
    
    for index, row in supplier_result.iterrows():
        supplier_filter = row['suppl']

        sql = """
            select 
                st.supplierid as supplierid,
                su.CompanyName as CompanyName,
                st.SupplierSKU,
                st.ItemID as ItemID,
                st.Name,
                st.Price,
                -- st.ShelfLife,
                -- st.OrderFrequency,
                
                st.SOH,
                -- st.LastUpdated,
                 st.MinSOH,
                -- st.MaxSOH,
                -- st.MOQ, 
                case when (st.MinSOH - st.SOH) >= st.MOQ then (st.MinSOH - st.SOH) else (st.MaxSOH - st.SOH) end OrderQty
        
            from 
                stock st
                Left Join supplier su on st.supplierid = su.supplierid 
            
            where 
                SOH <= MinSOH 
                and st.supplierId = %s
                
                ;"""%(supplier_filter)

        table_data = pd.read_sql(sql, con=connection)   
        print(table_data)

get_data()