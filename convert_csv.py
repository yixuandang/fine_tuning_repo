import json
import csv
import sys

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <input_json_file> <output_csv_file>")
    sys.exit(1)

input_json_file = sys.argv[1]
output_csv_file = sys.argv[2]

# Open the JSON file and load the data
with open(input_json_file, 'r') as json_file:
    data = json.load(json_file)

# Define the fieldnames
fieldnames = list(data[0].keys()) if data else []

# Write data to CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write rows
    for item in data:
        writer.writerow(item)

print(f"CSV file '{output_csv_file}' has been created successfully.")

