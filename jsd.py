import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict
import argparse

def identify_valid_tags(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')
    valid_tags = set()

    for tag in soup.find_all(True):
        valid_tags.add(tag.name)

    return valid_tags

def extract_data_from_xml(xml_content, valid_tags):
    soup = BeautifulSoup(xml_content, 'xml')
    item = soup.find('item')
    
    if item is None:
        return None

    data = defaultdict(lambda: defaultdict(str))

    for tag_name in valid_tags:
        tag_list = item.find_all(tag_name)
        if tag_list:
            tag_value = tag_list[0].text

            # Ignore attributes with values equal to "", "\n", "\n\n", "\n\n\n" or "0"
            if tag_value not in ["", "\n", "0", "1","\n\n", "\n\n\n", "No CHANGES needed","IT Help"]:
                if tag_name == 'project':
                    data[tag_name] = {
                        'id': tag_list[0].get('id', ''),
                        'key': tag_list[0].get('key', ''),
                        'name': tag_value
                    }
                elif tag_name in ['status', 'resolution']:
                    data[tag_name] = {
                        'id': tag_list[0].get('id', ''),
                        'name': tag_value
                    }
                elif tag_name in ['comment', 'attachment']:
                    data[tag_name + 's'] = [{
                        'id': tag.get('id', ''),
                        'author': tag.get('author', ''),
                        'created': tag.get('created', ''),
                        'text': tag.text
                    } for tag in tag_list if tag.get('id', '') not in ["", "\n", "0"] and tag.get('author', '') not in ["", "\n", "0"] and tag.get('created', '') not in ["", "\n", "0"] and tag.text not in ["", "\n", "0"]]
                else:
                    # Ignore attributes with values equal to "", "\n", or "0"
                    if tag_value not in ["", "\n", "0"]:
                        data[tag_name] = tag_value

    return dict(data)


def process_xml_files(folder_path):
    total_files = 0
    processed_elements = 0
    extracted_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            total_files += 1
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
                valid_tags = identify_valid_tags(xml_content)
                data = extract_data_from_xml(xml_content, valid_tags)
                if data is not None:
                    processed_elements += 1
                    extracted_data.append(data)
                else:
                    print(f"Skipped {filename}: No 'item' tag found in the XML.")
    
    print("\nProcessing complete.")
    print(f"Total XML files: {total_files}")
    print(f"Processed elements: {processed_elements}")

    return extracted_data

def save_json(data_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=2)
    
    print(f"Final JSON file saved at: {os.path.abspath(output_file)}")

def main():
    parser = argparse.ArgumentParser(description='Process XML files and create a JSON file.')
    parser.add_argument('xml_folder', default='.', nargs='?', help='Path to the folder containing XML files')
    parser.add_argument('output_json', default="output.json", nargs='?', help='Name of the output JSON file')
    args = parser.parse_args()

    extracted_data = process_xml_files(args.xml_folder)
    save_json(extracted_data, args.output_json)

if __name__ == "__main__":
    main()
