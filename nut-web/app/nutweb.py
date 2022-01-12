import pyNUT

from flask import Blueprint, g, redirect, render_template, request, session, url_for

from socket import error as socket_error

bp = Blueprint("nut", __name__, url_prefix="/")

nut_connected = False


def start_pyNUT(nut_tries=12):
	print("Connecting to UPS, tries left : ",nut_tries,flush=True)
	global nut_connected
	global nut
	try:
		print("Connecting to UPS, tries left : ",nut_tries,flush=True)
		nut = pyNUT.PyNUTClient(host="nut-ups.shaytech.net",login="monitor",password="monitor",debug=True)
		nut_connected = True
		print("Successfully Connected to UPS",flush=True)
	except socket_error as e:
		print("Failed to connect to UPS",flush=True)
		if nut_tries > 0:
			start_pyNUT(nut_tries-1)


start_pyNUT()


status_translation = {
	"OFF":("OFF","off.svg"),
	"OL":("Online","online.svg"),
	"OL CHRG":("Online Charging","online.svg"),
	"OB DISCHRG":("On Battery Discharging","onbattery.svg"),
	"ON":("On Battery","onbattery.svg"),
	"LB":("Low Battery","lowbattery.svg"),
	"RB":("Replace Battery","broken.svg"),
	"OVER":("Overload","broken.svg"),
	"TRIM":("Voltage Trim","broken.svg"),
	"BOOST":("Voltage Boost","broken.svg"),
	"CAL":("Calibration","broken.svg"),
	"BYPASS":("Bypass","broken.svg"),
	"NULL":("Null","broken.svg")
	}

@bp.route("/", methods=("GET",))
def show_UPS_info():
	try:
		result = nut.GetUPSVars(ups="apc")
	except EOFError as e:
		start_pyNUT()
		return show_UPS_info()
	result = {k.decode("ascii"):result.get(k).decode("ascii") for k in result.keys()}
	result["status_decode"] = status_translation[result["ups.status"]][0]
	result["status_img"] = status_translation[result["ups.status"]][1]
	result["battery.charge"] = int(result["battery.charge"])
	batchar = result["battery.charge"]
	if batchar < 50:
		batcolor = "red"
	elif batchar < 80:
		batcolor = "yellow"
	else:
		batcolor = "green"
	result["battery.color"] = batcolor
	result["ups.load"] = int(result["ups.load"])
	if result["ups.load"] < 30:
		loadcolor = "green"
	elif result["ups.load"] < 70:
		loadcolor = "yellow"
	else:
		loadcolor = "red"
	result["load.color"] = loadcolor
	result["battery.runtime"] = int(result["battery.runtime"])
	result["battery.runtime.low"] = int(result["battery.runtime.low"])
	result["battery.runtime.full"] = int(result["battery.runtime"] / (result["battery.charge"]/100))
	result["battery.runtime.per"] = int((result["battery.runtime"] / result["battery.runtime.full"])*100)
	result["battery.runtime.low.per"] = int((result["battery.runtime.low"] / result["battery.runtime.full"])*100)
	return render_template("ups.html", upsvars=result)
