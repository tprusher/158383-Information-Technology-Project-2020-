

"""
Goal: 
1. Will need to query RDS MySQL DB -- COMPLETE
2. Perform Calculations off the back of that to determine whether or not a PO should be raised.. 
"""


import pymysql
import pandas as pd
import pdfkit as pdf
from datetime import datetime
import weasyprint as w

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
                st.SupplierSKU,
                -- st.ItemID as ItemID,
                st.Name,
                st.Price,
                -- st.ShelfLife,
                -- st.OrderFrequency,
                
                st.SOH,
                -- st.LastUpdated,
                 st.MinSOH,
                 st.MaxSOH,
                 st.MOQ, 
                case when (st.MinSOH - st.SOH) >= st.MOQ then (st.MinSOH - st.SOH) else (st.MaxSOH - st.SOH) end OrderQty

        
            from 
                stock st
                join supplier su on st.supplierid = su.supplierid 
            
            where SOH <= MinSOH and st.supplierId = %s;"""%(supplier_filter)
        table_data = pd.read_sql(sql, con=connection)   
        
        z = (table_data.CompanyName.unique()) 
        date_time = datetime.now().strftime("%d/%m/%y %H:%M")

        pdf_file_name = '%s Order'%(z[0])
        pdf_header = """<h2> %s Order</h2>      
        """%(z[0])
        footer_details = """ <p id='footer_notes'>
            Order Generated: %s<br>
            Order For: [CLIENT COMPANY NAME] <br>
            Contact #: [CLIENT CONTACT #] <br>
            Services provided by Group 1​ (Codie Springer 13067864,  Kate Robbie 93014642,Thomas Prusher 15131284, Mi Jin Park 19029015​)
            </p>
            """%(date_time)
        to_portal = """<a href="https://www.google.com/" class="accept_button"> ACCEPT </a> <a href="https://www.google.com/" class="edit_button"> EDIT </a> """
        

        css_style = """
        <style> 
        h2 { 
            color: 0099FF;
        }
        h3 {
            color: black;
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
                color: #DCDCDC;
                font-style: italic;
             }
            
            .accept_button {
                background-color: #4CAF50;;
                border: none;
                color: white;
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
                            border: none;
                            color: white;
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
        
        pdf_data = pdf_header + pdf_table + to_portal + css_style + footer_details
        

        # Create a html ouput.
        po_html = open("%s.html"%(pdf_file_name), "w")
        po_html.write(pdf_data)
        po_html.close()

        # Create the pdf 
        my_pdf_output = w.HTML("%s.html"%(pdf_file_name)).write_pdf("%s.pdf"%(pdf_file_name))
        
        print("** Finished : %s.html **"%(pdf_file_name))

        # Create and excel output;

        # try:
        #     table_data.to_excel ('/Users/tprusher/Documents/Coding/158383-Information-Technology-Project-2020-/'+'%s.xlsx'%(z[0]),
        #             index = False, header=True, sheet_name='%s'%(z[0]))
        #     print('Created File >>')
        # except: 
        #     print('Failed to Create File >>')





get_data()