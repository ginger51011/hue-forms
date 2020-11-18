#!/usr/bin/env python3

# External imports
import requests as req
import configparser
from os import path
from time import sleep

# Internal imports
from hue_forms.options import OPTIONS
import hue_forms.sheets_checker as sc

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
    last_leader = ""
    lamp_ids = get_all_color_lamps()
    
    if not lamp_ids:
        raise ValueError("No valid lamps found!")

    while True:
        new_leader = sc.check_leader(sheet_id=SHEET_ID)

        if new_leader != last_leader:
            update_lights(OPTIONS[new_leader]["body"], lamp_ids=lamp_ids)
            last_leader = new_leader
        
        sleep(TIME_BETWEEN_UPDATES)

def test_google_sheet():
    leader = sc.check_leader(sheet_id=SHEET_ID)
    print(f"Leader is: {leader}")