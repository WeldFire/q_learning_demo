from __future__ import division
from noise import snoise2 # pip install noise
from pprint import pprint
from MapValidator import MapValidator
import random
import time

class MapManager:
	#Change verbosity here!
	verbose = False
	MaxTries = 50
	currentTryCount = 0
	
	def createMap(self, width, height, type='lava'):
		start = time.time()
		seed = getSeed()#64554
		MapManager.currentTryCount = MapManager.currentTryCount + 1
	
		tb = TerrianBuilder(width, height, type)
		mm = MapMaker()
		
		noiseMap = tb.createMap(seed, .5)
		
		if MapManager.verbose:
			pprint2DArray(noiseMap)
		
		normalMap = tb.normalizeMap(noiseMap)
		
		if MapManager.verbose:
			pprint2DArray(normalMap)
			
		highestValue = max(map(max, normalMap))
		lowestValue = min(map(min, normalMap))
		
		if MapManager.verbose:
			print("Highest: {}, Lowest: {}".format(highestValue, lowestValue))
		
		mv = MapValidator()
		terrian = [mm.calculateWallTypes(row, highestValue, lowestValue) for row in normalMap]
		
		#Place starting position
		player = (random.randint(0, width-1), random.randint(0, height-1))
		terrian[player[1]][player[0]] = 1
		
		isPossibleMap = mv.isPossibleToSolve(terrian)
		
		if MapManager.verbose:
			end = time.time()
			pprint2DArray(terrian)
			print("Map created and checked in :", end - start, " seconds")
			print("Map is possible to complete? " + str(isPossibleMap))
		
		if(isPossibleMap):
			return mm.getWallsAndSpecials(terrian, player)
		else:
			if(MapManager.currentTryCount > MapManager.MaxTries):
				print("")
				print("Maximum map generation attempts tried...")
				print("Please try again with different map settings!")
				return ([],[], (0, MapValidator.height-1))
			else:
				return MapManager.createMap(self, width, height)

class TerrianBuilder:
	def __init__(self, width, height, type='lava'):
		self.width = width
		self.height = height
		self.type = type

	"""
	Produce my custom version of "noise"
	"""
	def knoise(self, x, y):
		maxLeveler = self.width + self.height
		leveler = x + (self.height - y)
		
		growthCoeff = (leveler/maxLeveler)*2
		#print(growthCoeff)
		#growthCoeff = 2
		
		return ((random.random()*growthCoeff)-1)
	
	"""
	Produce my custom version of "lava noise"
	"""
	def lavanoise(self, x, y, seed):
		return snoise2(x, y, 1, base=seed) + TerrianBuilder.knoise(self, x, y)
		
	"""
	Produce a completely random map
	"""
	def completelyRandom(self, x, y):
		return ((random.random()*2)-1)
		
	"""
	Produce layered simplex noise map
	"""
	def layeredSimplex(self, x, y, seed):
		period = 0.5
		adjustedX = (x/2) * period
		adjustedY = (y/2) * period
		
		map1 = snoise2(adjustedX, adjustedY, 1, base=seed)
		map2 = snoise2(adjustedX, adjustedY, 2, base=seed)
		map3 = snoise2(adjustedX, adjustedY, 3, base=seed)
		
		merged = (map1*3 + map2*2 + map3*1)/6
		
		return merged
	
	"""
	Produce a simplex noise map
	"""
	def createMap(self, seed, period):
		random.seed(seed)
		
		def createNoisePoint(x, y):
			if(self.type == 'random'):
				return TerrianBuilder.completelyRandom(self, x, y)
			if(self.type == 'lava'):
				return TerrianBuilder.lavanoise(self, x, y, seed)
			if(self.type == 'simplex'):
				return TerrianBuilder.layeredSimplex(self, x, y, seed)
			else:
				return TerrianBuilder.knoise(self, x, y)
		
		return [[createNoisePoint(x, y) for x in range(self.width)] for y in range(self.height)]

	
	"""
	Produce "normal" values from 0 to 100 from the snoise map (which is currently -1 to 1)
	"""
	def normalizeMap(self, noiseMap):
		def normalizer(val):
			nVal = (((val + 1.0)/2.0) * 100.0)
			nVal = min(100, max(0, nVal))
			return nVal
			
		return [[normalizer(val) for val in row] for row in noiseMap]
			
class MapMaker:
	goalID = 10
	badID = -9
	wallID = 5
	emptyID = 0
	
	def calculateWallTypes(self, arr, highestVal, lowestVal):
		global goalID
		global badID 
		global wallID
		global emptyID
		result = []
		for var in arr:
			if(var == highestVal):
				result.append(MapMaker.goalID)
			elif(var == lowestVal):
				result.append(MapMaker.badID)
			elif(var >= 40 and var <= 60):
				result.append(MapMaker.wallID)
			else:
				result.append(MapMaker.emptyID)
				
		return result
		
	def getWallsAndSpecials(self, terrian, player):
		walls = []
		specials = []
		
		def generateWallsandSpecials(x, y, val):
			if val == MapMaker.goalID:
				specials.append((x, y, "green", 1))
			elif val == MapMaker.badID:
				specials.append((x, y, "red", -1))
			elif val == MapMaker.wallID:
				walls.append((x,y))
		
		[[generateWallsandSpecials(x,y,terrian[y][x]) for x in range(len(terrian[y]))] for y in range(len(terrian))]
		
		return (walls, specials, player)

def getSeed():
	return random.randint(1, 999999)
	
def pprint2DArray(array):
	print('\n'.join([''.join(['{: 6.2f} '.format(item) for item in row]) for row in array]))
	print('\n')
	
def main():
	width = 10
	height = 10
	
	mm = MapManager()
	#MapManager.verbose = True
	
	pprint(mm.createMap(width, height))
	
	

if __name__ == "__main__":
	main()