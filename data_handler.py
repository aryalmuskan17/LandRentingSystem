# Function to read land data from a file
def read_land_data(file_name):
    # Initialize an empty list to store land data
    land_data = []
    
    # Open the file for reading
    with open(file_name, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Split the line by comma and strip any extra spaces
            parts = line.strip().split(', ')
            
            # Check if the line contains all required fields
            if len(parts) == 6:
                # Create a dictionary representing a single land entry
                land_entry = {
                    "kitta_number": int(parts[0]),    # Convert kitta number to integer
                    "city_district": parts[1],         # City/District name
                    "direction": parts[2],             # Direction the land is facing
                    "area": int(parts[3]),             # Area of the land in anna (assuming)
                    "price": int(parts[4]),            # Price per month for renting the land
                    "status": parts[5]                 # Status of the land (Available or Occupied)
                }
                # Add the land entry to the list
                land_data.append(land_entry)
            else:
                # Print a warning message if the line doesn't have the correct format
                print(f"Invalid data format in line: {line.strip()}")
    
    # Return the list containing all land data
    return land_data
