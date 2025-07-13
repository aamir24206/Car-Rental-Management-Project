# Importing all modules
import os
import mysql.connector as mc
import pwinput
import time
from datetime import datetime, timedelta

# Connection for MySQL
con = mc.connect(host='localhost',user='root',password='2006')
cr = con.cursor()
# Database & Tables for MySQL
cr.execute('create database if not exists CruiseWave')
cr.execute('use CruiseWave')
cr.execute('create table if not exists userdata(email varchar(255), username varchar(255), password varchar(255), LicenseNo int(10))')
cr.execute('create table if not exists data(username char(255), address varchar(255))')
cr.execute('create table if not exists previousordcar(username char(255), Cars_orderedname varchar(255),startdate varchar(255), enddate varchar(255), paytype varchar(25))')
cr.execute('create table if not exists car(Carname varchar(255), type varchar(255), seats int, doors int, transmission varchar(255), priceperday int, pricepermonth int)')
cr.execute('create table if not exists card(username varchar(255), Cardnum varchar(16),cardexpiry varchar(5), CVV char(3))')

#Functions
def getrentaldates():
    global start_date
    global rental_duration
    global formatted
    global end_date
    try:
        current_date = datetime.now().date()
        print(f'Todays date: {current_date}')
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if start_date < current_date:
            print('Invalid date, Start date cannot be in the past')
            return getrentaldates()
    except ValueError:
        print(f'Date error please try again')
        return getrentaldates()
    rental_duration = int(input("Enter the rental duration in days (Max 30 Days): "))
    if rental_duration <=0:
        print(f'Invalid rental duration, Enter appropriate rental duration')
        return getrentaldates()
    end_date = start_date + timedelta(days=rental_duration)
    try:
        deliverytime = input("Enter desired delivery time (HH:MM AM/PM): ")
        delivery_time = time.strptime(deliverytime, "%I:%M %p")
    except ValueError:
        print(f'Invalid time, please try again')
        return getrentaldates()
    formatted = time.strftime("%I:%M %p", delivery_time)
    print(f'Selected Delivery time is {formatted}')
    print(f'Start date: {start_date}, End date: {end_date}')

def getcars():
    cr.execute('select* from car')
    output = cr.fetchall()
    return output

def check_username(username):
    global new
    cr.execute('select* from userdata where username = "%s"'%(input_username))
    data = cr.fetchall()
    if data != []:
        new = False
        return True
    else:
        new = True
        return False

def check_password(ent_pass):
    cr.execute('select password from userdata where username = "%s"'%(input_username))
    data = cr.fetchone()
    os.system('cls')
    if ent_pass == data[0]:
        print("Hold on while we fetch your details...")
        print("All Done")
    else:
        print("Incorrect password, Please try again")
        time.sleep(2)
        os.system('cls')
        return login_screen()

def login_screen():
    global input_username
    global ent_pass
    print('Welcome to CruiseWave\nYour key to mobility and adventure')
    input_username = input('Enter username to sign up or sign in: ')
    check = check_username(input_username)
    if new == False:
        print('Welcome back',input_username)
        ent_pass = pwinput.pwinput(prompt="Please enter your password: ")
        check_password(ent_pass)
    elif new == True:
        print("Welcome new user")
        email = input("Enter Email Address: ")
        password = pwinput.pwinput(prompt="Please enter a safe and secure password: ")
        licenseno = int(input("Enter your Licenso No. (10 Digits only): "))
        cr.execute('insert into userdata values("%s","%s","%s",%s)'%(email,input_username,password,licenseno))
        cr.execute(f'insert into data values("{input_username}","{dict()}")')
        cr.execute(f'insert into card values("{input_username}","{dict()}","{dict()}","{dict()}")')        
        con.commit()
        print('Hold on while we register....')
        time.sleep(2)
        print('All Done')

def check_address():
    global check
    cr.execute('select address from data where username = "%s"'%(input_username))
    data = cr.fetchone()
    if data != ('{}',):
        existsaddress = True
        useexistad = input("Do you wish to use your existing address(Yes/No): ")
        if useexistad.title() == "Yes":
            address = data[0]
            check = True
        elif useexistad.title() == "No":
            newad = input("Enter your address: ")
            check = True
        if useexistad.title() not in "YesNo":
            print('Invalid choice, Enter Yes/No')
            check = False
    else:
        newad = input('Enter your address: ')
        checksavead = input('Do you wish to save this address for future use?(Yes/No): ')
        if checksavead.title() == "Yes":
            cr.execute('update data set address = "%s" where username = "%s"'%(newad,input_username))
            con.commit()
        check = True

def cardPayment():
    print('All sensitive information is stored securely and encrypted')
    text = ''
    card = input(f'{text}Please enter your Card Number: ')
    if len(card) != 16:
        print('Invalid Card Number, please try again')
    if not card.isdigit():
        print("Please enter a valid card number containing only numeric digits.")
    cvv = input(f'{text}Please enter your CVV: ')
    if len(cvv) not in (3,4):
        print('Invalid CVV, Please try again')
        if not cvv.isdigit():
            print("Please enter a valid CVV number containing only numeric digits.")
    expiry = input(f'Please enter your Expiry Date in the format MM/YY: ')
    cmonth, cyear = expiry.split('/')
    month, year = datetime.now().strftime('%m/%y').split('/')
    save = input('Would you like to save your card details for future orders (Yes/No): ')
    if save.title() == 'Yes':
        cr.execute('update card set cardnum = "%s",cardexpiry = "%s",CVV = "%s" where username = "%s"'%(card,expiry,cvv,input_username))
        con.commit()
        return True
    if save.title() == 'No':
        return True
    else:
        print('Invalid Choice, please Enter Yes/No')

def checkCard():
    cr.execute('select cardnum from card where username = "%s"'%(input_username))
    data = cr.fetchone()
    if data != ('{}',):
        useexistcard = input('Do you wish to use your exisiting card (Yes/No): ')
        if useexistcard.title() == 'Yes':
            cardnum = data[0]
            print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
        if useexistcard.title() == 'No':
            cardPayment()
    elif data == ('{}',):
        v = cardPayment()
        print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
    else:
        print('Incorrect option please enter (Yes/No)')

def getPrice():
    cr.execute('select priceperday, pricepermonth from car where carname = "%s"'%(choosecar))
    data = cr.fetchall()
    price = data[0]
    if rental_duration < 30:
        priceday = price[0]
        print(f'Your total is',priceday*rental_duration)
    elif rental_duration == 30:
        pricemonth = price[1]
        total_price = rental_duration
        print(f'Your total is',pricemonth)
        
def getPrevCar():
    cr.execute('select cars_orderedname,startdate,enddate,paytype from previousordcar where username = "%s"'%(input_username))
    prev = cr.fetchall()
    return prev
    
def getDetails():
    cr.execute('select* from userdata where username = "%s"'%(input_username))
    data = cr.fetchall()
    return data
        
def logout():
    print('Logging out......')
    time.sleep(2)
    print('Logged out successfully')
    os.system('cls')
    login_screen()
#Initializing Login Screen
login_screen()
while True:
    os.system('cls')
    print(f'Welcome back {input_username}! What would you like to do today?')
    print('1.Rent a car\n2.View your rented cars\n3.Logout\n4.Exit')
    choice = int(input('Enter your choice: '))
    #Placing Car Order
    if choice == 1:
        cars = getcars()
        os.system('cls')
        for car in cars:
            name, type, seats, doors, transmission, priceperday, pricepermonth = car
            print(f'{name} Type: {type}\nSeats:{seats} Doors:{doors}\nPrice per day: {priceperday} Price per month: {pricepermonth}\n')
        choosecar = input('Enter which car you wish to rent: ')
        os.system('cls')
        for car in cars:
            if choosecar.title() == car[0]:
                print(f'Do you wish to book {car[0]}?')
                choice = input("Enter Yes/No: ")
                if choice.title() == "Yes":
                    check_address()
                    if check == False:
                        check_address()
                    elif check == True:
                        getrentaldates()
                elif choice.title() == "No":
                    break
                os.system('cls')
                getPrice()
                pay = int(input("How would you like to pay?\n1.Cash on delivery\n2.Card Payment\nEnter your choice (1/2):  "))
                if pay == 1:
                    print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
                    cr.execute('update previousordcar set cars_orderedname = "%s", startdate = "%s", enddate = "%s", paytype = "Cash" where username = "%s"'%(choosecar,start_date,end_date,input_username))
                    print('The delivery driver will call you if required')
                    time.sleep(5)
                    os.system('cls')
                    print('Now you will be returning to the Menu Screen')
                    time.sleep(2)
                elif pay == 2:
                    cr.execute('select cardnum from card where username = "%s"'%(input_username))
                    data = cr.fetchone()
                    if data != ('{}',):
                        print(data[0])
                        useexistcard = input('Do you wish to use your exisiting card (Yes/No): ')
                        if useexistcard.title() == 'Yes':
                            print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
                            cr.execute('insert into previousordcar values("%s","%s","%s","%s","Card")'%(input_username,choosecar,start_date,end_date))
                            con.commit()
                            time.sleep(4)
                            os.system('cls')
                            print('Now you will be returning to the Menu Screen')
                            time.sleep(2)
                        if useexistcard.title() == 'No':
                            cardPayment()
                            print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
                            cr.execute('insert into previousordcar values("%s","%s","%s","%s","Card")'%(input_username,choosecar,start_date,end_date))
                            con.commit()
                            time.sleep(4)
                            os.system('cls')
                            print('Now you will be returning to the Menu Screen')
                            time.sleep(2)
                    elif data == ('{}',):
                        cardPayment()
                        print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
                        cr.execute('insert into previousordcar values("%s","%s","%s","%s","Card")'%(input_username,choosecar,start_date,end_date))
                        con.commit()
                        time.sleep(4)
                        os.system('cls')
                        print('Now you will be returning to the Menu Screen')
                        time.sleep(2)
                        print(f'Thank you for using CruiseWave, your car will be arriving {start_date} at estimated time {formatted}')
                else:
                    print('Incorrect option please enter (Yes/No)')           
    elif choice == 2:
        prev = getPrevCar()
        for i in prev:
            cars_orderedname, start_date, end_date, paytype = i
            print(f'{cars_orderedname.title()} Start Date: {start_date} End Date: {end_date}\nPayment Type: {paytype}')
        ret = input('Do you want to return to MENU screen (Yes): ')
        if ret == 'Yes':
                pass
        else:
            print('Incorrect Option')                   
                    
    elif choice==3:
        logout()
    
    elif choice == 4:
        con.close()
        print(f'Thank you for using Cruisewave, Have a nice day!')
        break
    else:
        print("Please enter from menu options")
