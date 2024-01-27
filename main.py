import argparse
import functions

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():

# This code defines the parser with argparse and adds a subparser that takes a command.
    
    product_parser = argparse.ArgumentParser(prog="Superpy", usage="Buy | Sell | Report | Advance days | Reset date", description="Welcome to the Superpy CLI! Track all buying and selling transactions, create reports and time travel with this program")
    subparsers = product_parser.add_subparsers(dest="command")

# This code defines the subparser that helps the user to enter what they buy. It takes multiple arguments to provide all the necessary information.

    buy_subparser = subparsers.add_parser("buy", description="Parser for registering bought products")
    buy_subparser.add_argument("id", help="A new id", type=int)
    buy_subparser.add_argument("product_name", help="The name of the product bought/imported", type=str)
    buy_subparser.add_argument("amount_bought", help="The number of products bought/imported", type=int, default=1)
    buy_subparser.add_argument("amount_sold", help="The number of products sold", type=int, default=1)
    buy_subparser.add_argument("buying_price", help="The import price", type=float)
    buy_subparser.add_argument("selling_price", help="The price its sold for", type=float)
    buy_subparser.add_argument("expiration_date", help="Product expires at this date")

# This code defines the subparser that helps the user to enter what they sell. It takes the same arguments as the buying parser.

    sell_subparser = subparsers.add_parser("sell", description="Parser for registering sold products")
    sell_subparser.add_argument("selling_id", help="A new transaction id", type=int)
    sell_subparser.add_argument("product_name", help="The name of the product sold", type=str)
    sell_subparser.add_argument("amount_bought", help="The number of products sold", type=int, default=1)
    sell_subparser.add_argument("amount_sold", help="The number of products sold", type=int, default=1)
    sell_subparser.add_argument("buying_price", help="The price the product is sold for", type=float)
    sell_subparser.add_argument("selling_price", help="The price the product is sold for", type=float)
    sell_subparser.add_argument("expiration_date", help="Product expires at this date")

# This code defines the subparser that helps the user to time travel. It takes one argument: days.

    advance_time_subparser = subparsers.add_parser("advance_time", description="Parser for advancing time")
    advance_time_subparser.add_argument("days", help="Amount of days you would like to advance", type=int)

# This code defines the subparser that helps the user to retrieve information on all the products. It could, if provided, also output specific information on stock per product. This last option requires one argument: product_name.

    report_subparser = subparsers.add_parser("report", description="Parser for reporting current stock, revenue and profit")
    report_subparser.add_argument("report_type", help="Type here product_list, stock, revenue or profit for reporting", choices=["product_list", "stock", "is_expired", "product_info"])
    report_subparser.add_argument("--product_name", help="The name of the product you want to know the current stock amount of", type=str)

# This code defines the subparser that helps the user to reset the date to the current date.

    subparsers.add_parser("reset_date", description="Parser for resetting date to current date")
    

#This line of code stores the parsed arguments in a variable that can and will be used in the if statements below.

    args = product_parser.parse_args()

#These if statements operate on the arguments that are provided in the CLI. Each one is connected to the functions created in the functions.py file.

    if args.command in ["buy", "sell", "report", "advance_time", "reset_date"]:

#This if statement retrieves various buying related values and passes it through the function to be stored in the designated csv.

        if args.command == "buy":
            bought_id = args.id
            product_name = args.product_name
            buying_price = args.buying_price
            selling_price = args.selling_price
            amount_bought = args.amount_bought
            amount_sold = args.amount_sold
            expiration_date = args.expiration_date
            functions.buy(bought_id, product_name, buying_price, selling_price, amount_bought, amount_sold, expiration_date)

#This if statement retrieves various selling related values and passes it through the function to be stored in the designated csv.

        elif args.command == "sell":
            selling_id = args.selling_id
            product_name = args.product_name
            amount_bought = args.amount_bought
            amount_sold = args.amount_sold
            buying_price = args.buying_price
            selling_price = args.selling_price
            expiration_date = args.expiration_date
            functions.sell(selling_id, product_name, buying_price, selling_price, amount_bought, amount_sold, expiration_date)

# This if statement passes through the number of days given to the function that advances time. It outputs the future date.

        elif args.command == "advance_time":
            days = args.days
            print(functions.advance_time(days))
        
        elif args.command == "reset_date":
            functions.reset_to_current_date()

# The report if statement is required to pass through another argument, either product_list, stock, is_expired or product_info 
# the last three elif statements take another agument: product_name). 
# It outputs either a product list or the number of product that is still in stock. But also whether a product is expired or some basic information on the product.

        elif args.command == "report":
            if args.report_type == "product_list":
                print(functions.product_overview())
            elif args.report_type == "stock":
                product_name = args.product_name
                print(functions.total_product(product_name))
            elif args.report_type == "is_expired":
                product_name = args.product_name
                print(functions.is_expired(product_name))
            elif args.report_type == "product_info":
                product_name = args.product_name
                print(functions.product_expiration(product_name))


if __name__ == "__main__":
    main()