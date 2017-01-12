__author__ = 'philippe'
from Tkinter import *
from MapManager import MapManager
import time
import sys
master = Tk()


#Determine when we have found the optimal path
lastScore = -sys.maxint - 1
bestScoreStreak = 0
bestScoreStreakTarget = 10
iterations = 0
startMapTraverse = None

#Board setup
triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 10
#SET YOUR MAP SIZE HERE!
(x, y) = (5, 5)
#SET YOUR MAP SIZE HERE!
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
score = 1
restart = False
walk_reward = -0.04

#Start timing map generation
startMapGen = time.time()
mm = MapManager()

#SET YOUR MAP TYPE HERE!
#choices=['core', 'lava', 'random', 'simplex']
walls, specials, player = mm.createMap(x, y, 'simplex')
#SET YOUR MAP TYPE HERE!

#Display map generation timing
endMapGen = time.time()
print("Total map generation and validation time :", endMapGen - startMapGen, " seconds")

playerInit = (player[0],player[1])

cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart, lastScore, bestScoreStreak, bestScoreStreakTarget, startMapTraverse, iterations
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
				iterations = iterations + 1
				print("Success! score: ", score)
				if(score == lastScore):
					bestScoreStreak = bestScoreStreak + 1
					if(bestScoreStreak >= bestScoreStreakTarget):
						endMapTraverse = time.time()
						print("")
						print("The agent has found the optimal path in ", iterations, " iterations!")
						print("The agent took :", endMapTraverse - startMapTraverse, " seconds")
						print("-------------------------------------------------")
						print("                                   (\_/)  ")
						print("Sayonara, thanks for stopping bye! (^-^)/)")
						print("-------------------------------------------------")
						raw_input("Please restart the program with different settings for more fun!")
				else:
					lastScore = score
					bestScoreStreak = 0					
            else:
				iterations = iterations + 1
				print("Fail! score: ", score)
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = playerInit
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game(args):
	#print(args.verbose)
	#if(args.verbose):
	#	MapManager.Verbose = True
	#
	#if(args.width is not None):
	#	x = args.width
	#	
	#if(args.height is not None):
	#	y = args.height	
	#	
	#print(args.type)
	
	global startMapTraverse
	startMapTraverse = time.time()
	master.mainloop()
