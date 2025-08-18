def bid_ask_spread(bids, asks):
    """
    Calculate the bid-ask spread using the highest bid and lowest ask from the first snapshot.
    """
    if not bids or not asks or not bids[0] or not asks[0]:
        return None  # or raise an Exception

    max_bid = max(price for price, qty in bids)
    min_ask = min(price for price, qty in asks)
    spread = min_ask - max_bid
    return spread

def total_qty(bids, asks):
    """
    Loop through the list of bids and asks and return the sum of the quantities in the first snapshot.
    """
    if not bids or not asks or not bids or not asks:
        return None, None  # or raise an Exception

    total_bid_qty = sum(qty for price, qty in bids)
    total_ask_qty = sum(qty for price, qty in asks)
    return total_bid_qty, total_ask_qty


def volume_weight_avg_price (orders):
    """ Calculate the volume-weighted average price (VWAP) for bids and asks"""
    if not orders: 
        return None
    total_qty = sum(qty for price, qty in orders)
    if total_qty == 0:
        return None  # Avoid division by zero
    
    vwap = sum(float(price) * float(qty) for price, qty in orders) / total_qty
    return vwap

def orderbook_imbalance(bids, asks):
    """Calculate the order book imblance as a percentage of the total volume"""
    bid_volume = sum(qty for price, qty in bids)
    asks_volume = sum(qty for price, qty in asks)
    total_volume = bid_volume + asks_volume 
    if total_volume == 0:
        return 0 
    imbalance = (bid_volume - asks_volume)/ total_volume 
    return imbalance 

def orderbook_depth(bids, asks):
    """Calculate the order book depth as the sum of the top N bids and asks"""
    from itertools import islice 
    N = 5 # This can be adjusted based on the depth required 
    top_bids = sum(qty for price, qty in islice(bids, N))
    top_asks = sum(qty for price, qty in islice(asks, N))
    return top_bids + top_asks 

def features ( bids, asks):
    """Calculate various features from the order book data."""
    results = {}
    results['bid_ask_spread'] = bid_ask_spread(bids, asks)