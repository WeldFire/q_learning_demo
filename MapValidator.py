import copy
import sys

sys.setrecursionlimit(100000)
goalID = 10
badID = -9
wallID = 5
emptyID = 0
	
class MapValidator:
	height = 0
	width = 0
	endpoint = (-1, -1)
	mapArr = [[]]
		
	def iterateMap(self, nextPoint):
		#print(nextPoint)
		nextUp = (nextPoint[0], nextPoint[1]+1)
		nextDown = (nextPoint[0], nextPoint[1]-1)
		nextLeft = (nextPoint[0]-1, nextPoint[1])
		nextRight = (nextPoint[0]+1, nextPoint[1])
		
		return MapValidator.determinePoint(self, nextUp) or MapValidator.determinePoint(self, nextDown) or MapValidator.determinePoint(self, nextLeft) or MapValidator.determinePoint(self, nextRight)
				
	def determinePoint(self, point):
		if(MapValidator.isInMap(self, point)):
			if(MapValidator.mapArr[point[1]][point[0]] == goalID):
				return True
			elif(MapValidator.mapArr[point[1]][point[0]] == wallID or MapValidator.mapArr[point[1]][point[0]] == badID):
				return False#do nothing.... these are bad walls
			else:
				MapValidator.mapArr[point[1]][point[0]] = wallID
				return MapValidator.iterateMap(self, point)
		else:
			return False
	
	def isInMap(self, coords):
		if(coords[0] >= 0 and coords[0] < MapValidator.width):
			if(coords[1] >= 0 and coords[1] < MapValidator.height):
				return True
		return False
		
	def findVal(self, mapArr, val):
		for y in range(len(mapArr)):
			for x in range(len(mapArr[0])):
				if(mapArr[y][x] == val):
					return (x, y)
		return (-1, -1)
		
	def isPossibleToSolve(self, mapArr):
		MapValidator.height = len(mapArr)
		MapValidator.width = len(mapArr[0])
		MapValidator.mapArr = copy.deepcopy(mapArr)
		MapValidator.endpoint = MapValidator.findVal(self, mapArr, 10)
		frontier = MapValidator.findVal(self, mapArr, 1)#Starting position #OG Default (0, MapValidator.height-1)
		#print("Height {} Width {} endpoint {} frontier {}", MapValidator.height, MapValidator.width, MapValidator.endpoint, frontier)
		
		return MapValidator.iterateMap(self, frontier)
	
def main():
	theMap = [[0,0,5,0,0,0,5,0,0,0],
			  [0,0,0,0,0,0,0,0,0,0],
			  [0,0,0,0,0,5,0,10,0,0],
			  [0,0,0,0,0,0,5,0,0,0],
			  [0,0,0,0,0,0,5,0,0,0],
			  [0,0,0,0,5,0,0,5,5,5],
			  [0,0,0,0,0,5,0,0,0,0],
			  [0,0,0,0,0,0,5,0,0,0],
			  [0,0,0,0,0,0,0,0,0,0],
			  [1,0,0,0,0,0,0,0,0,0]]
		
	mv = MapValidator()
	print(mv.isPossibleToSolve(theMap))
	

if __name__ == "__main__":
	main()