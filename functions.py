import csv
import pandas as pd
import datetime
from tabulate import tabulate

# This function calculates the amount of products that are currently in stock and returns the list of all products, number in stock, price it's bought for and the expiration date in table form.

def product_overview():
    inventory = pd.read_csv('inventory.csv')
    inventory['amount_left'] = inventory['num_bought'] - inventory['num_sold']
    select_columns = ['product_name','amount_left', 'bought_price', 'exp_date']
    overview_list = inventory[select_columns].reset_index()
    table_data = [overview_list.columns.tolist()] + overview_list.reset_index().values.tolist()
    table = tabulate(table_data, headers='firstrow', tablefmt='fancy_grid')
    return table
    
# This function returns all products (names) in list form.

def product_list():
    with open('inventory.csv', 'r') as file:
        inventory = csv.reader(file)
        headers = next(inventory)
        product_name_index = headers.index('product_name')
        
        product_list = []
        for product in inventory:
            product_list.append(product[product_name_index])
    return product_list


# This function calculates and returns the remaining inventory of a product.

def total_product(name):
    inventory = pd.read_csv('inventory.csv')
    inventory['amount_left'] = inventory['num_bought'] - inventory['num_sold']

    if name in inventory['product_name'].tolist():
        total_left = inventory.loc[inventory['product_name'] == name,'amount_left'].values[0]
        return total_left
    else:
        return f"Product '{name}' not found in the inventory."


# This function returns, per given product name, the bought price and expiration date.

def product_expiration(name):
    inventory = pd.read_csv('inventory.csv')
    select_columns = ['product_name','bought_price','exp_date']
    product_price_exp_dict = inventory[select_columns].set_index('product_name').to_dict(orient= 'index')
    if name in product_price_exp_dict:
        price_exp = product_price_exp_dict[name]
        return price_exp
    else: 
        return f"Product '{name}' not found in the inventory!"

# This function adds the given buying values to the bought.csv file per line.

def buy(product_id, product_name, bought_price, selling_price, num_bought, num_sold, exp_date):
    with open('bought.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([product_id, product_name, bought_price, selling_price, num_bought, num_sold, exp_date])

# This function adds the given selling values to the sold.csv file per line.

def sell(selling_id, product_name, bought_price, selling_price, num_bought, num_sold, exp_date):
    with open('sold.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([selling_id, product_name, bought_price, selling_price, num_bought, num_sold, exp_date])

# This function helps to reset the date to the current date.

def reset_to_current_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Update 'today.txt' with the current date
    with open('today.txt', 'w') as file:
        file.write(current_date)

# This function takes the date from a text file and adds the number of days given en returns the future date.

def advance_time(days):
    with open('today.txt', 'r') as file:
        today = file.read()
        try:
            today = datetime.datetime.strptime(today, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format in 'today.txt'")
    advanced_date = today + datetime.timedelta(days=days)
    formatted_advanced_date = advanced_date.strftime("%Y-%m-%d")
    with open('today.txt', 'w') as file:
        file.write(formatted_advanced_date)
    return formatted_advanced_date


# This function checks and returns whether a product is expired or not.

def is_expired(name):
    inventory = pd.read_csv('inventory.csv')
    inventory['exp_date'] = pd.to_datetime(inventory['exp_date'])
    with open('today.txt', 'r') as file:
        current = file.read()
        try:
            current = datetime.datetime.strptime(current, "%Y-%m-%d") 
        except ValueError:
            raise ValueError("Invalid date format in 'today.txt")
    inventory['expired'] = ['No' if exp_date > current 
                                  else 'Yes!' if exp_date < current 
                                  else 'Give discount, the product is going to expire today!' 
                                  for exp_date in inventory['exp_date']]

    select_columns = ['product_name', 'selling_price', 'expired', 'exp_date']
    product_check_dict = inventory[select_columns].set_index('product_name').to_dict(orient='index')
    if name in product_check_dict:
        price_exp = product_check_dict[name]
        return price_exp
    else: 
        return f"Product '{name}' not found in the inventory!"
