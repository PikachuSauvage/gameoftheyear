# -*- coding: utf-8 -*-

from Tkinter import *
import socket
import sys
import time
import numpy as np

# TRON Client version Alpha 0.1.2

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
			print 'Name'+'\t\t\t'+'Session wins'+'\t'+'All Time wins'+'\t'+'Color'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				if len(p[0])>7 and len(p[0])<15:
					print p[0]+'\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>15:
					print p[0]+'\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				else:
					print p[0]+'\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
			for i in range(10-nbPlayer):
				print ''
		elif inGame :
			print 'Game started since '+str(int(game.ite*game.speed*game.sp))+' seconds.'
			print ' '
			print 'Players connected : '
			print ' '
			print 'Name'+'\t\t\t'+'Session wins'+'\t'+'All Time wins'+'\t'+'Color'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				if len(p[0])>7 and len(p[0])<15:
					print p[0]+'\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>15:
					print p[0]+'\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				else:
					print p[0]+'\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
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
		self.turned = False
		
	def phase_init(self):
		
    	# Affichage du decompte dans la  fenetre graphique
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
					#~ print 'send = ',msg
					LP = self.sock.recv(size).split()
					LP.pop(0)
					#~ print 'recv = ',LP
					listPlayer = []
					for lp in LP:
						p = lp.split(':')
						listPlayer.append([p[0],p[1],p[2],p[3]])
					window.update()
					terminaldisplay()
					
					time.sleep(0.01)
			else :
				canvas.delete("all")
				window.update()
				wait = False
				WaitingToStart = False
				inGame = True
				msg='who'
				self.sock.send(msg)
				#~ print 'send = ',msg
				LP = self.sock.recv(size).split()
				LP.pop(0)
				
				#~ print 'recv = ',LP
				listPlayer = []
				for lp in LP:
					p = lp.split(':')
					listPlayer.append([p[0],p[1],p[2],p[3]])
				terminaldisplay()
		
	def change(self,c):
		
		# Changement de direction sur commande du joueur
		if not self.turned:
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
			self.turned = True
		
	def draw(self):
		
		# Affichage des nouvelles positions dans la fenetre
		global canvas
		currentTime = time.time()
		global NotInGame,WaitingToStart,inGame,startingTime,lastWinner
		if inGame:
			# Le client interroge le serveur sur les positions de l'iteration precedente
			if currentTime > self.timeNextIte: 
				if self.ite%4==0:
					self.turned = False
				ask = '? ' + str(self.ite)
				self.sock.send(ask)
				tab = self.sock.recv(size).split()
				
				# Si la partie est terminee, reinitialisation des parametres
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
					startingTime = float(params[6])
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
						
			# Envoi du changement de direction au serveur
			tell = 'move '+str(self.ite)+' '+str(self.Id)+' '+str(self.dxm)+' '+str(self.dxp)+' '+str(self.dym)+' '+str(self.dyp)
			self.sock.send(tell)
			answer = self.sock.recv(size)
			if answer[0] == 'NoGame':
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
				startingTime = float(params[6])
				self.dxm =  int(params[7])
				self.dxp =  int(params[8])
				self.dym =  int(params[9])
				self.dyp =  int(params[10])
				self.speed = float(params[11])
				self.begin()
			
			self.disp += 1
			if self.disp > 100:
				terminaldisplay()
				self.disp = 0	
				
	def begin(self):
		
		# Demarrage du nouveau jeu
		global NotInGame,WaitingToStart,inGame
		self.phase_init()
		for i in range(100000):
			window.after(10,self.draw())
			window.update()			
	

 	def reset(self):
		
 		# Reinitialisation de la fenetre graphique
		global canvas
		canvas.delete("all")
		window.update()
	
	def newgame(self):
		
		# Demande de reinitialisation cote serveur
		def start():
			print ''
			print "Asking serveur to reset the game"
			self.sock.send('reset')
			a = self.sock.recv(size)
		return start

def findGame(sock):
	
	# Recoit les parametres du joueur
	global NotInGame,WaitingToStart,inGame
	Received = False
	while not Received:
		data = 'name '+ player
		sock.send(data)
		s = sock.recv(size)
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
Initialisation = True
listPlayer = []
lastWinner = 'None'

# Parametres socket

Connected = False
port = 3333
size = 1024
version = "0.1.2"

#~ host = '127.0.0.1'
#~ host = 'bs406-s31-23.insa-lyon.fr' #4BIM
#~ host = '134.214.159.30'
#~ player = 'insert_name_here'

# Ces parametres sont a rentrer en ligne de commande dans le terminal
host = sys.argv[1]
player = sys.argv[2]
Initialisation = False

# Creation de la fenetre graphique
window = Tk()
window.title('TRON')

# Connexion et demarrage du jeu
ConnectionServer()

canvas = Canvas(window,bg='black',height=game.he*game.sp,width=game.wi*game.sp)
canvas.pack(side=TOP)

b=Button(window,text="New Game")
b.config(command=game.newgame())
b.pack()


window.bind('<Right>', lambda event: game.change('right'))
window.bind('<Left>', lambda event: game.change('left'))
window.update()

game.begin()

window.mainloop()



####### TODO List :

# 1- Change the time management so it is based on UTC time and not local time

####### Optionnal :

# Color selecting ? Maybe depending of their number of wins ?

