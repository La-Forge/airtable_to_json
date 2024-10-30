# Airtable Base Exporter

This Python script exports data from all tables in one or more Airtable bases. It retrieves data using the Airtable API and saves each table's data as a JSON file. This tool is useful for backing up Airtable data or migrating it to another system.

## Features

- Exports all tables from one or more specified Airtable bases.
- Saves each table's data in JSON format, organized by base name.
- Configurable to export all accessible bases or only selected bases.
- Stores exported data in a configurable directory.

## Configuration

The script requires a config.yaml file for configuration. This file should contain your Airtable API key, the backup directory, and an optional list of base IDs to export.

- api_key: Your Airtable API key. You can obtain this from your Airtable account settings.
- backup_directory: The directory where the exported data will be saved.
- bases: A list of base IDs to export. If this list is empty, the script will export data from all bases accessible with the provided API key.

### Sample config.yaml
```plaintext
airtable:
  api_key: 'your_api_key'
  backup_directory: 'your_backup_folder'  # Path to the folder where backups will be saved
  bases:  # Optional: specify base IDs to export; leave empty to export all accessible bases
    - 'appMcxefsViu55eF5'
    - 'appi1K0YweJOS255s'
    - 'appUCFNiJjXgD1hXb'
```

## Prerequisites

1. **Python 3.x**: Ensure Python is installed.
2. **Install dependencies**: Use the provided `requirements.txt` file to install the necessary libraries:

    ```bash
    pip install -r requirements.txt
    ```