#!/usr/bin/python3

# Set API key and default station abbreviation code
apikey = "MW9S-E7SL-26DU-VV8V"
defaultstation = "12th"
advisory = "yes"

import cgi, cgitb, re, sys
from bs4 import BeautifulSoup
import urllib.request

form = cgi.FieldStorage()

print("Content-type: text/html")
print("")
print("<!DOCTYPE html>")

# obtains input from URL
if form.getvalue("station"):
	formstation = form.getvalue("station")
	# validates form
	stationRE = re.compile(r"^[a-zA-Z0-9]{4}$")
	if not stationRE.match(formstation):
		print("Content-type: text/html")
		print("")
		print("station: error")
		sys.exit()
	stationCode = str(formstation)

else:
# Sets default station
	stationCode = defaultstation

#print(stationCode)
apilink = "https://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key={}".format(stationCode,apikey)
rawdata = urllib.request.urlopen(apilink).read()
soup = BeautifulSoup(rawdata, "xml")
station = soup.find('name').text
directions = len(soup.find_all('etd'))

#Collects advisories
if advisory == "yes":
	bsaapilink = "https://api.bart.gov/api/bsa.aspx?cmd=bsa&key={}".format(apikey)
	bsarawdata = urllib.request.urlopen(bsaapilink).read()
	bsasoup = BeautifulSoup(bsarawdata, "xml")
	bsa = bsasoup.find("description").text

print("<head>")
print("<meta http-equiv='refresh' content='45'>") 
print("<meta name='og:description' content='Estimated departure times for BART'><meta name='og:image' content='https://511contracosta.org/wp-content/uploads/2010/07/BART-logo-large.jpg'>")
print("<meta name='viewport' content='width=device-width, initial-scale=0.70'>")
print("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>")
print("<style>body {background:white; font-family: Arial; color: #222; padding: 0.5em;} .bar {border-left-style: solid; border-left-width: 10px; height: 4em;margin-bottom:0.4em; padding-left:0.8em;} .stationname {font-size:1.8em; font-weight: bold; white-space:pre;} .bsa {background-color: #fff200; color: black; padding: 0.5em 1em; padding-bottom: 0.7em; margin-bottom: 1em;} .bsatitle {margin-top:0.2em; margin-bottom:0.2em;} .subtitle {color: #bbb; font-weight:normal; font-style:italic; font-family: 'Helvetica'} .mins {color:#000;}</style>")
print("<title>BART Departures: {} Station</title>".format(station))
print("</head><body>")
# prints advisories if setting marked to yes
if advisory == "yes":
	if bsa != "No delays reported.":
		print("<div class='bsa'><h3 class='bsatitle'><i class='fa fa-exclamation-triangle'></i> BART Service Advisory</h3>{}</div><br>".format(bsa))
print("<span class='stationname'>{} Station  </span><i class='fa fa-subway fa-2x'></i>".format(station))
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
	# Properly formatted list of minutes
	minDisp = ', '.join(minlistclean)
	# Checks if last ETD in list is "Leaving", to remove trailing "mins"
	if str(minlist[-1]) == "Leaving":
		minUnits = ""
	# Print out each destination's ETD
	print("<div class=\'bar\' style=\'border-left-color:{};\'><a style=\'font-weight: bold; font-size: 1.5em;\'>{}</a><br>       <a class='mins'>{}</a> <span style=\'color:#bbb\'>{}</span></div>".format(color,dest,minDisp,minUnits))

# Prints no upcoming service if no estimate provided
if directions == 0:
	print("<div class=\'bar\' style=\'border-left-color:white;\'><a style=\'font-weight: bold; font-size: 1.5em;\'>No service</a><br>        <span style=\'color:#bbb\'>There are no upcoming departures at this time</span></div>")


#print(apilink)
print("<br><br><br><br>")

print("""
<form id="" name="form" method="get" action="/">
<select name="station" onchange="this.form.submit()">
          <option value="">Select another station...</option>
          <option value="12th">12th St. Oakland City Center</option>
          <option value="16th">16th St. Mission (SF)</option>
          <option value="19th">19th St. Oakland</option>
          <option value="24th">24th St. Mission (SF)</option>
          <option value="ashb">Ashby (Berkeley)</option>
          <option value="antc">Antioch</option>
          <option value="balb">Balboa Park (SF)</option>
          <option value="bayf">Bay Fair (San Leandro)</option>
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
</select>
</form>
""")

print("</body>")
