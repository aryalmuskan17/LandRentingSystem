import datetime
import random
import string

# Function to write land data back to the file 
def write_land_data(land_data, file_name):
    with open(file_name, 'w') as file:
        for land in land_data:
            file.write(f"{land['kitta_number']}, {land['city_district']}, {land['direction']}, {land['area']}, {land['price']}, {land['status']}\n")

# Function to generate a random transaction code
def generate_transaction_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(8))

# Function to rent a land
def rent_land(land_data, kitta_number, customer_name, duration):
    try:
        # Attempt to convert duration to an integer
        duration = int(duration)
    except ValueError:
        # If duration cannot be converted to an integer, handle the exception
        print("Invalid input for duration. Please enter a valid integer value.")
        return None, None, 0, None
    # Check if the duration is at least 6 months
    if duration < 6:
        print("Minimum duration for renting is 6 months.")
        return None, None, 0, None
    
    # Iterate through land data to find the specified land
    for land in land_data:
        # Check if kitta number matches and land is available for rent
        if str(land["kitta_number"]) == kitta_number and land["status"] == "Available":
            # Check if price per month is provided
            if land["price"] is not None:
                # Calculate total amount
                total_amount = land["price"] * duration
                # Update land status
                land["status"] = "Not Available"
                # Generate transaction code
                transaction_code = generate_transaction_code()
                land["transaction_code"] = transaction_code  # Assign transaction code to the land
                return land_data, land, total_amount, transaction_code
            else:
                print("Price per month is not provided for this land.")
                return None, None, 0, None
    
    print("Land not available for rent or invalid kitta number.")
    return None, None, 0, None

# Function to return a rented land
def return_land(land_data, kitta_number, customer_name, duration, return_duration, transaction_code_input):
    fine = None  # Initialize fine to None
    # Iterate through land data to find the specified land
    for land in land_data:
        # Check if kitta number matches and land is not available
        if str(land["kitta_number"]) == kitta_number and land["status"] == "Not Available":
            # Check if transaction code matches
            if "transaction_code" in land and land["transaction_code"] == transaction_code_input:
                # Check if price per month is provided
                if land["price"] is not None:
                    # Calculate total amount
                    total_amount = land["price"] * duration
                    # Apply fine if return duration is different from rental duration
                    if return_duration < duration:
                        fine = total_amount * 0.05
                        total_amount += fine
                    # Update land status
                    land["status"] = "Available"
                    write_land_data(land_data, "land_data.txt")
                    return land_data, land, total_amount, fine, True  # Return True to indicate successful return
                else:
                    print("Price per month is not provided for this land.")
                    return None, None, 0, None, False
            else:
                print("Invalid transaction code.")
                return None, None, 0, None, False
    
    print("Invalid kitta number or land not rented.")
    return None, None, 0, fine, False

# Function to generate invoice
def generate_invoice(transaction_type, customer_name, land, duration, total_amount, transaction_code, fine=None):
    # Constructing the top part of the invoice
    bill_top = f"""
                                        Techno Property Nepal
                                    Hospital Chowk-10, Pokhara, Nepal
VAT No: 1769                                                                            Ph. No:99999999999

Name: {customer_name:<20}                                                               Date: {datetime.datetime.now().date()}
Transaction Code: {transaction_code}
--------------------------------------------------------------------------------------------------------
| Kitta Number | Customer Name   | City/District | Direction | Area | Duration of Rent | Total Amount |
--------------------------------------------------------------------------------------------------------
"""

    # Constructing the middle part of the invoice
    bill_middle = f"\n| {land['kitta_number']:<12} | {customer_name:<15} | {land['city_district']:<17} | {land['direction']:<9} | {land['area']:<5} | {duration:<10} | {total_amount:<14} |"

    # If there's a fine, add a row for it in the middle part of the invoice
    if fine is not None:
        total_amount += fine
        bill_middle += f"\n| Fine                                                                                 | {fine:<13} |"

    # Calculating VAT and grand total
    vat = 0.13 * total_amount
    grand_total = total_amount + vat

    # Constructing the bottom part of the invoice
    bill_bottom = f"""
--------------------------------------------------------------------------------------------------------
                                                                        Taxable Total: NPR {total_amount}
                                                                                  VAT: NPR {vat:.2f}
                                                                          Grand Total: NPR {grand_total}
"""

    # Combining all parts of the invoice
    bill = bill_top + bill_middle + bill_bottom

    # Append invoice text to the file
    file_name = f"{customer_name.replace(' ', '_')}_invoices.txt"
    with open(file_name, "a") as file:
        file.write(bill)

    # Print bill to console
    print(bill)