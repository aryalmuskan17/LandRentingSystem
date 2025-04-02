# Importing necessary functions from modules
from data_handler import read_land_data
from transaction_handler import rent_land, return_land, generate_invoice, write_land_data

# Function to display all lands
def display_all_lands(land_data):
    print("All Lands:")
    for land in land_data:
        print(f"Kitta Number: {land['kitta_number']}, City/District: {land['city_district']}, Land Facing: {land['direction']}, Area: {land['area']} anna, Price per Month: {land['price']}, Status: {land['status']}")

# Function to display available lands for rent
def display_available_lands(land_data):
    print("Available Lands:")
    for land in land_data:
        if land["status"] == "Available":
            print(f"Kitta Number: {land['kitta_number']}, City/District: {land['city_district']}, Land Facing: {land['direction']}, Area: {land['area']} anna, Price per Month: {land['price']}")

# Main function to control the flow of the program
def main():
    # Reading land data from file
    land_data = read_land_data("land_data.txt")
    
    # Main program loop
    while True:
        # Printing menu options
        print("*" * 140)
        print(" Welcome To TechnoPropertyNepal Land Renting System".center(140))
        print("*" * 140)
        print("1. Display All Lands".center(140))
        print("2. Rent Land".center(140))
        print("3. Return Land".center(140))
        print("4. Exit".center(140))
        
        # Getting user choice
        choice = input("Select your choice:\n".center(140))
        
        # Branching based on user choice
        if choice == "1":
            display_all_lands(land_data)
        elif choice == "2":
            # Renting land
            display_available_lands(land_data)
            num_lands = int(input("Enter the number of lands you want to rent: "))
            customer_name = input("Enter customer name: ")
            for _ in range(num_lands):
                display_available_lands(land_data)
                kitta_number = input("Enter the kitta number of the land to rent: ")
                duration = int(input("Enter duration of rent (months): "))
                land_data, land, total_amount, transaction_code = rent_land(land_data, kitta_number, customer_name, duration)
                if land:
                    generate_invoice("rent", customer_name, land, duration, total_amount, transaction_code)
                    print("Land rented successfully.")
                    # Write updated land data back to file
                    write_land_data(land_data, "land_data.txt")
                else:
                    print("Land not available for rent or invalid kitta number.")
        elif choice == "3":
            # Returning land
            kitta_number = input("Enter the kitta number of the land to return: ")
            customer_name = input("Enter customer name: ")
            return_duration = int(input("Enter duration of rental period (months): "))
            transaction_code_input = input("Enter the transaction code: ")
            land_data, land, total_amount, fine, success = return_land(land_data, kitta_number, customer_name, return_duration, duration, transaction_code_input)
            if success:
                generate_invoice("return", customer_name, land, return_duration, total_amount, transaction_code_input, fine=fine)
                print("Land returned successfully.")
                 # Write updated land data back to file
                write_land_data(land_data, "land_data.txt")
            else:
                print("Error returning land.")
        elif choice == "4":
            # Exiting the program
            print("Thank you for using our service.")
            print("Namaste, Have a great day.")
            break
        else:
            # Handling invalid input
            print("Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Please enter valid choice")
            print("Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# Entry point of the program
if __name__ == "__main__":
    main()
