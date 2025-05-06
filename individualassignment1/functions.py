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
