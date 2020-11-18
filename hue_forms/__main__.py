#!/usr/bin/env python3

from hue_forms.options import OPTIONS

if size(OPTIONS) < 1:
    raise ValueError("No options set; please edit options.py")