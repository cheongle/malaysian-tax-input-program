from functions import verify_user, calculate_tax, save_to_csv, read_from_csv, check_user_entry, calculate_relief, relief_categories,collect_user_reliefs
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
            print("Invalid IC format!\n")
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
    
    for attempt in range(3):
        password = input("Enter password: ").strip()
    
        if verify_user(ic, password):
            break
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print(f"Authentication failed. You have {remaining} attempt(s) left. Try again.")
            else:
                print("Too many invalid attempts. Exiting the Program...")
                return
    
    while True:
        print("\nWhat would you like to do next?")
        print("1. Enter/Update Income & Tax Relief")
        print("2. View Tax Records Only")
        next_choice = input("Enter your choice (1 / 2): ").strip()

        if next_choice == "1":
            while True:
                try:
                    income = float(input("Enter your annual income: "))
                    if income < 0:
                        print("Income cannot be negative. Please try again.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")

            print("You are automatically granted RM9,000 individual tax relief as a working adult.")
            while True: 
                relief_choice = input("Are you eligible for any other tax reliefs?\n1. Yes\n2. No\n Enter your choice (1 / 2): ").strip()
                if relief_choice in ("1", "2"):
                    break
                else:
                    print("Invalid choice. Please enter 1 / 2")

            if relief_choice == "1":
                print("*********************************************\nAvailable Tax Relief Categories: ")
                user_reliefs = collect_user_reliefs(relief_categories)
                if not user_reliefs:
                    print("No tax reliefs.")
                    relief = 9000
                else:
                    relief = calculate_relief(user_reliefs)
            else:
                print("Skipping tax reliefs as requested...")
                relief = 9000
    
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
            break

        elif next_choice == "2":
            print("\nViewing records...")
            break

        else:
            print("Invalid option. Please choose 1 or 2.\n")
            
    print("*********************************************\nTax Records: ")
    df = read_from_csv(FILENAME)
    if df is not None:
        print(df.to_string(index = False))
    else: 
        print("No records found.")

if __name__ == "__main__" :
    main()