import time
import numpy as np
import socket
import threading
import random
import os

# TRON Server version Alpha 0.0.6

version = "0.0.6"

class Head:

	""" Classe associee a un joueur """
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
		
	def move(self,wi,he,sp):
		self.x = (self.x + self.dxp - self.dxm)%(wi)
		self.y = (self.y + self.dyp - self.dym)%(he)

class Game:

	""" Classe contenant tous les joueurs """
	def __init__(self,wi,he,sp):
		self.sp = sp
		self.list_Head = []
		self.wall = np.ones((wi,he))*17
		self.wi = wi
		self.he = he
		self.sp = sp
		self.number_player = 0
		self.ite = 0
		self.StringIte = []
		self.timeNextIte = 0 
		self.winner = 'None2'

	def addHead(self,h):

		# Ajout d'un nouveau joueur au jeu
		global AllTimePlayers
		positionned = False
		while not positionned:
			Ok = True
			x = np.random.randint(self.wi)
			y = np.random.randint(self.he)
			for k in self.list_Head:
				dist = 0
				dist += abs(x-k.x)
				dist += abs(y-k.y)
				if dist < 25:
					Ok = False
			if Ok:
				h.x = x
				h.y = y
				positionned=True

		# Direction de deplacement initial aleatoire
		direction = np.random.randint(4)
		if direction == 0:
			h.dxm = 1
		if direction == 1:
			h.dxp = 1
		if direction == 2:
			h.dym = 1
		if direction == 3:
			h.dyp = 1
		
		new = True
		for p in AllTimePlayers:
			if len(p)>0:
				if p[0]==h.name:
					new = False
					h.wins = p[2]
					h.totalwins = p[1]
		if new :
			AllTimePlayers.append([h.name,0,0])
					
		h.Id = self.number_player
		self.list_Head.append(h)
		self.number_player += 1
	
	def change(self,c,Id):

		# Changement de direction sur commande du joueur
		if c == 'right':
			swap = self.list_Head[Id].dym
			self.list_Head[Id].dym = self.list_Head[Id].dxp
			self.list_Head[Id].dxp = self.list_Head[Id].dyp
			self.list_Head[Id].dyp = self.list_Head[Id].dxm
			self.list_Head[Id].dxm = swap
		if c == 'left':
			swap = self.list_Head[Id].dym
			self.list_Head[Id].dym = self.list_Head[Id].dxm
			self.list_Head[Id].dxm = self.list_Head[Id].dyp
			self.list_Head[Id].dyp = self.list_Head[Id].dxp
			self.list_Head[Id].dxp = swap
	
	def gameUpdate(self):

		# Deplacement de chaque joueur
		self.collision()
		for h in self.list_Head:      
			self.wall[h.x][h.y] = h.Id  
			h.move(self.wi,self.he,self.sp)
			
	def generateDataString(self):

		# Donnees envoyees au joueur
		s = str(self.ite)
		if (self.ite%4) == 0:
			self.gameUpdate()
		for h in self.list_Head:      
			s += " "+h.name+":"+str(h.x)+":"+str(h.y)+":"+str(h.color)
		return s
	
	def getString(self,n):
		return self.StringIte[int(n)]
	
	def collision(self):
		global endGame,endTime
		for h in self.list_Head:
			if self.wall[h.x][h.y] != 17:
				h.dxm = 0
				h.dxp = 0
				h.dym = 0
				h.dyp = 0
				if h.alive == 1:
					self.number_player -= 1
					h.alive = 0
		if self.number_player < 2:
			if not endGame:
				print 'ending soon'
				endGame = True
				endTime = time.time()
				print 'The end time is', endTime
				for i in self.list_Head:
					if i.alive == 1:
						self.winner = i.name

	def reset(self):

		# Reinitialisation du jeu
		global startingTime,speed,sp,wi,he
		self.number_player = 0
		self.list_Head = []
		self.wall = np.ones((wi,he))*17	
		self.ite = 0
		self.StringIte = []
		self.timeNextIte = startingTime + speed*sp
		
	def returnName(self):
		s = '' 
		for i in self.list_Head:
			s += i.name+':'+str(i.wins)+':'+str(i.totalwins)+' '
		return s

def newgame():

	global delay,startingTime,endTime,endGame,nbParties
	nbParties += 1
	startingTime = time.time() + delay
	updateHighscore(game.winner)
	game.reset()
	endTime = time.time() + 20000
	inGame = False
	endGame = False
	waitingForPlayers = True
	
	
def getNewColor():

	# Attribue au joueur une couleur aleatoire
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    return '#%02x%02x%02x' % (r,g,b)
    
def getHighscore():

	global AllTimePlayers
	if os.path.exists('highscore.txt'):
		f = open('highscore.txt','r')
		lignes = f.readlines()
		for li in lignes:
			if len(li) > 0:
				t = li.split('\t')
				if len(t) > 1:
					AllTimePlayers.append([t[0],int(t[1]),0])
		f.close()

def updateHighscore(winner):

	global AllTimePlayers
	s = ''
	for p in AllTimePlayers:
		if len(p) > 0:
			if p[0] == winner:
				p[1] += 1
				p[2] += 1
			s += (p[0]+'\t'+str(p[1])+'\n')
	f = open('highscore.txt','w')
	f.writelines(s)
	f.close()
	    
def handler(newsock):
	# thread gerant les messages entre client et serveur
	threadLoop = True
	global count
	count += 1
	global waitingForPlayers,startingSoon,inGame,endGame,admin,startingTime, \
	       delay,sp,speed,endTime,endGame,nbParties,delayDeath
	while threadLoop:
		try:
			currentTime = time.time()
			if inGame and currentTime > game.timeNextIte:
				s = game.generateDataString()
				game.StringIte.append(s)
				game.timeNextIte += speed*sp
				game.ite += 1
			if waitingForPlayers and currentTime > (startingTime-1):
				waitingForPlayers = False
				startingSoon = True
			if startingSoon and currentTime > startingTime:
				startingSoon = False
				inGame = True
				s = game.generateDataString()
				game.StringIte.append(s)
				game.timeNextIte = startingTime + speed*sp
				game.ite += 1
				endTime = time.time() + 20000
				print game.number_player
				if game.number_player < 2:
					waitingForPlayers = True
					inGame = False
					game.winner = 'None'
					newgame()
					print 'Game autoresetting'
				#~ print game.StringIte
			#~ print currentTime-(endTime+5)
			if currentTime > (endTime+delayDeath):
				print 'You waited too long '
				waitingForPlayers = True
				inGame = False
				game.winner = game.winner
				newgame()
				print 'Game autoresetting'
				print count,nbParties
			if endGame:
				waitingForPlayers = True
				inGame = False
				newgame()
			# Communication client-serveur
			data = newsock.recv(size)
			if not data:
				newsock.shutdown(0)
				players.remove(newsock)
				threadLoop = False
			else:
				sd = data.split() 
				if sd[0] == 'name' and waitingForPlayers:
					color = getNewColor()
					print "New player with pseudo %s joined the server"%sd[1]
					h = Head(color,sd[1])
					game.addHead(h)
					if admin:
						admin = False
						startingTime = currentTime + delay
						newsock.send('accepted ' + str(wi) + ' ' + str(he) + ' ' + str(sp)+ ' ' \
							+ str(1) + ' ' +str(h.Id) + ' ' + str(startingTime)+ ' ' + str(h.dxm) + \
							' ' + str(h.dxp)+ ' ' + str(h.dym)+ ' ' + str(h.dyp)+ ' ' + str(speed))
					else:
						newsock.send('accepted ' +str(wi) + ' ' + str(he) + ' ' + str(sp)+ ' ' \
							+ str(0)+ ' ' + str(h.Id)+ ' ' + str(startingTime)+ ' ' + str(h.dxm)+ \
							' ' + str(h.dxp)+ ' ' + str(h.dym)+ ' ' + str(h.dyp)+ ' ' + str(speed))
				elif sd[0] == '?' and waitingForPlayers:
					newsock.send('NoGame '+str(startingTime)+' '+game.winner)
				elif sd[0] == '?' and inGame:
					msg = game.getString(sd[1])
					#~ print nbParties
					newsock.send(msg)
				elif sd[0] == 'move' and inGame:
					h = game.list_Head[int(sd[2])]
					h.dxm = int(sd[3])
					h.dxp = int(sd[4])
					h.dym = int(sd[5])
					h.dyp = int(sd[6])
				elif sd[0] == 'reset':
					waitingForPlayers = True
					inGame = False
					newgame()
					print 'Game resetting'
				elif sd[0] == 'who':
					newsock.send(game.returnName())
					#~ print game.returnName()
				#~ print AllTimePlayers
		except:
			break

# Parametres du serveur	
size = 1024
wi = 60
he = 48
sp = 12
speed = 0.0025
delay = 3
delayDeath = 2
admin = True
waitingForPlayers = True
startingSoon = False 
inGame = False
endGame = False
nbParties = 0
startingTime =  time.time() + 10000
endTime = time.time() + 20000
count = 0
players = []

# Initialisation du serveur
# Socket avec les protocoles IPv4 et TCP

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',3333))

AllTimePlayers = []
getHighscore()

game = Game(wi,he,sp)

sock.listen(15)

while True:
	print "Waiting for new connections..."
	newsock, addr = sock.accept()
	players.append(newsock)
	thr = threading.Thread(target = handler, args=(newsock,))
	thr.start()
	#~ if nbParties>10:
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

 
 
