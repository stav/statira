import configparser
import os


file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(file_path)
mixed_path = os.path.join(parent_dir, "..", "config.ini")
config_file_path = os.path.abspath(mixed_path)
config = configparser.ConfigParser()
config.read(config_file_path)

BEARER_TOKEN = config["AUTH"]["BEARER_TOKEN"]
AGENT_NAME = config["AGENT"]["NAME"]
AGENT_TIN = config["AGENT"]["TIN"]
