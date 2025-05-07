import pandas as pd
import os 

def verify_user(ic_number, password):
    #3a.
    return len(ic_number) == 12 and password == ic_number[-4:]

def calculate_tax(income, tax_relief):
    #3b.
    taxable_income = max(0, income - tax_relief)
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
    #3c.
    data['IC Number'] = str(data['IC Number']).zfill(12)
    df_new = pd.DataFrame([data])

    if os.path.exists(filename):
        df_existing = pd.read_csv(filename, dtype = {'IC Number': str})
        df_existing['IC Number'] = df_existing['IC Number'].apply(lambda x: str(x).zfill(12))
        df_combined = df_existing[df_existing['IC Number'] != data['IC Number']]
        df_combined = pd.concat([df_combined, df_new], ignore_index = True)
    else:
        df_combined = df_new

    df_combined.to_csv(filename, index = False)

def read_from_csv(filename):
    #3d.
    if not os.path.exists(filename):
        return None
    return pd.read_csv(filename)

def check_user_entry(user_id, ic_number, filename):
    """
    Returns (is_allowed: bool, is_new_user: bool)
    """
    if not os.path.exists(filename):
        return True, True
    
    df = pd.read_csv(filename, dtype = {'IC Number': str})
    df['IC Number'] = df['IC Number']

    match_ic = df[df['IC Number'] == ic_number]
    match_id = df[df['ID'] == user_id]

    if match_ic.empty and match_id.empty:
        return True, True
    elif not match_ic.empty and match_ic.iloc[0]['ID'] == user_id:
        return True, False
    else:
        return False, False

relief_categories = [
    ("spouse", 4000, "fixed"),
    ("child", 8000, "variable"),
    ("medical", 8000, "fixed"),
    ("lifestyle", 2500, "fixed"),
    ("education", 7000, "fixed"),
    ("parental", 5000, "fixed"),
]

valid_relief_categories = {r[0] for r in relief_categories}

def calculate_relief(user_reliefs):
    total_relief = 9000
    claimed = set()

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
    for idx, (name, cap, mode) in enumerate(relief_categories, start = 1):
        print(f"{idx}.{name.capitalize()} (Max: RM{cap})")

    chosen = input("\nEnter the numbers of the reliefs you are eligible to claim (separated by commas, e.g. 1,3,5): ")
    selected_indices = [int(x.strip()) for x in chosen.split(",") if x.strip().isdigit()]

    user_reliefs = {}

    for idx in selected_indices:
        if 1 <= idx <= len(relief_categories):
            name, cap, mode = relief_categories[idx - 1] 
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