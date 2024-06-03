import csv
import json
import yaml
import xml.etree.ElementTree as ET

# Define file paths
info_files = {
    "text": 'info/info.txt',
    "xml": 'info/info.xml',
    "yaml": 'info/info.yaml',
    "json": 'info/info.json',
    "csv": 'info/info.csv'
}

product_files = {
    "text": 'products/product.txt',
    "xml": 'products/product.xml',
    "yaml": 'products/product.yaml',
    "json": 'products/product.json',
    "csv": 'products/product.csv'
}

# Reading and parsing the text file
def parse_text(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        key, value = line.strip().split(': ', 1)
        data[key.lower().replace(' ', '_')] = value
    return data

# Reading and parsing the XML file
def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = {child.tag: child.text for child in root}
        return data
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
        return {}

# Reading and parsing the YAML file
def parse_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        return {}

# Reading and parsing the JSON file
def parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file {file_path}: {e}")
        return {}

# Reading and parsing the CSV file
def parse_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = next(reader)
        return data
    except Exception as e:
        print(f"Error parsing CSV file {file_path}: {e}")
        return {}

# Parsing files
def parse_files(files):
    parsed_data = {}
    for format, file_path in files.items():
        if format == "text":
            parsed_data[format] = parse_text(file_path)
        elif format == "xml":
            parsed_data[format] = parse_xml(file_path)
        elif format == "yaml":
            parsed_data[format] = parse_yaml(file_path)
        elif format == "json":
            parsed_data[format] = parse_json(file_path)
        elif format == "csv":
            parsed_data[format] = parse_csv(file_path)
    return parsed_data

contact_info = parse_files(info_files)
product_inventory = parse_files(product_files)

print("Contact Info:", contact_info)
print("Product Inventory:", product_inventory)
