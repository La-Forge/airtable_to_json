# Airtable Base Exporter

This Python script exports data from all tables in one or more Airtable bases. It retrieves data using the Airtable API and saves each table's data as a JSON file. This tool is useful for backing up Airtable data or migrating it to another system.

## Features

- Exports all tables from one or more specified Airtable bases.
- Saves each table's data in JSON format, organized by base name.
- Configurable to export all accessible bases or only selected bases.
- Stores exported data in a configurable directory.

## Configuration

Configuration is read **from the environment first**, falling back to a
`config.yaml` file. The environment path is what the container uses, so no
secret is written to disk; `config.yaml` remains convenient for local runs and
is optional when the environment supplies everything.

| Variable | Equivalent in `config.yaml` |
| --- | --- |
| `AIRTABLE_API_KEY` | `airtable.api_key` |
| `AIRTABLE_BACKUP_DIR` | `airtable.backup_directory` |
| `AIRTABLE_BASES` | `airtable.bases` — comma- or newline-separated |
| `AIRTABLE_CONFIG` | path to the config file itself (default `config.yaml`) |

Setting `AIRTABLE_BASES` to an empty string means *every base the key can see*,
which is the same meaning an empty `bases:` list has. Leaving it unset falls
back to the file.

### Running as a container

```bash
docker build -t airtable-to-json .
docker run --rm \
  -e AIRTABLE_API_KEY=... \
  -e AIRTABLE_BACKUP_DIR=/app/backup \
  -e AIRTABLE_BASES=appXXXX,appYYYY \
  -v /path/on/host:/app/backup \
  airtable-to-json python3 /app/export.py
```

The image idles on `sleep infinity` so a scheduler can `exec` into it.
`run.sh` is the entry point for that: it runs the export, then pushes an
uptime-kuma heartbeat **whatever the outcome** (`UPTIME_KUMA_PUSH_URL`) and
exits with the export's own status. Chaining the heartbeat behind `&&` — as a
crontab commonly does — means a failure pushes nothing, which looks exactly
like a run that has not started yet.

### Using a config file instead

This file should contain your Airtable API key, the backup directory, and an optional list of base IDs to export.

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