from features import volume_weight_avg_price, bid_ask_spread, total_qty
series = [
    { "bids": [[3023.00 , 4.0]], "asks": [[860000.00 , 5.0]]},
    { "bids": [[9003.00 , 1.5]], "asks": [[600000.00 , 1.0]]},
    { "bids": [[10900.00 , 3.0]], "asks": [[5000.00 , 3.0]]},
    { "bids": [[100000.00 , 8.0]], "asks": [[1000.00 , 2.0]]},
    { "bids": [[165000.00 , 10.0]], "asks": [[71000.00 , 6.5]]},
    { "bids": [[36000.00 , 1.0]], "asks": [[200000.00 , 3.5]]},
    { "bids": [[18000.00 , 2.0]], "asks": [[111111.00 , 2.0]]},
    { "bids": [[11000.00 , 0.5]], "asks": [[11001.00 , 0.5]]},
    { "bids": [[1000.00 , 4.5]], "asks": [[1000.00 , 4.5]]},
    { "bids": [[6000.00 , 5.5],[9000.00, 1.0]], "asks": [[2000.00 , 1.0], [2200, 1.0 ]]},
    { "bids": [[5912.00 , 30.0]], "asks": [[5900.00 , 1.0]]},
    { "bids": [[66660.11 , 1.0]], "asks": [[66665.00 , 20.5]]},
    { "bids": [[]], "asks": [[78230.00 , 1.5]]},
    { "bids": [[36739.11 , 1.0]], "asks": [[]]},
    { "bids": [[1000.00 , 4.5]], "asks": [[1000.00 , 4.5]]},
]   
## Zero Variables 
def clean_orders(orders):
    """Clean the orders to ensure they are in the correct format,"""
    return [item for item in orders if isinstance(item, list) and len(item) == 2 and item[1] > 0]

def snapshot_to_order(snapshot):
    """Convert a snapshot to a list of orders."""
    bids = clean_orders(snapshot["bids"])
    asks = clean_orders(snapshot["asks"])
    total_buying = sum(qty for price, qty in bids)
    total_selling = sum(qty for price, qty in asks)
    if total_buying > total_selling and total_buying > 0: 
        decision = "GO LONG"
    elif total_selling > total_buying and total_selling > 0:
        decision = "GO SHORT"   
    else:
        decision = "NEUTRAL"
    return decision, total_buying, total_selling
def backtest(series):
    """Backtest the trading strategy on a series of snapshots."""
    final_total_buying = 0
    final_total_selling = 0
    for i, snapshot in enumerate(series, start = 1):
        decision, total_buying, total_selling = snapshot_to_order(snapshot)
        final_total_buying += total_buying
        final_total_selling += total_selling 
        print(f"Snapshot {i}: {decision} | Total Buying: {total_buying} | Total Selling: {total_selling}")
    print(f"Final Total Buying: {final_total_buying} | Final Total Selling: {final_total_selling}")     

    print("\n===Summary===")
    print(f"Final Total Buying Pressure: {final_total_buying }")
    print(f"Final Total Suying Pressure: {final_total_selling }") 
    if final_total_buying > final_total_selling:
        print("Overall Decision: GO LONG")
    elif final_total_selling > final_total_buying:
        print("Overall Decision: GO SHORT" )
    else:
        print("Overall Decision: NEUTRAL")
        
if __name__ == "__main__": 
    backtest(series)