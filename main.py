# main

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pyBill"
)

mycursor = mydb.cursor()

from Tkinter import *
import tkMessageBox , pickle
# import dbconnect

class iteminfo(object):
    def __init__(self):
        self.icode = StringVar()
        self.item = StringVar()
        self.price = StringVar()
        self.qty = StringVar()
        self.disc = StringVar()
    def calAmount(self , qty) :
        k = float(self.qty)
        k -= float(qty)
        self.qty = str(k)
        return ((float(self.price) * float(qty)) * (1 - float(self.disc)/100.0) * (1 + 18/100.0))   

def users() :
        global userList , manager , cashier
        userList = pickle.load(open("login.dat" , "rb"))
        manager = userList[0]
        cashier = userList[1]

def signIn(username , password) :
        # if username in manager.keys() :
        #         if password == manager[username] :
        #                 open("temp" , "w").write(username)
        #                 tkMessageBox.showinfo("Login Status", "Login Successful")
        #                 userText.delete(0, END)
        #                 passText.delete(0, END)
        #                 root.destroy()
        #                 import managerAccount
        #         else :
        #                 tkMessageBox.showinfo("Login Status", "Invalid Username/Password! Please Try Again.")
        #                 passText.delete(0 , END)
        # elif username in cashier.keys() :
        #         if password == cashier[username] :
        #                 open("temp" , "w").write(username)
        #                 tkMessageBox.showinfo("Login Status", "Login Successful")
        #                 userText.delete(0, END)
        #                 passText.delete(0, END)
        #                 root.destroy()
        #                 import cashierAccount
        #         else :
        #                 tkMessageBox.showinfo("Login Status", "Invalid Username/Password! Please Try Again.")
        #                 passText.delete(0 , END)
        # else :
        #         tkMessageBox.showinfo("Login Status", "This Username Doesn't Exist. Please Create An Account!")
        #         userText.delete(0, END)
        #         passText.delete(0, END)     
        # 
        
        mycursor = mydb.cursor()
        sql = "SELECT password, userType FROM Users WHERE username = %s" # INSERT INTO Users (username, password, userType) VALUES (%s, %s, %s)"
        val = (username,)
        mycursor.execute(sql, val)
        results = mycursor.fetchall()
        if (password == results[0][0]):
            if (results[0][1] == 1):
                print("cashier is logged in")
                import managerAccount
            elif (results[0][1] == 2):
                print("manager is loggeed in")
                import cashierAccount
        

def insert(username, password, userType):
        sql = "INSERT INTO Users (username, password, userType) VALUES (%s, %s, %s)"
        val = (username, password, userType)
        try:
            mycursor.execute(sql, val)
            tkMessageBox.showinfo("Login Status", "Congratulations! You Have Successfully Registered.")
        except:
            tkMessageBox.showinfo("Login Status", "Username already exists.")
        mydb.commit()
        regUserText.delete(0 , END)
        regPassText.delete(0 , END)
        regConPassText.delete(0 , END)
        passStrength.config(text = "")

def register(username , password ,confirmPassword , userType) :
    if username == "" or password == "":
        tkMessageBox.showinfo("Login Status", "Please Enter Username And Password.")
    else :
        if len(regPassText.get()) >= 7 :
            if password == confirmPassword :
                    users()
                    if  userType == 1 :
                            manager[username] = password
                            userList[0] = manager
                            insert(username, password, userType)
                    elif userType == 2 :
                            cashier[username] = password
                            userList[1] = cashier
                            insert(username, password, userType)
                    else:
                            tkMessageBox.showinfo("Login Status", "Please Choose Out Of Cashier/Manager")
                            regUserText.delete(0 , END)
                            regPassText.delete(0 , END)
                            regConPassText.delete(0 , END)
                            passStrength.config(text = "")

            else :
                    tkMessageBox.showinfo("Error", "Passwords Do Not Match.")
                    regPassText.delete(0 , END)
                    regConPassText.delete(0 , END)
                    passStrength.config(text = "")
        else :
            tkMessageBox.showinfo("Weak Password", "Please choose a stronger Password.")
            regPassText.delete(0 , END)
            regConPassText.delete(0 , END) 
            passStrength.config(text = "") 
            
                    
def passCheck(event):
    for i in regPassText.get() :
        if (i in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and len(regPassText.get()) >= 10) or len(regPassText.get()) >= 15 :
            passStrength.config(text = "The Password is Very Strong.")
        elif (i in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and len(regPassText.get()) > 7) or (i not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and len(regPassText.get()) >= 10) :
            passStrength.config(text = "The Password is Strong.")
        elif i not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and (15 > len(regPassText.get()) >= 7) :
            passStrength.config(text = "The Password is Weak.")
        elif len(regPassText.get()) <= 6 :
            passStrength.config(text = "The Password is Too Weak.")
    if len(regPassText.get()) == 1 :
        passStrength.config(text = "")
        
root = Tk()
root.title("Login Page")
try :
    root.state("zoomed")
except:
    root.attributes('-fullscreen', True)

projectName = Label(root , text = "pyBill Systems" , font = ("Arial" , 50 , "bold"))
projectName.pack(pady = 100)

loginHead = Label(root , text = "Login" , font = ("Arial" , 20 , "bold"))
loginHead.place(x = 400 , y = 320)

userLabel = Label(root , text = "Username ")
userLabel.place(x = 400 , y = 370)

userText = Entry(root)
userText.place(x = 480 , y = 370)

passLabel = Label(root , text = "Password  ")
passLabel.place(x = 400 , y = 400)

passText = Entry(root , show = "*")
passText.place(x = 480 , y = 400)

login = Button(root , text = "Sign In" , command = lambda: signIn(userText.get(),passText.get()) , width = 28)
login.place(x = 400 , y = 450)

regHead = Label(root , text = "Create Account" , font = ("Arial" , 20 , "bold"))
regHead.place(x = 750 , y = 320)

userTypeLabel = Label(root , text = "User Type ")
userTypeLabel.place(x = 750 , y = 370)

userType = IntVar()
regType1 = Radiobutton(root , text = "Manager" , variable = userType , value = 1)
regType1.place(x = 830 , y = 370)

regType2 = Radiobutton(root , text = "Cashier" , variable = userType , value = 2)
regType2.place(x = 830 , y = 390)

regUserLabel = Label(root , text = "Username ")
regUserLabel.place(x = 750 , y = 420)

regUserText = Entry(root)
regUserText.place(x = 890 , y = 420)

regPassLabel = Label(root , text = "Password  ")
regPassLabel.place(x = 750 , y = 450)

regPassText = Entry(root , show = "*")
regPassText.place(x = 890 , y = 450)
regPassText.bind("<Key>" , passCheck)

passStrength = Label(root)
passStrength.place(x = 1050 , y = 450)

regConPassLabel = Label(root , text = "Confirm Password  ")
regConPassLabel.place(x = 750 , y = 480)

regConPassText = Entry(root , show = "*")
regConPassText.place(x = 890 , y = 480)

signUp = Button(root , text = "Sign Up" , command = lambda: register(regUserText.get().lower(),regPassText.get(),regConPassText.get(),userType.get()), width = 28)
signUp.place(x = 750 , y = 520)

header = Label(root , text = " " , font = ("Arial" , 40))
header.place(x = 690 ,  y = 80 , anchor = CENTER)
               
root.mainloop()
