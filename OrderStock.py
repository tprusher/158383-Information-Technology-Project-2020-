

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
                -- st.MinSOH,
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
        b = insert_order_data(table_data) 

        # NOW CREATE THE OUTPUT.. 
        create_output(supplier_filter, b)


def insert_order_data(data): 
    order_id = create_order_id()

    for index, row in data.iterrows():  
        # CREATE TABLE order_detail (
        #     OrderLineUUID int(6) AUTO_INCREMENT, 
        #     OrderID INT(6), 
        #     Date TIMESTAMP,
        #     SupplierID INT(6),
        #     ItemID INT(6),
        #     Total FLOAT,
        #     Status VARCHAR(40),

        insert_sql = """
                INSERT INTO order_detail (OrderID, Date, SupplierID, ItemID, Total, Status)
                VALUES (%s, current_timestamp(), %s, %s, %s, 'Pending')
                """%(order_id, row['supplierid'], row['ItemID'], row['Price'] * row['OrderQty']) 

        cur.execute(insert_sql)
    return order_id
    

def create_order_id(): 
        # CREATE TABLE order_header (
        #     OrderID INT(6) AUTO_INCREMENT,
        #     DateCreated TIMESTAMP,
        #     Status VarChar(20),

    z = """insert into order_header (DateCreated, Status) values(current_timestamp(), 'Pending');"""
    cur.execute(z)
    connection.commit()

    z2 = """
        select 
            oh.OrderID OrderID,
            oh.DateCreated

        from 
            order_header oh
            Join (Select Max(DateCreated) DateCreated from order_header) oh2 on oh.DateCreated = oh2.DateCreated        
        ;"""
    LatestOrder = pd.read_sql(z2, con=connection) 

    Tom_ORDER_ID = LatestOrder['OrderID']

    return Tom_ORDER_ID[0]



def create_output(supplier_filter, order_id): 

        output_sql = """ 
            SELECT
                od.OrderID, 
                od.Date,
                su.CompanyName,
                s.SupplierSKU,
                s.Name as ProductName,
                case when (s.MinSOH - s.SOH) >= s.MOQ then (s.MinSOH - s.SOH) else (s.MaxSOH - s.SOH) end OrderQty,
                od.Total,
                od.Status

            FROM
                order_detail od 
                Join stock s on od.ItemID = s.ItemID 
                Join supplier su on od.SupplierID = su.SupplierID

            Where
                od.OrderID = %s 
                and od.SupplierID = %s

        ;"""%(order_id, supplier_filter)

        order_val_sql = """
            SELECT
                Sum(od.Total) OrderValue

            FROM
                order_detail od 
                Join stock s on od.ItemID = s.ItemID 
                Join supplier su on od.SupplierID = su.SupplierID

            Where
                od.OrderID = %s 
                and od.SupplierID = %s
        """%(order_id, supplier_filter)

        table_data = pd.read_sql(output_sql, con=connection) 
        #print(table_data)

        order_value_df = pd.read_sql(order_val_sql, con=connection) 


        suppl_name = pd.read_sql("""Select distinct CompanyName from supplier where supplierId = %s;"""%(supplier_filter), con=connection) 
        supplyKEY = suppl_name['CompanyName'][0]

        filtered_order_id = pd.read_sql("""
        select OrderID, Status from order_detail od 
            Where od.OrderID = %s and od.SupplierID = %s
            Having Max(Date)
        ;"""%(order_id, supplier_filter), con=connection)

        filtered_order_key =  filtered_order_id['OrderID'][0]
        order_status_key = filtered_order_id['Status'][0]
        order_value = order_value_df['OrderValue'][0]
          
        date_time = datetime.now().strftime("%d/%m/%y %H:%M")

        pdf_file_name = '%s Order'%(supplyKEY)

        pdf_header = """<h2> %s</h2>"""%(supplyKEY)
        sub_header = """<h4> 
                        Order ID: %s <br> 
                        Status: %s <br>
                        Order Value: $%s
                        </h4>
                        """%(filtered_order_key, order_status_key, order_value)

        footer_details = """<p id='footer_notes'>
            Order Generated: %s<br>
            Services provided by: Group 1​ (Codie Springer 13067864,  Kate Robbie 93014642,Thomas Prusher 15131284, Mi Jin Park 19029015​) <br>
            Phone: 021 123 456 789<br>
            Email: 158383StockOrdering@gmail.com
            </p>
            """%(date_time)

        client_business = """
                    <p id = "ClientBusiness"> 
                    <br><b>Julian's Berry Farm and Cafe <b><br> 
                    <b> Address: <b> 12 Huna Road, Coastlands, Whakatane 3191<br>
                    <b> Phone:<b> 07-308 4253 <br>
                    <a href=" https://www.juliansberryfarm.co.nz/">
                    <img src="https://www.juliansberryfarm.co.nz/sites/www.juliansberryfarm.co.nz/files/logo.png" width="400" height="200"></a>
                    </p><br>
                    """
                

        to_portal = """ <div id='myButtons'> 
        <a href="https://www.google.com/" class="accept_button" id="button-hover">ACCEPT </a> 
        <a href="https://www.google.com/" class="edit_button" id="button-hover">EDIT </a> </div> """
        
        css_style = """
        <style> 
            #button-hover:hover { 
                background-color: black; 
                color: white;
            }
            #ClientBusiness {
                font-size: 13px;
            }
            #myButtons { 
                width: 100%; 
                padding-top: 1%;
            }
            h2 { 
                color: 0099FF;
            }
            h3 {
                color: black;
                font-size: 11px;
                font-weight: bold;

            }
            #status_color {
                color: orange;
            }
            
            p { 
                font-size: 10px;
            }

            table.dataframe {
                border: 1px solid #1C6EA4;
                background-color: #EEEEEE;
                width: 100%;
                
                text-align: center;
                border-collapse: collapse;
                }
                table.dataframe  td, table.dataframe  th {
                border: 0.5px solid  	#D3D3D3;
                padding: 3px 2px;
                text-align: center;
                }
                table.dataframe  tbody td {
                font-size: 12px;
                font-weight: bold;
                }
                table.dataframe  tr:nth-child(even) {
                background: #D0E4F5;
                }
            table.dataframe  thead {
                background: #1C6EA4;
                background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
                background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
                background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
                border-bottom: 1px solid #444444;
                bottom-padding: 1px; 
                }
                table.dataframe  thead th {
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
                border-left: 1px solid #444444;
                }
                table.dataframe  thead th:first-child {
                border-left: none;
                }

                table.dataframe  tfoot {
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
                background: #D0E4F5;
                background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
                background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
                background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
                border-top: 2px solid #444444;
                }
                table.dataframe  tfoot td {
                font-size: 14px;
                }
                table.dataframe  tfoot .links {
                text-align: right;
                }
                table.dataframe  tfoot .links a{
                display: inline-block;
                background: #1C6EA4;
                color: #FFFFFF;
                padding: 2px 8px;
                border-radius: 5px;
                }

                #footer_notes {
                    color: #696969;
                    font-style: italic;
                }
                
                .accept_button {
                    background-color: #4CAF50;
                    font-weight: bold;
                    width: 5%;
                    border: none;
                    color: white;
                    top-padding: 5px;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 12px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 25px;
                    }

                .edit_button {
                                background-color:  	#FF7F50;
                                width: 5%;
                                transition-duration: 0.4s;

                                font-weight: bold;
                                border: none;
                                color: white;
                                top-padding: 5px;
                                padding: 15px 32px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 12px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border-radius: 25px;
                                }
        </style> 
        """

        pdf_table = table_data.to_html()
        
        pdf_data = pdf_header + sub_header + pdf_table + to_portal + css_style + client_business + footer_details
        
        # Create a html ouput.
        # po_html = open("%s.html"%(pdf_file_name), "w")
        # po_html.write(pdf_data)
        # po_html.close()

        # Create a pdf ouput.
        #my_pdf_output = w.HTML("%s.html"%(pdf_file_name)).write_pdf("%s.pdf"%(pdf_file_name))
        
        send_email(subject = pdf_file_name, email_copy=pdf_data, vendor = pdf_file_name)
        print("** Finished : %s **"%(pdf_file_name))

def send_email(subject, email_copy, vendor): 
    #print('SEND EMAIL --\n',subject,'\n', email_copy)  

    username = '158383StockOrdering@gmail.com'
    password = 'pCKgbp83Mcuuvqe'

    me = '158383StockOrdering@gmail.com'

    # << CHANGE THIS TO CHANGE WHO GETS THE EMAIL >> 
    # WE WILL NEED THIS TO BE PASSED IN AS A VAR IN REAL LIFE 
    you = "tprusher@hotmail.co.uk"   

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New PO for %s (Pending)"%(vendor)
    msg['From'] = me
    msg['To'] = you

    copy = MIMEText(email_copy, 'html')
    msg.attach(copy)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()




get_data()


