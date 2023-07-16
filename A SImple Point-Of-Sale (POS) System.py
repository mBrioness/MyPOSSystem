from enum import Enum
import datetime

class Item:
    
    def __init__(self, upc, desc, itemMaxQty, ordThresh, replOrdQty, itemsOnHand, unitPrice):
        self.upc = upc
        self.description = desc
        self.itemMaxQty = itemMaxQty
        self.orderThreshold = ordThresh
        self.replenishOrderCount = replOrdQty
        self.itemsOnHand = itemsOnHand
        self.unitPrice = unitPrice

        
    def updatedItemsOnHand(self, numOfItems):
        self.itemsOnHand += numOfItems 
        
    def get_description(self):
        return self.description

    def get_items_on_hand(self):
        return self.itemsOnHand

    def get_order_threshold(self):
        return self.orderThreshold
    
class Inventory:
   def __init__(self): 
       self.AllItemsDict = {} 
       
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

   def get_item_by_upc(self, upc):
        if upc in self.AllItemsDict:
            return self.AllItemsDict[upc]
        else:
            return None

   def getItem(self, upc):
       
        if upc in self.AllItemsDict:
            itemObj = self.AllItemsDict[upc]
            print(f"Item description: {itemObj.description}")
        else:
            print("Item not found in the inventory.")
             
class Sale():

    def __init__(self, item, soldQty):
        self.soldQty = soldQty
        self.returnMaxQty = soldQty
        self.item = item

  
    def updatedItemsSold(self, totalSoldQty):
        self.soldQty += totalSoldQty
        
    def updatedItemsReturned(self, totalReturnedQty):
        self.returnMaxQty -= totalReturnedQty
             
class PosSystem:
   
    class POSOptions(Enum):
        NEW_SALE = 1
        RETURN_ITEMS = 2
        BACKROOM_OPERATIONS = 3
        EXIT_APPLICATION = 9
        
    
    def __init__(self):
        self.user_psswd_dict = self.getAllUIAndPasswordData()
        self.inventory = Inventory()
        self.sale_dict = {} 
        self.current_sale = []
        
        self.user = self.login()
            

        while(True):
            self.process_interaction()
    
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
    
    def process_interaction(self):
        while True:
            # user enters input
            option = input("Please select your options: 1 = New Sale, 2 = Return Item(s), 3 = Backroom Operations, 9 = Exit Application\n\n")
            if option == str(self.POSOptions.NEW_SALE.value):
                self.start_new_sale()
            elif option == str(self.POSOptions.RETURN_ITEMS.value):
                self.return_items()
            elif option == str(self.POSOptions.BACKROOM_OPERATIONS.value):
                self.backroom_operations()
            elif option == str(self.POSOptions.EXIT_APPLICATION.value):
                print("Exiting. Goodbye!")
                break  # Exit the loop and end the program
            else:
                print("Unknown option [" + option + "]. please try again.")

            
    def start_new_sale(self):
        self.current_sale = []
    
    def add_item_to_sale(self, itemObj):
        self.current_sale.append(itemObj)
        print(f"Item '{itemObj.description}' added to the sale.")

    def remove_item_from_sale(self, itemObj):
        if itemObj in self.current_sale:
            self.current_sale.remove(itemObj)
            print(f"Item '{itemObj.description}' removed from the sale.")
        else:
            print("Item not found in the sale.")
            
    def return_items(self):
        if not self.current_sale:
            print("No items in the sale to return.")
            return

        item_to_return = input("Enter the UPC of the item to return: ")
        returned_item = None

        for item in self.current_sale:
            if item.upc == item_to_return:
                returned_item = item
                break

        if returned_item:
            self.current_sale.remove(returned_item)
            print(f"Item '{returned_item.description}' returned.")
        else:
            print("Item not found in the sale.")
            
    def backroom_operations(self):
        while True:
            print("Backroom Operations Menu:")
            print("1. Replenish Items")
            print("2. Print Inventory Report")
            print("3. Print Sales Report")
            print("4. Exit Backroom Operations")
        
            option = input("Please select your option: ")
        
            if option == '1':
                self.replenish_items()
            elif option == '2':
                self.generate_inventory_report()
            elif option == '3':
                self.generate_sales_report()
            elif option == '4':
                break
            else:
                print("Unknown option. Please try again.")

    def replenish_items(self):
        print("Replenish Items:")
        upc = input("Enter the UPC of the item to replenish: ")
        
        if upc in self.inventory.AllItemsDict:
            item_obj = self.inventory.AllItemsDict[upc]
            quantity_to_add = int(input("Enter the quantity to add: "))
        
            if quantity_to_add > 0:
                item_obj.updatedItemsOnHand(quantity_to_add)
                print(f"Item '{item_obj.description}' replenished. New quantity: {item_obj.itemsOnHand}")
            else:
                print("Invalid quantity. Quantity should be greater than 0.")
        else:
            print("Item not found in the inventory.")

  
    def generate_inventory_report(self):
        print("Inventory Report:")
        for upc, item in self.inventory.AllItemsDict.items():
            print(f"Item: {item.description}")
            print(f"Quantity: {item.get_items_on_hand()}")
            print(f"Threshold: {item.get_order_threshold()}")
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
                print(f"Date: {sale['date']}")
                print()
                total_sales += sale['total_amount']
            print(f"Total Sales: {total_sales}")

    def createReciept(self):
       if self.new_sale:
           print("Current sale: ")
           for itemObj in self.new_sale:
               print(f"- '{itemObj.description}' removed from the sale.")
           else:
               print("No items found in the current sale.")
               
    def finalizeSale(self):
        if not self.new_sale:
            print("No items in the sale. Cannot finalize.")
            return

        total_amount = 0.0
        for itemObj in self.new_sale:
            total_amount += itemObj.unitPrice

        print("Sale Total:", total_amount)
        cash_received = float(input("Enter the amount of cash received: "))
        change = cash_received - total_amount

        if change >= 0:
            print("Sale finalized. Change:", change)
            for itemObj in self.new_sale:
                self.inventory.getItem(itemObj.upc)
            self.new_sale = []
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

class POSSystemReport:
    def __init__(self, pos_system):
        self.pos_system = pos_system
   
    def generate_inventory_report(self):
        print("Inventory Report:")
        for upc, item in self.pos_system.inventory.AllItemsDict.items():
            print(f"Item: {item.description}")
            print(f"Quantity: {item.get_items_on_hand()}")
            print(f"Threshold: {item.get_order_threshold()}")
            print()

    def generate_sales_report(self):
        total_sales = 0.0
        print("Sales Report:")
        for sale in self.pos_system.sales:
            print(f"Sale ID: {sale['sale_id']}")
            print("Items Sold:")
            for item in sale['items']:
                print(f"- {item.get_description()}")
            print(f"Total Amount: {sale['total_amount']}")
            print()
            total_sales += sale['total_amount']
        print(f"Total Sales: {total_sales}")
        
# Create the report object
pos_system_report = POSSystemReport(my_pos_system)

# Generate and print the inventory report
pos_system_report.generate_inventory_report()

# Generate and print the sales report
pos_system_report.generate_sales_report()

class POSSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.current_sale = []
        self.sales = []

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

    def return_items(self, item):
        if not self.new_sale:
            print("No items in the sale to return.")
            return

        item_to_return = input("Enter the UPC of the item to return: ")
        returned_item = None

        for item in self.new_sale:
            if item.upc == item_to_return:
                returned_item = item
                break

        if returned_item:
            self.new_sale.remove(returned_item)
            print(f"Item '{returned_item.description}' returned.")
        else:
            print("Item not found in the sale.")
            
    def record_sale(self):
        total_amount = 0.0
        for item in self.current_sale:
            total_amount += item.unitPrice

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

# Generate today's sales report
pos_system.generate_today_sales_report()

# Generate monthly sales report
pos_system.generate_monthly_sales_report()