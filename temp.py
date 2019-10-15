import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pyBill"
)

mycursor = mydb.cursor()

sql = "SELECT * FROM Users"
myresult = mycursor.execute(sql)
print myresult
for i in myresult:
    print i