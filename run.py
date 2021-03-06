import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, validate that user provided exactly 6 values. Validate
     that each value can be converted to an integer. Convert values to
     integers. Raise ValueError if neither test doesn't pass
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Updates the required worksheet in the data spreadsheet with a new row of
     data
    """
    print(f"Updating {worksheet} worksheet...\n")
    updated_worksheet = SHEET.worksheet(worksheet)
    updated_worksheet.append_row(data)
    print(f"{worksheet} data updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Calculate the surplus using the sales and stock data
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_five_entries_sales():
    """
    Grab the last 5 values for eacn sandwich type
     in the sales worksheet; returns a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns_data = []
    for ind in range(1, 7):
        col_data = sales.col_values(ind)
        columns_data.append(col_data[-5:])

    return columns_data


def calculate_stock_data(data):
    """
    Return average of last 5 days for each sandwich type and add 10%
    """
    print("Calculating stock data...\n")

    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    print(stock_data)


print("Welcome to Love Sandwiches Data Automation Program")
main()
