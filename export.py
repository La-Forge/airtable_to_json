import requests
import json
import yaml
import os
from urllib.parse import quote  # Import quote for URL encoding
import re

# Load API_KEY, backup_directory, and list of bases from the YAML configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

API_KEY = config['airtable']['api_key']
BASE_IDS = config['airtable'].get('bases', [])  # Retrieve bases list or an empty list if not provided
BACKUP_DIR = config['airtable']['backup_directory']

HEADERS = {'Authorization': f'Bearer {API_KEY}'}

# Function to list all bases and generate a dictionary of base_id: base_name
def list_all_bases():
    response = requests.get('https://api.airtable.com/v0/meta/bases', headers=HEADERS)
    response.raise_for_status()  # Check for HTTP errors
    bases = response.json()['bases']
    
    # Create a dictionary with base_id as the key and base name as the value
    base_dict = {base['id']: base['name'] for base in bases}
    
    return base_dict

# Create a root directory to store all base exports
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Function to get all tables in a base
def get_tables(base_id):
    url = f'https://api.airtable.com/v0/meta/bases/{base_id}/tables'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['tables']

# Function to export all data from a table
def export_table_data(base_id, table_name):
    encoded_table_name = quote(table_name, safe="")
    url = f'https://api.airtable.com/v0/{base_id}/{encoded_table_name}'
    records = []
    
    while True:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        records.extend(data['records'])
        
        # Check if there are more pages of data
        if 'offset' in data:
            url = f'https://api.airtable.com/v0/{base_id}/{table_name}?offset={data["offset"]}'
        else:
            break

    return records

# Function to get the name of a base
def get_base_name(base_dict, base_id):
    return base_dict.get(base_id, base_id)

# Function to export all tables in a base
def export_base_tables(base_dict, base_id):
    base_name = get_base_name(base_dict, base_id)
    print(f"Exporting base {base_name}...")
    
    # Create a directory for the base
    base_dir = os.path.join(BACKUP_DIR, base_name.replace(" ", "_"))  # Replace spaces with underscores for folder names

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Get and export each table in the base
    tables = get_tables(base_id)
    for table in tables:
        table_name = table['name']
        print(f"\tExporting {table_name} from base {base_id}...")
        table_data = export_table_data(base_id, table_name)
        
        # Save each table's data to a separate JSON file
        # Remplace les caractères interdits
        filename = re.sub(r'[\/:*?"<>|]', '_', table_name)
        file_path = os.path.join(base_dir, f"{filename}.json")
        with open(file_path, 'w') as f:
            json.dump(table_data, f, indent=4)

# Retrieve the dictionary of all accessible bases
base_dict = list_all_bases()

# Determine the list of base IDs to process
if not BASE_IDS:
    # If BASE_IDS is empty, use all bases in base_dict
    base_ids_to_export = base_dict.keys()
else:
    # Use the specified base IDs from the configuration
    base_ids_to_export = BASE_IDS

# Export each base
for base_id in base_ids_to_export:
    export_base_tables(base_dict, base_id)