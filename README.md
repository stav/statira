# README

## Install

### Clone

    $ git clone git@github.com:stav/statira.git

### Virtual Environment

    $ python  -m venv venv
    $ source venv/bin/activate

### Dependencies

    $ pip install --upgrade pip
    $ pip install -r requirements.txt

### Structure

    [drwxr-xr-x stav     stav     4.0K]  .
    ├── [-rwxr-xr-x stav     stav      245]  anthem.sh
    ├── [-rw-r--r-- stav     stav       94]  clients.csv
    ├── [-rw-r--r-- stav     stav      261]  config.ini
    ├── [-rw-r--r-- stav     stav     132K]  llms-ctx.txt
    ├── [drwxr-xr-x stav     stav      12K]  output
    │   ├── [drwxr-xr-x stav     stav      68K]  cache
    │   ├── [drwxr-xr-x stav     stav     4.0K]  change
    │   └── [drwxr-xr-x stav     stav     4.0K]  recent
    ├── [-rw-r--r-- stav     stav     2.4K]  README.md
    ├── [-rw-r--r-- stav     stav      730]  requirements.txt
    ├── [drwxr-xr-x stav     stav     4.0K]  statira
    │   ├── [-rw-r--r-- stav     stav     7.3K]  anthem.py
    │   ├── [-rw-r--r-- stav     stav      401]  config.py
    │   ├── [-rw-r--r-- stav     stav     2.7K]  index.py
    │   ├── [-rw-r--r-- stav     stav      504]  main.py
    │   ├── [-rw-r--r-- stav     stav     3.0K]  parse.py
    │   ├── [drwxr-xr-x stav     stav     4.0K]  static
    │   └── [-rw-r--r-- stav     stav     1.9K]  upload.py
    └── [drwxr-xr-x stav     stav     4.0K]  venv

#### Files

- `anthem.sh`: Shell script for running the application.
- `clients.csv`: List of clients with details such as name, DOB, MBI, SSN, Medicaid ID, and Effective date.
- `config.ini`: Configuration file containing authentication and agent details.
- `llms-ctx.txt`: Context file for language model processing.
- `output/`: Directory for storing output files.
    - `cache/`: Cached server responses.
    - `change/`: Server responses that differ from previous responses.
    - `recent/`: The most recent server response.
- `README.md`: Documentation file for the project.
- `requirements.txt`: Python dependencies required for the project.
- `statira/`: Main application directory.
    - `anthem.py`: Main script to run the application.
    - `config.py`: Handles configuration settings.
    - `index.py`: Home page for the client user interface.
    - `main.py`: Entry point for client operations.
    - `parse.py`: Parsing logic for input data.
    - `static/`: Directory for static files.
    - `upload.py`: Handles file uploads.
- `venv/`: Virtual environment directory for Python dependencies.

##### clients.csv

```csv
First Name,Last Name,DOB,MBI,SSN,Medicaid,PED
John,Doe,01/01/1951,123456789,123-45-1111,987654321,07/01/2025
Jane,Doe,02/02/1952,234567891,987-65-2222,,
John,Smith,01/01/1953,345678912,,987654321,
Jane,Smith,02/02/1954,456789123,,,
```
- `First Name`: First name of the individual
- `Last Name`: Last name of the individual
- `DOB`: Date of birth of the individual
- `MBI`: Medicare Beneficiary Identifier
- `SSN`: Social Security Number (optional)
- `Medicaid`: Medicaid ID of the client (optional)
- `PED`: Proposed Effective Date of a new insurance plan (optional)

##### config.ini

```ini
[AUTH]
BEARER_TOKEN = ey...

[AGENT]
NAME = Steven Almeroth
TIN = ..........

[CLIENT]
PORT = 7001
```

## Development

When writing your code, we recommend enabling Python's [development mode][1] (python -X dev).

### Client

    $ STA=devel python -X dev statira/main.py


[1]: https://docs.python.org/3/library/devmode.html
