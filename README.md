# Airtable Base Exporter

This Python script exports data from all tables in one or more Airtable bases. It retrieves data using the Airtable API and saves each table's data as a JSON file. This tool is useful for backing up Airtable data or migrating it to another system.

## Features

- Exports all tables from one or more specified Airtable bases.
- Saves each table's data in JSON format, organized by base name.
- Configurable to export all accessible bases or only selected bases.
- Stores exported data in a configurable directory.

## Prerequisites

1. **Python 3.x**: Ensure Python is installed.
2. **Install dependencies**: Use the provided `requirements.txt` file to install the necessary libraries:

    ```bash
    pip install -r requirements.txt
    ```

### `requirements.txt`

```plaintext
requests