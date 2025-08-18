import heapq ## python heapq code(heaps ares trees where each parent is ordered before its children)
"""This code simulates how a basic order book works in the financial markets.
    It keeps an account of who wants to buy or sell what at what $$$ and quanttiy
    ALL done by ORDERBOOKMODEL
    Buy orders - This defines the highest payers those willing to spend the most money
    Sell orders - This defines the cheapest sellers, those that want to sell at low prices
    This code organizes these two so that they are always at the top of the sell list
    Moreover, when there is an overlap between the highest price someone is willing to pay
    more than or equal to the cheapest sale price then the code creates a trade
        - priority for those willing to pay more and those that want to sell for the lowest
        - trade happens at the avg price of the overlap price"""
## This is the blueprint for creating objects that handle order book data.
class OrderBookModel:
    def __init__(self):
        ## This is a list that will hold the order book data 
        self.buy_orders = []
        self.sell_orders = []

""" defines a method to add orders to the order book
     Takes the order_type(string: buy,sell), price (number): price per unit for the order, and quanity(number: units to buy or sell)"""
def add_order(self, order_type, price, quantity):
## This is making a dictionary order to represent one order 
    order = {"type": order_type, "price": price, "quantity": quantity}
    
    if order_type == "buy":
        self.buy_orders.append(order) ## adds the new buy order dictionary to the buy_orders list
        self.buy_orders.sort(key=lambda x: -x["price"])## sores the buying_orders list in descending order by the price where high payers get priority )
        ## The lamda x: -x[]"price"] is to sort by negative prices 
   
    elif order_type == "sell":
        self.sell_orders.append(order) #adds the new buy order dictionary to the sell_orders list
        self.sell_orders.sort(key=lambda x: x["price"]) ## people that are willing to accept sell for less are prioritized 
        self.match_orders() ## matches buying and sell orders 

def match_orders(self):
    trades = []
    ## Loops both buy orders and sell orders
    while self.buy_orders and self.sell_orders:
        highest_buy = self.buy_orders[0] ## Checks the best buyer (highest prices) and puts it in first place in buy orders
        highest_sell = self.sell_orders[0] ## looks at lowest sale and puts it in first in sell_orders
        
        if highest_buy["price"] >= highest_sell["price"]:   
        ## if there is an ovelap between these two quantities it means that there is a trade that can be done 
            trade_qty = min(highest_buy["quantity"], highest_sell["quantity"])    
            trade_price_avg = (highest_buy["price"]+ highest_sell["price"])/2 ## Calculates the trade price as the avg of the buying and selling 
            trades.append({"price": trade_price_avg, "quantity" : trade_qty})
            highest_buy["quanitity"] -= trade_qty
            highest_sell["quantity"] -= trade_qty
    
    ## Making a conditional statement that if buy order is full (0) remove it from the list of buy orders      
        if highest_buy["quantity"] == 0:
            self.buy_orders.pop(0) 
            
        if highest_sell["quantity"] == 0:
            self.sell_orders.pop(0)    
        
        else: 
            break 
    
    return trades 

"""The class Order takes each order and turns it into an object and comparing them in a way 
    that we described in the first section of the code but with min and max. 
    Heaps takes the most appealing order and places it at the top. 
    Once the quantity becomes 0 it's removed from the sysem
        - Makes it fasters to match buyers and sellers """
class Order: 
    def __init__(self, price, volume, side):
        self.price = price 
        self.volume = volume 
        self.side = side 
## Makes the objects above comparable 
    def __lt__(self, other):
        if self.side == 'buy':
            return self.price > other.price 
        else:
            return self.price < other.price 
        
class Orderbook: 
    def __inti__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == 'buy':
            heapq.heapqpush(self.buy_orders, order) ## heapqpush maintains the heap property 
        
        else: 
            heapq.heappush(self.sell_orders, order)
            
    def match_orders(self):
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]
            
            if best_buy.price > best_sell.price:
                traded_volume = min(best_buy.volume, best_sell.volume)
                print(f"Trade executed: {traded_volume} units at {best_sell.volume}")
                best_buy.volume -= traded_volume 
                best_sell.volume -= traded_volume 
            
            if best_buy == 0: # If order is satisfied then remove it from the heap 
                heapq.heappush(self.buy_orders)
                
            if best_sell == 0:
                heapq.headpush(self.sell_orders)
            
            else:
                break 
        
    