# managerAccount

from Tkinter import *
import tkMessageBox , ttk , pickle , datetime , re

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

def change(code , x) :
    selections = pickle.load(open("inventory.dat" , "rb"))
    try :
        if float(x) < 0 :
            raise NegativeError
        for i in selections :
            if i.icode == code : 
                k = float(i.qty) 
                k += float(x) 
                i.qty = str(k) 
        pickle.dump(selections , open("inventory.dat" , "wb")) 
        root1.destroy() 
        addItemLayout() 
    except NegativeError: 
        tkMessageBox.showinfo("Quantity Error", "Please Enter A Valid Quantity.") 
        root1.lift() 
    except ValueError : 
        newQty.delete(0 , END) 
        tkMessageBox.showinfo("Value Error", "Please Enter An Integer.") 
        root1.lift()            
            
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
    l = pickle.load(open('inventory.dat','rb'))
    nameList = [[],[]]
    for i in l :
        nameList[0].append(i.item)
        nameList[1].append(i.icode)
    if name.lstrip() == "" or code.lstrip() == "" or price.lstrip() == "" or qty.lstrip() == "" or disc.lstrip() == "" :
        tkMessageBox.showinfo("Input Error","All Fields Are Mandatory.")
    elif (name not in nameList[0]) and (code not in nameList[1]):
        try :
            price , qty , disc = float(price) , float(qty) , float(disc)
            table.insert("" , END , text = name , values = (code , price , qty , disc , tax))        
            a = iteminfo()
            l.append(a)
            a=l[-1]
            a.icode = code
            a.item = name
            a.price = str(price)
            a.qty = str(qty)
            a.disc = str(disc)           
            pickle.dump(l , open('inventory.dat','wb'))            
        except:
            tkMessageBox.showinfo("Data Error","Price , Quantity And Discount Should Be Numerical.")
        productNameText.delete(0 , END)
        productCodeText.delete(0 , END)
        productPriceText.delete(0 , END)
        productQtyText.delete(0 , END)
        productDiscText.delete(0 , END)    
    else :
        tkMessageBox.showinfo("Data Error","Item Name And Item Code Must Be Unique.")
        
def deleteItem1():
    try :        
            selectedItem = table.selection()[0]
            name =  table.item(table.focus())["text"]
            table.delete(selectedItem)
            l = pickle.load(open("inventory.dat" , "rb"))
            for i in l :
                if i.item == name :
                    l.remove(i)
            pickle.dump(l , open("inventory.dat" , "wb"))            
    except :
            tkMessageBox.showinfo("Remove Item", "Please Select An Item.")

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
    
    options = pickle.load(open("inventory.dat" , "rb"))
    for j in options:
        table.insert("" , END , text = j.item , values = (j.icode , j.price , j.qty , j.disc , productTaxText.get() ))

def details(event):    
    try:
        if len(phoneNoText.get()) == 0 :
            raise IOError
        elif len(phoneNoText.get()) in (8,10):
            int(phoneNoText.get())
            file2 = open("details.dat" , "rb")
            det = pickle.load(file2)
            for i in det.keys():
                if i == phoneNoText.get():
                    clientNameText.delete(0 , END)
                    clientNameText.insert(0 , det[i][0])
                    emailText.delete(0 , END)
                    emailText.insert(0 , det[i][1])
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
            for i in selections :
                if variable.get() == i.item :
                    if float(qty) > 0 :
                        if float(qty) <= float(i.qty) :
                            amount = i.calAmount(qty)
                            amountList.append(amount)
                        else:
                            raise PositiveError
                    else :
                        raise NegativeError
                    
            totalText.config(state = NORMAL)
            totalText.delete(0 , END)
            totalText.insert(0 , str(sum(amountList)))
            totalText.config(state = DISABLED)
            
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
        for i in selections :
            if variable.get() == i.item :
                productCodeText.config(state = NORMAL)
                productCodeText.delete(0 , END)
                productCodeText.insert(0 , i.icode)
                productCodeText.config(state = DISABLED)
                productPriceText.config(state = NORMAL)
                productPriceText.delete(0 , END)
                productPriceText.insert(0 , i.price)
                productPriceText.config(state = DISABLED)
                productDiscText.config(state = NORMAL)
                productDiscText.delete(0 , END)
                productDiscText.insert(0 , i.disc)
                productDiscText.config(state = DISABLED)
                break

def deleteItem2():
    try :        
        selectedItem = table.selection()[0]
        name =  table.item(table.focus())["text"]
        qty = table.item(table.focus())["values"][2]
        amt = table.item(table.focus())["values"][5]            
        del(itemDetails[int(selectedItem[1:]) - 1])
        table.delete(selectedItem)
    except :
        tkMessageBox.showinfo("Remove Item", "Please Select An Item.")

    for i in selections :
        if i.item == name :
            k = float(i.qty)
            k += float(qty)
            i.qty = str(k)
            amountList.remove(float(amt))
            totalText.config(state = NORMAL)
            totalText.delete(0 , END)
            totalText.insert(0 , str(sum(amountList)))
            totalText.config(state = DISABLED)

def generateBill() :
    if clientNameText.get().lstrip() == "" or invoiceText.get().lstrip() == "" or float(totalText.get()) == 0:
        tkMessageBox.showinfo("Data Error", "Data Provided Is Insufficient." , icon = "warning")
    else :            
        pickle.dump(selections , open("inventory.dat" , "wb"))
        
        file1 = open(username + ".dat" , "ab")
        clientDetails = [clientNameText.get() , phoneNoText.get() ,  emailText.get() , issueDateText.get() , offerText.get() ,totalText.get() , offerDiscText.get() , grandTotalText.get()]
        d = {"invoiceNumber":invoiceText.get() , 'cDetails': clientDetails , 'iDetails' : itemDetails }
        pickle.dump(d,file1)
        tkMessageBox.showinfo("Congratulations!", "Invoice Has Been Generated." )
        
        file2 = open("details.dat" , "rb")
        det = pickle.load(file2)
        det[phoneNoText.get()] = (clientNameText.get() , emailText.get())
        pickle.dump(det , open("details.dat" , "wb"))
        
        newInvoiceLayout()       
            
def newInvoiceLayout() :
    global body ,phoneNoText , itemDetails ,emailText , grandTotalText , offerDiscText, offerText ,offerLabel ,clientNameText,invoiceText, issueDateText,totalText,table , variable , productCodeText , productPriceText , productQtyText , productDiscText , totalText , selections , amountList

    amountList = []
    itemDetails=[]

    selections = pickle.load(open("inventory.dat" , "rb"))   

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
    
    issueDateLabel = Label(clientFrame , text = "Issue Date (DD/MM/YYYY)")
    issueDateLabel.place(x = 950 , y = 30)

    issueDateText = Entry(clientFrame , width = 23 , disabledforeground = "black" , disabledbackground = "white")
    issueDateText.insert(0 , datetime.datetime.now().strftime('%d/%m/%Y'))
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

    options = pickle.load(open("inventory.dat" , "rb"))
    l = [ a.item for a in options ]

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

    remove = Button(itemFrame , text = "Remove Item" , command = deleteItem2 , width = 10)
    remove.place(x = 1240 , y = 25)

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
    oldTable.bind("<Double-1>", viewBill)    
    
    try :
        bills = open(username + ".dat","rb")
        while True:
            try:            
                j = pickle.load(bills)
                oldTable.insert("" , END , text = j["invoiceNumber"] , values = (j['cDetails'][0] ,  j['cDetails'][1]  ,  j['cDetails'][2]  , j['cDetails'][3] , j['cDetails'][-1]))            
            except EOFError:
                break
    except IOError:
        pass

def viewBill(event):
    def closeBill():
        root1.destroy()
        
    try:
        bills = open(username + ".dat","rb")
        item = oldTable.selection()[0]
    except:
        pass
    else:
        try:
            i = 0
            while i != int (item[1:]):
                j = pickle.load(bills)
                i += 1            
        except EOFError:
            pass     
        root1 = Tk()
        try :
            root1.state("zoomed")
        except:
            root1.attributes('-fullscreen', True)
        root1.title("Old Invoice  : " + j["invoiceNumber"])    
    
        body = Frame(root1 , bd = 5)
        body.pack(side = TOP , fill = BOTH , expand = True)

        clientFrame = LabelFrame(body , text = "Client Details" , font = ("Arial" , 15))
        clientFrame.pack(fill = BOTH)

        phoneNoLabel = Label(clientFrame , text = "Contact Number ")
        phoneNoLabel.place(x = 10 , y = 30)

        phoneNoText = Entry(clientFrame , width = 30 , disabledforeground = "black" , disabledbackground = "white" )
        phoneNoText.place(x = 120 , y = 30)
        phoneNoText.insert(0 , j["cDetails"][1])
        phoneNoText.config(state = DISABLED )
         
        clientNameLabel = Label(clientFrame , text = "Client Name ")
        clientNameLabel.place(x = 10 , y = 80)

        clientNameText = Entry(clientFrame , width = 30 , disabledforeground = "black" , disabledbackground = "white")
        clientNameText.place(x = 120 , y = 80)
        clientNameText.insert(0 , j["cDetails"][0])
        clientNameText.config(state = DISABLED)
        
        emailLabel = Label(clientFrame , text = "Email Address ")
        emailLabel.place(x = 470 , y = 80)

        emailText = Entry(clientFrame , width = 30 , disabledforeground = "black" , disabledbackground = "white")
        emailText.place(x = 610 , y = 80)
        emailText.insert(0 , j["cDetails"][2])
        emailText.config(state = DISABLED )
        
        invoiceLabel = Label(clientFrame , text = "Invoice Number ")
        invoiceLabel.place(x = 470 , y = 30)

        invoiceText = Entry(clientFrame , width = 30 , disabledforeground = "black" , disabledbackground = "white")
        invoiceText.place(x = 610 , y = 30)
        invoiceText.insert(0 , j["invoiceNumber"])
        invoiceText.config(state = DISABLED)
        
        issueDateLabel = Label(clientFrame , text = "Issue Date (DD/MM/YYYY)")
        issueDateLabel.place(x = 950 , y = 30)

        issueDateText = Entry(clientFrame , width = 23 , disabledforeground = "black" , disabledbackground = "white")
        issueDateText.insert(0 , j["cDetails"][3])
        issueDateText.config(state = DISABLED )
        issueDateText.place(x   =  1150 , y = 30)

        offerLabel = Label(clientFrame , text = "Monthly Offer")
        offerLabel.place(x = 950 , y = 80)

        offerText = Entry(clientFrame , width = 23  ,disabledforeground = "black" , disabledbackground = "white")
        offerText.place(x = 1150 , y= 80)
        offerText.insert(0 , j["cDetails"][4])
        offerText.config(state = DISABLED )

        lineBreak = Label(clientFrame , text = "\n\n\n\n\n\n\n")
        lineBreak.pack(side = RIGHT)

        itemFrame = LabelFrame(body , text = "Item Details" , font = ("Arial" , 15))
        itemFrame.pack(fill  =  BOTH , expand = YES)

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
        table.place(x = 10 , y = 10 , height = 400 , width = 1330)
        
        for i in range(len(j["iDetails"])):
                table.insert("" , END , text = j["iDetails"][i][0] , values = (j["iDetails"][i][1] , j["iDetails"][i][2] ,j["iDetails"][i][3] , j["iDetails"][i][4] , j["iDetails"][i][5] , j["iDetails"][i][6]))

        totalLabel = Label(itemFrame , text = "Total")
        totalLabel.place(relx = 1 , rely = 1 , x = -200 , y = -90) 

        totalText = Entry(itemFrame)
        totalText.insert(0 , j["cDetails"][5])
        totalText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
        totalText.place(relx = 1 , rely = 1 , x = -30 , y = -70 , anchor = SE)

        offerDiscLabel = Label(itemFrame , text = "Offer Discount")
        offerDiscLabel.place(relx = 1 , rely = 1 , x = -166 , y = -50 , anchor = SE)
        
        offerDiscText = Entry(itemFrame )
        offerDiscText.place(relx = 1 , rely = 1 , x = -30 , y = -50 , anchor = SE)
        offerDiscText.insert(0 ,j["cDetails"][6])
        offerDiscText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")
        
        grandTotalLabel = Label(itemFrame , text = "Grand Total")
        grandTotalLabel.place(relx = 1 , rely = 1 , x = -166 , y = -30 , anchor = SE)
        
        grandTotalText = Entry(itemFrame )
        grandTotalText.place(relx = 1 , rely = 1 , x = -30 , y = -30 , anchor = SE)
        grandTotalText.insert(0 , j["cDetails"][-1])
        grandTotalText.config(state = DISABLED , disabledforeground = "black" , disabledbackground = "white")

        closeBill = Button(itemFrame , text = "Close" , command =  closeBill, width = 20)
        closeBill.pack(side = BOTTOM , pady = 10)
        
        root1.mainloop()

def aboutLayout():
    global body
    
    body.destroy()

    body = Frame(root , bd = 5)
    body.pack(side = TOP , fill = BOTH , expand = True)

    instructions = Text(body , height = 40)
    instructions.insert(END , "\n 1. Click on Inventory to :\n\n (a) See available items.\n (b) Add new items.\n (c) Remove an item.\n (d) Double click to update quantity of an item.\n\n 2. Click on New Invoice :\n\n (a) Add client details.\n (b) Choose items from existing items and click on Auto Fill.\n (c) Enter quantity.\n (d) Click on Add Item to add it to the bill table.\n (e) Select item and Click  on Remove Item to remove it from the bill table.\n (f) Click on Generate Bill to generate the invoice.\n\n 3. Click on Existing Invoices to : \n\n (a) See Old Invoices.\n (b) Double Click on any invoice to see its detailed copy.\n\n\n\n\n\n\n\n\n\n\n\n\n ------------------------------------------------------------------------------\n CREDITS :\n\n 1. Vansh Goel (XII - A ; 13 ; RDPS ; 2017-18)\n 2. Sarthak Garg (XII - A ; 14 ; RDPS ; 2017-18)\n 3. Tanya Batra (XII - A ; 22 ; RDPS ; 2017-18)")
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
