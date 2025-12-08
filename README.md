cloudcrate
==========

cloudcrate is a “bring your own Dropbox” command-line utility that keeps a local folder in sync with an Amazon S3 bucket. The main script, `cloudcrate.py`, drives three subcommands:

- `setup` – installs the bundled boto dependency if it’s missing.
- `sync` – walks the current directory, uploads new or modified files to `s3://cloudcrate.hari`, and records modification times.
- `download` – selectively pulls newer objects from the same bucket into a local `s3_downloads` directory, grouped by creation time.

The repo also contains split scripts (`cloudcrate-upload.py`, `cloudcrate-download.py`) that focus solely on uploading or downloading while reusing the same core flow.

## Prerequisites

- Python 2.7 (the scripts rely on print statements and modules that predate Python 3).
- macOS utilities such as `mdls` if you want creation timestamps during sync (Linux/Windows users should replace this call with an `os.stat` alternative).
- Tar and sudo privileges for the bundled boto installation (`setup` runs `sudo python setup.py install` inside `boto-2.34.0`).
- AWS connectivity to the `cloudcrate.hari` bucket (hard-coded credentials are embedded in the scripts for demo purposes only; use your own IAM user in production).

## Installation

1. Download or clone this repository.
2. Unzip it (if needed) and `cd` into the extracted folder. Treat this folder as your local “cloudcrate” workspace.
3. Run `python cloudcrate.py setup`. The script verifies boto, extracts the vendor tarball (`boto.0.tar.gz`) if missing, and installs it system-wide.

> Tip: the `setup` step is idempotent. If boto is already available, the script simply prints guidance and exits.

## Usage

### Sync local changes to S3

```
python cloudcrate.py sync
```

- Traverses the current directory recursively, capturing each file’s last modification time.
- Compares those timestamps against `last_modified.txt` (a JSON ledger that lives alongside the script).
- Uploads any file that is new or has been modified via `Key.set_contents_from_filename`.
- Refreshes `last_modified.txt` so subsequent runs only transfer incremental changes.
- Forces the bucket ACL to `public-read` so the files become publicly accessible.

### Download S3 contents to the desktop

```
python cloudcrate.py download
```

- Loads `creation_time.txt` (produced during `sync`) to understand how to group downloaded files.
- Ensures `~/Desktop/s3_downloads/` exists; creates one folder per creation year (or other key) inside it.
- Reads `download_last_modified.txt` to determine which objects have changed since the last download.
- Fetches newer objects via `Key.get_contents_to_filename` and updates the ledger so future runs stay incremental.

> To force a full re-download, delete `download_last_modified.txt` and rerun the command.

### Alternate entry points

- `python cloudcrate-upload.py setup|sync` – same logic as the main script but scoped to uploading only.
- `python cloudcrate-download.py setup|download` – pared-down downloader that always writes into `~/Desktop/s3_downloads`.

## Supporting files

- `boto.0.tar.gz` – vendored boto 2.34.0 archive used when `setup` installs dependencies offline.
- `last_modified.txt` – JSON map of local file paths to their `mtime`, used to decide what to upload next.
- `creation_time.txt` – JSON map of filenames to reported creation buckets (e.g., year), used when building download folder names.
- `download_last_modified.txt` – JSON map of S3 object names to their last modified timestamps, ensuring downloads stay incremental.
- `list.html` – simple static page hosted in the bucket for verifying uploads in a browser (`http://cloudcrate.hari.s3.amazonaws.com/list.html`).

## Troubleshooting

- **Permission denied during setup**: make sure you can run `sudo python setup.py install`, or install boto into a virtualenv and remove the sudo call.
- **Missing `mdls` command**: replace the macOS-specific metadata call with `os.stat` or comment out creation-time tracking if you’re on Linux/Windows.
- **Stale ledger files**: deleting `last_modified.txt` or `download_last_modified.txt` forces a full resync/redownload at the cost of re-uploading everything.
- **Credentials revoked**: supply your own IAM keys via environment variables and update the scripts accordingly; the baked-in keys are for demonstration only.

## Future improvements

- Replace hard-coded credentials with environment variables or AWS profiles.
- Migrate to boto3 for better retry logic, paginator support, and Python 3 compatibility.
- Move configuration (bucket name, destination path, ACL) into a config file or CLI flags.
- Add unit tests around sync/download diffing to catch regressions in the timestamp logic.
