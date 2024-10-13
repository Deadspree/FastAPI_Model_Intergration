import sqlite3

con = sqlite3.connect("example.db") #If there is no database of this name, it will create one. If there is, it will connect to it
cur = con.cursor() #Let us actually command in our database

cur.execute('''CREATE TABLE IF NOT EXISTS tshirts 
                (sku text PIRMARY KEY, name text, size text, price real)''') #Tshirts is name of the table

cur.execute('''INSERT OR IGNORE INTO tshirts VALUES
                ('SKU1234', 'Black Logo Tshirt', 'Medium', '24,99')''') #If pirmary key already exists, it wont add new data, if primary key havent existed, it will add the new data

con.commit()

for row in cur.execute('''select * FROM tshirts'''):
    print(row)