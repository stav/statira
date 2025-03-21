# README

## Install

### Clone

### Virtual Environment

    $ python  -m venv venv
    $ source venv/bin/activate

### Dependencies

    $ pip install aiohttp[speedups]
    $ pip install --upgrade pip

### Structure

    [drwxr-xr-x stav     stav     4.0K]  .
    ├── [-rw-r--r-- stav     stav      781]  clients.csv
    ├── [-rw-r--r-- stav     stav      188]  config.ini
    ├── [drwxr-xr-x stav     stav     4.0K]  output
    ├── [-rw-r--r-- stav     stav      980]  README.md
    ├── [-rw-r--r-- stav     stav      793]  requirements.txt
    ├── [drwxr-xr-x stav     stav     4.0K]  statira
    │   ├── [-rw-r--r-- stav     stav     2.7K]  anthem.py
    │   ├── [-rw-r--r-- stav     stav      318]  config.py
    └── [drwxr-xr-x stav     stav     4.0K]  venv

## Development

When writing your code, we recommend enabling Python’s [development mode][1] (python -X dev).

    $ python -X dev anthem.py

### Production

Copy `config.ini`.

    [AUTH]
    BEARER_TOKEN = "ey..."

    [AGENT]
    NAME = "Steven Almeroth"
    TIN = ".........."


[1]: https://docs.python.org/3/library/devmode.html
