import nmea


def handle_gpgga(data):
	print data.get('latitude')
	print data.get('longitude')



nmea = nmea.NMEA(tmap='tmap_gps.plist')
nmea.push_handlers(GPGGA=handle_gpgga)

data = open('gps/nmea.log').read()

for line in data.splitlines():
	nmea.push(line)
	
#map(nmea.push, data.splitlines())

nmea.pump_messages()
