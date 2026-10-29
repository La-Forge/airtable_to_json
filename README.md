# Airtable Base Exporter

This Python script exports data from all tables in every Airtable base that the API key can see. It retrieves data using the Airtable API and saves each table's data as a JSON file. This tool is useful for backing up Airtable data or migrating it to another system.

## Features

- Retrieves the list of bases from the Airtable API, so no base ID is hardcoded.
- Exports all tables from each base.
- Saves each table's data in JSON format, in one folder for each base, named `<base name>_<base ID>`.
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
| `AIRTABLE_CONFIG` | path to the config file itself (default `config.yaml`) |

The script exports every base that the API key can see. To limit the scope of
the backup, limit the scope of the token in Airtable.

### Running as a container

```bash
docker build -t airtable-to-json .
docker run --rm \
  -e AIRTABLE_API_KEY=... \
  -e AIRTABLE_BACKUP_DIR=/app/backup \
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

This file should contain your Airtable API key and the backup directory.

- api_key: Your Airtable API key. You can obtain this from your Airtable account settings.
- backup_directory: The directory where the exported data will be saved.

### Sample config.yaml
```plaintext
airtable:
  api_key: 'your_api_key'
  backup_directory: 'your_backup_folder'  # Path to the folder where backups will be saved
```

## Prerequisites

1. **Python 3.x**: Ensure Python is installed.
2. **Install dependencies**: Use the provided `requirements.txt` file to install the necessary libraries:

    ```bash
    pip install -r requirements.txt
    ```