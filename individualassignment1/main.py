from functions import verify_user, calculate_tax, save_to_csv, read_from_csv
import pandas as pd

FILENAME = 'tax_data.csv'

def main():
    print("Welcome to the Malaysian Tax Input Program!")

    user_id = input("Enter your ID: ")
    ic = input("Enter your 12-digit IC number without hyphen. (Last 4 digits will be your password): ")

    if not verify_user(ic, ic[-4:]):
        print("Invalid IC format or password!")
        return
    
    password = input("Enter password: ")
    
    if not verify_user(ic, password):
        print("Authentication failed.")
        return
    
    try:
        income = float(input("Enter your annual income: "))
        relief = float(input("Enter your tax relief amount: "))
    except ValueError:
        print("Please enter valid numbers.")
        return
    
    tax = calculate_tax(income, relief)
    print(f"Your tax payable is: RM {tax}")

    data = {
        'ID' : user_id,
        'IC Number' : ic,
        'Income' : income,
        'Tax Relief' : relief,
        'Tax Payable' : tax
    }

    save_to_csv(data, FILENAME)

    print("\nTax Records: ")
    df = read_from_csv(FILENAME)
    if df is not None:
        print(df.to_string(index = False))
    else: 
        print("No records found.")

if __name__ == "__main__" :
    main()