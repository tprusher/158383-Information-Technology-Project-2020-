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

    supplier_count = """ Select distinct SupplierID as suppl From order_detail Where Status='Approved' and Date between date - 7 and date;"""
    supplier_result = pd.read_sql(supplier_count, con=connection)   
    
    for index, row in supplier_result.iterrows():
        supplier_filter = row['suppl']

        #b = insert_order_data(table_data) 

        # NOW CREATE THE OUTPUT.. 
        create_output(supplier_filter)



def create_output(supplier_filter): 

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
                od.SupplierID = %s
                and od.Date between date - 7 and date
                and od.Status = 'Approved'

        ;"""%(supplier_filter)

        order_val_sql = """
            SELECT
                Sum(od.Total) OrderValue

            FROM
                order_detail od 
                Join stock s on od.ItemID = s.ItemID 
                Join supplier su on od.SupplierID = su.SupplierID

            Where
                od.SupplierID = %s
                and od.Date between date - 7 and date
                and od.Status = 'Approved'
                ;

        """%(supplier_filter)

        table_data = pd.read_sql(output_sql, con=connection) 
        #print(table_data)

        order_value_df = pd.read_sql(order_val_sql, con=connection) 


        suppl_name = pd.read_sql("""Select distinct CompanyName from supplier where supplierId = %s;"""%(supplier_filter), con=connection) 
        supplyKEY = suppl_name['CompanyName'][0]

         
        date_time = datetime.now().strftime("%d/%m/%y %H:%M")

        pdf_file_name = '%s Order'%(supplyKEY)

        pdf_header = """<h2> %s</h2>"""%(supplyKEY)

        #  Services provided by: Group 1​ | Codie Springer,  Kate Robbie,Thomas Prusher, Mi Jin Park <br>
        footer_details = """<p id='footer_notes'>
            Order Generated: %s<br>
           
            Phone: 021 123 456 789<br>
            Email: 158383StockOrdering@gmail.com
            </p>
            """%(date_time)

        client_business = """
                    <h4> Deliver to: </h4>
                    <p id = "ClientBusiness"> 
                    <br><b>Julian's Berry Farm and Cafe <b><br> 
                    <b> Address: <b> 12 Huna Road, Coastlands, Whakatane 3191<br>
                    <b> Phone:<b> 07-308 4253 <br>
                    <a href=" https://www.juliansberryfarm.co.nz/">
                    <img src="https://www.juliansberryfarm.co.nz/sites/www.juliansberryfarm.co.nz/files/logo.png" width="400" height="200"></a>
                    </p><br>
                    """
                

        # to_portal = """ <div id='myButtons'> 
        # <a href="https://www.google.com/" class="accept_button" id="button-hover">ACCEPT </a> 
        # <a href="https://www.google.com/" class="edit_button" id="button-hover">EDIT </a> </div> """
        
        css_style = """
        <style> 
            #button-hover:hover { 
                background-color: black; 
                color: white;
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
        
        pdf_data = pdf_header + pdf_table + css_style + client_business + footer_details
        
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
    recipients = ["tprusher@hotmail.co.uk" , "pietapan@outlook.com", "codie.springer@gmail.com", "mijinpark87@gmail.com"]  

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "SUPPLIER EMAIL --> for Julian's Berry Farm and Cafe"
    msg['From'] = me
    msg['To'] = ", ".join(recipients)

    copy = MIMEText(email_copy, 'html')
    msg.attach(copy)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(me, recipients, msg.as_string())
    mail.quit()




get_data()


