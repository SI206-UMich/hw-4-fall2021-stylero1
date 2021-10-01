
import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet -= amount
        Cashier(cashier).receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:

    #initialize items
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    #decrese the inventory, if there is one, by the quantity
    def process_order(self, food_name, quantity):
        if self.inventory[food_name] > 0:
            self.inventory[food_name] -= quantity

    #if there is exact number of items in stall there is still enough to process the order
    def has_item(self, food_name, quantity):
        #first check if food_name is in the inventory
        if food_name in self.inventory.keys():
            if self.inventory[food_name] - quantity >= 0:
                return True
            else:
                return False
        return False
    #if food not in dictionary keys -> introduce new element, else add quantity
    def stock_up(self, food_name, quantity):
        if food_name not in self.inventory.keys():
            self.inventory[food_name] = quantity          
        else:
            self.inventory[food_name] += quantity
            
    #multiply because all the same cost
    def compute_cost(self, quantity):
        return quantity * self.cost 

    #printing __str__ function
    def __str__(self):
        return "Hello, we are {}. This is the current menu {}. We charge ${} per item. We have ${} in total.".format(self.name, self.inventory, self.cost, self.earnings)
    
    

class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(10), 100)
        self.assertEqual(self.s3.compute_cost(7), 49)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        inventory = {"Burger": 10, "Salad": 2}
        s4 = Stall("Big House", inventory)
        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertEqual(s4.has_item("Pizza", 5), 0)
        self.assertEqual(s4.has_item("Donnut", 2), 0)
        
        # Test case 2: the stall does not have enough food item: 
        self.assertEqual(s4.has_item("Burger", 15), 0)
        self.assertEqual(s4.has_item("Salad", 5), 0)

        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertEqual(s4.has_item("Burger", 5), 1)
        self.assertEqual(s4.has_item("Salad", 2), 1)
        

	# Test validate order
    def test_validate_order(self):

        inventory = {"Burger":40, "Taco":50}

        cc1 = Customer("Andrew")
        cc2 = Customer("Andrew", 5)
        cc3 = Customer("Andrew", 50)
        
		#Test case 1: test if a customer doesn't have enough money in their wallet to order      
        self.assertEqual(cc2.validate_order(self.c2, self.s2, "Burger", 10), None)
        #Test case 1a: test if a customer does have enough money in their wallet to order
        self.assertEqual(cc3.validate_order(self.c2, self.s2, "Burger", 1), None)

		#Test case 2: test if the stall doesn't have enough food left in stock
        self.assertEqual(cc1.validate_order(self.c2, self.s1, "Salad", 1), None)
        #Test case 2a: test if the stall does have enough food left in stock
        self.assertEqual(cc1.validate_order(self.c2, self.s1, "Taco", 1), None)

		#Test case 3: check if the cashier can order item from that stall        
        self.assertEqual(cc1.validate_order(self.c1, Stall("Big House", inventory), "Burger", 1), None)
        #Test case 3a: check if the cashier can actually order item from that stall
        self.assertEqual(cc1.validate_order(self.c1, self.s1, "Burger", 1), None)
        

    # Test if a customer can add money to their wallet
    def test_reload_money(self):

        custo = Customer("Ondrej", 10)

        self.assertEqual(custo.reload_money(10), None)

    
### Write main function
def main():
    #Create different objects 

    #create inventory of dif food obj
    inventory1 = {'Rice': 20, 'Raviolli': 30, 'Chicken': 20, 'Tomato': 25}
    inventory2 = {'Broccoli': 25, 'Onion': 15, 'Beef': 20, 'Potatos': 25}
    

    #customers - names and wallet balance
    fu = Customer("Fu", 200)
    alex = Customer("Alex", 150)
    brady = Customer("Brady", 50)
    

    #stall objects with inventory and prize
    fuelling_blue = Stall("Fuelling Blue", inventory1)
    pizza_house = Stall("Pizza House", inventory2, 25)
    snack_station = Stall("Snack Station", inventory1, 20)
    bobs = Stall("Bob's", inventory2, 35)
    

    #cashiers with food names and list of stalls
    cashier1 = Cashier("Cashier 1", [fuelling_blue, pizza_house])
    cashier2 = Cashier("Cashier 2", [snack_station, bobs])
    cashier3 = Cashier("Cashier 1", [fuelling_blue, bobs])
    

    

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    alex.validate_order(cashier2, "Big House", "Noodles", 10)
    brady.validate_order(cashier1, "Big House", "Humus", 5)
    fu.validate_order(cashier3, "Big House", "Cookies", 9)
    
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    brady.validate_order(cashier1, fuelling_blue, "Broccoli", 10)
    alex.validate_order(cashier2, snack_station, "Watermelon", 10)
    fu.validate_order(cashier3, bobs, "Cookies", 9)

    
    #case 3: the customer does not have enough money to pay for the order: 
    brady.validate_order(cashier1, fuelling_blue, "Rice", 10)
    alex.validate_order(cashier2, snack_station, "Raviolli", 10)
    fu.validate_order(cashier3, bobs, "Broccoli", 10)
    
    #case 4: the customer successfully places an order
    brady.validate_order(cashier1, fuelling_blue, "Rice", 1)
    alex.validate_order(cashier2, snack_station, "Raviolli", 1)
    fu.validate_order(cashier3, bobs, "Broccoli", 2)


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
