print("DOES THIS PART FUCKING WORK???????",flush=True)

import pyNUT, threading, time

from http.server import BaseHTTPRequestHandler, HTTPServer

from socket import error as socket_error

#from socket import EOFError

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

def is_ready():
	global nut_connected
	global nut
	ready=False
	print("nut_connected is ",   nut_connected,flush=True)
	if nut_connected:
		try:
			result = nut.GetUPSVars(ups="apc")
		except EOFError as e:
			start_pyNUT()
			return is_ready()
		result = {k.decode("ascii"):result.get(k).decode("ascii") for k in result.keys()}
		print(result,flush=True)
		if "ups.mfr" in result and result["ups.mfr"] is not None:
			print("found a ups mfr",flush=True)
			ready=True
	return ready

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

class UpsServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/healthz':
			healthz = is_ready()
			if healthz:
				self.send_response(200)
				self.send_header("Content-type","text/plain")
				self.end_headers()
				self.wfile.write("OK".encode("utf8"))
			else:
				self.send_response(500)
				self.send_header("Content-type","text/plain")
				self.end_headers()
				self.wfile.write("NOTOK".encode("utf8"))


server_address = ("0.0.0.0",80)
httpd = HTTPServer(server_address,UpsServer)

print("creating threads...",flush=True)
http_thread = threading.Thread(target=httpd.serve_forever,daemon=True)
nut_thread = threading.Thread(target=start_pyNUT,daemon=True)
print("starting http thread",flush=True)
http_thread.start()
print("started http thread, starting nut thread",flush=True)
nut_thread.start()
print("started nut thread",flush=True)

while is_any_thread_alive([http_thread,nut_thread]):
	time.sleep(1)
