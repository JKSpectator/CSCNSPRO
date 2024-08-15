import math

from simulation import Simulation


def latLonToXYZ(earth_radius, lat, lon):
		x = earth_radius * math.cos(lat) * math.cos(lon)
		y = earth_radius * math.cos(lat) * math.sin(lon)
		z = earth_radius * math.sin(lat)
		return [x, y, z]


configfile = "config.txt"
earth_radius = 6371000 	# the mean radius of the earth in meters according to wikipedia
make_links = True 	# if true, will enable calculating network link-state
network_designs = "SPARSE" 	# ["SPARSE", "+GRID", "IDEAL"]
planesNum = 12
nodesNum = 12
inc = 65.0
sma = 500
timeStep = 10 #int : simulation process timestep
placenames = None


def main():
	with open(configfile, 'r') as f:
		for line in f:
			words = line.split()
			if words[0] == 'EARTH_RADIUS':
				earth_radius = int(words[1])
			elif words[0] == 'MAKE_LINKS':
				if words[1] == "True":
					make_links = True
				else:
					make_links = False
			elif words[0] == 'NETWORK_DESIGNS':
				network_designs = words[1]
			elif words[0] == 'planesNum':
				planesNum = int(words[1])
			elif words[0] == 'nodesNum':
				nodesNum = int(words[1])
			elif words[0] == 'inc':
				inc = float(words[1])
			elif words[0] == 'sma':
				sma = int(words[1]) * 1000 +earth_radius
			elif words[0] == 'timeStep':
				timeStep = int(words[1])

	simulation = Simulation(planesNum, nodesNum, inc, sma, timeStep, make_links)






if __name__ == "__main__":
	main()


