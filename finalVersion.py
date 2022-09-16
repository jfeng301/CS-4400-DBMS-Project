# from inspect import Parameter
from email import message
from multiprocessing import Manager
# import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pymysql
# import mysql.connector
from tkinter import ttk
# from functools import partial
from datetime import datetime
# import time
import re


class GUI:

    def __init__(self) -> None:
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.LoginPage()

    # 所有测试只要改这里的密码就行了，其他不用动
    def connect(self):
        try:
            self.database = pymysql.connect(host='localhost', user='root', password='.', db='bank_management',
                                            port=3306)  # pwd2: rootroot
            return self.database
        except:
            messagebox.showwarning("Cannot Connect", "Check your internet connection")

    # Screen 19 ✅
    def LoginPage(self):
        self.login = Tk()
        self.login.title("Sign In")
        self.login.config(bg="white")
        self.login.geometry('300x250')

        UserNameLabel = Label(self.login, text='User Name:', bg="SkyBlue3")
        UserNameLabel.place(x=10, y=90)
        self.UserNameEntry = Entry(self.login, width=20)
        self.UserNameEntry.place(x=80, y=90)

        passwordlabel = Label(self.login, text="Password:", bg="SkyBlue2")
        passwordlabel.place(x=10, y=110)
        self.passwordEntry = Entry(self.login, show='*', width=20)
        self.passwordEntry.place(x=80, y=110)

        registerButton = Button(self.login, text="Sign Up", width=8, command=self.registerPage)
        registerButton.place(x=150, y=140)
        loginButton = Button(self.login, text="Sign In", width=8, command=self.loginCheck)
        loginButton.place(x=75, y=140)

        self.login.mainloop()

    def loginCheck(self):
        self.connect()
        cursor = self.database.cursor()
        result = cursor.execute("SELECT perid, pwd FROM person")
        result = cursor.fetchall()

        username = self.UserNameEntry.get()
        self.username = username
        password = self.passwordEntry.get()

        name_list = [it[0] for it in result]

        admin = cursor.execute("select perID from system_admin")
        admin = cursor.fetchall()
        admin = [x[0] for x in admin]

        manager = cursor.execute("select manager from bank")
        manager = cursor.fetchall()
        manager = [x[0] for x in manager]

        employee = cursor.execute("select perID from employee")
        employee = cursor.fetchall()
        employee = [x[0] for x in employee]

        customer = cursor.execute("select perID from customer")
        customer = cursor.fetchall()
        customer = [x[0] for x in customer]

        if not (username and password):
            messagebox.showwarning(title='Warning', message='You must fill in username and password')

        else:
            if username in name_list:
                if password == result[name_list.index(username)][1]:
                    messagebox.showinfo(title='Welcome!', message=' Login!')
                    if self.username in admin:
                        self.adminMenu()
                    elif self.username in manager:
                        if self.username in customer:
                            self.MGRorCUST()
                        else:
                            self.ManagerMenu()
                    elif (self.username in employee) and (self.username not in customer):
                        messagebox.showinfo(title='Error', message='No Menu for Employee')
                    elif self.username in customer:
                        self.customerMenu()
                else:
                    messagebox.showerror(title='Error!', message='Wrong password')
            else:
                messagebox.showerror(title='Error!',
                                     message="Your Username is invalid!\n Please register before login!")

    def MGRorCUST(self):
        self.login.withdraw()
        window = Toplevel()
        window.title('Choose The Menu')
        window.config(bg="white")
        window.geometry("250x150")

        MGRButton = Button(window, text="Manager Menu", command=lambda: [window.destroy(), self.ManagerMenu()])
        MGRButton.place(x=30, y=75)

        CUSTButton = Button(window, text="Customer Menu", command=lambda: [window.destroy(), self.customerMenu()])
        CUSTButton.place(x=140, y=75)

    def registerPage(self):
        self.login.withdraw()
        register = Tk()
        self.register = register
        self.register.title("Sign Up")
        self.register.config(bg="white")
        self.register.geometry("300x250")

        newusernameLabel = Label(self.register, text="Username:", bg="SkyBlue2")
        newusernameLabel.place(x=30, y=40)
        newusernameEntry = Entry(register, width=15)
        newusernameEntry.place(x=100, y=40)
        self.new_username = newusernameEntry

        con_usernameLabel = Label(self.register, text="Confirm Username:", bg="SkyBlue2")
        con_usernameLabel.place(x=60, y=80)
        con_usernameEntry = Entry(register, width=15)
        con_usernameEntry.place(x=170, y=80)
        self.connew_username = con_usernameEntry

        passwordLabel = Label(register, text="Password:", bg="SkyBlue2")
        passwordLabel.place(x=30, y=110)
        passwordEntry = Entry(register, show='*', width=15)
        passwordEntry.place(x=100, y=110)
        self.regpasswordEntry = passwordEntry

        conpasswordLabel = Label(register, text="Confirm Password:", bg="SkyBlue2")
        conpasswordLabel.place(x=60, y=150)
        con_passwordEntry = Entry(register, show='*', width=15)
        con_passwordEntry.place(x=170, y=150)
        self.con_regpasswordEntry = con_passwordEntry

        acceptButton = Button(register, text="Sign Up", width=15,
                              command=lambda: [self.registerNew(), self.register.destroy(), self.LoginPage()])
        acceptButton.place(x=150, y=200)

    def registerNew(self):

        username = self.new_username.get()
        confirmusername = self.connew_username.get()
        password = self.regpasswordEntry.get()
        passwordConfirm = self.con_regpasswordEntry.get()
        self.connect()
        cursor = self.database.cursor()
        sql = "SELECT perid FROM person;"
        cursor.execute(sql)
        perid = []
        for item in cursor:
            if item not in perid:
                perid.append(item)

        if username == '':
            messagebox.showwarning("Username", "You must enter an username!")
        else:
            if username != confirmusername:
                messagebox.showwarning("Username", "Usernames don't match!")

            elif username in perid:
                messagebox.showwarning("Username Not Available", "That username is already in use. Please login.")

            elif username not in perid:
                if password == '':
                    messagebox.showwarning("Passwords", "You must enter an password!")
                elif password != passwordConfirm:
                    messagebox.showwarning("Passwords", "Your passwords don't match!")
                else:
                    newsql = "INSERT INTO person (perID,pwd) VALUES(%s,%s)"
                    cursor.execute(newsql, (username, password))
                    self.database.commit()
                    # newsql2 = "INSERT INTO CREDIT_CARD (CCNumber,ExpiryMonth,ExpiryYear,CVV,Email) VALUES (%s,%s,%s,%s,%s)"
                    # cursor.execute(newsql2, (creditCard, expiryMonth, expiryYear, '333', email))
                    # self.database.commit()
                    messagebox.showinfo("Registered", "You are now registered!")
                    self.register.withdraw()

    # Screen 20 ✅
    def adminMenu(self):
        self.login.withdraw()
        adminMenu = Toplevel()
        self.adminmenu = adminMenu
        self.adminmenu.title("Admin Menu")
        self.adminmenu.config(bg="white")
        self.adminmenu.geometry("700x350")

        viewStatsButton = Button(adminMenu, text="View Stats", width=16, command=self.viewStats)
        viewStatsButton.place(x=200, y=40)

        createCorporationButton = Button(adminMenu, text="Create Corporation", width=16, command=self.CreateCorporation)
        createCorporationButton.place(x=400, y=40)

        manageUsersButton = Button(adminMenu, text="Manage Users", width=16, command=self.manageUsers)
        manageUsersButton.place(x=200, y=80)

        hireWorkerButton = Button(adminMenu, text="Hire Worker", width=16, command=self.HireWorker4Admin)
        hireWorkerButton.place(x=400, y=80)

        replaceManagerButton = Button(adminMenu, text="Replace Manager", width=16, command=self.replaceManager)
        replaceManagerButton.place(x=200, y=120)

        createBankButton = Button(adminMenu, text="Create Bank", width=16, command=self.CreateBank)
        createBankButton.place(x=400, y=120)

        createFeeButton = Button(adminMenu, text="Create Fee", width=16, command=self.CreateFee)
        createFeeButton.place(x=200, y=160)

        manageOverdraftButton = Button(adminMenu, text="Manage Overdraft", width=16, command=self.StartStopOverdraft)
        manageOverdraftButton.place(x=400, y=160)

        payEmployeesButton = Button(adminMenu, text="Pay Employees", width=16, command=self.PayEmployee)
        payEmployeesButton.place(x=200, y=200)

        manageAccountButton = Button(adminMenu, text="Manage Account", width=16,
                                     command=self.manageaccessAdmin)  # ！！！！！！！！！！！！
        manageAccountButton.place(x=400, y=200)

        Quitbutton = Button(adminMenu, text='Quit System', width=12, command=self.login.quit)
        Quitbutton.place(x=350, y=250)

        SwitchAccountButton = Button(adminMenu, text='Switch Account', width=12,
                                     command=lambda: [adminMenu.destroy(), self.LoginPage()])
        SwitchAccountButton.place(x=350, y=300)

    # Screen 21 ✅
    def manageUsers(self):
        self.adminmenu.withdraw()
        manageUsers = Toplevel()
        manageUsers.title("Manage Users")
        manageUsers.config(bg="white")
        manageUsers.geometry("700x350")
        self.manageusers = manageUsers

        createEmployeeButton = Button(self.manageusers, text="Create Employee Role", width=16,
                                      command=self.CreateEmployeeRole)
        createEmployeeButton.place(x=200, y=40)

        createCustomerButton = Button(self.manageusers, text="Create Customer Role", width=16,
                                      command=self.CreateCustomerRole)
        createCustomerButton.place(x=400, y=40)

        stopEmployeeButton = Button(self.manageusers, text="Stop Employee Role", width=16, command=self.StopEmployee)
        stopEmployeeButton.place(x=200, y=80)

        stopCustomerButton = Button(self.manageusers, text="Stop Customer Role", width=16, command=self.StopCustomer)
        stopCustomerButton.place(x=400, y=80)

        Quitbutton = Button(self.manageusers, text='Quit System', width=12, command=self.login.quit)
        Quitbutton.place(x=350, y=250)

        SwitchAccountButton = Button(self.manageusers, text='Back', width=12,
                                     command=lambda: [self.manageusers.destroy(), self.adminMenu()])
        SwitchAccountButton.place(x=350, y=290)

    # Screen 22 ✅
    def viewStats(self):
        self.adminmenu.withdraw()
        self.viewstats = Toplevel()
        self.viewstats.title("View Stats")
        self.viewstats.config(bg="white")
        self.viewstats.geometry("700x350")

        BackButton = Button(self.viewstats, text="Back", width=16,
                            command=lambda: [self.viewstats.destroy(), self.adminMenu()])
        BackButton.place(x=350, y=200)

        displayAccountButton = Button(self.viewstats, text="Display Account Stats", width=20, command=self.accountStats)
        displayAccountButton.place(x=200, y=40)

        displayCorporationButton = Button(self.viewstats, text="Display Corporation Stats", width=20,
                                          command=self.corpStats)
        displayCorporationButton.place(x=400, y=40)

        displayBankButton = Button(self.viewstats, text="Display Bank Stats", width=20, command=self.bankStats)
        displayBankButton.place(x=200, y=80)

        displayCustomerButton = Button(self.viewstats, text="Display Customer Stats", width=20,
                                       command=self.customerStats)
        displayCustomerButton.place(x=400, y=80)

        displayEmployeeButton = Button(self.viewstats, text="Display Employee Stats", width=20,
                                       command=self.EmployeeStats)
        displayEmployeeButton.place(x=200, y=120)

        BackButton = Button(self.viewstats, text="Back", width=16,
                            command=lambda: [self.viewstats.destroy(), self.adminMenu()])
        BackButton.place(x=350, y=200)

    # Screen 24 ✅
    def customerMenu(self):
        self.login.withdraw()
        customerMenu = Toplevel()
        customerMenu.title("Customer Menu")
        customerMenu.config(bg="white")
        customerMenu.geometry("700x350")
        self.customermenu = customerMenu

        managerAccountButton = Button(customerMenu, text="Manage Accounts", width=16, command=self.manageaccessCustomer)
        managerAccountButton.place(x=300, y=40)

        depositWithdrawalButton = Button(customerMenu, text="Deposit /  Withdrawal", width=16,
                                         command=self.MakeDepositWithdrawal)
        depositWithdrawalButton.place(x=300, y=80)

        manageOverdraftButton = Button(customerMenu, text="Manage Overdraft", width=16, command=self.StartStopOverdraft)
        manageOverdraftButton.place(x=300, y=120)

        makeTransferButton = Button(customerMenu, text="Make Transfer", width=16, command=self.MakeAccountTransfer)
        makeTransferButton.place(x=300, y=160)

        Quitbutton = Button(self.customermenu, text='Quit System', width=12, command=self.login.quit)
        Quitbutton.place(x=350, y=250)

        SwitchAccountButton = Button(self.customermenu, text='Switch Account', width=12,
                                     command=lambda: [self.customermenu.destroy(), self.LoginPage()])
        SwitchAccountButton.place(x=350, y=290)

    # Screen 23 ✅
    def ManagerMenu(self):
        self.login.withdraw()
        mgrMenu = Toplevel()
        mgrMenu.title("Manager Menu")
        mgrMenu.config(bg="white")
        mgrMenu.geometry("500x350")
        self.managermenu = mgrMenu

        payemployeeButton = Button(mgrMenu, text="Pay Employees", width=20, command=self.PayEmployee)
        payemployeeButton.place(x=190, y=40)

        HireWorkerButton = Button(mgrMenu, text="Hire Workers", width=20, command=self.HireWorker4Manager)
        HireWorkerButton.place(x=190, y=80)

        Quitbutton = Button(mgrMenu, text='Quit System', width=20, command=self.login.quit)
        Quitbutton.place(x=190, y=120)

        SwitchAccountButton = Button(mgrMenu, text='Switch Account', width=20,
                                     command=lambda: [mgrMenu.destroy(), self.LoginPage()])
        SwitchAccountButton.place(x=190, y=160)

    # Screen 1 ✅
    def CreateCorporation(self):
        self.adminmenu.withdraw()
        createCorporation = Toplevel()
        self.createCorporation = createCorporation
        self.createCorporation.geometry("600x300")
        self.createCorporation.title("Create Corporation")

        corpIDLabel = Label(self.createCorporation, text="Corporation ID", font=("bold", 10))
        corpIDLabel.place(x=20, y=30)
        corpIDEntry = Entry(self.createCorporation)
        corpIDEntry.place(x=180, y=30)
        self.corpID = corpIDEntry

        LongNameLabel = Label(self.createCorporation, text="Long Name", font=("bold", 10))
        LongNameLabel.place(x=20, y=60)
        LongNameEntry = Entry(self.createCorporation)
        LongNameEntry.place(x=180, y=60)
        self.corpLongName = LongNameEntry

        ShortNameLabel = Label(self.createCorporation, text="Short Name", font=("bold", 10))
        ShortNameLabel.place(x=20, y=90)
        ShortNameEntry = Entry(self.createCorporation)
        ShortNameEntry.place(x=180, y=90)
        self.corpShortName = ShortNameEntry

        ResAssetsLabel = Label(self.createCorporation, text="Reserved Assets", font=("bold", 10))
        ResAssetsLabel.place(x=20, y=120)
        ResAssetsEntry = Entry(self.createCorporation)
        ResAssetsEntry.place(x=180, y=120)
        self.corpRA = ResAssetsEntry

        def CreateNewCorporation():
            corpID = self.corpID.get()
            LongName = self.corpLongName.get()
            ShortName = self.corpShortName.get()
            ResAssets = self.corpRA.get()

            self.connect()
            cursor = self.database.cursor()
            sql = f"SELECT corpID FROM corporation;"
            cursor.execute(sql)
            result = cursor.fetchall()

            ExistedCorp = [cp[0] for cp in result]

            if (not (corpID and LongName and ShortName and ResAssets)):
                messagebox.showwarning("Insert Status", "All Fields are Required")
            else:

                if corpID in ExistedCorp:
                    messagebox.showwarning("Insert Failed", "This corporation already exists.")
                elif not (ResAssets.isdigit()):
                    messagebox.showwarning("Insert Status", "Please set the input of Reserved Assets as integer")
                else:
                    con = self.connect()
                    cursor = con.cursor()
                    cursor.execute(
                        f"insert into corporation values('{corpID}', '{LongName}', '{ShortName}', {int(ResAssets)})")
                    cursor.execute("commit")
                    messagebox.showinfo("Insert Status", "Inserted Successfully")
                    con.close()

        CreateNewCorporationButton = Button(self.createCorporation, text='Create Corporation',
                                            command=CreateNewCorporation)
        CreateNewCorporationButton.place(x=150, y=200)

        BackButton = Button(self.createCorporation, text="Back",
                            command=lambda: [self.createCorporation.destroy(), self.adminMenu()])
        BackButton.place(x=400, y=200)

    # Screen 2 ✅
    def CreateBank(self):
        self.adminmenu.withdraw()
        window = Toplevel()
        self.createbank = window
        self.createbank.geometry("600x300")
        self.createbank.title("Bank Management")

        con = self.connect()
        cursor = con.cursor()

        BankID = Label(self.createbank, text="BankID", font=("bold", 10))
        BankID.place(x=30, y=30)

        BankName = Label(self.createbank, text="BankName", font=("bold", 10))
        BankName.place(x=300, y=30)

        AddressInfo = Label(self.createbank, text="Address Info", font=("bold", 10))
        AddressInfo.place(x=30, y=60)

        Street = Label(self.createbank, text="Street", font=("bold", 10))
        Street.place(x=30, y=90)

        City = Label(self.createbank, text="City", font=("bold", 10))
        City.place(x=300, y=90)

        State = Label(self.createbank, text="State", font=("bold", 10))
        State.place(x=30, y=120)

        ZipCode = Label(self.createbank, text="ZipCode", font=("bold", 10))
        ZipCode.place(x=300, y=120)

        OperationInfo = Label(self.createbank, text="Operation Info", font=("bold", 10))
        OperationInfo.place(x=30, y=150)

        ResAssets = Label(self.createbank, text="Reserved Assets", font=("bold", 10))
        ResAssets.place(x=30, y=180)

        CorpID = Label(self.createbank, text="Corporation ID", font=("bold", 10))
        CorpID.place(x=300, y=180)

        ManagerID = Label(self.createbank, text="Manager ID", font=("bold", 10))
        ManagerID.place(x=30, y=210)

        EmployeeID = Label(self.createbank, text="Employee ID", font=("bold", 10))
        EmployeeID.place(x=300, y=210)

        e_bankID = Entry(self.createbank)
        e_bankID.place(x=150, y=30)

        e_BankName = Entry(self.createbank)
        e_BankName.place(x=450, y=30)

        e_Street = Entry(self.createbank)
        e_Street.place(x=150, y=90)

        e_City = Entry(self.createbank)
        e_City.place(x=450, y=90)

        e_State = Entry(self.createbank)
        e_State.place(x=150, y=120)

        e_ZipCode = Entry(self.createbank)
        e_ZipCode.place(x=450, y=120)

        e_ResAssets = Entry(self.createbank)
        e_ResAssets.place(x=150, y=180)

        cursor.execute("SELECT corpID FROM corporation")
        options1 = [i[0] for i in cursor.fetchall()]

        clicked1 = StringVar(master=self.createbank)

        drop1 = OptionMenu(window, clicked1, *options1)
        drop1.pack()
        drop1.place(x=450, y=180)

        cursor.execute("SELECT perID FROM employee")
        options2 = [i[0] for i in cursor.fetchall()]

        clicked2 = StringVar(master=self.createbank)

        drop2 = OptionMenu(window, clicked2, *options2)
        drop2.pack()
        drop2.place(x=150, y=210)

        cursor.execute("SELECT perID FROM employee")
        options3 = [i[0] for i in cursor.fetchall()]

        clicked3 = StringVar(master=self.createbank)

        drop3 = OptionMenu(window, clicked3, *options3)
        drop3.pack()
        drop3.place(x=450, y=210)

        cursor.execute("SELECT manager FROM bank")
        managerList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT perID FROM workfor")
        workforList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT corpID FROM corporation")
        corpList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT perID FROM employee")
        employeeList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT bankID FROM bank")
        bankList = [i[0] for i in cursor.fetchall()]

        def insert():
            BankID = e_bankID.get()
            BankName = e_BankName.get()
            Street = e_Street.get()
            City = e_City.get()
            State = e_State.get()
            ZipCode = e_ZipCode.get()
            ResAssets = e_ResAssets.get()
            CorpID = clicked1.get()
            ManagerID = clicked2.get()
            EmployeeID = clicked3.get()

            if (not (
                    BankID and BankName and Street and City and State and ZipCode and ResAssets and CorpID and ManagerID and EmployeeID)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif BankID in bankList:
                messagebox.showinfo("Insert Status", "Bank already in the system")
            elif not ResAssets.isdigit():
                messagebox.showinfo("Insert Status", "Reserved Assets should be a digit")
            elif CorpID not in corpList:
                messagebox.showinfo("Insert Status", "Corporation does not exist")
            elif ManagerID not in employeeList:
                messagebox.showinfo("Insert Status", "Manager selected is not an employee")
            elif ManagerID in managerList:
                messagebox.showinfo("Insert Status", "Manager is a manager at other bank")
            elif ManagerID in workforList:
                messagebox.showinfo("Insert Status", "Manager is working for other bank")
            elif EmployeeID in managerList:
                messagebox.showinfo("Insert Status", "Employee is a manager at other bank")
            elif EmployeeID not in employeeList:
                messagebox.showinfo("Insert Status", "Employee does not exist")
            else:
                cursor.execute(
                    f"insert into bank values('{BankID}', '{BankName}', '{Street}', '{City}', '{State}', '{ZipCode}', {int(ResAssets)}, '{CorpID}', '{ManagerID}')")
                cursor.execute("commit")
                cursor.execute(f'insert into workfor values("{BankID}", "{EmployeeID}")')
                cursor.execute("commit")

                messagebox.showinfo("Insert Status", "Inserted Successfully")
                con.close()

        insertbutton = Button(self.createbank, text="Create New Bank", bg="white", command=insert)
        insertbutton.place(x=30, y=240)
        BackButton = Button(self.createbank, text="Back", width=16,
                            command=lambda: [self.createbank.destroy(), self.adminMenu()])
        BackButton.place(x=300, y=240)

        window.mainloop()

    # Screen 3 ✅
    def CreateEmployeeRole(self):
        self.manageusers.withdraw()
        window = Toplevel()
        self.createemployee = window
        self.createemployee.geometry("600x300")
        self.createemployee.title("Create Employee Role")

        con = self.connect()
        cursor = con.cursor()

        PersonID = Label(self.createemployee, text="PersonID", font=("bold", 10))
        PersonID.place(x=30, y=30)

        Salary = Label(self.createemployee, text="Salary", font=("bold", 10))
        Salary.place(x=30, y=60)

        NumOfPayment = Label(self.createemployee, text="Num Of Payment", font=("bold", 10))
        NumOfPayment.place(x=30, y=90)

        AccumulatedEarning = Label(self.createemployee, text="Accumulated Earning", font=("bold", 10))
        AccumulatedEarning.place(x=30, y=120)

        cursor.execute("SELECT perID FROM person")
        options1 = [i[0] for i in cursor.fetchall()]

        clicked1 = StringVar(master=self.createemployee)

        e_PersonID = OptionMenu(self.createemployee, clicked1, *options1)
        e_PersonID.pack()
        e_PersonID.place(x=170, y=30)

        e_Salary = Entry(self.createemployee)
        e_Salary.place(x=170, y=60)

        e_NumOfPayment = Entry(self.createemployee)
        e_NumOfPayment.place(x=170, y=90)

        e_AccumulatedEarning = Entry(self.createemployee)
        e_AccumulatedEarning.place(x=170, y=120)

        cursor.execute("SELECT perID FROM system_admin")
        AdminList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT perID FROM employee")
        EmployeeList = [i[0] for i in cursor.fetchall()]

        def insert():
            PersonID = clicked1.get()
            Salary = e_Salary.get()
            NumOfPayment = e_NumOfPayment.get()
            AccumulatedEarning = e_AccumulatedEarning.get()

            if (not (PersonID and Salary and NumOfPayment and AccumulatedEarning)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif (not (Salary.isdigit() and NumOfPayment.isdigit() and AccumulatedEarning.isdigit() )):
                messagebox.showinfo("Insert Status", "Inputs must be integer")
            elif PersonID in AdminList:
                messagebox.showinfo("Insert Status", "User is an admin")
            elif PersonID in EmployeeList:
                messagebox.showinfo("Insert Status", "User is an employee")
            else:
                con = self.connect()
                cursor = con.cursor()
                cursor.execute(
                    f'insert into employee values("{PersonID}", "{Salary}", "{NumOfPayment}", {AccumulatedEarning})')
                cursor.execute("commit")

                messagebox.showinfo("Insert Status", "Inserted Successfully")
                con.close()

        insertbutton = Button(self.createemployee, text="INSERT", bg="white", command=insert)
        insertbutton.place(x=20, y=160)
        BackButton = Button(self.createemployee, text="Back", width=16,
                            command=lambda: [self.createemployee.destroy(), self.manageUsers()])
        BackButton.place(x=300, y=160)

    # Screen 4 ✅
    def CreateCustomerRole(self):
        self.manageusers.withdraw()
        window = Toplevel()
        window.geometry("600x300")
        window.title("Create Customer Role")
        self.createcustomerrole = window

        con = self.connect()
        cursor = con.cursor()

        PersonID = Label(window, text="PersonID", font=("bold", 10))
        PersonID.place(x=30, y=30)

        cursor.execute("SELECT perID FROM person")
        options1 = [i[0] for i in cursor.fetchall()]

        clicked1 = StringVar(master=window)

        e_PersonID = OptionMenu(window, clicked1, *options1)
        e_PersonID.pack()
        e_PersonID.place(x=150, y=30)

        cursor.execute("SELECT perID FROM system_admin")
        AdminList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT perID FROM customer")
        CustomerList = [i[0] for i in cursor.fetchall()]

        def insert():
            PersonID = clicked1.get()

            if (not (PersonID)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif PersonID in AdminList:
                messagebox.showinfo("Insert Status", "User is an admin")
            elif PersonID in CustomerList:
                messagebox.showinfo("Insert Status", "User is an customer")
            else:
                con = self.connect()
                cursor = con.cursor()
                cursor.execute(f'insert into customer values("{PersonID}")')
                cursor.execute("commit")

                messagebox.showinfo("Insert Status", "Inserted Successfully")
                con.close()

        insertbutton = Button(window, text="INSERT", bg="white", command=insert)
        insertbutton.place(x=20, y=140)
        BackButton = Button(self.createcustomerrole, text="Back", width=16,
                            command=lambda: [self.createcustomerrole.destroy(), self.manageUsers()])
        BackButton.place(x=300, y=160)

    # Screen 5 - Stop Customer ✅
    def StopCustomer(self):
        self.manageusers.withdraw()
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT perID FROM customer")
        options = [i[0] for i in cursor.fetchall()]

        window = Toplevel()
        window.title("Screen 5: Stop Customer")
        window.geometry("600x300")

        Label(window, text='Person ID:').place(x=60, y=30)

        clicked1 = StringVar(master=window)

        drop = OptionMenu(window, clicked1, *options)
        drop.pack()
        drop.place(x=270, y=30)

        cursor.execute("SELECT perID FROM employee")
        employeeList = [i[0] for i in cursor.fetchall()]

        def deleteCus():

            customer = clicked1.get()
            print(customer)
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT bankID, accountID FROM access GROUP BY bankID, accountID HAVING count(*) = 1")
            single = [[i[0], i[1]] for i in cursor.fetchall()]
            cursor.execute(f"SELECT bankID, accountID FROM access WHERE perID='{customer}'")
            account = [[i[0], i[1]] for i in cursor.fetchall()]

            status = False

            for i in account:
                if i in single:
                    status = True
                    break

            if not customer:
                messagebox.showinfo("Delete Status", "All Fields are Required")
            elif status:
                messagebox.showinfo("Delete Status", "Customer is the only holder of an account")
            elif customer in employeeList:
                cursor.execute(f'DELETE FROM access WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM customer_contacts WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM customer WHERE perID = "{customer}"')
                cursor.execute("commit")

                messagebox.showinfo("Delete Status", "Still an Employee. Deleted Successfully from Customer")
                #connection.close()
            else:
                cursor.execute(f'DELETE FROM access WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM customer_contacts WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM customer WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM bank_user WHERE perID = "{customer}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM person WHERE perID = "{customer}"')
                cursor.execute("commit")

                messagebox.showinfo("Delete Status", "Deleted Successfully from the system")
                #connection.close()

        BackButton = Button(window, text="Cancel", command=lambda: [window.destroy(), self.manageUsers()])
        BackButton.place(x=240, y=120)
        btn_login = Button(window, text='Confirm', command=deleteCus)
        btn_login.place(x=330, y=120)

    # Screen 5 - Stop Employee ✅
    def StopEmployee(self):
        self.manageusers.withdraw()
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT perID FROM employee")
        options = [i[0] for i in cursor.fetchall()]

        window = Toplevel()
        window.title("Screen 5: Stop Employee")
        window.geometry("600x300")

        Label(window, text='Person ID:').place(x=60, y=30)

        clicked1 = StringVar(master=window)

        drop = OptionMenu(window, clicked1, *options)
        drop.pack()
        drop.place(x=270, y=30)

        cursor.execute("SELECT manager FROM bank")
        managerList = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT perID FROM customer")
        customerList = [i[0] for i in cursor.fetchall()]

        def deleteEmp():

            employee = clicked1.get()

            cursor.execute(f"SELECT bankID FROM workfor WHERE perID = '{employee}'")
            bank = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT count(*) FROM workfor WHERE bankID = '{bank}'")
            num = cursor.fetchall()[0][0]

            if not employee:
                messagebox.showinfo("Delete Status", "All Fields are Required")
            elif employee in managerList:
                messagebox.showinfo("Delete Status", "Employee is manager of a bank")
            elif num == 1:
                messagebox.showinfo("Delete Status", "Employee is last employee at the bank")
            elif employee in customerList:
                cursor.execute(f'DELETE FROM workfor WHERE perID = "{employee}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM employee WHERE perID = "{employee}"')
                cursor.execute("commit")

                messagebox.showinfo("Delete Status", "Still a customer. Deleted Successfully from Employee")
            else:
                cursor.execute(f'DELETE FROM workfor WHERE perID = "{employee}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM employee WHERE perID = "{employee}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM bank_user WHERE perID = "{employee}"')
                cursor.execute("commit")
                cursor.execute(f'DELETE FROM person WHERE perID = "{employee}"')
                cursor.execute("commit")

                messagebox.showinfo("Delete Status", "Deleted Successfully from the system")
                connection.close()

        BackButton = Button(window, text="Cancel", command=lambda: [window.destroy(), self.manageUsers()])
        BackButton.place(x=240, y=120)
        btn_login = Button(window, text='Confirm', command=deleteEmp)
        btn_login.place(x=330, y=120)

     # Screen 6 Still need to be improved✅
    def HireWorker4Admin(self):

        self.adminmenu.withdraw()
        window = Toplevel()
        window.geometry("600x300")
        window.title("Hire Worker")

        con = self.connect()
        cursor = con.cursor()

        Bank = Label(window, text="Bank", font=("bold", 10))
        Bank.place(x=30, y=30)
        cursor.execute("SELECT distinct(bankID) FROM bank")
        bankList = [i[0] for i in cursor.fetchall()]
        clicked1 = StringVar(master=window)
        bankList1 = OptionMenu(window, clicked1, *bankList)
        bankList1.pack()
        bankList1.place(x=150, y=30)

        employee = Label(window, text="Employee", font=("bold", 10))
        employee.place(x=30, y=60)
        cursor.execute("SELECT distinct(perID) FROM workFor")
        perList = [i[0] for i in cursor.fetchall()]
        clicked2 = StringVar(master=window)
        employeeList1 = OptionMenu(window, clicked2, *perList)
        employeeList1.pack()
        employeeList1.place(x=150, y=60)

        def update():

            Bank = clicked1.get()
            Employee = clicked2.get()
            # print(BankAccount)

            # sqlchecking = "SELECT count(*) FROM workFor where bankID = %s and perID = %s;"
            cursor.execute(f'SELECT distinct(perID) FROM workFor where bankID = "{Bank}";')
            check= [i[0] for i in cursor.fetchall()]

            if (not (Bank and Employee)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif (Employee in check):
                messagebox.showinfo("Insert Status", "The worker is working for this bank")
            else:
                sql3 = 'SET FOREIGN_KEY_CHECKS=0;'
                cursor.execute(sql3)
                cursor.execute(f'INSERT INTO workFor VALUES ("{Bank}", "{Employee}");')

                cursor.execute("commit")
                sql4 = 'SET FOREIGN_KEY_CHECKS=1;'
                cursor.execute(sql4)
                messagebox.showinfo("Insert Status", "Insert Successfully")

        insert = Button(window, text="Create", bg="white", command=update)
        insert.place(x=30, y=90)
        BackButton = Button(window, text="Back", command=lambda: [window.destroy(), self.adminMenu()])
        BackButton.place(x=150, y=90)

    # Screen 6 Still need to be improved
    def HireWorker4Manager(self):

            self.ManagerMenu
            window = Toplevel()
            window.geometry("600x300")
            window.title("Hire Worker For Manager")

            con = self.connect()
            cursor = con.cursor()

            Bank = Label(window, text="Bank", font=("bold", 10))
            Bank.place(x=30, y=30)
            cursor.execute("SELECT bankID FROM bank")
            bankList = [i[0] for i in cursor.fetchall()]
            clicked1 = StringVar(master=window)
            bankList1 = OptionMenu(window, clicked1, *bankList)
            bankList1.pack()
            bankList1.place(x=150, y=30)

            employee = Label(window, text="Employee", font=("bold", 10))
            employee.place(x=30, y=60)
            cursor.execute("SELECT distinct(perID) FROM employee")
            perList = [i[0] for i in cursor.fetchall()]
            clicked2 = StringVar(master=window)
            employeeList1 = OptionMenu(window, clicked2, *perList)
            employeeList1.pack()
            employeeList1.place(x=150, y=60)

            def update():

                Bank = clicked1.get()
                Employee = clicked2.get()
                # print(BankAccount)

                # sqlchecking = "SELECT count(*) FROM workFor where bankID = %s and perID = %s;"
                cursor.execute(f'SELECT perID FROM workFor where bankID = "{Bank}";')
                check= [i[0] for i in cursor.fetchall()]

                cursor.execute(f'SELECT manager FROM bank;')
                check2= [i[0] for i in cursor.fetchall()]

                if (not (Bank and Employee)):
                    messagebox.showinfo("Insert Status", "All Fields are Required")
                elif (Employee in check):
                    messagebox.showinfo("Insert Status", "The worker is working for this bank")
                elif (Employee in check2):
                    messagebox.showinfo("Insert Status", "The worker is a manager at other bank")
                else:
                    sql3 = 'SET FOREIGN_KEY_CHECKS=0;'
                    cursor.execute(sql3)
                    cursor.execute(f'INSERT INTO workFor VALUES ("{Bank}", "{Employee}");')

                    cursor.execute("commit")
                    sql4 = 'SET FOREIGN_KEY_CHECKS=1;'
                    cursor.execute(sql4)
                    messagebox.showinfo("Insert Status", "Insert Successfully")

            insert = Button(window, text="Create", bg="white", command=update)
            insert.place(x=30, y=90)
            BackButton = Button(window, text="Back", command=lambda: [window.destroy(), self.ManagerMenu()])
            BackButton.place(x=150, y=90)

            # self.window.mainloop()

    # Screen 7 ✅
    def replaceManager(self):

        self.adminmenu.withdraw()
        window = Toplevel()
        window.geometry("600x300")
        window.title("Replace Manager")

        con = self.connect()
        cursor = con.cursor()

        Bank = Label(window, text="Bank", font=("bold", 10))
        Bank.place(x=30, y=30)
        cursor.execute("SELECT bankID FROM bank")
        bankList = [i[0] for i in cursor.fetchall()]
        clicked1 = StringVar(master=window)
        bankList1 = OptionMenu(window, clicked1, *bankList)
        bankList1.pack()
        bankList1.place(x=150, y=30)

        employee = Label(window, text="Employee", font=("bold", 10))
        employee.place(x=30, y=60)
        cursor.execute("SELECT perID FROM employee")
        perList = [i[0] for i in cursor.fetchall()]
        clicked2 = StringVar(master=window)
        employeeList1 = OptionMenu(window, clicked2, *perList)
        employeeList1.pack()
        employeeList1.place(x=150, y=60)

        salary = Label(window, text="New Salary", font=("bold", 10))
        salary.place(x=30, y=90)
        input_Salary = Entry(window)
        input_Salary.place(x=150, y=90)

        def update():

            Bank = clicked1.get()
            Employee = clicked2.get()
            newSalary = input_Salary.get()
            # print(BankAccount)

            cursor.execute(f'SELECT manager FROM bank where bankID = "{Bank}";')
            check = cursor.fetchone()

            cursor.execute(f'SELECT manager FROM bank;')
            check1 = cursor.fetchall()
            mgrlist = [i[0] for i in check1 ]

            if (not (salary and Employee)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif (Employee in check):
                messagebox.showinfo("Insert Status", "Choose the Old Manager")
            elif (Employee in mgrlist):
                messagebox.showinfo("Insert Status", "The Employee Selected has alreday been a manager.")
            elif not (newSalary.isdigit()):
                messagebox.showerror("Insert Status",'Salary should be a number.')
            else:
                sql3 = 'SET FOREIGN_KEY_CHECKS=0;'
                cursor.execute(sql3)
                # cursor.execute(f"update bank set manager = 'Employee' where bankID = 'Bank';" )
                cursor.execute(f'update bank set manager = "{Employee}" where bankID = "{Bank}";')
                cursor.execute(f'update employee set salary = "{newSalary}" where perID = "{Employee}" ;')
                cursor.execute("commit")
                sql4 = 'SET FOREIGN_KEY_CHECKS=1;'
                cursor.execute(sql4)
                messagebox.showinfo("Insert Status", "Insert Successfully")

        insert = Button(window, text="Create", bg="white", command=update)
        insert.place(x=30, y=120)
        BackButton = Button(window, text="Back", command=lambda: [window.destroy(), self.adminMenu()])
        BackButton.place(x=150, y=120)

    # Screen 8 Manage Account for Customer ✅
    def manageaccessCustomer(self):
        self.customermenu.withdraw()
        window = Toplevel()
        window.geometry("600x500")
        window.title("Manage Account - Customer")

        con = self.connect()
        cursor = con.cursor()

        # LEFT
        leftLabel = Label(window, text="Existing Account: Add/Remove Owners")
        leftLabel.place(x=250, y=20)

        requesterLabel = Label(window, text='Accessible Accounts')
        requesterLabel.place(x=30, y=80)

        requester = Label(window, text=self.username)
        requester.place(x=30, y=100)

        # dropdown1
        #cursor.execute("SELECT perID FROM customer")
        #requester = [i[0] for i in cursor.fetchall()]

        #requesterOptions = StringVar(window)
        #requesterOptions.set('Accessible Accounts')
        #requesterDrop = OptionMenu(window, requesterOptions, *requester)
        #requesterDrop.pack()
        #requesterDrop.place(x=30, y=70)

        # dropdown2
        cursor.execute("SELECT perID FROM customer")
        customer = [i[0] for i in cursor.fetchall()]

        customerOptions = StringVar(window)
        customerOptions.set('Customer')
        customerDrop = OptionMenu(window, customerOptions, *customer)
        customerDrop.pack()
        customerDrop.place(x=30, y=110)

        # dropdown3
        operationOptions = StringVar(window)
        operationOptions.set('Operation')
        operationDrop = OptionMenu(window, operationOptions, 'Add Owner', 'Remove Owner')
        operationDrop.pack()
        operationDrop.place(x=30, y=150)

        # RIGHT

        # dropdown4
        cursor.execute("SELECT bankID FROM bank")
        bank = [i[0] for i in cursor.fetchall()]

        bankOptions = StringVar(window)
        bankOptions.set('Bank')
        bankDrop = OptionMenu(window, bankOptions, *bank)
        bankDrop.pack()
        bankDrop.place(x=300, y=60)

        # accountID
        accountIDLabel = Label(window, text="AccountID")
        accountIDLabel.place(x=300, y=90)

        AccountID = Entry(window)
        AccountID.place(x=300, y=110)

        def confirm():
            operation_ = operationOptions.get()
            requester_ = self.username
            customer_ = customerOptions.get()
            bank_ = bankOptions.get()
            accountID_ = AccountID.get()
            dtStartShare_ = datetime.today().strftime('%Y-%m-%d')

            cursor.execute(f'select perID from access where bankID= "{bank_}" and accountID= "{accountID_}" ')
            ip_requester = cursor.fetchall()
            ip_requester = [x[0] for x in ip_requester]
            print(ip_requester)

            cursor.execute("select bankID,accountID from bank_account")
            ip_access = cursor.fetchall()
            ip_access = [(x[0], x[1]) for x in ip_access]
            print(ip_access)

            cursor.execute("select perID,bankID,accountID from access")
            ip_dup = cursor.fetchall()
            ip_dup = [(x[0], x[1],x[2]) for x in ip_dup]
            print(ip_dup)

            if operation_ =='Operation':
                messagebox.showinfo("Insert Status", "Fields are Required")

            if operation_ == 'Add Owner':

                if requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif (bank_, accountID_) not in ip_access:
                    messagebox.showinfo("Insert Status", "Input must be a valid account")
                elif requester_ not in ip_requester:
                    messagebox.showinfo("Insert Status", "No Permission")
                elif (customer_, bank_, accountID_) in ip_dup:
                    messagebox.showinfo("Insert Status", "Duplicated Access")
                else:
                    args = (
                    requester_, customer_, None, bank_, accountID_, None, None, None, None, None, None, dtStartShare_)
                    print(args)
                    cursor.callproc('add_account_access', args)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

            if operation_ == 'Remove Owner':

                if requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif requester_ not in ip_requester:
                    messagebox.showinfo("Insert Status", "No Permission")
                elif customer_ not in ip_requester:
                    messagebox.showinfo("Insert Status", "Invalid Owner")
                else:
                    argss = (requester_, customer_, bank_, accountID_)
                    cursor.callproc('remove_account_access', argss)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

        confirmbutton = Button(window, text="Comfirm", bg="white", command=confirm)
        confirmbutton.place(x=320, y=200)
        back = Button(window, text="Back", bg="white", command=lambda: [window.destroy(), self.customerMenu()])
        back.place(x=150, y=200)

    # Screen 8 Manage Account for Admin ✅
    def manageaccessAdmin(self):
        self.adminmenu.withdraw()
        window = Toplevel()
        window.geometry("600x500")
        window.title("Manage Account - For Admin")

        con = self.connect()
        cursor = con.cursor()

        # LEFT
        leftLabel = Label(window, text="Existing Account: Add/Remove Owners")
        leftLabel.place(x=30, y=20)

        # dropdown1
        cursor.execute("SELECT perID FROM system_admin")
        requester = [i[0] for i in cursor.fetchall()]

        requesterOptions = StringVar(window)
        requesterOptions.set('Accessible Accounts')
        requesterDrop = OptionMenu(window, requesterOptions, *requester)
        requesterDrop.pack()
        requesterDrop.place(x=30, y=70)

        # dropdown2
        cursor.execute("SELECT perID FROM customer")
        customer = [i[0] for i in cursor.fetchall()]

        customerOptions = StringVar(window)
        customerOptions.set('Customer')
        customerDrop = OptionMenu(window, customerOptions, *customer)
        customerDrop.pack()
        customerDrop.place(x=30, y=110)

        # dropdown3
        operationOptions = StringVar(window)
        operationOptions.set('Operation')
        operationDrop = OptionMenu(window, operationOptions, 'Add Owner', 'Remove Owner')
        operationDrop.pack()
        operationDrop.place(x=30, y=150)

        # RIGHT
        rightLabel = Label(window, text="Create New Account")
        rightLabel.place(x=300, y=20)

        # dropdown4
        cursor.execute("SELECT bankID FROM bank")
        bank = [i[0] for i in cursor.fetchall()]

        bankOptions = StringVar(window)
        bankOptions.set('Bank')
        bankDrop = OptionMenu(window, bankOptions, *bank)
        bankDrop.pack()
        bankDrop.place(x=300, y=60)

        # accountID
        accountIDLabel = Label(window, text="AccountID")
        accountIDLabel.place(x=300, y=90)

        AccountID = Entry(window)
        AccountID.place(x=300, y=110)

        # dropdown5
        typeOptions = StringVar(window)
        typeOptions.set('Account Type')
        typeDrop = OptionMenu(window, typeOptions, 'checking', 'savings', 'market')
        typeDrop.pack()
        typeDrop.place(x=300, y=150)

        # bottom
        noteLabel = Label(window, text="If not applicable, please fill in with 0")
        noteLabel.place(x=150, y=180)

        initialBalanceLabel = Label(window, text="Initial Balance")
        initialBalanceLabel.place(x=50, y=200)
        initialBalance = Entry(window)
        initialBalance.place(x=50, y=220)

        interestRateLabel = Label(window, text="Interest Rate")
        interestRateLabel.place(x=280, y=200)
        interestRate = Entry(window)
        interestRate.place(x=280, y=220)

        minBalanceLabel = Label(window, text="Min Balance")
        minBalanceLabel.place(x=50, y=250)
        minBalance = Entry(window)
        minBalance.place(x=50, y=270)

        maxWithdrawLabel = Label(window, text="Max Withdraw")
        maxWithdrawLabel.place(x=280, y=250)
        maxWithdraw = Entry(window)
        maxWithdraw.place(x=280, y=270)

        numWithdrawLabel = Label(window, text="Num Withdrawal")
        numWithdrawLabel.place(x=50, y=300)
        numWithdraw = Entry(window)
        numWithdraw.place(x=50, y=320)

        dtDepositLabel = Label(window, text="Date Deposit")
        dtDepositLabel.place(x=280, y=300)
        dtDeposit = Entry(window)
        dtDeposit.place(x=280, y=320)

        def confirm():
            operation_ = operationOptions.get()
            format = "%Y-%m-%d"

            if operation_ =='Operation':
                messagebox.showinfo("Insert Status", "Fields are Required")

            elif operation_ == 'Add Owner':

                requester_ = requesterOptions.get()
                customer_ = customerOptions.get()
                bank_ = bankOptions.get()
                accountID_ = AccountID.get()
                type_ = typeOptions.get()
                initialBalance_ = initialBalance.get()
                interestRate_ = interestRate.get()
                minBalance_ = minBalance.get()
                maxWithdraw_ = maxWithdraw.get()
                numWithdraw_ = numWithdraw.get()
                dtDeposit_ = dtDeposit.get()
                dtStartShare = datetime.today().strftime('%Y-%m-%d')

                cursor.execute("select perID,bankID,accountID from access")
                ip_dup = cursor.fetchall()
                ip_dup = [(x[0], x[1],x[2]) for x in ip_dup]
                print(ip_dup)

                cursor.execute(f'select perID from access where bankID= "{bank_}" and accountID= "{accountID_}" ')
                ip_requester = cursor.fetchall()
                ip_requester = [x[0] for x in ip_requester]
                print(ip_requester)

                if requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank' or type_ =='Account Type':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not accountID_ or not initialBalance_ or not interestRate_ or not minBalance_ or not maxWithdraw_ or not numWithdraw_:
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not initialBalance_.isdigit() or not interestRate_.isdigit() or not minBalance_.isdigit() or not maxWithdraw_.isdigit() or not numWithdraw_.isdigit():
                    messagebox.showinfo("Insert Status", "Inputs must be integer")
                elif int(interestRate_)>100:
                    messagebox.showinfo("Insert Status", "Must be a valid Interest Rate")
                elif not re.fullmatch("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", dtDeposit_):
                    messagebox.showinfo("Insert Status", "Input must be a valid date")
                elif (customer_, bank_, accountID_) in ip_dup:
                    messagebox.showinfo("Insert Status", "Duplicated Access")
                else:
                    args = (requester_, customer_, type_, bank_, accountID_, int(initialBalance_), int(interestRate_), dtDeposit_,
                            int(minBalance_), int(numWithdraw_), int(maxWithdraw_), dtStartShare)
                    cursor.callproc('add_account_access', args)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

            if operation_ == 'Remove Owner':

                requester_ = requesterOptions.get()
                customer_ = customerOptions.get()
                bank_ = bankOptions.get()
                accountID_ = AccountID.get()

                if requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not accountID_:
                    messagebox.showinfo("Insert Status", "Account ID is Required")
                elif customer_ not in ip_requester:
                    messagebox.showinfo("Insert Status", "Invalid Owner")
                else:
                    argss = (requester_, customer_, bank_, accountID_)
                    cursor.callproc('remove_account_access', argss)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

        confirmbutton = Button(window, text="Comfirm", bg="white", command=confirm)
        confirmbutton.place(x=320, y=370)

        back = Button(window, text="Back", bg="white", command=lambda: [window.destroy(), self.adminMenu()])
        back.place(x=150, y=370)

        self.adminmenu.withdraw()
        window = Tk()
        window.geometry("600x500")
        window.title("Manage Account - For Admin")

        con = self.connect()
        cursor = con.cursor()

        # LEFT
        leftLabel = Label(window, text="Existing Account: Add/Remove Owners")
        leftLabel.place(x=30, y=20)

        # dropdown1
        cursor.execute("SELECT perID FROM system_admin")
        requester = [i[0] for i in cursor.fetchall()]

        requesterOptions = StringVar(window)
        requesterOptions.set('Accessible Accounts')
        requesterDrop = OptionMenu(window, requesterOptions, *requester)
        requesterDrop.pack()
        requesterDrop.place(x=30, y=70)

        # dropdown2
        cursor.execute("SELECT perID FROM customer")
        customer = [i[0] for i in cursor.fetchall()]

        customerOptions = StringVar(window)
        customerOptions.set('Customer')
        customerDrop = OptionMenu(window, customerOptions, *customer)
        customerDrop.pack()
        customerDrop.place(x=30, y=110)

        # dropdown3
        operationOptions = StringVar(window)
        operationOptions.set('Operation')
        operationDrop = OptionMenu(window, operationOptions, 'Add Owner', 'Remove Owner')
        operationDrop.pack()
        operationDrop.place(x=30, y=150)

        # RIGHT
        rightLabel = Label(window, text="Create New Account")
        rightLabel.place(x=300, y=20)

        # dropdown4
        cursor.execute("SELECT bankID FROM bank")
        bank = [i[0] for i in cursor.fetchall()]

        bankOptions = StringVar(window)
        bankOptions.set('Bank')
        bankDrop = OptionMenu(window, bankOptions, *bank)
        bankDrop.pack()
        bankDrop.place(x=300, y=60)

        # accountID
        accountIDLabel = Label(window, text="AccountID")
        accountIDLabel.place(x=300, y=90)

        AccountID = Entry(window)
        AccountID.place(x=300, y=110)

        # dropdown5
        typeOptions = StringVar(window)
        typeOptions.set('Account Type')
        typeDrop = OptionMenu(window, typeOptions, 'checking', 'savings', 'market')
        typeDrop.pack()
        typeDrop.place(x=300, y=150)

        # bottom
        noteLabel = Label(window, text="If not applicable, please fill in with 0")
        noteLabel.place(x=150, y=180)

        initialBalanceLabel = Label(window, text="Initial Balance")
        initialBalanceLabel.place(x=50, y=200)
        initialBalance = Entry(window)
        initialBalance.place(x=50, y=220)

        interestRateLabel = Label(window, text="Interest Rate")
        interestRateLabel.place(x=280, y=200)
        interestRate = Entry(window)
        interestRate.place(x=280, y=220)

        minBalanceLabel = Label(window, text="Min Balance")
        minBalanceLabel.place(x=50, y=250)
        minBalance = Entry(window)
        minBalance.place(x=50, y=270)

        maxWithdrawLabel = Label(window, text="Max Withdraw")
        maxWithdrawLabel.place(x=280, y=250)
        maxWithdraw = Entry(window)
        maxWithdraw.place(x=280, y=270)

        numWithdrawLabel = Label(window, text="Num Withdrawal")
        numWithdrawLabel.place(x=50, y=300)
        numWithdraw = Entry(window)
        numWithdraw.place(x=50, y=320)

        dtDepositLabel = Label(window, text="Date Deposit")
        dtDepositLabel.place(x=280, y=300)
        dtDeposit = Entry(window)
        dtDeposit.place(x=280, y=320)

        def confirm():
            operation_ = operationOptions.get()
            format = "%Y-%m-%d"

            if operation_ == 'Add Owner':

                requester_ = requesterOptions.get()
                customer_ = customerOptions.get()
                bank_ = bankOptions.get()
                accountID_ = AccountID.get()
                type_ = typeOptions.get()
                initialBalance_ = initialBalance.get()
                interestRate_ = interestRate.get()
                minBalance_ = minBalance.get()
                maxWithdraw_ = maxWithdraw.get()
                numWithdraw_ = numWithdraw.get()
                dtDeposit_ = dtDeposit.get()
                dtStartShare = datetime.today().strftime('%Y-%m-%d')

                cursor.execute("select perID,bankID,accountID from access")
                ip_dup = cursor.fetchall()
                ip_dup = [(x[0], x[1],x[2]) for x in ip_dup]
                print(ip_dup)

                if operation_ =='Operation' or requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank' or type_ =='Account Type':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not accountID_ or not initialBalance_ or not interestRate_ or not minBalance_ or not maxWithdraw_ or not numWithdraw_:
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not initialBalance_.isdigit() or not interestRate_.isdigit() or not minBalance_.isdigit() or not maxWithdraw_.isdigit() or not numWithdraw_.isdigit():
                    messagebox.showinfo("Insert Status", "Inputs must be integer")
                elif int(interestRate_)>100:
                    messagebox.showinfo("Insert Status", "Must be a valid Interest Rate")
                elif not (re.fullmatch("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", dtDeposit_)):
                    messagebox.showinfo("Insert Status", "Input must be a valid date")
                elif (customer_, bank_, accountID_) in ip_dup:
                    messagebox.showinfo("Insert Status", "Duplicated Access")
                else:
                    args = (requester_, customer_, type_, bank_, accountID_, int(initialBalance_), int(interestRate_), dtDeposit_,
                            int(minBalance_), int(numWithdraw_), int(maxWithdraw_), dtStartShare)
                    cursor.callproc('add_account_access', args)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

            if operation_ == 'Remove Owner':

                requester_ = requesterOptions.get()
                customer_ = customerOptions.get()
                bank_ = bankOptions.get()
                accountID_ = AccountID.get()

                if operation_ =='Operation' or requester_ == "Accessible Accounts" or customer_ == 'Customer' or bank_ =='Bank':
                    messagebox.showinfo("Insert Status", "Fields are Required")
                elif not accountID_:
                    messagebox.showinfo("Insert Status", "Account ID is Required")
                else:
                    argss = (requester_, customer_, bank_, accountID_)
                    cursor.callproc('remove_account_access', argss)
                    con.commit()
                    messagebox.showinfo("Insert Status", "Modification Completed")

        confirmbutton = Button(window, text="Comfirm", bg="white", command=confirm)
        confirmbutton.place(x=320, y=370)

        back = Button(window, text="Back", bg="white", command=lambda: [window.destroy(), self.adminMenu()])
        back.place(x=150, y=370)

    # Screen 9 - Create Fee ✅
    def CreateFee(self):
        self.adminmenu.withdraw()
        window = Toplevel()
        window.geometry("600x300")
        window.title("Create Fee")

        con = self.connect()
        cursor = con.cursor()

        BankAccount = Label(window, text="Bank Account", font=("bold", 10))
        BankAccount.place(x=30, y=30)

        cursor.execute("SELECT bankID, accountID FROM interest_bearing")
        accountList = cursor.fetchall()

        clicked1 = StringVar(master=window)

        e_Account = OptionMenu(window, clicked1, *accountList)
        e_Account.pack()
        e_Account.place(x=150, y=30)

        Fee = Label(window, text="Fee Type", font=("bold", 10))
        Fee.place(x=30, y=60)

        e_Fee = Entry(window)
        e_Fee.place(x=150, y=60)

        def update():

            Fee = e_Fee.get()
            BankAccount = clicked1.get()[1:-1].split(", ")
            con = self.connect()
            cursor = con.cursor()
            result = cursor.execute( f"select fee from interest_bearing_fees where bankID = {BankAccount[0]} and accountID = {BankAccount[1]};" )
            result = cursor.fetchall()
            feelist = [i[0] for i in result]

            if (not (Fee and BankAccount)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif Fee in feelist:
                messagebox.showinfo("Insert Status", "The Fee already exists")
            else:
                cursor.execute(
                    f"INSERT INTO interest_bearing_fees VALUES ({BankAccount[0]}, {BankAccount[1]}, '{Fee}')")
                cursor.execute("commit")
                messagebox.showinfo("Insert Status", "Insert Successfully")

        insert = Button(window, text="Create Fee", bg="white", command=update)
        insert.place(x=30, y=90)
        BackButton = Button(window, text="Back", command=lambda: [window.destroy(), self.adminMenu()])
        BackButton.place(x=300, y=90)

    # Screen 10  半完成，部分判断条件缺失
    def StartStopOverdraft(self):

        window = Toplevel()
        window.geometry("600x300")
        window.title("Manage overdraft")

        con = self.connect()
        cursor = con.cursor()

        def Start():
            checking = clicked1.get()[1:-1].split(", ")
            savings = clicked2.get()[1:-1].split(", ")

            con = self.connect()
            cursor = con.cursor()
            cursor.execute(
                f"SELECT protectionBank, protectionAccount FROM checking where bankID={checking[0]} and accountID={checking[1]}")
            result = cursor.fetchall()[0]

            if (not (checking and savings)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif None not in result:
                messagebox.showinfo("Insert Status", "Account is enrolled in overdraft protection")
            else:
                con = self.connect()
                cursor = con.cursor()
                cursor.execute(
                    f'UPDATE checking SET protectionBank = {savings[0]}, protectionAccount = {savings[1]} WHERE bankID={checking[0]} and accountID={checking[1]}')
                cursor.execute("commit")
                messagebox.showinfo("Insert Status", "Started Overdraft Successfully")
                con.close()

        def Stop():
            checking = clicked1.get()[1:-1].split(", ")
            savings = clicked2.get()[1:-1].split(", ")

            con = self.connect()
            cursor = con.cursor()
            cursor.execute(
                f"SELECT protectionBank, protectionAccount FROM checking where bankID={checking[0]} and accountID={checking[1]}")
            result = [f"'{i}'" for i in cursor.fetchall()[0]]

            if (not (checking and savings)):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            elif None in result:
                messagebox.showinfo("Insert Status", "Account is not enrolled in overdraft protection")
            elif savings != result:
                messagebox.showinfo("Insert Status",
                                    "Account is not enrolled in overdraft protection with the specified saving account")
            else:
                con = self.connect()
                cursor = con.cursor()
                cursor.execute(
                    f'UPDATE checking SET protectionBank = null, protectionAccount = null WHERE bankID={checking[0]} and accountID={checking[1]}')
                cursor.execute("commit")

                messagebox.showinfo("Insert Status", "Stopped Overdraft Successfully")
                con.close()

        CheckingAccount = Label(window, text="Checking Account", font=("bold", 10))
        CheckingAccount.place(x=30, y=30)

        SavingAccount = Label(window, text="Saving Account", font=("bold", 10))
        SavingAccount.place(x=30, y=60)

        var1 = IntVar()

        def StartStop():
            if var1.get() == 1:
                Start()
            else:
                Stop()

        c1 = Checkbutton(window, text='Adding Overdraft Policy', variable=var1, onvalue=1, offvalue=0)
        c1.pack()

        cursor.execute("SELECT perID from system_admin")
        AdminList = [i[0] for i in cursor.fetchall()]

        if self.username in AdminList:
            cursor.execute(
                "SELECT bankID, accountID FROM checking")  # 存疑， 这个Menu是customer admin都有access，所以他们看到的overdraft account 列表应该是不同的。
            options1 = cursor.fetchall()
            cursor.execute("SELECT bankID, accountID FROM savings")
            SavingList = cursor.fetchall()
        else:

            cursor.execute(
                f"SELECT bankID, accountID FROM access NATURAL JOIN checking where perID = '{self.username}'")
            options1 = cursor.fetchall()
            cursor.execute(f"SELECT bankID, accountID FROM access NATURAL JOIN savings where perID = '{self.username}'")
            SavingList = cursor.fetchall()

        clicked1 = StringVar(master=window)

        if not (options1 or SavingList):
            options1 = [[]]
            SavingList = [[]]
            messagebox.showerror("Warning", "Customer does not have access to checking or saving account")
        elif not options1:
            options1 = [[]]
            messagebox.showerror("Warning", "Customer does not have access to checking account")
        if not SavingList:
            SavingList = [[]]
            messagebox.showerror("Warning", "Customer does not have access to saving account")

        e_Checking = OptionMenu(window, clicked1, *options1)
        e_Checking.pack()
        e_Checking.place(x=150, y=30)

        clicked2 = StringVar(master=window)

        e_Saving = OptionMenu(window, clicked2, *SavingList)
        e_Saving.pack()
        e_Saving.place(x=150, y=60)

        insert = Button(window, text="INSERT", bg="white", command=StartStop)
        insert.place(x=20, y=140)
        window.mainloop()

    # Screen 11 ✅ 基本完成
    def MakeDepositWithdrawal(self):
        self.customermenu.withdraw()
        window = Toplevel()
        window.geometry("600x300")
        window.title("Deposit/ Withdrawal")

        con = self.connect()
        cursor = con.cursor()

        TransactionType = Label(window, text="Transaction Type", font=("bold", 10))
        TransactionType.place(x=30, y=30)

        cursor.execute("SELECT bankID, accountID FROM checking")
        options1 = ["Deposit", "Withdraw"]

        clicked1 = StringVar(master=window)

        e_Checking = OptionMenu(window, clicked1, *options1)
        e_Checking.pack()
        e_Checking.place(x=150, y=30)

        BankAccount = Label(window, text="Bank Account", font=("bold", 10))
        BankAccount.place(x=30, y=60)

        cursor.execute(f"SELECT bankID, accountID FROM access WHERE perID = '{self.username}'")
        accountList = cursor.fetchall()

        if not accountList:
            accountList = [[]]
            messagebox.showerror("No access", "No access to bank account")

        clicked2 = StringVar(master=window)

        e_Account = OptionMenu(window, clicked2, *accountList)
        e_Account.pack()
        e_Account.place(x=150, y=60)

        Amount = Label(window, text="Amount", font=("bold", 10))
        Amount.place(x=30, y=90)

        e_Amount = Entry(window)
        e_Amount.place(x=150, y=90)

        def update():

            Amount = e_Amount.get()
            BankAccount = clicked2.get()[1:-1].split(", ")
            cursor.execute(
                f"SELECT balance FROM bank_account WHERE bankID={BankAccount[0]} and accountID={BankAccount[1]}")
            balance = cursor.fetchall()[0][0]

            if (not (Amount and BankAccount and clicked1.get())):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            else:
                try:
                    Amount = int(Amount)
                except:
                    messagebox.showinfo("Insert Status", "Please enter integer for balance")

                if (clicked1.get()) == "Withdraw":
                    if Amount > float(balance):
                        messagebox.showerror(title='Error', message="Insufficient balance!")
                    else:
                        cursor.execute(
                            f"UPDATE bank_account SET balance = balance - {Amount} WHERE bankID={BankAccount[0]} and accountID={BankAccount[1]}")
                        cursor.execute("commit")
                        messagebox.showinfo("Insert Status", "Withdraw Successfully")
                else:
                    cursor.execute(
                        f"UPDATE bank_account SET balance = ifnull(balance,0) + {Amount} WHERE bankID={BankAccount[0]} and accountID={BankAccount[1]}")
                    cursor.execute("commit")
                    messagebox.showinfo("Insert Status", "Deposit Successfully")

        insert = Button(window, text="INSERT", bg="white", command=update)
        insert.place(x=100, y=140)
        BackButton = Button(window, text="Cancel", command=lambda: [window.destroy(), self.customerMenu()])
        BackButton.place(x=200, y=140)
        window.mainloop()

    # Screen 12 ✅
    def MakeAccountTransfer(self):
        self.customerenu.withdraw()
        MAT = Toplevel()
        MAT.title('Transfer')
        MAT.geometry('400x300')
        self.mat = MAT

        con = self.connect()
        cursor = con.cursor()

        fromLabel = Label(self.mat, text="From: ", font=("bold", 10))
        fromLabel.place(x=20, y=30)

        sql = f"SELECT concat(bankID,' ',accountID) FROM access WHERE perID = '{self.username}';"
        cursor.execute(sql)
        result = cursor.fetchall()
        bankIDlist = [it[0] for it in result]
        frombankID = StringVar(master=self.mat)
        bankID = OptionMenu(self.mat, frombankID, *bankIDlist)
        bankID.pack()
        bankID.place(x=70, y=30)

        AmountLabel = Label(self.mat, text="Amount($): ", font=("bold", 10))
        AmountLabel.place(x=20, y=70)
        AmountofMoney = Entry(self.mat)
        AmountofMoney.place(x=120, y=70)

        ToLabel = Label(self.mat, text="To: ", font=("bold", 10))
        ToLabel.place(x=20, y=110)

        sql2 = f"SELECT concat(bankID,' ',accountID) FROM access"
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        TobankIDlist = [it[0] for it in result2]
        TobankID = StringVar(master=self.mat)
        TobankIDMenu = OptionMenu(self.mat, TobankID, *TobankIDlist)
        TobankIDMenu.pack()
        TobankIDMenu.place(x=70, y=110)

        def Transfer():
            con = self.connect()
            cursor = con.cursor()

            if (not (AmountofMoney and frombankID and TobankID.get())):
                messagebox.showinfo("Insert Status", "All Fields are Required")
            else:
                frombankaccount = frombankID.get()
                frombank = frombankaccount.split()[0]
                fromaccount = frombankaccount.split()[1]
                Money = AmountofMoney.get()
                tobankaccount = TobankID.get()
                tobank = tobankaccount.split()[0]
                toaccount = tobankaccount.split()[1]

                sql3 = f"SELECT balance FROM bank_account WHERE bankID = '{frombank}' and accountID = '{fromaccount}';"
                cursor.execute(sql3)
                balance = cursor.fetchone()[0]
                if (frombank == tobank) & (fromaccount == toaccount):
                    messagebox.showerror(title='Error',
                                         message='You cannot transfer money to yourself. Please try it again')
                else:
                    try:
                        Money = int(Money)
                        transfer = True
                    except:
                        messagebox.showerror("Insert Status", "Please enter integer for Transfer Amount")
                        transfer = False

                if not transfer:
                    messagebox.showerror("Error", "There is an error with your transfer.")
                else:
                    if Money > float(balance):
                        messagebox.showerror(title='Error', message="Insufficient balance!")
                    else:
                        # parameter = ( self.username , int(Money) , frombank , fromaccount , tobank , toaccount , self.date  )
                        # cursor.callproc('account_transfer',args=parameter)
                        cursor.execute(
                            f"UPDATE bank_account SET balance = ifnull(balance,0) - {int(Money)} WHERE bankID='{frombank}' and accountID='{fromaccount}'")
                        cursor.execute(
                            f"UPDATE bank_account SET balance = ifnull(balance,0)  + {int(Money)} WHERE bankID='{tobank}' and accountID='{toaccount}'")
                        cursor.execute(
                            f" UPDATE access SET dtAction = '{self.date}' where perID='{self.username}' and bankID= '{frombank}' and accountID = '{fromaccount}';")
                        con.commit()
                        messagebox.showinfo(title='Success', message='Transfer successfully!')

        transferbutton = Button(self.mat, text='Transfer Money', width=20, command=Transfer)
        transferbutton.place(x=190, y=230)
        BackButton = Button(self.mat, text="Cancel", width=20,
                            command=lambda: [self.mat.destroy(), self.customerMenu()])
        BackButton.place(x=190, y=260)

    # Screen 13 ✅
    def PayEmployee(self):
        PayEmployeeWD = Toplevel()
        PayEmployeeWD.geometry("200x200")
        PayEmployeeWD.title("Pay Employee")
        self.payemployee = PayEmployeeWD

        def PayAllEmployees():
            con = self.connect()
            cursor = con.cursor()
            cursor.callproc('pay_employees')
            con.commit()
            messagebox.showinfo("Status", "Pay Employees Successfully")

        PayButton = Button(self.payemployee, text="Pay All Employees", command=PayAllEmployees)
        PayButton.place(x=90, y=100)
        BackButton = Button(self.payemployee, text="Back", command=lambda: [self.payemployee.destroy()])
        BackButton.place(x=90, y=150)

    # Screen 14 ✅
    def accountStats(self):
        self.viewstats.withdraw()
        self.accounstats = Toplevel()
        self.accounstats.geometry("1000x500")
        self.accounstats.title("Account Stats")

        BackButton = Button(self.accounstats, text="Back", width=16,
                            command=lambda: [self.accounstats.destroy(), self.viewStats()])
        BackButton.place(x=200, y=300)

        tree = ttk.Treeview(self.accounstats)  # 表格
        # 怎么设置显示结果
        tree["columns"] = ("Bank", "Account ID", "Account Balance($)", "Number of Owners")
        tree.column("Bank", width=150)  # 表示列,不显示
        tree.column("Account ID", width=150)
        tree.column("Account Balance($)", width=150)
        tree.column("Number of Owners", width=150)

        tree.heading("Bank", text="Bank")  # 显示表头
        tree.heading("Account ID", text="Account ID")
        tree.heading("Account Balance($)", text="Account Balance($)")
        tree.heading("Number of Owners", text="Number of Owners")

        connection = self.connect()
        cur = connection.cursor()
        sql = f"select bankName as Bank, bank_account.accountID as 'Account ID' , balance as 'Account Balance($)' , count(distinct perID) as 'Number of Owners' from (bank_account left outer join bank on bank_account.bankID = bank.bankID) left join access on bank_account.accountID = access.accountID group by bank_account.bankID , bank_account.accountID order by bankName desc;"
        cur.execute(sql)
        f = cur.fetchall()
        for i in range(len(f)):
            # for j in range(len(i)):
            tree.insert('', i, value=(f[i][0], f[i][1], f[i][2], f[i][3]))

        tree.pack()

    # Screen 15 ✅
    def bankStats(self):
        self.viewstats.withdraw()
        self.bankstats = Toplevel()
        self.bankstats.geometry("1000x500")
        self.bankstats.title('Bank Stats')

        BackButton = Button(self.bankstats, text="Back", width=16,
                            command=lambda: [self.bankstats.destroy(), self.viewStats()])
        BackButton.place(x=200, y=300)
        tree2 = ttk.Treeview(self.bankstats)  # 表格
        # 怎么设置显示结果
        tree2["columns"] = (
        "bankID", "corpID", "bankName", "street", "city", "state", "zip", "NumberofAccounts", "BankAssets",
        "TotalAssets")
        tree2.column("bankID", width=70)  # 表示列,不显示
        tree2.column("corpID", width=70)
        tree2.column("bankName", width=100)
        tree2.column("street", width=150)
        tree2.column("city", width=80)
        tree2.column("state", width=50)
        tree2.column("zip", width=80)
        tree2.column("NumberofAccounts", width=50)
        tree2.column("BankAssets", width=80)
        tree2.column("TotalAssets", width=80)

        tree2.heading("bankID", text="bankID")  # 显示表头
        tree2.heading("corpID", text="Account ID")
        tree2.heading("bankName", text="Bank Name")
        tree2.heading("street", text="street")
        tree2.heading("city", text="city")
        tree2.heading("state", text="state")
        tree2.heading("zip", text="zip")
        tree2.heading("NumberofAccounts", text="NumberofAccounts")
        tree2.heading("BankAssets", text="BankAssets")
        tree2.heading("TotalAssets", text="TotalAssets")

        connection = self.connect()
        cur2 = connection.cursor()
        sql2 = "SELECT bank.bankID AS 'Bank ID', corporation.shortName AS 'Corporation Name', bank.bankName AS 'Bank Name' , bank.street AS 'Street', bank.city AS 'City' , bank.state AS 'State', bank.zip AS 'Zip', count(distinct bank_account.accountID) as 'Number of Accounts', ifnull(bank.resAssets,0) as 'Bank Assets($)' , ifnull(bank.resAssets,0)+sum(ifnull(bank_account.balance,0)) as 'Total Assets' FROM (bank LEFT JOIN bank_account on bank.bankID = bank_account.bankID) JOIN corporation ON bank.corpID = corporation.corpID GROUP BY bank.bankID;"
        cur2.execute(sql2)
        f2 = cur2.fetchall()
        for i in range(len(f2)):
            # for j in range(len(i)):
            tree2.insert('', i, value=(
            f2[i][0], f2[i][1], f2[i][2], f2[i][3], f2[i][4], f2[i][5], f2[i][6], f2[i][7], f2[i][8], f2[i][9]))
        tree2.pack()

    # Screen 16 ✅
    def corpStats(self):
        self.viewstats.withdraw()
        self.corpstats = Toplevel()
        self.corpstats.geometry("1000x500")
        self.corpstats.title("Corporation Stats")
        BackButton = Button(self.corpstats, text="Back", width=16,
                            command=lambda: [self.corpstats.destroy(), self.viewStats()])
        BackButton.place(x=200, y=300)

        tree2 = ttk.Treeview(self.corpstats)  # 表格
        # 怎么设置显示结果
        tree2["columns"] = (
        "Corporation ID", "Short Name", "Formal Name", "Number of Banks", "Corporation Assets", "Total Assets")
        tree2.column("Corporation ID", width=80)  # 表示列,不显示
        tree2.column("Short Name", width=120)
        tree2.column("Formal Name", width=150)
        tree2.column("Number of Banks", width=70)
        tree2.column("Corporation Assets", width=100)
        tree2.column("Total Assets", width=100)

        tree2.heading("Corporation ID", text="Corporation ID")  # 显示表头
        tree2.heading("Short Name", text="Short Name")
        tree2.heading("Formal Name", text="Formal Name")
        tree2.heading("Number of Banks", text="Number of Banks")
        tree2.heading("Corporation Assets", text="Corporation Assets")
        tree2.heading("Total Assets", text="Total Assets")

        connection = self.connect()

        cur2 = connection.cursor()
        sql2 = "select corporation.corpID as 'Corporation ID', shortName as 'Short Name', longName as 'Formal Name', count(distinct bank.bankID) as 'Number of Banks', ifnull(corporation.resAssets,0) as 'Corporation Assets($)' ,ifnull(corporation.resAssets,0) + sum(ifnull(bank.resAssets,0)) + sum(ifnull(bank_account.balance,0)) as 'Total Assets' from ( corporation left join bank on corporation.corpID = bank.corpID ) left join bank_account on bank.bankID = bank_account.bankID group by corporation.corpID;"
        cur2.execute(sql2)
        f2 = cur2.fetchall()
        for i in range(len(f2)):
            # for j in range(len(i)):
            tree2.insert('', i, value=(f2[i][0], f2[i][1], f2[i][2], f2[i][3], f2[i][4], f2[i][5]))

        tree2.pack()

    # Screen 17 ✅
    def customerStats(self):
        self.viewstats.withdraw()
        self.custstats = Toplevel()
        self.custstats.geometry("1000x500")
        self.custstats.title("Customer Stats")
        BackButton = Button(self.custstats, text="Back", width=16,
                            command=lambda: [self.custstats.destroy(), self.viewStats()])
        BackButton.place(x=200, y=300)
        tree2 = ttk.Treeview(self.custstats)  # 表格
        # 怎么设置显示结果
        tree2["columns"] = (
        "CustomerID", "TaxID", "CustomerName", "DateofBirth", "JoinedDate", "Street", "city", "state", "zip",
        "NumberofAccounts", "CustomersAssets")
        tree2.column("CustomerID", width=80)  # 表示列,不显示
        tree2.column("TaxID", width=80)
        tree2.column("CustomerName", width=120)
        tree2.column("DateofBirth", width=80)
        tree2.column("JoinedDate", width=80)
        tree2.column("Street", width=200)
        tree2.column("city", width=80)
        tree2.column("state", width=50)
        tree2.column("zip", width=50)
        tree2.column("NumberofAccounts", width=10)
        tree2.column("CustomersAssets", width=20)

        tree2.heading("CustomerID", text="Customer ID")  # 显示表头
        tree2.heading("TaxID", text="Tax IDID")
        tree2.heading("CustomerName", text="Customer Name")
        tree2.heading("DateofBirth", text="Date of Birth")
        tree2.heading("JoinedDate", text="Joined Date")
        tree2.heading("Street", text="Street")
        tree2.heading("city", text="city")
        tree2.heading("state", text="state")
        tree2.heading("zip", text="zip")
        tree2.heading("NumberofAccounts", text="Number of Accounts")
        tree2.heading("CustomersAssets", text="Customers Assets")

        connection = self.connect()

        cur2 = connection.cursor()
        sql2 = "select bank_user.perID as 'Customer ID', taxID as 'TAX ID' , concat(firstName,' ',lastName) as 'Customer Name', birthdate as 'Date of Birth', dtJoined as 'Joined Date' , street as 'Street' , city as 'City' , state as 'State' , zip as 'Zip' , count(distinct concat(access.bankID,access.accountID)) as 'Number of Accounts' , sum(ifnull(bank_account.balance,0)) as 'Customer Assets($)' from (( bank_user right join customer on bank_user.perID = customer.perID ) left join access on bank_user.perID = access.perID) left join bank_account on concat(access.bankID,access.accountID) = concat(bank_account.bankID,bank_account.accountID) group by customer.perID;"
        cur2.execute(sql2)
        f2 = cur2.fetchall()
        for i in range(len(f2)):
            # for j in range(len(i)):
            tree2.insert('', i, value=(
            f2[i][0], f2[i][1], f2[i][2], f2[i][3], f2[i][4], f2[i][5], f2[i][6], f2[i][7], f2[i][8], f2[i][9],
            f2[i][10]))

        tree2.pack()

    # Screen 18 ✅
    def EmployeeStats(self):
        self.viewstats.withdraw()
        self.employeestats = Toplevel()
        self.employeestats.geometry("1000x500")
        self.employeestats.title("Screen 18: Employee Stats")

        BackButton = Button(self.employeestats, text="Back", width=16,
                            command=lambda: [self.employeestats.destroy(), self.viewStats()])
        BackButton.place(x=200, y=300)

        tree2 = ttk.Treeview(self.employeestats)  # 表格
        # 怎么设置显示结果
        tree2["columns"] = (
        "PerID", "TaxID", "Name", "DOB", "DateJoined", "Street", "city", "state", "zip", "NumberofBanks", "BankAssets")
        tree2.column("PerID", width=80)  # 表示列,不显示
        tree2.column("TaxID", width=80)
        tree2.column("Name", width=120)
        tree2.column("DOB", width=100)
        tree2.column("DateJoined", width=100)
        tree2.column("Street", width=150)
        tree2.column("city", width=70)
        tree2.column("state", width=50)
        tree2.column("zip", width=70)
        tree2.column("NumberofBanks", width=50)
        tree2.column("BankAssets", width=70)

        tree2.heading("PerID", text="PerID")  # 显示表头
        tree2.heading("TaxID", text="TaxID")
        tree2.heading("Name", text="Name")
        tree2.heading("DOB", text="DOB")
        tree2.heading("DateJoined", text="DateJoined")
        tree2.heading("Street", text="Street")
        tree2.heading("city", text="city")
        tree2.heading("state", text="state")
        tree2.heading("zip", text="zip")
        tree2.heading("NumberofBanks", text="NumberofBanks")
        tree2.heading("BankAssets", text="BankAssets")

        connection = self.connect()

        cur2 = connection.cursor()
        sql2 = "select bank_user.perID as 'Person ID', taxID as 'TAX ID' , concat(firstName,' ',lastName) as 'Name', birthdate as 'Date of Birth', dtJoined as 'Joined Date' , bank_user.street as 'Street' , bank_user.city as 'City' , bank_user.state as 'State' , bank_user.zip as 'Zip' , count(distinct bank.bankID) as 'Number of Banks' , sum(ifnull(bank.resAssets,0)) as 'Bank Assets' from (( bank_user right join employee on bank_user.perID = employee.perID) left join workfor on bank_user.perID = workfor.perID ) left join bank on bank.bankID = workfor.bankID group by bank_user.perID order by bank_user.perID;"
        cur2.execute(sql2)
        f2 = cur2.fetchall()
        for i in range(len(f2)):
            # for j in range(len(i)):
            tree2.insert('', i, value=(
            f2[i][0], f2[i][1], f2[i][2], f2[i][3], f2[i][4], f2[i][5], f2[i][6], f2[i][7], f2[i][8], f2[i][9],
            f2[i][10]))

        tree2.pack()


app = GUI()
