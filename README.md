# INTRODUCTION
This program is a BART departure signboard that is run on a web server using cgi-bin and python. It uses the BART API to obtain real-time data and can be served on any browser and was originally designed to be similar to a simple, clean departure signboard.

![(Screenshot](img/preview.png)

It also removes duplicate trains from the BART API, which the official BART app does not do, and accurately reflects an actual departure signboard.

### Why?
Why not? BART's official app takes a while to load, and it's better to pull of a web page yourself. The advantage of a web app is that many computers have web browsers, which increases the accessibility for many people. This project was originally designed for me to improve my Python abilities, but also to learn about BeautifulSoup. Feel free to edit the code yourself to fit your needs.

### Live example
Click [here](https://live.homelab.app/) to view a working example of the program running.

# Features
### Autorefresh
The page is designed to automatically refresh if set in the *bart.py* code. Its setting can be overriden by attaching the variable `autorefresh` to `yes` or `no`. In other words, attach `?autorefresh=yes` to the end of the URL to force the page to autorefresh, such as `example.com/?autorefresh=yes`. If the variable is not the first in the URL, replace the `?` with a `&`, such as `example.com/?station=sfia&autorefresh=yes`.

### Manual station selection
In the code, there is a section that enables you to select a different station on the HTML page. Or you can simply add `station` variable in the URL followed by the 4-alphanumberic station code. A full list of the BART station codes are available [here](http://api.bart.gov/docs/overview/abbrev.aspx). Example: `example.com/?station=EMBR` or `example.com/?autorefresh=yes&station=24th`

### Defaults
You can set the main homepage to default to your desired settings mentioned above in the code itself. Edit variables in the *bart.py* code to set your defaults.


