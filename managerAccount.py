
from Tkinter import *
import tkMessageBox , ttk , pickle , datetime , re
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pyBill"
)

mycursor = mydb.cursor()

def signout() :
    result = tkMessageBox.askquestion("Sign Out", "Are You Sure You Want To Sign Out?", icon='warning')
    if result == "yes" :
            open("temp" , "w").write("")
            root.destroy()
            import main

class NegativeError(Exception) :
    pass

class PositiveError(Exception) :
    pass


   

def calAmount(qty, price, disc) :

    return ((float(price) * float(qty)) * (1 - float(disc)/100.0) * (1 + 18/100.0))

def change(code , x) :
    x=int(x)

    sql = "SELECT quantity FROM items WHERE productCode = %s"
    val = (code,)
    mycursor.execute(sql,val)
    results = mycursor.fetchall()

    x += results[0][0]
    sql = "UPDATE items SET quantity = %s WHERE productCode = %s"
    val = (x, code)
    mycursor.execute(sql,val)
    mydb.commit()
    root1.destroy() 
    addItemLayout() 

            
def editItem(event) :
    global newQty , root1
    
    try:       
        item = table.selection()[0]
    except :
        pass
    else:
        root1 = Tk()
        root1.title("Edit Item")
        productName = Label(root1 , text = table.item(item , "text")).pack(side = TOP)
    
        newQtyLabel = Label(root1 , text = "Enter Quantity To Be Added").pack(side = LEFT , padx = 10)
        newQty = Entry(root1)
        newQty.pack(side = LEFT , padx = 10)
    
        okButton = Button(root1 , text = "Add" , command = lambda : change(table.item(table.focus())["values"][0] , newQty.get()))
        okButton.pack(side = BOTTOM , pady = 5)
        root1.mainloop()
   
def addItem1(name , code , price , qty , disc , tax) :

    if name.lstrip() == "" or code.lstrip() == "" or price.lstrip() == "" or qty.lstrip() == "" or disc.lstrip() == "" :
        tkMessageBox.showinfo("Input Error","All Fields Are Mandatory.")
    else:
        sql = "INSERT INTO items VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, code, price, qty, disc, tax)
        mycursor.execute(sql, val)
        mydb.commit()
        productNameText.delete(0 , END)
        productCodeText.delete(0 , END)
        productPriceText.delete(0 , END)
        productQtyText.delete(0 , END)
        productDiscText.delete(0 , END)
        addItemLayout()
        

        
def deleteItem1():


    selectedItem = table.selection()[0]
    code =  table.item(table.focus())["values"][0]

    sql = "DELETE FROM items WHERE productCode = %s"
    val = (code,)
    mycursor.execute( sql , val )
    mydb.commit()
    addItemLayout()
    
def addItemLayout():
    global body , items , productNameText , table , productCodeText , productPriceText , productQtyText , productDiscText , productTaxText

    body.destroy()
    
    body = Frame(root , bd = 5)
    body.pack(side = TOP , fill = BOTH , expand = True)

    itemFrame = LabelFrame(body , text = "Add Item" , font = ("Arial" , 15))
    itemFrame.pack(fill  =  BOTH)

    lineBreak = Label(itemFrame , text = "\n\n\n\n")
    lineBreak.pack(side = RIGHT)        

    productNameLabel = Label(itemFrame , text  =  "Product Name ")
    productNameLabel.place(x  =  10 , y = 10)

    productNameText = Entry(itemFrame)
    productNameText.place(x = 10 , y = 30)

    productCodeLabel = Label(itemFrame , text  =  "Product Code ")
    productCodeLabel.place(x  =  200 , y = 10)

    productCodeText = Entry(itemFrame)
    productCodeText.place(x  =  200 , y  =  30)

    productPriceLabel = Label(itemFrame , text  =  "Price/Unit (INR)")
    productPriceLabel.place(x  =  390 , y = 10)

    productPriceText = Entry(itemFrame)
    productPriceText.place(x  =  390 , y = 30)

    productQtyLabel = Label(itemFrame , text  =  "Quantity  ")
    productQtyLabel.place(x  =  580 , y = 10)

    productQtyText = Entry(itemFrame)
    productQtyText.place(x  =  580 , y = 30)

    productDiscLabel = Label(itemFrame , text  =  "Discount (%) ")
    productDiscLabel.place(x  =  760 , y = 10)

    productDiscText = Entry(itemFrame)
    productDiscText.place(x  =  760 , y = 30)

    productTaxLabel = Label(itemFrame , text  =  "Tax (%) ")
    productTaxLabel.place(x  =  950 , y = 10)
    
    productTaxText = Entry(itemFrame)
    productTaxText.insert(0 , "18")
    productTaxText.configure(state = DISABLED)
    productTaxText.place(x  =  950 , y = 30)   

    items = [productNameText.get() , productCodeText.get() , productPriceText.get() , productQtyText.get() , productDiscText.get()]
    add = Button(itemFrame , text = "Add Item" , command = lambda : addItem1(productNameText.get().upper() , productCodeText.get().upper() , productPriceText.get() , productQtyText.get() , productDiscText.get() , productTaxText.get()) , width = 10)
    add.place(x = 1120 , y = 25)       

    remove = Button(itemFrame , text = "Remove Item" , command = deleteItem1 , width = 10)
    remove.place(x = 1240 , y = 25)

    itemsInStockFrame = LabelFrame(body , text = "Items Available" , font = ("Arial" , 15))
    itemsInStockFrame.pack(fill  =  BOTH , expand = YES)
        
    table = ttk.Treeview(itemsInStockFrame , selectmode = "extended" , columns = ("code" , "price" , "qty" , "disc" , "tax" , "amnt") , height = 24)
    
    table.heading("#0" , text = "Product Name")
    table.heading("#1" , text = "Product Code")
    table.heading("#2" , text = "Price/Unit (INR)")
    table.heading("#3" , text = "Quantity")
    table.heading("#4" , text = "Discount (%)")
    table.heading("#5" , text = "Tax (%)")
    
    table.column("#0" , minwidth = 500 , width = 500 , stretch = False , anchor = CENTER)
    table.column("#1" , minwidth = 180 , width = 200 , stretch = False , anchor = CENTER)
    table.column("#2" , minwidth = 137 , width = 150 , stretch = False , anchor = CENTER)
    table.column("#3" , minwidth = 130 , width = 150 , stretch = False , anchor = CENTER)
    table.column("#4" , minwidth = 130 , width = 150 , stretch = False , anchor = CENTER)
    table.column("#5" , minwidth = 100 , width = 177 , stretch = False , anchor = CENTER)
    table.place(x = 10 , y = 10 , height = 510 , width = 1330)
    table.bind("<Double-1>", editItem)
    

    mycursor = mydb.cursor()
    sql = "SELECT * FROM items"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for i in results:
        table.insert("" , END , text = i[0] , values = (i[1] , i[2] , i[3] , i[4] , i[5]))

def details(event):    
    try:
        if len(phoneNoText.get()) == 0 :
            raise IOError
        elif len(phoneNoText.get()) in (8,10):

            sql = "SELECT cname, email FROM customers WHERE contactNo = %s"
            val = (phoneNoText.get(), )
            mycursor.execute(sql,val)
            results = mycursor.fetchall()
            clientNameText.delete(0 , END)
            clientNameText.insert(0 , results[0][0])
            emailText.delete(0 , END)
            emailText.insert(0 , results[0][1])
            

        else :
            raise ValueError
    except ValueError:
        tkMessageBox.showinfo("Input Error", "Phone Number Is Invalid." , icon = "warning")
        phoneNoText.delete(0 , END)
        phoneNoText.focus_set()
    except IOError :
        pass

def validateEmail(event):
    if emailText.get() == "" :
        pass
    elif re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" , emailText.get()) == None :
        tkMessageBox.showinfo("Input Error", "Email ID Is Invalid." , icon = "warning")
        emailText.delete(0 , END)
        emailText.focus_set()
    
def offerDecider():
    global flag
    if datetime.datetime.now().strftime('%m') == "02":
        offerText.config(state = NORMAL)
        offerText.insert(0,"End of Season Sale (30%)")
        offerText.config(state = DISABLED)
        flag =1
    elif datetime.datetime.now().strftime('%m') == "10":
        offerText.config(state = NORMAL)
        offerText.insert(0,"Festive Sale (30%)")
        offerText.config(state = DISABLED)
        flag = 1
    else:
        offerText.config(state = NORMAL)
        offerText.insert(0,"No Offer")
        offerText.config(state = DISABLED)
        flag = 0
       
def addItem2(name , code , price , qty , disc , tax) :
    if not code :
        tkMessageBox.showinfo("Data Error", "Please Select An Item And Click On Auto Fill Button.")
    else:        
        try:                    

            if int(qty)>0:
                sql="SELECT quantity FROM items WHERE productCode = %s"
                val = (code, )
                mycursor.execute(sql,val)
                results=mycursor.fetchall()
                if int(qty)<=int(results[0][0]):
                    amount=calAmount(qty,price,disc)
                    amountList.append(amount)
                    newQuantity = int(results[0][0]) - int(qty)
                    sql = "UPDATE items SET quantity = %s WHERE productCode = %s"
                    val = (newQuantity,code)
                    mycursor.execute(sql,val)
                    mydb.commit()
                    totalText.config(state = NORMAL)
                    totalText.delete(0 , END)
                    totalText.insert(0 , str(sum(amountList)))
                    totalText.config(state = DISABLED)
                else:
                    tkMessageBox.showinfo("Data Error", "Quantity is out of stock. Please enter a lower quantity" , icon = "warning")
            
            
            if flag == 1 :               
                offerDiscText.config(state = NORMAL)
                offerDiscText.delete(0 , END)
                offerDiscText.insert (0 , str(-float(offerText.get()[-4:-2:1]) * float(totalText.get())/100))
                offerDiscText.config(state = DISABLED)
                
            grandTotalText.config(state = NORMAL)
            grandTotalText.delete(0 , END)
            grandTotalText.insert(0,str(float(totalText.get()) + float(offerDiscText.get() ))) 
            grandTotalText.config(state = DISABLED)
            
            table.insert("" , END , text = name , values = (code , price , qty , disc , tax , amount))
            itemDetails.append((name , code , price , qty , disc , tax , amount))
            
            variable.set("Choose Item")
            productCodeText.config(state = NORMAL)
            productCodeText.delete(0 , END)
            productCodeText.config(state = DISABLED)
            productPriceText.config(state = NORMAL)
            productPriceText.delete(0 , END)
            productPriceText.config(state = DISABLED)
            productQtyText.delete(0 , END)
            productDiscText.config(state = NORMAL)
            productDiscText.delete(0 , END)            
            productDiscText.config(state = DISABLED)
            
        except NegativeError :
            tkMessageBox.showinfo("Quantity Error", "Please Enter A Valid Quantity.")
        except PositiveError :
            tkMessageBox.showinfo("Quantity Error", "Entered Quamtity Not Available. Please Enter Again.")
        except ValueError:
            tkMessageBox.showinfo("Quantity Error", "Please Enter Quantity.")
            
def autoFill() :    
    if  variable.get() == 'Choose Item':
        tkMessageBox.showinfo("Data Error", "Please Select An Item. ")
    else:
        sql = "SELECT * FROM items WHERE productName = %s"
        variables = variable.get()
        val = (variables,)
        mycursor.execute(sql,val)
        results = mycursor.fetchall()

        productCodeText.config(state = NORMAL)
        productCodeText.delete(0 , END)
        productCodeText.insert(0 , results[0][1])
        productCodeText.config(state = DISABLED)
        productPriceText.config(state = NORMAL)
        productPriceText.delete(0 , END)
        productPriceText.insert(0 , results[0][2])
        productPriceText.config(state = DISABLED)
        productDiscText.config(state = NORMAL)
        productDiscText.delete(0 , END)
        productDiscText.insert(0 , results[0][4])
        productDiscText.config(state = DISABLED)

def generateBill() :
    if clientNameText.get().lstrip() == "" or invoiceText.get().lstrip() == "" or float(totalText.get()) == 0:
        tkMessageBox.showinfo("Data Error", "Data Provided Is Insufficient." , icon = "warning")
    else :            
        sql="SELECT cname FROM customers WHERE contactNo = %s"
        val = (phoneNoText.get(), )
        mycursor.execute(sql,val)
        results = mycursor.fetchall()
        if(results == []):
            sql = "INSERT INTO customers VALUES (%s , %s , %s)"
            val = (phoneNoText.get(),clientNameText.get(), emailText.get())
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            pass
        sql = "INSERT INTO bills VALUES (%s , %s, %s , %s, %s)"
        val = (invoiceText.get(), issueDateText.get(), grandTotalText.get(), phoneNoText.get(), username    )
        mycursor.execute( sql, val)
        mydb.commit()
        tkMessageBox.showinfo("Success", "Congratulations, The invoice has been generated." , icon = "warning")
        newInvoiceLayout()       
            
def newInvoiceLayout() :
    global body ,phoneNoText , itemDetails ,emailText , grandTotalText , offerDiscText, offerText ,offerLabel ,clientNameText,invoiceText, issueDateText,totalText,table , variable , productCodeText , productPriceText , productQtyText , productDiscText , totalText , selections , amountList

    amountList = []
    itemDetails=[]


    body.destroy()
    
    body = Frame(root , bd = 5)
    body.pack(side = TOP , fill = BOTH , expand = True)

    clientFrame = LabelFrame(body , text = "Client Details" , font = ("Arial" , 15))
    clientFrame.pack(fill = BOTH)

    phoneNoLabel = Label(clientFrame , text = "Contact Number ")
    phoneNoLabel.place(x = 10 , y = 30)

    phoneNoText = Entry(clientFrame , width = 30 )
    phoneNoText.place(x = 120 , y = 30)
    phoneNoText.bind("<FocusOut>", details)
     
    clientNameLabel = Label(clientFrame , text = "Client Name ")
    clientNameLabel.place(x = 10 , y = 80)

    clientNameText = Entry(clientFrame , width = 30)
    clientNameText.place(x = 120 , y = 80)    
    
    emailLabel = Label(clientFrame , text = "Email Address ")
    emailLabel.place(x = 470 , y = 80)

    emailText = Entry(clientFrame , width = 30)
    emailText.place(x = 610 , y = 80)
    emailText.bind("<FocusOut>",validateEmail)    
    
    invoiceLabel = Label(clientFrame , text = "Invoice Number ")
    invoiceLabel.place(x = 470 , y = 30)

    invoiceText = Entry(clientFrame , width = 30 , disabledforeground = "black" , disabledbackground = "white")
    invoiceText.place(x = 610 , y = 30)
    invoiceText.insert(0 , datetime.datetime.now().strftime('%d%m%Y%H%M%S'))
    invoiceText.config(state = DISABLED)
    
    issueDateLabel = Label(clientFrame , text = "Issue Date (YYYY-MM-DD)")
    issueDateLabel.place(x = 950 , y = 30)

    issueDateText = Entry(clientFrame , width = 23 , disabledforeground = "black" , disabledbackground = "white")
    issueDateText.insert(0 , datetime.datetime.now().strftime('%Y-%m-%d'))
    issueDateText.config(state = DISABLED )
    issueDateText.place(x   =  1150 , y = 30)

    offerLabel = Label(clientFrame , text = "Monthly Offer")
    offerLabel.place(x = 950 , y = 80)

    offerText = Entry(clientFrame , width = 23 ,state = DISABLED ,disabledforeground = "black" , disabledbackground = "white")
    offerText.place(x = 1150 , y= 80)

    lineBreak = Label(clientFrame , text = "\n\n\n\n\n\n\n")
    lineBreak.pack(side = RIGHT)

    itemFrame = LabelFrame(body , text = "Item Details" , font = ("Arial" , 15))
    itemFrame.pack(fill  =  BOTH , expand = YES)

    productNameLabel = Label(itemFrame , text  =  "Product Name ")
    productNameLabel.place(x  =  10 , y = 10)



    sql = "SELECT productName FROM items"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    l=[]
    for i in results:
        l.append(i[0])
    variable = StringVar()
    variable.set("Choose Item")
    productNameList = apply(OptionMenu , (itemFrame , variable) + tuple(l))
    productNameList.config(width = 15)
    productNameList.place(x = 10 , y = 30)
    
    productCodeLabel = Label(itemFrame , text  =  "Product Code ")
    productCodeLabel.place(x  =  200 , y = 10)

    productCodeText = Entry(itemFrame , state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    productCodeText.place(x  =  200 , y  =  30)

    productPriceLabel = Label(itemFrame , text  =  "Price/Unit (INR) ")
    productPriceLabel.place(x  =  390 , y = 10)

    productPriceText = Entry(itemFrame , state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    productPriceText.place(x  =  390 , y = 30)

    productQtyLabel = Label(itemFrame , text  =  "Quantity  ")
    productQtyLabel.place(x  =  580 , y = 10)

    productQtyText = Entry(itemFrame)
    productQtyText.place(x  =  580 , y = 30)

    productDiscLabel = Label(itemFrame , text  =  "Discount (%) ")
    productDiscLabel.place(x  =  760 , y = 10)

    productDiscText = Entry(itemFrame , state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    productDiscText.place(x  =  760 , y = 30)

    productTaxLabel = Label(itemFrame , text  =  "Tax (%) ")
    productTaxLabel.place(x  =  950 , y = 10)

    productTaxText = Entry(itemFrame)
    productTaxText.insert(0 , "18")
    productTaxText.configure(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    productTaxText.place(x  =  950 , y = 30)
    
    add = Button(itemFrame , text = "Add Item" , command = lambda : addItem2(variable.get() , productCodeText.get() , productPriceText.get() , productQtyText.get() , productDiscText.get() , productTaxText.get()) , width = "10")
    add.place(x = 1120 , y = 25)

    autoFillButton = Button(itemFrame , text = "Auto Fill" , command = autoFill , width = 10)
    autoFillButton.place(x = 12 , y = 65)

    table = ttk.Treeview(itemFrame , selectmode = "extended" , columns = ("code" , "price" , "qty" , "disc" , "tax" , "amnt") , height = 24)
    
    table.heading("#0" , text = "Product Name")
    table.heading("#1" , text = "Product Code")
    table.heading("#2" , text = "Price/Unit (INR)")
    table.heading("#3" , text = "Quantity")
    table.heading("#4" , text = "Discount (%)")
    table.heading("#5" , text = "Tax (%)")
    table.heading("#6" , text = "Amount")
    
    table.column("#0" , minwidth = 500 , width = 500 , stretch = False , anchor = CENTER)
    table.column("#1" , minwidth = 180 , width = 180 , stretch = False , anchor = CENTER)
    table.column("#2" , minwidth = 137 , width = 137 , stretch = False , anchor = CENTER)
    table.column("#3" , minwidth = 130 , width = 130 , stretch = False , anchor = CENTER)
    table.column("#4" , minwidth = 130 , width = 130 , stretch = False , anchor = CENTER)
    table.column("#5" , minwidth = 100 , width = 100 , stretch = False , anchor = CENTER)
    table.column("#6" , minwidth = 150 , width = 150 , stretch = False , anchor = CENTER)
    table.place(x = 10 , y = 100 , height = 300 , width = 1330)

    totalLabel = Label(itemFrame , text = "Total")
    totalLabel.place(relx = 1 , rely = 1 , x = -200 , y = -80) 

    totalText = Entry(itemFrame)
    totalText.insert(0 , "0")
    totalText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    totalText.place(relx = 1 , rely = 1 , x = -30 , y = -60 , anchor = SE)

    offerDiscLabel = Label(itemFrame , text = "Offer Discount")
    offerDiscLabel.place(relx = 1 , rely = 1 , x = -166 , y = -40 , anchor = SE)
    
    offerDiscText = Entry(itemFrame )
    offerDiscText.place(relx = 1 , rely = 1 , x = -30 , y = -40 , anchor = SE)
    offerDiscText.insert(0 , "0")
    offerDiscText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    
    grandTotalLabel = Label(itemFrame , text = "Grand Total")
    grandTotalLabel.place(relx = 1 , rely = 1 , x = -166 , y = -20 , anchor = SE)
    
    grandTotalText = Entry(itemFrame )
    grandTotalText.place(relx = 1 , rely = 1 , x = -30 , y = -20 , anchor = SE)
    grandTotalText.insert(0 , "0")
    grandTotalText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
    
    genBill = Button(itemFrame , text = "Generate Bill" , command = generateBill , width = 20)
    genBill.pack(side = BOTTOM , pady = 10)

    offerDecider()
                       
def oldInvoiceLayout() :
    global body , oldTable
    
    body.destroy()

    body = Frame(root , bd = 5)
    body.pack(side = TOP , fill = BOTH , expand = True)

    heading = Label(body , text = "Invoices" , font = ("Arial" , 30))
    heading.place(x = 575 , y = 20)
    
    oldTable = ttk.Treeview(body , selectmode = "extended" , columns = ( "ClientName" , "phoneNo" , "email" , "issueDate" , "total") , height = 24)
    
    oldTable.heading("#0" , text = "Invoice Number")    
    oldTable.heading("#1" , text = "Client Name")
    oldTable.heading("#2" , text = "Contact Number")
    oldTable.heading("#3" , text = "Email ID")
    oldTable.heading("#4" , text = "Issue Date ")
    oldTable.heading("#5" , text = "Total Amount")

    oldTable.column("#0" , minwidth = 150 , width = 150 , stretch = False , anchor = CENTER)
    oldTable.column("#1" , minwidth = 250 , width = 250 , stretch = False , anchor = CENTER)
    oldTable.column("#2" , minwidth = 150 , width = 150 , stretch = False , anchor = CENTER)
    oldTable.column("#3" , minwidth = 200 , width = 200 , stretch = False , anchor = CENTER)
    oldTable.column("#4" , minwidth = 150 , width = 150 , stretch = False , anchor = CENTER)
    oldTable.column("#5" , minwidth = 150 , width = 150 , stretch = False , anchor = CENTER)    
    oldTable.pack(side = BOTTOM , expand = YES)
    
    try :
        sql = "SELECT * FROM bills, customers WHERE bills.contactNo = customers.contactNo"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for i in results:
            try:            
                oldTable.insert("" , END , text = i[0] , values = (i[6] ,  i[3]  ,  i[7]  , i[1] , i[2]))            
            except EOFError:
                break
    except IOError:
        pass



def aboutLayout():
    global body
    
    body.destroy()

    body = Frame(root , bd = 5)
    body.pack(side = TOP , fill = BOTH , expand = True)

    instructions = Text(body , height = 40)
    instructions.insert(END , "\n 1. Click on New Invoice :\n\n (a) Add client details.\n (b) Choose items from existing items and click on Auto Fill.\n (c) Enter quantity.\n (d) Click on Add Item to add it to the bill table.\n (e) Select item and Click  on Remove Item to remove it from the bill table.\n (f) Click on Generate Bill to generate the invoice.\n\n 2. Click on Existing Invoices to : \n\n (a) See old invoices.\n (b) Double Click on any invoice to see its detailed copy.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n ------------------------------------------------------------------------------\n CREDITS :\n\n 1. Vansh Goel (18BCE0594)\n 2. Tanishk Aggarwal (18BCE0578)\n 3. Sparsh Khurana (18BCE0573)")
    instructions.config(state = DISABLED)
    instructions.pack(side = TOP , expand = True)
        
root = Tk()
root.title("Manager UI")
try :
    root.state("zoomed")
except:
    root.attributes('-fullscreen', True)
    
head = Frame(root , height = 30 , bd = 5)
head.pack(side = TOP , fill = BOTH)

body = Frame(root , bd = 5)
body.pack(side = TOP , fill = BOTH , expand = True)

welcome = Label(body , text = "Welcome to Manager Account" , font = ("Arial" , 40))
welcome.place(x = 350 , y = 300)

username = open("temp" , "r").read()

logout = Button(root , text = "Logout" , command = signout , width = 10)
logout.place(rely = 0, relx = 1, x = 0, y = 0, anchor=NE)

userLabel = Label(root , text = username , font = ("Arial" , 14) , bg = "white" , foreground = "blue")
userLabel.place(rely = 0, relx = 1, x = -120, y = 3, anchor=NE)

items = Button(head , text = "Inventory" , width = 30 , command = addItemLayout)
items.place(x = 0)

newInvoice = Button(head , text = "New Invoice" , width = 30 , command = newInvoiceLayout)
newInvoice.place(x = 250)

oldInvoice = Button(head , text = "Existing Invoices" , width = 30 , command = oldInvoiceLayout)
oldInvoice.place(x = 500)

about = Button(head , text = "Help" , width = 30 , command = aboutLayout)
about.place(x = 750)
    
root.mainloop()
