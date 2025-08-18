# Yanira's Portfolio
Univeristy of Michigan Undergrad Student

Major: Undecided - Data Science and Robotics 
### Projects 
Flights Predictor

Machine Learning Therapist 

###Financial Predictor


**data_loader:** This script is design to load and organize stock market data so it can be anaylzed and used for back testing strategies.

  - Downloads the Nifty50 stock market dataset from kaggle 
  
  - Reads CSV files and extracts important information from every order, like whether       it’s a buy or sell, and $ price or quantity.
  
  - It handles errors, ex: missing files, incorrect data. This keeps the code from           crashing 
  
  - Outputs a clean list of orders that can be used in other parts of the project, like      feature generation and backtesting.

**backtest:**:This script makes an elementary trading approach utilizing snapshots of stock market orders. It's goal being to anaylzing the buying and selling pressure of at different points in time and make a decision for each of the snapshots


- Each snapshot contains a list of bids (buy orders) and asks (sell orders).The script cleans the orders to make sure each one has a valid price and quantity.
  - Then it calculates total buying and selling pressure by:
     Adding up the quantities of all buy and sell orders in each snapshot.
    
  - Makes decisions per snapshot:
      If total buying pressure is greater than selling, it outputs GO LONG.
      If selling pressure is greater, it outputs GO SHORT.
      If buying and selling are equal, it outputs NEUTRAL.
    
  - Backtests the entire series:
      Loops through all snapshots, printing the decision, total buying, and total selling for each.
      Calculates the overall total buying and selling pressure.
      Gives an overall trading recommendation based on the total pressure in the form of  (GO LONG, GO SHORT, NEUTRAL) 

**features:** This script aids in the analysis of market behavior as well as extracts important indicators from stock market order book data. It calculates:
    - Bid-ask spread – difference between highest buy and lowest sell prices
    
    - Total quantities – total buy and sell order sizes
    
    - VWAP (Volume Weighted Average Price) – average price weighted by order size
    
    - Order book imbalance – shows whether buying or selling pressure dominates
    
    - Order book depth – liquidity near the top of the order book
    
**model.py:** This scriptkeeps track of buy and sell orders and matches them when the prices overlap: 

    - Buy orders are prioritized by the highest price, while sell orders are prioritized by the lowest price
    
    - When the highest buy price meets or exceeds the lowest sell price, a trade occurs at the average price
    
    - Orders are automatically removed once fully executed
    
    - Uses Python heaps to efficiently manage and match orders based on priority

https://github.com/ydes-cyber/orderbook-friction-strategy.git

