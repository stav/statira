# README

## Install

### Clone

    $ git clone git@github.com:stav/statira.git

### Virtual Environment

    $ python  -m venv venv
    $ source venv/bin/activate

### Dependencies

    $ pip install aiohttp[speedups]
    $ pip install --upgrade pip

### Structure

    [drwxr-xr-x stav     stav     4.0K]  .
    ├── [-rw-r--r-- stav     stav      222]  anthem.sh
    ├── [-rw-r--r-- stav     stav      981]  clients.csv
    ├── [-rw-r--r-- stav     stav      239]  config.ini
    ├── [drwxr-xr-x stav     stav      12K]  output
    │   ├── [drwxr-xr-x stav     stav      32K]  cache
    │   ├── [drwxr-xr-x stav     stav     4.0K]  change
    │   └── [drwxr-xr-x stav     stav     4.0K]  recent
    ├── [-rw-r--r-- stav     stav     2.2K]  README.md
    ├── [-rw-r--r-- stav     stav      730]  requirements.txt
    ├── [drwxr-xr-x stav     stav     4.0K]  statira
    │   └── [drwxr-xr-x stav     stav     4.0K]  sserver
    │       ├── [-rw-r--r-- stav     stav     6.4K]  anthem.py
    │       └── [-rw-r--r-- stav     stav      407]  config.py
    └── [drwxr-xr-x stav     stav     4.0K]  venv


#### Files

- `clients.csv`: List of clients
- `config.ini`: Configuration file for authentication and agent details.
- `output/`: Directory for storing output files.
  - `cache/`: Server responses.
  - `change/`: Server responses that differ from previous responses.
  - `recent/`: The most recent server response.
- `README.md`: This file.
- `requirements.txt`: List of Python dependencies.
- `statira/`: Directory containing the main application code.
  - `anthem.py`: Main script to run the application.
  - `config.py`: Configuration handling.
- `venv/`: Virtual environment directory.

##### clients.csv

```csv
First Name,Last Name,DOB,MBI,SSN,Medicaid
John,Doe,01/01/1951,123456789,123-45-1111,987654321
Jane,Doe,02/02/1952,234567891,987-65-2222,
John,Smith,01/01/1953,345678912,,987654321
Jane,Smith,02/02/1954,456789123,,
```

##### config.ini

```ini
[AUTH]
BEARER_TOKEN = ey...

[AGENT]
NAME = Steven Almeroth
TIN = ..........
```

## Development

When writing your code, we recommend enabling Python's [development mode][1] (python -X dev).

    $ python -X dev anthem.py

### Production


[1]: https://docs.python.org/3/library/devmode.html
