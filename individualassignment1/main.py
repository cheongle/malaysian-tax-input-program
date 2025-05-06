from functions import verify_user, calculate_tax, save_to_csv, read_from_csv, check_user_entry
import pandas as pd

FILENAME = 'tax_data.csv'

def main():
    print("Welcome to the Malaysian Tax Input Program!\n*********************************************")

    while True:
        print("1. Login.")
        print("2. Exit.")
        login_choice = input("Choose an option: ").strip()

        if login_choice == "2":
            print("Exiting the Program. Goodbye!")
            return
        elif login_choice != "1":
            print("Invalid option. Please choose 1 or 2.")
            continue

        user_id = input("Enter your ID: ").strip()
        ic = input("Enter your 12-digit IC number without hyphen. (Last 4 digits will be your password): ")

        if not verify_user(ic, ic[-4:]):
            print("Invalid IC format or password!\n")
            continue

        is_allowed, is_new_user = check_user_entry(user_id, ic, FILENAME)

        if not is_allowed:
            print("Your ID or IC do not match our existing records. Please Try Again.\n")
            continue
        
        if is_new_user:
            print("Your user ID and IC have been successfully registered!\n")
        else:
            print("Welcome back!\n")

        break
    
    password = input("Enter password: ").strip()
    
    if not verify_user(ic, password):
        print("Authentication failed.\n")
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

    print("*********************************************\nTax Records: ")
    df = read_from_csv(FILENAME)
    if df is not None:
        print(df.to_string(index = False))
    else: 
        print("No records found.")

if __name__ == "__main__" :
    main()