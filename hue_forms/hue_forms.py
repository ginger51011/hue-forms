#!/usr/bin/env python3

# External imports
import requests as req
import configparser
from os import path
from time import sleep
from json import load, loads

# Internal imports
import hue_forms.sheets_checker as sc

# Defining constants from config
CONFIG = configparser.ConfigParser()
CONFIG.read(path.join(path.expanduser("~"), "./.config/hue-forms/config.ini")) # Orka få detta snyggt

# For hue
USERNAME = CONFIG["hue"]["username"]
BRIDGE_IP = CONFIG["hue"]["bridge_ip"]
BASE_API_URL = f"http://{BRIDGE_IP}/api/{USERNAME}/lights/"

# For Google Spreadsheets
SHEET_ID = CONFIG["sheets"]["sheet_id"]
TIME_BETWEEN_UPDATES = float(CONFIG["sheets"]["time_between_updates"])

# Loading in options
OPTIONS_PATH = path.join(path.expanduser("~"), "./.config/hue-forms/options.json")

"""
An ugly fix; If you are going from "effect": "colorloop" to "effect: "none";
this will be parsed by the API last and set lamp to last known state, i.e. not
the specified color.
"""
OPTIONS_CONTAINS_SPECIAL_EFFECTS = False

with open(OPTIONS_PATH) as options:
    OPTIONS = load(options)
    for key in OPTIONS:
        if "effect" in OPTIONS[key]["body"]:
            if OPTIONS[key]["body"]["effect"] != "none":
                OPTIONS_CONTAINS_SPECIAL_EFFECTS = True
                break  # Only need to find one

def update_lights(body, lamp_ids=[]):
    """
    Updates the lights, using body
    in a PUT.
    """
    for id in lamp_ids:
        api_url = f"{BASE_API_URL}{id}/state"
        
        if OPTIONS_CONTAINS_SPECIAL_EFFECTS:
            req.put(url=api_url, json={"effect": "none"})
        
        req.put(url=api_url, json=body)

def get_all_color_lamps() -> list:
    """
    Returns a list of all lamps with color
    capabilities
    """
    lamps = []

    api_url = BASE_API_URL
    response_content = loads(req.get(url=api_url).content)

    for id in response_content:
        lamps.append(id)
    
    return lamps

def main():
    print("Collecting information about available lamps...")
    last_leader = ""
    lamp_ids = get_all_color_lamps()
    
    if not lamp_ids:
        raise ValueError("No valid lamps found!")
    if not OPTIONS:
        raise ValueError("options.json not found in ~/.config/hue-forms/")

    print("Starting form-checking...")
    while True:
        new_leader = sc.check_leader(sheet_id=SHEET_ID)

        if new_leader != last_leader:
            if new_leader not in OPTIONS:
                if new_leader == "": 
                    # If script is running and we remove cells, the
                    # script will break. This is not desireable, 
                    # so we continue looping instead
                    continue
                else:
                    raise ValueError("{new_leader} not in options.json! Cannot select this!")
            else:  
                update_lights(OPTIONS[new_leader]["body"], lamp_ids=lamp_ids)
                last_leader = new_leader
                print(f"{new_leader} has taken the lead!")
        
        sleep(TIME_BETWEEN_UPDATES)

def test_google_sheet():
    leader = sc.check_leader(sheet_id=SHEET_ID)
    print(f"Leader is: {leader}")