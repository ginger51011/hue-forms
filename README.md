# hue-forms
A Python script to control Philips Hue via API through Google Sheets, preferable via Google Forms. Since it's very easy to link a Google Form with a Google Sheet, this is a neat way to let democracy decide your lighting. Or not. I hacked this together real fast like, so no promises that this is any good.

After installation, run in command-line as `hue_forms`. You can test if your spreadsheet is working by running `hue_forms --test-google-sheet`.

# Installation

___Installation is a bit tedious and currently requires user to send 1 GET request to get personal username___

You need some command-line experience, a file of credentials from Google API and a username from your Philips Hue Bridge. The last one is done by sending a GET-request acording to [this](https://developers.meethue.com/develop/get-started-2/) guide.

Make sure `config.ini.default` is saved as `~/.config/hue-forms/config.ini` and fill it out. You can find your sheet-id in the URL of your Google Spreadsheet.

Change `options.json.default` according to how you would like it, and move to `~./config/hue-forms/options.json`. You can use `example_options.json` for reference. Add your Google API credentials as `~/.config/hue-forms/credentials.json` (downloaded from google).

After this is done, run `pip3 install . --user` or whatever in project root directory to install required Python scripts.

## The form

This was created for a single-answer single-question Google Form, using sheets to check values. Note that options MUST BE the same as defined in `options.json`!

## Finding colors

To find your colors i XY-space, try DuckDuckGoing for ___"CEI XY chart"___. Then you can choose the correct (x, y)-values.


