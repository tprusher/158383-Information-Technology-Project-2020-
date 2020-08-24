
    

import pandas 
  
# reading the CSV file 
csvFile = pandas.read_csv('Stock_Import_File.csv') 
  
# displaying the contents of the CSV file 
print(csvFile[['Name', 'Price']]) 



for index, row in csvFile.iterrows():
    if int(row['Price']) > 3:
        print(row['Name'], row['Price'], True)
    else:
        print(row['Name'], row['Price'], False)

