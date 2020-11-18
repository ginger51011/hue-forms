#!/usr/bin/env python3

from hue_forms.options import OPTIONS
import hue_forms.hue_forms as hf

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test-google-sheet", action="store_true",
                    help="Checks Google Sheet in config and outputs leader")
args = parser.parse_args()      # Collects our input in args

def parse():
    if args.test_google_sheet:
        hf.test_google_sheet()
    else:
        if not OPTIONS:
            raise ValueError("No options set; please edit options.py")
        hf.main()