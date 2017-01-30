# -*- coding: utf-8 -*-

from Tkinter import *
import socket
import sys
import time
import numpy as np

# TRON Client version Alpha 0.0.6

def terminaldisplay():
	# Affichage dans le terminal
	global NotInGame,WaitingToStart,inGame,version,game,listPlayer,lastWinner,Initialisation
	for i in range(5):
		print ''
	print "########## Welcome to TRON ###############"
	print ''
	print "Version " + version
	print ''
	if Initialisation:
		print ''
	else :
		print 'Last game winner : ' + lastWinner 
		print ''
		if NotInGame:
			print " Waiting for game "
			for i in range(13):
				print ''
		elif WaitingToStart:
			global startingTime
			numb = str(int(round(startingTime-time.time())))
			print 'Game starting in '+numb+' seconds'
			print ' '
			print 'Players connected : '
			print ' '
			print 'Name'+'\t\t'+'Session wins'+'\t'+'All Time wins'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				print p[0]+'\t\t'+p[1]+'\t\t'+p[2]
			for i in range(10-nbPlayer):
				print ''
		elif inGame :
			print 'Game started since '+str(int(game.ite*game.speed*game.sp))+' seconds.'
			print ' '
			print 'Players connected : '
			print ' '
			print 'Name'+'\t\t'+'Session wins'+'\t'+'All Time wins'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				print p[0]+'\t\t'+p[1]+'\t\t'+p[2]
			for i in range(10-nbPlayer):
				print ''
		
class GameClient:
	""" Classe gerant la connexion du client et les messages au serveur """

	def __init__(self,params,sock):
		global startingTime
		self.sock = sock
		self.wi = int(params[1])
		self.he = he = int(params[2])
		self.sp = int(params[3])
		self.ad = int(params[4])
		self.Id = int(params[5])
		startingTime = float(params[6])
		self.dxm = int(params[7])
		self.dxp = int(params[8])
		self.dym = int(params[9])
		self.dyp = int(params[10])
		self.speed = float(params[11])
		self.number_player = 0
		self.ite = 0
		self.disp = 0
		self.timeNextIte = startingTime + self.speed*self.sp
		self.notLoadedPos = True
		
	def phase_init(self):
    	# Ecriture du decompte dans la  fenetre graphique
		global NotInGame,WaitingToStart,inGame,startingTime,ad,listPlayer
		wait = True
		while wait:
			currentTime = time.time()
			if currentTime < startingTime:
				if round(startingTime-currentTime-round(startingTime-currentTime),5) == 0:
					numb = str(int(round(startingTime-currentTime)))
					c = [0,0,0,0,0,0,0,0]
					c2 = [0,0,0,0,0,0,0,0]
					num = int(numb)
					if (num>9):
						c2=[1,1,1,1,0,0,0,0]
					else:
						c2=[0,0,0,0,0,0,0,0]
					if (numb=='9' or numb=='19'):
						c=[1,1,0,0,1,1,1,1]	
					elif (numb=='8' or numb=='18' or numb=='10'):
						c=[1,1,1,1,1,1,1,1]	
					elif (numb=='7' or numb=='17'):
						c=[1,0,0,0,1,1,1,1]		
					elif (numb=='6' or numb=='16'):
						c=[1,1,1,1,1,0,1,1]	
					elif (numb=='5' or numb=='15'):
						c=[1,1,0,1,1,0,1,1]	
					elif (numb=='4' or numb=='14'):
						c=[1,1,1,0,0,0,1,1]			
					elif (numb=='3' or numb=='13'):
						c=[1,0,0,1,1,1,1,1]
					elif (numb=='2' or numb=='12'):
						c=[1,0,1,1,1,1,0,1]
					elif (numb=='1' or numb=='11'):
						c=[0,0,0,0,1,1,1,1]
					for i in range(2):
						for j in range(4):
							if c[i*4+j]==0:
								col='#000000'
							else:
								col='#C0E9E6'
							if c2[i*4+j]==0:
								col2='#000000'
							else:
								col2='#C0E9E6'
							canvas.create_rectangle((self.wi/2-2*(1-i))*self.sp,(self.he/2-2*(2-j))*self.sp,\
								(self.wi/2+2*i)*self.sp,(self.he/2-2*(1-j))*self.sp,fill=col)
							canvas.create_rectangle((self.wi/2-2*(4-i))*self.sp,(self.he/2-2*(2-j))*self.sp,\
								(self.wi/2-4+2*i)*self.sp,(self.he/2-2*(1-j))*self.sp,fill=col2)
					msg='who'
					self.sock.send(msg)
					LP = self.sock.recv(size).split()
					LP.pop(0)
					#~ print 'send = ',msg
					#~ print 'recv = ',LP
					listPlayer = []
					for lp in LP:
						p = lp.split(':')
						listPlayer.append([p[0],p[1],p[2]])
					window.update()
					terminaldisplay()
					
					time.sleep(0.01)
			else :
				wait = False
				WaitingToStart = False
				inGame = True
				msg='who'
				
				self.sock.send(msg)
				LP = self.sock.recv(size).split()
				LP.pop(0)
				#~ print 'send = ',msg
				#~ print 'recv = ',LP
				listPlayer = []
				for lp in LP:
					p = lp.split(':')
					listPlayer.append([p[0],p[1],p[2]])
				terminaldisplay()
		
	def change(self,c):
		# Changement de direction
		#~ print c
		if c=='left':
			swap = self.dym
			self.dym = self.dxp
			self.dxp = self.dyp
			self.dyp = self.dxm
			self.dxm = swap
		if c=='right':
			swap = self.dym
			self.dym = self.dxm
			self.dxm = self.dyp
			self.dyp = self.dxp
			self.dxp = swap
		
	def draw(self):
		# Affichage des nouvelles positions
		global canvas
		currentTime = time.time()
		global NotInGame,WaitingToStart,inGame,startingTime,lastWinner
		if inGame:
			if currentTime > self.timeNextIte: 
				ask = '? ' + str(self.ite)
				self.sock.send(ask)
				tab = self.sock.recv(size).split()
				#~ print 'send = ',ask
				#~ print tab
				
				#~ if(np.random.random()<0.05):
					#~ if(np.random.random()<0.5):
						#~ self.change('right')
					#~ else:
						#~ self.change('left')
				
				if tab[0] == 'NoGame':
					inGame = False
					NotInGame = True	
					self.reset()
					startingTime = float(tab[1])
					lastWinner = tab[2]
					self.timeNextIte = startingTime + self.speed*self.sp
					params = findGame(self.sock)
					self.ite = 0
					self.wi = int(params[1])
					self.he = int(params[2])
					self.sp = int(params[3])
					self.Id = int(params[5])
					self.dxm =  int(params[7])
					self.dxp =  int(params[8])
					self.dym =  int(params[9])
					self.dyp =  int(params[10])
					self.speed = float(params[11])
					self.begin()
				else :
					self.timeNextIte += self.speed*self.sp
					self.ite += 1
					i = 1
					while i < (len(tab)):
						h = tab[i].split(':')
						canvas.create_rectangle(int(h[1])*self.sp,int(h[2])*self.sp,(int(h[1])+1)*self.sp,(int(h[2])+1)*self.sp,fill=h[3])
						i += 1
			tell = 'move '+str(self.ite)+' '+str(self.Id)+' '+str(self.dxm)+' '+str(self.dxp)+' '+str(self.dym)+' '+str(self.dyp)
			
			self.sock.send(tell)
			a = self.sock.recv(size)
			#~ print 'send = ',tell
			#~ print 'recv = ',a
			
			self.disp += 1
			if self.disp > 100:
				terminaldisplay()
				self.disp = 0	
				
	def begin(self):
		# Demarrage du nouveau jeu
		global NotInGame,WaitingToStart,inGame,LabelNotCreated
		if LabelNotCreated:
			self.createLabel()
		self.phase_init()
		for i in range(100000):
			window.after(10,self.draw())
			window.update()			
				
			
	def createLabel(self):
		l = Label( window, font=('times', 20, 'bold'), bg='green',text='Host')
		l.pack()

 	def reset(self):
 		# Reinitialisation de la fenetre graphique
		global canvas
		canvas.delete("all")
		#~ canvas = Canvas(window,bg='black',height=he*sp,width=wi*sp)
		window.update()
	
	def newgame(self):
		# Reinitialisation des parametres
		def start():
			print ''
			print "Asking serveur to reset the game"
			self.sock.send('reset')
			print 'send = reset'
			a = self.sock.recv(size)
			print 'recv = ',a
		return start

def findGame(sock):
	# Recoit les parametres du joueur
	global NotInGame,WaitingToStart,inGame
	Received = False
	while not Received:
		data = 'name '+ player
		sock.send(data)
		s = sock.recv(size)
		#~ print 'send = ',data
		#~ print 'recv = ',s
		
		if len(s.split())>1:
			if s.split()[0] == 'accepted':
				NotInGame = False
				WaitingToStart = True
				params = s.split()
				Received = True
		terminaldisplay()
		if not Received:
			time.sleep(0.1)
	return params


def ConnectionServer():
   # Initialisation de la connexion
	# Socket avec les protocoles IPv4 et TCP
    global Connected
    global game
    if Connected == False:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sock.connect((host, port))
            # Dialogue avec le serveur via la classe GameClient
            params = findGame(sock)
            game = GameClient(params,sock)
            Connected = True
           
        except socket.error:
            print 'Error : Connection failed !'

# Parametres du jeu

startingTime = 0
NotInGame = True
WaitingToStart = False 
inGame = False
LabelNotCreated = False
Initialisation = True
listPlayer = []
lastWinner = 'None'

# Parametres socket

Connected = False
port = 3333
size = 1024
version = "0.0.6"
#~ host = '127.0.0.1'
#~ host = 'bs406-s31-20.insa-lyon.fr'
host = 'bs406-s16-24.insa-lyon.fr'
#~ host = '134.214.159.30'
#~ player = 'insert_name_here'

# Script terminal initial

#terminaldisplay()
#~ 
# while True:
# 	try:
# 		#~ print ('WARNING : Please execute this script from a real terminal ')
# 		print ''
# 		print ('Where is the server launched ?')
# 		print ('For example if it is on bs406-s31-15 enter 15')
# 		print ''
# 		x = int(input(""))
# 		host = 'bs406-s31-'+str(x)
# 		break
# 	except ValueError:
# 		print("Oops!  That was no valid number.  Try again...")
		
terminaldisplay()

while True:
	try:
		print('What is your name ?')
		print('Example : xXDarkRangerdu93Xx or John')
		print ''
		s = raw_input("")
		player = s
		Initialisation = False
		break
	except ValueError:
		print("Oops!  That was not a valid name.  Try again...")

# Creation de la fenetre graphique
window = Tk()
window.title('TRON')

# Connexion et demarrage du jeu
ConnectionServer()

canvas = Canvas(window,bg='black',height=game.he*game.sp,width=game.wi*game.sp)
canvas.pack(side=TOP)

#~ if ad:

b=Button(window,text="New Game")
b.config(command=game.newgame())
b.pack()


window.bind('<Right>', lambda event: game.change('right'))
window.bind('<Left>', lambda event: game.change('left'))
window.update()

game.begin()

window.mainloop()


# TODO List :

####### 1- End of game if only one player alive 

####### 2- Change the time management so it is based on UTC time and not local time

####### Optionnal :

# Reducing input lag by adding more iteration between gameUpdate()
# Put might compromise the network by demanding more connections...

# Color selecting ? Maybe depending of their number of wins ?

# A better UI ?
