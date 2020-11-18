# hue-forms
A Python script to control Philips Hue via API through Google Sheets, preferable via Google Forms

# Installation

Make sure `config.ini.default` is saved as `~/.config/hue-forms/config.ini` and fill it out.

Change `options.json.default` according to how you would like it, and move to `~./config/hue-forms/options.json`. Add your Google API credentials as `~/.config/hue-forms/credentials.json`.

# The form

This was created for a single-answer single-question Google Form, using sheets to check values. Note that options MUST BE the same as defined in `options.py`!

# Finding colors

To find your colors i XY-space, try DuckDuckGoing for __"CEI XY chart"__. Then you can choose the correct (x, y)-values. 