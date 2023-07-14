from enum import Enum

class Sale():
     
    def __init__(self, upc, desc, unitPrice, soldQty, maxQty = 0, ordThresh = 0, replOrdQty = 0, itemsOnHand = 0):
        super().__init__(upc, desc, maxQty, ordThresh, replOrdQty, itemsOnHand, unitPrice)
        self.soldQty = soldQty
        self.returnMaxQty = soldQty
        
    def updatedItemsSold(self, totalSoldQty):
        self.soldQty += totalSoldQty
        
    def updatedItemsReturned(self, totalReturnedQty):
        self.returnMaxQty -= totalReturnedQty
             
   
class Item:
    
    def __init__(self, upc, desc, itemMaxQty, ordThresh, replOrdQty, itemsOnHand, unitPrice):
        self.upc = upc
        self.description= desc
        self.itenMaxQty = itemMaxQty
        self.orderThreshold = ordThresh
        self.replenishOrderCount = replOrdQty
        self.itemsOnHand = itemsOnHand
        self.unitPrice = unitPrice
        
    def updatedItemsOnHand(self, numOfItems):
        self.itemsOnHand += numOfItems # or try self.itemsOnHand -= numOfItems??
             
class Inventory:
   def __init__(self): 
       self.AllItemsDict = {} # this will sotre all items
       
       with open("RetailStoreDataPOS.txt", 'r') as f:
           for line in f:
               data = line.split(",")
               upc = data[0]
               desc = data[1]
               maxQty = data[2]
               ordThresh = data[3]
               replOrdQty = data[4]
               itemOnHand = data[5]
               unitPrice = data[6]
               
               itemObj = Item(upc, desc, maxQty, ordThresh, replOrdQty, itemOnHand, unitPrice)
               self.AllItemsDict[upc] = itemObj 

   def getItem(self, line, upc):
        self.upc = ()
        if upc in line:
            itemObj = line[upc]
            print(f"Item description:{itemObj.description}")
        else:
            print("Item not found in the inventory.")

class PosSystem:
   
    class Options(Enum):
        NEW_SALE = 1
        RETURN_ITEMS = 2
        BACKROOM_OPERATIONS = 3
        EXIT_APPLICATION = 9
        
    
    def __init__(self):
        self.user_psswd_dict = self.getAllUIAndPasswordData()
        self.inventory = Inventory()
        self.sale_dict = {} #the key will be the reciept # and the value will be the sale object
        self.new_sale = []
        # Login the user
        self.user = self.login()

        while(True):
            self.process_interacion()
    
    def login(self):
        UIandPWcounts = 0
        print("Welcome to the POS System\n\n")
        
        while(True):
            userID = input("Please enter userid: ")
            password = input("Please enter password: ")
            
            if (self.verifyUIandPW(userID, password)):
                print("Welcome, " + userID)
                return userID

            print("Incorrect user id andd/or password. Please try again")
            UIandPWcounts +=1
                
            if UIandPWcounts >= 3:
                print(userID + "Your account have been locked out. Please contact your system admin.")
                exit(0)
        
    def getAllUIAndPasswordData(self):
        UIPassDict = {}
        
        with open("UserIDPassword.txt",'r') as passwordFile:
            for aLine in passwordFile:
                data = aLine.split()
                userID = data[0]
                password = data[1] 
                UIPassDict[userID] = password
        
        return UIPassDict
    
    def verifyUIandPW(self, userID, password):
        passReturned = self.user_psswd_dict.get(userID)
        return passReturned == password
    
    def process_interacion(self):
        # user enters input
        option = input("Please select your options: 1 = New Sale, 2 = Return Item(s), 3 = Backroom Operations, 9 = Exit Application\n\n")
        
        if option == str(self.Options.NEW_SALE.value):
            self.new_sale()
        elif option == str(self.Options.RETURN_ITEMS.value):
            self.return_items()
        elif option == str(self.Options.BACKROOM_OPERATIONS.value):
            self.backroom_operations()
        elif option == str(self.Options.EXIT_APPLICATION.value):
            print("Exiting. Goodbye!")
            exit(0)
        else:
            print("Unknown option [" + option + "]. please try again")
    def new_sale(self):
        self.new_sale = []
    
    def addItemsToSale(self, itemObj):
        self.new_sale.append(itemObj)
        print(f"Item '{itemObj.desc}' added to the sale.")
        
    def removeItemFromSale(self, itemObj):
        if itemObj in self.new_sale:
            self.new_sale.remove(itemObj)
            print(f"Item '{itemObj.desc}' removed from the sale.")
        else:
            print("Item not found in the sale")
        
    def createReciept(self):
       if self.new_sale:
           print("Current sale: ")
           for itemObj in self.new_sale:
               print(f"- '{itemObj.desc}' removed from the sale.")
           else:
               print("No items found in the current sale.")

my_pos_system = PosSystem()

my_pos_system.start_new_sale() # this will startnnew sale

my_pos_system.removeItemFromSale()

my_pos_system.createReciept()

my_pos_system.removeItemFromSale()

my_pos_system.createReciept()

class PosSystem:
  def __init__(self):
        self.current_sale = []

  def start_new_sale(self):
        self.current_sale = []

  def add_item_to_sale(self, item):
        self.current_sale.append(item)
        print(f"Item '{item.description}' added to the sale.")

  def remove_item_from_sale(self, item):
        if item in self.current_sale:
            self.current_sale.remove(item)
            print(f"Item '{item.description}' removed from the sale.")
        else:
            print("Item not found in the sale.")

  def print_current_sale(self):
        if self.current_sale:
            print("Current Sale:")
            for item in self.current_sale:
                print(f"- {item.description}")
        else:
            print("No items in the current sale.")

  def finalize_sale(self):
        total_amount = 0.0
        for item in self.current_sale:
            total_amount += item.unit_price

        print("Sale Total:", total_amount)

        cash_received = float(input("Enter the amount of cash received: "))
        change = cash_received - total_amount
        if change >= 0:
            print("Sale finalized. Change:", change)
            self.start_new_sale()
        else:
            print("Insufficient cash received. Sale not finalized.")


# Usage
my_pos_system = PosSystem()

# Start a new sale
my_pos_system.start_new_sale()

# Add items to the sale
item1 = Item('1234567890', 'Item 1', 10, 5, 2, 8, 9.99)
item2 = Item('2345678901', 'Item 2', 20, 10, 5, 15, 19.99)

my_pos_system.add_item_to_sale(item1)
my_pos_system.add_item_to_sale(item2)

# Print the current sale
my_pos_system.print_current_sale()

# Finalize the sale
my_pos_system.finalize_sale()

class POSSystem:
    def __init__(self):
        self.current_sale = []

    def start_new_sale(self):
        self.current_sale = []

    def add_item_to_sale(self, item):
        self.current_sale.append(item)
        print(f"Item '{item.description}' added to the sale.")

    def remove_item_from_sale(self, item):
        if item in self.current_sale:
            self.current_sale.remove(item)
            print(f"Item '{item.description}' removed from the sale.")
        else:
            print("Item not found in the sale.")

    def print_current_sale(self):
        if self.current_sale:
            print("Current Sale:")
            for item in self.current_sale:
                print(f"- {item.description}")
        else:
            print("No items in the current sale.")

    def finalize_sale(self):
        total_amount = 0.0
        for item in self.current_sale:
            total_amount += item.unit_price

        print("Sale Total:", total_amount)

        cash_received = float(input("Enter the amount of cash received: "))
        change = cash_received - total_amount
        if change >= 0:
            print("Sale finalized. Change:", change)
            self.start_new_sale()
        else:
            print("Insufficient cash received. Sale not finalized.")

    def cancel_sale(self):
        self.start_new_sale()
        print("Sale canceled.")

    def return_item(self, item):
        if item in self.current_sale:
            self.current_sale.remove(item)
            print(f"Item '{item.description}' returned.")
        else:
            print("Item not found in the sale.")

# Usage
pos_system = POSSystem()

# Start a new sale
pos_system.start_new_sale()

# Add items to the sale
item1 = Item('1234567890', 'Item 1', 10, 5, 2, 8, 9.99)
item2 = Item('2345678901', 'Item 2', 20, 10, 5, 15, 19.99)

pos_system.add_item_to_sale(item1)
pos_system.add_item_to_sale(item2)

# Print the current sale
pos_system.print_current_sale()

# Return an item
pos_system.return_item(item1)

# Print the updated sale
pos_system.print_current_sale()

# Cancel the sale
pos_system.cancel_sale()

# Print the current sale after cancellation
pos_system.print_current_sale()


class POSSystem:
    def __init__(self):
        self.current_sale = []
        self.sales = []

    # ...existing methods...

    def generate_inventory_report(self, inventory):
        print("Inventory Report:")
        for upc, item in inventory.items():
            print(f"UPC: {item.upc}")
            print(f"Description: {item.description}")
            print(f"Quantity: {item.item_on_hand}")
            print(f"Threshold: {item.order_threshold}")
            print()

    def generate_sales_report(self):
        total_sales = 0.0
        print("Sales Report:")
        for sale in self.sales:
            print(f"Sale ID: {sale['sale_id']}")
            print("Items Sold:")
            for item in sale['items']:
                print(f"- {item.description}")
            print(f"Total Amount: {sale['total_amount']}")
            print()
            total_sales += sale['total_amount']
        print(f"Total Sales: {total_sales}")

    def record_sale(self):
        total_amount = 0.0
        for item in self.current_sale:
            total_amount += item.unit_price

        sale_id = len(self.sales) + 1
        sale_info = {'sale_id': sale_id, 'items': self.current_sale, 'total_amount': total_amount}
        self.sales.append(sale_info)

        self.start_new_sale()

# Usage
pos_system = POSSystem()

# Start a new sale
pos_system.start_new_sale()

# Add items to the sale
item1 = Item('1234567890', 'Item 1', 10, 5, 2, 8, 9.99)
item2 = Item('2345678901', 'Item 2', 20, 10, 5, 15, 19.99)

pos_system.add_item_to_sale(item1)
pos_system.add_item_to_sale(item2)

# Finalize the sale
pos_system.finalize_sale()

# Record the sale
pos_system.record_sale()

# Generate inventory report
inventory = pos_system.get_inventory_data()  # Assuming a method to retrieve inventory data
pos_system.generate_inventory_report(inventory)

# Generate sales report
pos_system.generate_sales_report()

class POSSystem:
    def __init__(self):
        self.inventory = {}

    # ...existing methods...

    def generate_inventory_report(self):
        print("Inventory Report:")
        for upc, item in self.inventory.items():
            print(f"Item: {item.description}")
            print(f"Quantity: {item.item_on_hand}")
            print(f"Threshold: {item.order_threshold}")
            print()

# Usage
pos_system = POSSystem()

# Load inventory data into pos_system.inventory (e.g., using load_inventory_data function)

# Generate inventory report
pos_system.generate_inventory_report()

import datetime

class POSSystem:
    def __init__(self):
        self.current_sale = []
        self.sales = []

    # ...existing methods...

    def record_sale(self):
        total_amount = 0.0
        for item in self.current_sale:
            total_amount += item.unit_price

        sale_id = len(self.sales) + 1
        sale_info = {'sale_id': sale_id, 'items': self.current_sale, 'total_amount': total_amount, 'date': datetime.date.today()}
        self.sales.append(sale_info)

        self.start_new_sale()

    def generate_today_sales_report(self):
        today = datetime.date.today()
        total_sales = 0.0
        print(f"Sales Report for {today}:")
        for sale in self.sales:
            if sale['date'] == today:
                print(f"Sale ID: {sale['sale_id']}")
                print("Items Sold:")
                for item in sale['items']:
                    print(f"- {item.description}")
                print(f"Total Amount: {sale['total_amount']}")
                print()
                total_sales += sale['total_amount']
        print(f"Total Sales for Today: {total_sales}")

    def generate_monthly_sales_report(self):
        current_month = datetime.date.today().month
        total_sales = 0.0
        print(f"Sales Report for Month {current_month}:")
        for sale in self.sales:
            if sale['date'].month == current_month:
                print(f"Sale ID: {sale['sale_id']}")
                print("Items Sold:")
                for item in sale['items']:
                    print(f"- {item.description}")
                print(f"Total Amount: {sale['total_amount']}")
                print()
                total_sales += sale['total_amount']
        print(f"Total Sales for Month {current_month}: {total_sales}")

# Usage
my_pos_system = POSSystem()

# Start a new sale
my_pos_system.start_new_sale()

# Add items to the sale
item1 = Item('1234567890', 'Item 1', 10, 5, 2, 8, 9.99)
item2 = Item('2345678901', 'Item 2', 20, 10, 5, 15, 19.99)

pos_system.add_item_to_sale(item1)
pos_system.add_item_to_sale(item2)

# Finalize the sale
pos_system.finalize_sale()

# Record the sale
pos_system.record_sale()

# Generate today's sales report
pos_system.generate_today_sales_report()

# Generate monthly sales report
pos_system.generate_monthly_sales_report()
  
    


 







    
        
        