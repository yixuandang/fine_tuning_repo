import json
import sys

def clean_json(input_file):
    cleaned_data_list = []

    # Load the combined JSON data
    with open(input_file, 'r') as f:
        combined_json = json.load(f)

    for data in combined_json:
        # Check if any of the required fields is empty or null
        if not data.get('title') or not data.get('description') or not data.get('comments'):
            continue  # Skip this JSON object if any required field is empty or null

        # Extract only the required fields and create a new dictionary for each JSON object
        cleaned_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'comments': data.get('comments')
        }

        cleaned_data_list.append(cleaned_data)

    return cleaned_data_list


def merge_json(cleaned_data_list):
    # Write the cleaned data to a new JSON file
    output_file = 'merged_cleaned_data.json'
    with open(output_file, 'w') as f:
        json.dump(cleaned_data_list, f, indent=4)

    print(f"Data merged and written to {output_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python jsd_cleanup.py <input_json_file>")
        return

    input_file = sys.argv[1]
    cleaned_data_list = clean_json(input_file)
    merge_json(cleaned_data_list)


if __name__ == "__main__":
    main()

