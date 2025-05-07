import pandas as pd
import os 

def verify_user(ic_number, password):
    """
    3a. Verifies user login using IC Number and Password.
    The password is the last 4 digits of the 12-digit IC Number.

    Returns:
        True if IC format is correct and password matches.
        False otherwise.
    """
    return len(ic_number) == 12 and password == ic_number[-4:]

def calculate_tax(income, tax_relief):
    """
    3b. Calculates tax payable based on progressive Malaysian tax brackets.

    Args:
        income (float): Annual income of the user.
        tax_relief (float): Total tax relief eligible.

    Returns:
        float: Tax amount rounded to two decimals.
    """

    # Deduct relief from income to get taxable income
    taxable_income = max(0, income - tax_relief)

    # Apply Malaysian tax brackets
    if taxable_income <= 5000:
        tax = 0
    elif taxable_income <= 20000:
        tax = taxable_income * 0.01
    elif taxable_income <= 35000:
        tax = taxable_income * 0.03
    elif taxable_income <= 50000:
        tax = taxable_income * 0.06
    elif taxable_income <= 70000:
        tax = taxable_income * 0.11
    elif taxable_income <= 100000:
        tax = taxable_income * 0.19
    elif taxable_income <= 400000:
        tax = taxable_income * 0.25
    elif taxable_income <= 600000:
        tax = taxable_income * 0.26
    elif taxable_income <= 2000000:
        tax = taxable_income * 0.28
    else:
        tax = taxable_income * 0.30 
    return round(tax, 2)

def save_to_csv(data, filename):
    """
    3c. Saves user tax data to a CSV file.
    Overwrites existing record for the same IC Number.

    Args:
        data (dict): Dictionary containing user ID, IC, income, relief and tax.
        filename (str): File path to the CSV file.
    """

    # Ensure IC is stored as 12-digit string
    data['IC Number'] = str(data['IC Number']).zfill(12)
    df_new = pd.DataFrame([data])

    if os.path.exists(filename):
        # Read existing data and remove old entry for the same IC
        df_existing = pd.read_csv(filename, dtype = {'IC Number': str})
        df_existing['IC Number'] = df_existing['IC Number'].apply(lambda x: str(x).zfill(12))
        df_combined = df_existing[df_existing['IC Number'] != data['IC Number']]
        df_combined = pd.concat([df_combined, df_new], ignore_index = True)
    else:
        df_combined = df_new

    # Save the updated DataFrame
    df_combined.to_csv(filename, index = False)

def read_from_csv(filename):
    """
    3d. Reads and returns contents of a CSV file as a pandas DataFrame.

    Args:
        filename (str): File path.

    Returns:
        DataFrame if file exists, otherwise None.
    """

    if not os.path.exists(filename):
        return None
    return pd.read_csv(filename)

def check_user_entry(user_id, ic_number, filename):
    """
    Check if the user's ID and IC are registered or new.

    Returns:
        (is_allowed, is_new_user)
        is_allowed (bool): Whether the user is allowed to log in or register.
        is_new_user (bool): True if the user is new and not yet in records.
    """

    if not os.path.exists(filename):
        # File doesn't exist, hence fresh entry.
        return True, True
    
    df = pd.read_csv(filename, dtype = {'IC Number': str})
    df['IC Number'] = df['IC Number']

    # Find matching ID and IC
    match_ic = df[df['IC Number'] == ic_number]
    match_id = df[df['ID'] == user_id]

    if match_ic.empty and match_id.empty:
        return True, True # New User
    elif not match_ic.empty and match_ic.iloc[0]['ID'] == user_id:
        return True, False # Returning User
    else:
        return False, False # Mismatch

# List of available tax reliefs with cap and type
relief_categories = [
    ("spouse", 4000, "fixed"),
    ("child", 8000, "variable"),
    ("medical", 8000, "fixed"),
    ("lifestyle", 2500, "fixed"),
    ("education", 7000, "fixed"),
    ("parental", 5000, "fixed"),
]

# Set of valid relief names for quick lookup
valid_relief_categories = {r[0] for r in relief_categories}

def calculate_relief(user_reliefs):
    """
    Calculates total tax relief based on user-provided reliefs.

    Args:
        user_reliefs (dict): Dictionary of selected relief categories and amounts.

    Returns:
        float: Total relief amount (including base RM9,000 individual relief).
    """

    total_relief = 9000 # Base Relief
    claimed = set() # To keep track of what was claimed

    for relief_name, amount in user_reliefs.items():
        if relief_name not in valid_relief_categories:
            continue
        for category, cap, mode in relief_categories:
            if relief_name == category:
                if mode == "fixed":
                    total_relief += min(amount, cap)
                    claimed.add(relief_name)
                elif mode == "variable":
                    n = min(int(amount), 12)
                    total_relief += n * cap
                    claimed.add(relief_name)
                break
    return total_relief

def collect_user_reliefs(relief_categories):
    """
    Asks the user which additional tax reliefs they are eligible for and collects relevant data.

    Args:
        relief_categories (list): List of available reliefs.

    Returns:
        dict: User-inputted reliefs and their values.
    """

    # Show relief options to user
    for idx, (name, cap, mode) in enumerate(relief_categories, start = 1):
        print(f"{idx}.{name.capitalize()} (Max: RM{cap})")

    # Ask for user selections
    chosen = input("\nEnter the numbers of the reliefs you are eligible to claim (separated by commas, e.g. 1,3,5): ")
    selected_indices = [int(x.strip()) for x in chosen.split(",") if x.strip().isdigit()]

    user_reliefs = {}

    # Process each selected relief
    for idx in selected_indices:
        if 1 <= idx <= len(relief_categories):
            name, cap, mode = relief_categories[idx - 1] 

            # Special check for spouse income requirement
            if name == "spouse":
                while True: 
                    try:
                        spouse_income = float(input("Enter your spouse's annual income (RM): "))
                        if spouse_income < 0:
                            print("Income cannot be negative. Please try again.")
                        elif spouse_income <= 4000:
                            user_reliefs[name] = cap
                            break
                        else: 
                            print("Spouse income exceeds RM4,000. Relief not applicable.")
                            break
                    except ValueError:
                        print("Invalid income input. Please try again.")
                continue

            # Handle variable child reliefs
            if mode == "variable" and name == "child":
                while True:
                    try:
                        children = int(input("Enter number of children (max 12, 8000 each): "))
                        if children < 0:
                            print("Number of children cannot be negative. Please try again.")
                        else:
                            user_reliefs[name] = children
                            break
                    except ValueError:
                        print("Invalid number. Please enter a whole number.")

            else:
                # Fixed reliefs (eg. medical, lifestyle)
                while True:
                    try:
                        amt = float(input(f"Enter amount for {name.capitalize()} relief (Max RM{cap}): "))
                        if amt < 0:
                            print("Amount cannot be negative. Please try again.")
                        else:
                            user_reliefs[name] = amt
                            break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
        else: 
            print(f"Invalid selection: {idx}")
    return user_reliefs