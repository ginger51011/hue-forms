#!/usr/bin/env python3

from hue_forms.options import OPTIONS
from hue_forms.hue_forms import main

if not OPTIONS:
    raise ValueError("No options set; please edit options.py")

def run():
    pass