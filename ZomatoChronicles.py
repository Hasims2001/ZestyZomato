import json
import datetime
import random

dishes = dict()
orders = dict()
stores = dict()
security = dict()
sales = dict()
orders_path = "./Orders.json"
dishes_path = "./Dishes.json"
store_path = "./Store.json"
security_path = "./Security.json"
sales_path = "./Sales.json"

cart = []
def ReadFiles():
    global dishes_path
    try:
        with open(dishes_path, "r") as dish:
            global dishes
            dishes = json.load(dish)
        with open(orders_path, "r") as order:
            global orders
            orders = json.load(order)
        with open(store_path, 'r') as store:
            global stores
            stores = json.load(store) 
        with open(security_path, "r") as secure:
            global security
            security = json.load(secure)
        with open(sales_path, 'r') as sale:
            global sales
            sales = json.load(sale)
    except FileNotFoundError:
        print(f'file not found at {dishes_path}')
    except json.JSONDecodeError as e:
        print(f"Error while reading file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def ViewDishes():
    print("----:Menu:---")
    for item in dishes:
        print(f"{dishes.get(item)}")

def getStoreInput(msg, options):
    print(":Available Store:")
    loc = options["location"]
    ind = 1
    for i in loc:
        print(f'{ind}. {i}')
        ind += 1
    try:
        opt = int(input(msg))
        if(opt >= 1 and opt <= len(loc)):
            return loc[opt-1]
        else:
            print("please choose correct options")
            getStoreInput(msg, options)
    except:
        print("please choose correct options")
        getStoreInput(msg, options)

def getDishes():
    avail = []
    for item in dishes:
        curr = dishes.get(item)
        if(curr["availability"] == 'Yes'):
            avail.append(item)
    
    return avail

def getItems(msg, options):
    inp = input(msg)
    global cart        
    if(inp != 'c' and inp in options):
        cart.append(inp)
        getItems(msg, options)
    elif(inp == 'c'):
        pass
    else:
        print("Sorry but this dish is not available!")
        getItems(msg, options)


def getPromoDiscount(totalBill):
    promo = input('Promo code(optional):')
    discount = 0
    if(promo == "Flat10" and totalBill > 1500):
        discount = totalBill*10/100
    elif(promo == "Flat5" and totalBill > 1000):
        discount = totalBill*5/100
    elif(promo == ""):
        pass
    else:
        print('promo code is not matched or your cart value is lower than required minimum order value')
    
    if(promo != ""):
        opt = input('do you want to update promo code? (yes or no):')
        if(opt == "yes"):
            getPromoDiscount(totalBill)

    return discount

def generateBill(totalBill, billItem, username, useremail, location):
    billId = random.randint(1000, 9999)
    today = datetime.date.today()
    date = today.strftime("%d/%m/%y")
    discount = getPromoDiscount(totalBill)
    totalBill = totalBill - discount
    print("\n-------------Zesty Zomato Bill-------------")
    ind = 1
    print(f" Your name:{username}           Your Email:{useremail}     ")
    print(f" Bill ID:{billId}           Date:{date}")
    print(f" Store:{location}")
    for i in billItem:
        print(f"\n     {ind}. {i['id']}-{i['name']}-{i['price']}      ")
        ind += 1
    print(f"\n     Promo Discount: {discount}       ")
    print(f"\n     Total Bill: {totalBill}        ")
    print("--------------------------------------------")
    global orders
    orders.update({billId : {"billId":str(billId),"status":"received",  "name": username, "email": useremail, "items": billItem, "date": date, "totalBill": totalBill, "store": location, "promoDiscount": discount }})
    
    orderFile = open(orders_path, 'w')
    orderFile.write(json.dumps(orders))
    orderFile.close()

    
def getOrders():
    try:
        opt = input("\nmay i have your order? (yes or no)")
        if(opt == "yes"):
            username = input("what is your good name? ")
            useremail = input("what is your E-mail? ")
            global stores
            location = getStoreInput("choose one store:", stores)
            availableItems = getDishes()
            getItems("enter Dish ID (c for completed):" , availableItems)
            global cart
            global dishes
            totalBill = 0
            billItem = []
            for i in cart:
                totalBill += dishes[i]["price"]
                billItem.append(dishes[i])
            
            cart = []
            generateBill(totalBill, billItem, username, useremail, location)
            
        elif(opt == 'no'):
            print("take your time.")
        else:
            print("please enter yes or no")
            getOrders()
    except Exception as e:
        print(f'error: {e}')

def orderStatus():
    orderId = input("Bill Id:")
    global orders
    if(orders[orderId]["billId"] == orderId):
        print("\nOrder Status:", orders[orderId]["status"])
        print("If there any issue connect with us. Contact:1234567890")
    else:
        print("Order not found, please check order ID")

def orderHistory():
    email = input("Your Email:")
    global orders
    for item in orders:
        single = orders.get(item)
        if(single["email"] == email):
            print(single)
    
    
def DailyDiscount():
    print("-:Daily Discount:-")
    print("1. 5% Flat Discount on order above 1000 only for you. promo code: Flat5")
    print("2. 10% Flat Discount on order above 1500 only for you. promo code: Flat10")
    print("\n promo code can be apply only one at once.")


def CustomerFeedback():
    try:
        BillId = input('Bill Id:')
        email = input('Your Email:')
        global orders
        if(orders[BillId]['status'] == 'delivered'):
            if(orders[BillId]['email'] == email):
                feedback = input(f"write the feedback of {BillId} order:")
                orders[BillId]["feedback"] = feedback
                print(orders[BillId])
                order_file = open(orders_path, 'w')
                order_file.write(json.dumps(orders))
                order_file.close()
                print("Thank you for your feedback!")
               
            else:
                print("Bill id or email is wrong.")
                CustomerFeedback()
        else:
            print('order is not delivered yet. please try after sometime.')
    except:
        pass

def CustomerRole():
    print("\n=====Zesty Zomato=====")
    print("\n1. View Menu")
    print("2. Place Order")
    print("3. Order Status")
    print("4. Order History")
    print("5. Daily Discount")
    print("6. Customer Feedback")
    print("7. Main Menu")
    print("\n====================")
    try:
        opt = int(input("choose one:"))
        if(opt == 1):
            ViewDishes()
            CustomerRole()
        elif(opt == 2):
            getOrders()
            CustomerRole()
        elif(opt == 3):
            orderStatus()
            CustomerRole()
        elif(opt == 4):
            orderHistory()
            CustomerRole()
        elif(opt == 5):
            DailyDiscount()
            CustomerRole()
        elif(opt == 6):
            CustomerFeedback()
            CustomerRole()
        elif(opt == 7):
            pass
        else:
            print(f"please choose the correct option")
            CustomerRole()
    except:
        print(f"please choose the correct option")
        CustomerRole()



def UpdateStatus(location):
    global orders
    orderId = input('bill Id:')
    if(orders[orderId]['store'] == location):
        print('Order:', orders[orderId])
        updated = input("status:")
        orders[orderId]['status'] = updated
        orderFile = open(orders_path, 'w')
        orderFile.write(json.dumps(orders))
        orderFile.close()
        print("updated successfully")
    else:
        print('please enter correct bill Id')
        UpdateStatus(location)

def ViewOrders(location):
    global orders
    for item in orders:
        single = orders.get(item)
        if(single["store"] == location):
            print(single)

def StaffRole(location):
    print('\n=========Zesty Zomato=========\n')
    print("1. View All Orders")
    print("2. Update Status")
    print("3. Add New Order")
    print("4. Main Menu")
    print("\n==============================")
    try:
        opt = int(input('choose one:'))
        if(opt == 1):
            ViewOrders(location)
            StaffRole(location)
        elif(opt == 2):
            UpdateStatus(location)
            StaffRole(location)
        elif(opt == 3):
            getOrders()
            StaffRole(location)
        elif(opt == 4):
            pass
        else:
            print("please choose the correct option")
            StaffRole(location)
    except:
        print("please choose the correct option")
        StaffRole(location)


def AddNewDish():
    try:
        name = input("dish name:")
        price = int(input("dish price:"))
        availability = input("availability (Yes or No)?:")
        if(availability !='Yes' and availability != 'No'):
            print("please write correct Availability")
            AddNewDish()
        else:
            global dishes
            id = random.randint(100, 999)
            dishes.update({id: {"id": str(id), "name": name, "price": price, "availability": availability }})

            dish_file = open(dishes_path, 'w')
            dish_file.write(json.dumps(dishes))
            print("Dish Added")

    except:
        print("something is wrong, try again...")
        AddNewDish()

def UpdateDish():
    try:
        id = input("Dish ID:")
        global dishes
        if(dishes[id] != None):
            print(dishes[id])
            name = input('dish name:')
            price = int(input('dish price:'))
            availability = input("availability (Yes or No)?:")
            if(availability !='Yes' and availability != 'No'):
                print("please write correct Availability")
                UpdateDish()
            else:
                dishes.update({id: {"id": id, "name": name, "price": price, "availability": availability }})

                dish_file = open(dishes_path, 'w')
                dish_file.write(json.dumps(dishes))
                print("Dish updated")
        else:
            print("please write correct dish id")
            UpdateDish()
    except:
        print("something is wrong, try again...")
        UpdateDish()


def DeleteDish():
    try:
        id = input("Dish ID:")
        global dishes
        if(dishes[id] != None):
            dishes.pop(id)
            dish_file = open(dishes_path, 'w')
            dish_file.write(json.dumps(dishes))
            print("Dish Deleted")
        else:
            print("please write correct dish id")
            DeleteDish()
    except:
        print("something is wrong, try again...")
        DeleteDish()

def UpdateSales():
    global orders
    global sales
    for item in orders:
        single = orders.get(item)
        if(single['status'] == 'delivered'):
            sales.update({item: single})

    sale_file = open(sales_path, 'w')
    sale_file.write(json.dumps(sales))


def ViewSales():
    UpdateSales()
    global sales
    global stores
    loc = stores['location']
    item_counts = {}
    print("\n-:Sales by each Store:-")
    for store in loc:
        totalSales = 0
        for item in sales:
            single = sales.get(item) 
            if(single['store'] == store):
                totalSales += single['totalBill']
        
        print(f"Total Sales at {store} store: {totalSales}")
    
    for bill_info in sales:
        bill_info = sales.get(bill_info)
        items = bill_info["items"]
        for item in items:
            item_name = item["name"]
            if item_name in item_counts:
                item_counts[item_name] += 1
            else:
                item_counts[item_name] = 1


    print('\n-:Top Selling Dish:-')
    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
    ind = 1
    for item in sorted_items:
        print(f'{ind}. {item[0]} ({item[1]})')
        ind += 1

def ViewFeedback():
    UpdateSales()
    global sales
    print('\n-:Feedbacks:-')
    for itm in sales:
        single = sales.get(itm)
        if("feedback" in single):
            print(f"Bill Id: {single['billId']}, Feedback: {single['feedback']}" )

def ManagerRole():
    print('\n=========Zesty Zomato=========\n')
    print("1. Add New Dish")
    print("2. Update Dish")
    print("3. Delete Dish")
    print("4. View Dish")
    print("5. Sales Analytics")
    print("6. Customer Feedbacks")
    print("7. Main Menu")
    print("\n==============================")
    try:
        opt = int(input('choose one:'))
        if(opt == 1):
            AddNewDish()
            ManagerRole()
        elif(opt == 2):
            UpdateDish()
            ManagerRole()
        elif(opt == 3):
            DeleteDish()
            ManagerRole()
        elif(opt == 4):
            ViewDishes()
            ManagerRole()  
        elif(opt == 5):
            ViewSales()
            ManagerRole()
        elif(opt == 6):
            ViewFeedback()
            ManagerRole()
        elif(opt == 7):
            pass
        else:
            print("please choose the correct option")
            ManagerRole()
    except:
        print("please choose the correct option")
        ManagerRole()

def defineRole():
    print("\n=========Zesty Zomato=========\n\n         1.Customer       \n         2.Staff     \n         3.Manager      \n         4.Exit\n\n==============================\n")
    
    try:
        role = int(input("choose one role:"))
        ReadFiles()
        global security
        if(role == 1):
            CustomerRole()
            defineRole()
        elif(role == 2):
            ID = input("staff Id:")
            key = input("password:")
            if(security['staff'][ID]["password"] == key):
                StaffRole(security['staff'][ID]["store"])
            else:
                print("something is wrong, try again...")
            defineRole()
        elif(role == 3):
            key = input("password:")
            if(security['manager'] == key):
                ManagerRole()
            else:
                print("something is wrong, try again...")
            defineRole()
        elif(role == 4):
            print("Good Bye...")
        else:
            print("please choose the correct role")
            defineRole()
    except Exception as e:
        print(f"please choose the correct role ")
        defineRole()

defineRole()