#!/usr/bin/env python3

# External imports
import requests as req
import configparser
from os import path
from time import sleep

# Internal imports
from hue_forms.options import OPTIONS
from hue_forms.sheet_checker import check

# Defining constants from config
CONFIG = configparser.ConfigParser()
CONFIG.read(path.join(path.expanduser("~"), "./.config/hue-forms/config.ini")) # Orka få detta snyggt

# For hue
USERNAME = CONFIG["hue"]["username"]
BRIDGE_IP = CONFIG["hue"]["bridge_ip"]
BASE_API_URL = f"http://{BRIDGE_IP}/api/{USERNAME}/"

# For Google Spreadsheets
SHEET_ID = CONFIG["sheets"]["sheet_id"]
TIME_BETWEEN_UPDATES = float(CONFIG["sheets"]["time_between_updates"])

def update_lights(body, lamp_ids=[]):
    """
    Updates the lights, using body
    in a PUT.
    """
    for id in lamp_ids:
        api_url = BASE_API_URL + id
        req.put(url=api_url, json=body)

def get_all_color_lamps() -> list:
    """
    Returns a list of all lamps with color
    capabilities
    """
    
    color_lamps = []

    api_url = BASE_API_URL + "lights/"
    response = req.get(url=api_url)

    for id in response:
        if response[id]["colormode"] == "xy":
            color_lamps.append(id)
    
    return color_lamps

def main():
    while True:
        check_leader(sheet_id=SHEET_ID)