#!/usr/bin/python3

#################
# Settings
#################

# Set API key
apikey = "MW9S-E7SL-26DU-VV8V"

# Set default station at home page (use station abbreviation)
defaultstation = "12th"

# Theme values 'white' or 'black'
theme = "black"

# Show service advisories when present
advisory = "yes"

# Refreshes the board every 15 seconds
autoref = "no"

# List of stations with ETD disabled
noetdlist = ["OAKL"]


from bs4 import BeautifulSoup
import cgi, cgitb, re, sys
import urllib.request

# Lowercases variables in settings
noetdlist = [v.lower() for v in noetdlist]
advisory = advisory.lower()
autoref = autoref.lower()
defaultstation = str.lower(defaultstation)

# Declare html document
print("Content-type: text/html")
print("")
print("""<!DOCTYPE html>

<head>
<link rel="shortcut icon" href="https://www.bart.gov/sites/all/themes/bart/favicon.ico" type="image/vnd.microsoft.icon" />""")

# obtains input from URL
form = cgi.FieldStorage()
if form.getvalue("station"):
	formstation = form.getvalue("station")
	# validates station abbreviation is 4 characters
	stationRE = re.compile(r"^[a-zA-Z0-9]{4}$")
	if not stationRE.match(formstation):
		print("Invalid station code. Please use the drop down menu to select a station.")
		sys.exit()
	stationCode = str.lower(formstation)

else:
	# Sets default station
	stationCode = defaultstation.lower()

# Obtains theme if provided
if form.getvalue("theme"):
        # notes the default theme
        themeDefault = theme
        theme = str.lower(form.getvalue("theme"))
        # Validates input
        themeRE = re.compile(r"^black$|^white$")
        if not themeRE.match(theme):
                # use the default theme
                theme = themeDefault
        else:
                # use validated values for theme
                theme = str.lower(form.getvalue("theme"))

# Takes autorefresh input from HTML, overrides default properties
if form.getvalue("autorefresh"):
	formautoref = str.lower(form.getvalue("autorefresh"))
	# validates autorefresh input
	autorefRE = re.compile(r"^yes|no$")
	if not autorefRE.match(formautoref):
		print("Invalid autorefresh parameter.")
		sys.exit()
	autoref = str(formautoref)

# Collect ETD data via BeautifulSoup
apilink = "https://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key={}".format(stationCode,apikey)
rawdata = urllib.request.urlopen(apilink).read()
soup = BeautifulSoup(rawdata, "xml")

# Exit script if error in 4-letter station code
if "invalid" in soup.find('message').text:
        print("Invalid station code. Please use the drop down menu to select a station.")
        sys.exit()

# Finds station and ETDs, and corrects Berryessa station name
station = soup.find('name').text
directions = len(soup.find_all('etd'))
if "berryessa" in station.lower():
        station = "Berryessa/North San Jos&#233;"

# Collects advisories
if advisory.lower() == "yes":
	bsaapilink = "https://api.bart.gov/api/bsa.aspx?cmd=bsa&key={}".format(apikey)
	bsarawdata = urllib.request.urlopen(bsaapilink).read()
	bsasoup = BeautifulSoup(bsarawdata, "xml")
	bsa = bsasoup.find_all("description")

if autoref.lower() == "yes":
	print("<meta http-equiv='refresh' content='15'>")
print("<meta name='og:description' content='Estimated departure times for BART'><meta name='og:image' content='https://511contracosta.org/wp-content/uploads/2010/07/BART-logo-large.jpg'>")
print("<meta name='viewport' content='width=device-width, initial-scale=1'>")
print("<link rel='stylesheet' href='lib/{}.css'>".format(theme))
print("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>")
print("<title>BART Departures: {} Station</title>".format(station))
print("</head><body>")
# prints advisories if setting marked to yes
if advisory.lower() == "yes":
	if "No delays reported." not in bsa[0]:
		print("<div class='bsa'><h3 class='bsatitle'><i class='fa fa-exclamation-triangle'></i> BART Service Advisory</h3>")
		for bsamsg in bsa:
			print("<p class='bsamsg'>{}</p>".format(bsamsg.text))
		print("</div>")
print("<span class='stationname'>{} Station  </span><i class='fa fa-subway fa-2x station-icon'></i>".format(station))
#print("<br><span class='subtitle'>Estimated departure times</span>")
#print("<i>Number of directions: {}</i><br>".format(directions))
print("<br><br>")


for dir in soup.find_all('etd'):
	color = dir.find('hexcolor').text
	dest = dir.find('destination').text
	minUnits = "mins"
	mins = dir.find_all('minutes')
	# Creates a list
	minlist = []
	# This step important to remove <minutes> tags. Adds clean numbers to list.
	for min in mins:
		minlist.append(min.text)
	# Removes duplicates
	minlistclean = []
	for m in minlist:
		if m not in minlistclean:
			minlistclean.append(m)
	# Properly formatted list of minutes with commas separating minutes
	minDisp = ', '.join(minlistclean)
	# Checks if last ETD in list is "Leaving", to remove trailing "mins"
	if str(minlist[-1]) == "Leaving":
		minUnits = ""
	# Print out each destination's ETD if station, if station is not set to disable ETD times (not in 'noetdlist' list)
	if stationCode not in noetdlist:
		print("<div class=\'bar\' style=\'border-left-color:{};\'><a class=\'destination\'>{}</a><br>       <a class='mins-num'>{}</a> <span class=\'mins\'>{}</span></div>".format(color,dest,minDisp,minUnits))

# If station in do not display etd list, print this message
if stationCode in noetdlist:
	print("<div class=\'icon-container\'><i class=\'fa fa-exclamation-circle fa-3x no-etd-icon\'></i></div><div class=\'no-bar\'><a class=\'no-service-msg\'>Unavailable</a><br>        <span class=\'no-service-details\'>Departure times are unavailable for {} Station.<br>Please refer to the BART time schedule.</span></div>".format(station))
# Prints no upcoming service if no estimate provided
elif directions == 0:
	print("<div class=\'icon-container\'><i class=\'fa fa-times fa-3x no-service-icon\'></i></div><div class=\'no-bar\'><a class=\'no-service-msg'>No service</a><br>        <span class=\'no-service-details\'>There are no upcoming departures at this time</span></div>")


print("<br><br><br><br>")

print("""
<form id="station" name="form" method="get" action="/" class="form">
<select class="select-bar" name="station" onchange="this.form.submit()">
          <option value="" disabled selected>Select another station...</option>
          <option value="12th">12th St. Oakland City Center</option>
          <option value="16th">16th St. Mission (SF)</option>
          <option value="19th">19th St. Oakland</option>
          <option value="24th">24th St. Mission (SF)</option>
          <option value="ashb">Ashby (Berkeley)</option>
          <option value="antc">Antioch</option>
          <option value="balb">Balboa Park (SF)</option>
          <option value="bayf">Bay Fair (San Leandro)</option>
          <option value="bery">Berryessa/North San Jose</option>
          <option value="cast">Castro Valley</option>
          <option value="civc">Civic Center (SF)</option>
          <option value="cols">Coliseum</option>
          <option value="colm">Colma</option>
          <option value="conc">Concord</option>
          <option value="daly">Daly City</option>
          <option value="dbrk">Downtown Berkeley</option>
          <option value="dubl">Dublin/Pleasanton</option>
          <option value="deln">El Cerrito del Norte</option>
          <option value="plza">El Cerrito Plaza</option>
          <option value="embr">Embarcadero (SF)</option>
          <option value="frmt">Fremont</option>
          <option value="ftvl">Fruitvale (Oakland)</option>
          <option value="glen">Glen Park (SF)</option>
          <option value="hayw">Hayward</option>
          <option value="lafy">Lafayette</option>
          <option value="lake">Lake Merritt (Oakland)</option>
          <option value="mcar">MacArthur (Oakland)</option>
          <option value="mlbr">Millbrae</option>
          <option value="mlpt">Milpitas</option>
          <option value="mont">Montgomery St. (SF)</option>
          <option value="nbrk">North Berkeley</option>
          <option value="ncon">North Concord/Martinez</option>
          <option value="oakl">Oakland Int'l Airport</option>
          <option value="orin">Orinda</option>
          <option value="pitt">Pittsburg/Bay Point</option>
          <option value="pctr">Pittsburg Center</option>
          <option value="phil">Pleasant Hill</option>
          <option value="powl">Powell St. (SF)</option>
          <option value="rich">Richmond</option>
          <option value="rock">Rockridge (Oakland)</option>
          <option value="sbrn">San Bruno</option>
          <option value="sfia">San Francisco Int'l Airport</option>
          <option value="sanl">San Leandro</option>
          <option value="shay">South Hayward</option>
          <option value="ssan">South San Francisco</option>
          <option value="ucty">Union City</option>
          <option value="warm">Warm Springs/South Fremont</option>
          <option value="wcrk">Walnut Creek</option>
          <option value="wdub">West Dublin</option>
          <option value="woak">West Oakland</option>
</select></form>
<button class="map-button" onclick="myFunction()">Show Map</button>
<div id="map" style="display:none;"><br><br><img class="bart-map" src="https://www.bart.gov/sites/default/files/images/basic_page/system-map-weekday.png"></div>
<script>
function myFunction() {
  var x = document.getElementById("map");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
</script>""")

print("</body>")
