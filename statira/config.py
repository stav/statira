import configparser
import os

from fasthtml.common import Link, MarkdownJS

env = os.getenv("STA", "production")

base_config = {
    "hdrs": [
        Link(rel="icon", href="/static/favicon.ico"),
        MarkdownJS(),
    ],
    "static_path": "./statira",
}

dev_config = {
    "live": True,
    "debug": True,
    **base_config,
}

prod_config = {
    "live": False,
    "debug": False,
    **base_config,
}

fast_config = prod_config if env == "production" else dev_config

file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(file_path)
mixed_path = os.path.join(parent_dir, "..", "config.ini")
config_file_path = os.path.abspath(mixed_path)
config = configparser.ConfigParser()
config.read(config_file_path)

BEARER_TOKEN = config["AUTH"]["BEARER_TOKEN"]
AGENT_NAME = config["AGENT"]["NAME"]
AGENT_TIN = config["AGENT"]["TIN"]
PORT = int(config["CLIENT"]["PORT"])
