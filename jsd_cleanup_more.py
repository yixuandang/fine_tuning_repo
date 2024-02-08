import json
import sys
import re

def cleanup_more(input_file):
    # Load the merged cleaned data
    with open(input_file, 'r') as f:
        cleaned_data = json.load(f)

    # timestamp pattern
    pattern = r"(?:[A-Za-z]|\s|\d)(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s(?:UTC|PST|EST|CST|IST)(?:[A-Za-z]|\s|\d)"

    cleaned_data_filtered = []
    for item in cleaned_data:

        if not item.get('comments') or item.get('comments') == "":
            continue
    
    # Clean up the descriptions
        description = item.get('description', '')
        # Remove <p>, <br/>, \n, and </p> tags
        description = re.sub(r'<p>|<br/>|\n|<\/p>|\u2019|\u201c|\u201d|<h2>.*?</h2>|<a.*?</a>|&amp|<ul class.*?>|\t|<li>|</li>|<span.*?<\/span>|\\r|\\n|\u00a0|\u2013|\u2026|\u2022|\u2192|\u00e1|\u25ba|\u251c|\u2500|\u2514|\u2014|\u2592|\u26a0|\ufe0f|\u2002|\u2018|\ufffd', '', description)
        description = re.sub(r'&lt;', '<', description)
        description = re.sub(r'&gt;', '>', description)
        description = re.sub(r'\\', '', description)
        description = re.sub(pattern, '', description)
        description = re.sub(r'  ', ' ', description)
        item['description'] = description

    # Clean up comments
    #for item in cleaned_data:
        comments = item.get('comments', '')
        comments = re.sub(r'\n|<p>|<\/p>|<span.*?<\/span>|<em>.*?</em>|<a.*?</a>|\u2013|<b>.*?</b>|\u00a0|<font color=\"#000000\">|</font>|<br/>|&amp|\u2019|\t|\u2018|\u2013|<ul>|<li>|</ul>|</li>|\u25cf|\u2022|\u2192|\u201c|\u201d|\u00e1|\u2026|\u25ba|\u251c|\u2500|\u2514|\u2014|\u2592|\u26a0|\ufe0f|\u2002|\u2018|\ufffd', '', comments)
        comments = re.sub(r'&lt;', '<', comments)
        comments = re.sub(r'&gt;', '>', comments)
        comments = re.sub(r'\\', '', comments)
        comments = re.sub(pattern, '', comments)
        comments = re.sub(r'  ', ' ', comments)
        item['comments'] = comments

    # Clean up the titles
    #for item in cleaned_data:
        title = item.get('title', '')
        title = re.sub(r'\u00a0|\u201d|\u201c', '', title)
        title = re.sub(pattern, '', title)
        title = title.split('] ', 1)[-1]  # Remove the part before '] '
        item['title'] = title

    # Clean up the descriptions and comments
    #for item in cleaned_data:
        # 1. Append ": " at the end of each title's value
        title = item.get('title', '')

        # 2. Insert title into the beginning of description
        description = item.get('description', '')
        item['description'] = title + ': ' + description

        # 3. Remove title field
        del item['title']

        # 4. Rename description to input
        item['input'] = item.pop('description', '')

        # 5. Rename comments to output
        item['output'] = item.pop('comments', '')

        cleaned_data_filtered.append(item)

    # Write the cleaned data to a new JSON file
    output_file = 'enhanced_cleaned_data.json'
    with open(output_file, 'w') as f:
        json.dump(cleaned_data_filtered, f, indent=4)

    print(f"Enhanced cleaned data written to {output_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python jsd_cleanup_more.py <input_json_file>")
        return

    input_file = sys.argv[1]
    cleanup_more(input_file)


if __name__ == "__main__":
    main()

