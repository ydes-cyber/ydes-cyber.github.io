import csv
import kagglehub
import pandas as pd
import os

path = kagglehub.dataset_download("rohanrao/nifty50-stock-market-data")

print("Path to dataset files:", path)

def load_orders_from_dataset(csv_file_path): 
    orders = []
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for order in reader:
                order_type = order.get('type', '').lower()
                
                if order_type in ['buy', 'sell']: 
                    converted_order = {
                        'type': order_type,
                        'price': float(order.get('price', 0)),
                        'quantity': int(order.get('quantity', 0))
                    }
                    orders.append(converted_order)
        return orders
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while loading orders: {e}")
        return []
files = os.listdir(path)
print("Files available:", files)
csv_file = os.path.join(path, files[0])
orders = load_orders_from_dataset(csv_file)
print(orders[:5])     
    