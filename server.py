import time
import numpy as np
import socket
import threading
import random
import os

# TRON Server version Alpha 0.0.6

version = "0.0.6"

# Class Head = one player
# Parameters :
# name : pseudonyme
# x,y,dxp,dxm,dyp,dym :position and current direction 
# Alive : has he encontered a wall or no 1-> Alive / 0-> Dead
# Id : ID given by the server 
# Color : Color in #00000 format
# wins : wins of the player since the server was started
# totalwins : wins of the player when the server was started on this machine
class Head:
	def __init__(self,color,name):
		self.name = name
		self.x = 0
		self.y = 0
		self.dxp = 0
		self.dxm = 0
		self.dyp = 0
		self.dym = 0
		self.alive = 1
		self.Id = 0
		self.color = color
		self.wins = 0
		self.totalwins = 0
	
	# Update position with the current speed(direction) of the Head
	def move(self,wi,he,sp):
		self.x = (self.x + self.dxp - self.dxm)%(wi)
		self.y = (self.y + self.dyp - self.dym)%(he)

# Class Game, omnipotent class that rules the game
# sp : number of pixel per frame
# list_Head : list of the head currently in the game
# wall : table which tracks which cell on the grid is a wall or not
# he : height of the game
# wi : width of the game
# sp : number of pixel of each cell
# number_player : number of still alive player
# ite : number of iteration of the game
# StringIte : Keep each Position String for each iteration
# timeNextIte: Time where the next iteration will occur
# winner : Keep tracks of the winner of the last game

class Game:
	def __init__(self,wi,he,sp):
		self.sp = sp
		self.list_Head = []
		self.wall = np.ones((wi,he))*17
		self.wi = wi
		self.he = he
		self.sp = sp
		self.number_player=0
		self.ite = 0
		self.StringIte = []
		self.timeNextIte = 0 
		self.winner = 'None2'
		
		# On the native version our game is torical
		# Decoment code bellow if you want borders to be walls 

		# for i in range(wi):
		# 	self.wall[i][0]=20
		# 	self.wall[i][he-1]=20
		# for i in range(he):
		# 	self.wall[0][i]=20
		# 	self.wall[wi-1][i]=20 
	
	
	# Add a new player to the game
	def addHead(self,h):
		global AllTimePlayers
		positionned = False
		while not positionned: # Try to find a spot not to close to other players
			Ok = True
			x = np.random.randint(self.wi)
			y = np.random.randint(self.he)
			for k in self.list_Head:
				dist=0
				dist+=abs(x-k.x)
				dist+=abs(y-k.y)
				if dist<25: # Try to find a spot at least 25 blocks away from every other player
					Ok = False
			if Ok:
				h.x=x
				h.y=y
				positionned=True
		direction=np.random.randint(4) # Set random starting direction to the player
		if direction==0:
			h.dxm=1
		if direction==1:
			h.dxp=1
		if direction==2:
			h.dym=1
		if direction==3:
			h.dyp=1
		
		new = True
		for p in AllTimePlayers:
			if len(p)>0:
				if p[0]==h.name:  # Checks if the name is already know by the server
					new = False
					h.wins = p[2]		# Get the data for wins and totalwins
					h.totalwins = p[1]
		if new : # If new player create a name in the server database (text based)
			AllTimePlayers.append([h.name,0,0]) 
											
		h.Id=self.number_player # Server assigns an Id to the player
		self.list_Head.append(h) # Player is added to the players currently in game
		self.number_player+=1 
	
	# Method that make a real iteration of the game
	def gameUpdate(self):
		self.collision() # Check if a players die
		for h in self.list_Head:      
			self.wall[h.x][h.y]=h.Id   # Update wall table
			h.move(self.wi,self.he,self.sp) # Move every player
	
	# Generate a string that holds the position of each player at the current iteration
	def generateDataString(self):
		s=str(self.ite)
		for h in self.list_Head:      
			s+=" "+h.name+":"+str(h.x)+":"+str(h.y)+":"+str(h.color)
		if (self.ite%4)==0: # Every 4 iteration make a real iteration
			self.gameUpdate()
		return s
	
	# If a client ask for an iteration strings returns it
	def getString(self,n):
		return self.StringIte[int(n)]
	
	# Check if a player collided with a wall
	
	def collision(self):
		global endGame,endTime
		for h in self.list_Head:
			if self.wall[h.x][h.y]!=17:
				h.dxm=0
				h.dxp=0
				h.dym=0
				h.dyp=0
				# If yes : we loose a player and he isnt alive anymore
				if h.alive==1:
					self.number_player-=1
					h.alive=0
		# If only one player is alive, server pass in "endGame" phase
		if self.number_player <2:
			if not endGame:
				print 'ending soon'
				endGame = True
				endTime = time.time()
				print endTime
				for i in self.list_Head:
					if i.alive==1:
						self.winner = i.name
	# In case of a new game resets all game variables
	def reset(self):
		global startingTime,speed,sp,wi,he
		self.number_player = 0
		self.list_Head = []
		self.wall = np.ones((wi,he))*17	
		self.ite = 0
		self.StringIte = []
		self.timeNextIte = startingTime+ speed*sp
		
	# Give the names and wins of the players currenlty in the game
	def returnName(self):
		s='' 
		for i in self.list_Head:
			s+=i.name+':'+str(i.wins)+':'+str(i.totalwins)+' '
		return s

# Reset servers variables in case of a new game
def newgame():
	global delay,startingTime,endTime,endGame,nbGames
	nbGames +=1
	startingTime = time.time()+delay
	updateHighscore(game.winner)
	game.reset()
	endTime = time.time()+20000
	inGame = False
	endGame = False
	waitingForPlayers = True
	
	
# Assign a random color to the player
def getNewColor():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    return '#%02x%02x%02x' % (r,g,b)

# Read the highcore textfile and load the informations in it
def getHighscore():
	global AllTimePlayers
	if os.path.exists('highscore.txt'):
		f = open('highscore.txt','r')
		lignes = f.readlines()
		for li in lignes:
			if len(li)>0:
				t = li.split('\t')
				if len(t)>1:
					AllTimePlayers.append([t[0],int(t[1]),0])
		f.close()
	else : # If he doesnt existe, create it
		f = open('highscore.txt','w')
		f.close()

# Update the textfile with current information
def updateHighscore(winner):
	global AllTimePlayers
	s = ''
	for p in AllTimePlayers:
		if len(p)>0:
			if p[0]==winner:
				p[1]+=1
				p[2]+=1
			s+=(p[0]+'\t'+str(p[1])+'\n')
	f = open('highscore.txt','w')
	f.writelines(s)
	f.close()

# Initialating Server global parameters
wi = 60
he = 48
sp = 12
speed = 0.0025
delay = 3
delayDeath = 2
waitingForPlayers = True
startingSoon = False 
inGame = False
endGame = False

startingTime =  time.time()+delay
endTime = time.time()+20000

# Server connexions and game count
nbGames = 0
count = 0	

# This method is runned each time a client connects to the server
def handler(newsock):
	currentTime = time.time() 
	global count
	count +=1
	# Load global parameters
	global waitingForPlayers,startingSoon,inGame,endGame,startingTime,delay,sp,speed,endTime,endGame,nbGames,delayDeath
	if inGame and currentTime>game.timeNextIte: 
		# If inGame and a iteration has passed do a new iteration
		s=game.generateDataString()
		game.StringIte.append(s)
		game.timeNextIte+=speed*sp
		game.ite+=1
	if  waitingForPlayers and currentTime>(startingTime-1): # Waiting -> Starting soon
		waitingForPlayers = False
		startingSoon = True
	if startingSoon and currentTime>startingTime: # Starting soon -> inGame
		startingSoon = False
		inGame = True
		s=game.generateDataString()
		game.StringIte.append(s)
		game.timeNextIte=startingTime+speed*sp
		game.ite+=1
		endTime = time.time()+20000
		print game.number_player
		if game.number_player<2: # If only one player connected game doesn't start
			waitingForPlayers = True
			inGame = False
			game.winner='None'
			newgame()
			print 'Game autoresetting'
		#~ print game.StringIte
	#~ print currentTime-(endTime+5)
	if currentTime>(endTime+delayDeath): # if game has ended since delayDeath restart a new one
		print 'You waited too long '
		waitingForPlayers = True
		inGame = False
		game.winner=game.winner
		newgame()
		print 'Game autoresetting'
		print count,nbGames
	data = newsock.recv(size) # Get the client message
	sd=data.split()  # Split it
	#~ print sd
	if sd[0]=='name' and waitingForPlayers: 
		# If he tries to connect while we are waiting for players
		# accept him and add his head to the game
		color = getNewColor()
		print "New player with pseudo %s joined the server"%sd[1]
		h = Head(color,sd[1])
		game.addHead(h)
		newsock.send('accepted '+str(wi) + ' ' + str(he) + ' ' + str(sp)+ ' ' +str(0)+ ' ' +str(h.Id)+ ' ' +str(startingTime)+ ' ' +str(h.dxm)+ ' ' +str(h.dxp)+ ' ' +str(h.dym)+ ' ' +str(h.dyp)+ ' ' +str(speed))
	if sd[0]=='?' and waitingForPlayers: 
		# if he thinks the game is still running while it isn't tell him 'NO'
		newsock.send('NoGame '+str(startingTime)+' '+game.winner)
	if sd[0]=='?' and inGame: # if the game is still running tell him the information is he asking for
		msg = game.getString(sd[1])
		#~ print nbGames
		newsock.send(msg)
	if sd[0]=='move' and inGame: # If the game is running update his movement decision
		h = game.list_Head[int(sd[2])]
		h.dxm = int(sd[3])
		h.dxp = int(sd[4])
		h.dym = int(sd[5])
		h.dyp = int(sd[6])
	if sd[0]=='reset': # If he ask to reset the game, do so
		waitingForPlayers = True
		inGame = False
		newgame()
		print 'Game resetting'
	if sd[0]=='who': # If he ask who is connected do so
		newsock.send(game.returnName())
		#~ print game.returnName()
	#~ print AllTimePlayers
	newsock.shutdown(1) # Close socket
	newsock.close()
	
	
# Network stuff

size = 1024
listhead = []

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',3333))

AllTimePlayers=[]

getHighscore()

game = Game(wi,he,sp)

sock.listen(15)
players = []

# Loop that listen to the port 3333 and execute the "handler" method
# each time a client connects to it
while True:
	newsock, addr = sock.accept()
	players.append(newsock)
	thr = threading.Thread(target = handler, args=(newsock,))
	thr.start()
	thr.join()
	#~ if nbGames>10:
		#~ break
sock.shutdown(1)
sock.close()



# TODO List :


####### 2- Change the time management so it is based on UTC time and not local time

####### Optionnal :

# Reducing input lag by adding more iteration between gameUpdate()
# Put might compromise the network by demanding more connections...

# Color selecting ? Maybe depending of their number of wins ?

# A better UI ?

 
 
