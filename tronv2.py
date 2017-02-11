# -*- coding: utf-8 -*-

from Tkinter import *
import socket
import sys
import time
import numpy as np
import random
import operator

# TRON Client version Alpha 0.1.4

version = "0.1.4"

def terminaldisplay():
	
	# Affichage dans le terminal
	global NotInGame,WaitingToStart,inGame,version,game,listPlayer,lastWinner,Initialisation,Alive
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
			print Alive
			print ' '
			print 'Name'+'\t\t\t\t'+'Session wins'+'\t'+'All Time wins'+'\t'+'Color'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				if len(p[0])>7 and len(p[0])<15:
					print p[0]+'\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>15 and len(p[0])<22:
					print p[0]+'\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>22:
					print p[0]+'\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				else:
					print p[0]+'\t\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
			for i in range(10-nbPlayer):
				print ''
		elif inGame :
			print 'Game started since '+str(int(game.ite*game.speed*game.sp))+' seconds.'
			print ' '
			print 'Players connected : '
			print ' '
			print Alive
			print ' '
			print 'Name'+'\t\t\t\t'+'Session wins'+'\t'+'All Time wins'+'\t'+'Color'
			nbPlayer = len(listPlayer)
			for p in listPlayer:
				if len(p[0])>7 and len(p[0])<15:
					print p[0]+'\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>15 and len(p[0])<22:
					print p[0]+'\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				elif len(p[0])>22:
					print p[0]+'\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
				else:
					print p[0]+'\t\t\t\t'+p[1]+'\t\t'+p[2]+'\t\t'+p[3]
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
		self.lastdxp = self.dxp
		self.lastdxm = self.dxm
		self.lastdyp = self.dyp
		self.lastdym = self.dym
		self.speed = float(params[11])
		self.number_player = 0
		self.ite = 0
		self.disp = 0
		self.timeNextIte = startingTime + self.speed*self.sp
		self.notLoadedPos = True
		self.turned = False
		
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
					self.UI()
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
				self.UI()
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
	def UI(self):
		global listPlayer,WaitingToStart,col
		sorted(listPlayer, key=operator.itemgetter(1),reverse=True)
		canvas.delete("all")
		sp = 16
		canvas.create_rectangle(self.sp*self.wi,0,self.sp*self.wi+5,self.sp*self.he,fill='white')
		canvas.create_text(self.sp*self.wi+50,20,text='Wins        Name',fill='white',anchor=NW)
		sp = 16
		#~ if WaitingToStart:
			#~ for i in range(len(col)):
				#~ canvas.create_rectangle(1*sp,(i+1)*sp,2*sp,(i+2)*sp,fill=col[i][1])
				#~ canvas.create_text(5*sp,(i+1.5)*sp,text=col[i][0],fill=col[i][1])
		for i in range(len(listPlayer)):
			canvas.create_rectangle(self.sp*self.wi+10,20+(i+3)*sp,self.sp*self.wi+sp+10,20+(i+4)*sp,fill=listPlayer[i][3])
			canvas.create_text(self.sp*self.wi+50,(i+4)*sp+5,text=listPlayer[i][1],fill=listPlayer[i][3],anchor=NW)
			canvas.create_text(self.sp*self.wi+100,(i+4)*sp+5,text=listPlayer[i][0],fill=listPlayer[i][3],anchor=NW)
		window.update()
	
	def change(self,c):
		
		# Changement de direction
		if not self.turned:
			#~ print c,self.ite
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
			
	def change2(self,c):
		
		# Changement de direction
		if not self.turned:
			#~ print c,self.ite
			if c=='left':
				if self.lastdxp == 0:
					self.dym = 0
					self.dxm = 1
					self.dyp = 0
					self.dxp = 0
			if c=='right':
				if self.lastdxm == 0:
					self.dym = 0
					self.dxm = 0
					self.dyp = 0
					self.dxp = 1
			if c=='down':
				if self.lastdym == 0:
					self.dym = 0
					self.dxm = 0
					self.dyp = 1
					self.dxp = 0
			if c=='up':
				if self.lastdyp == 0:
					self.dym = 1
					self.dxm = 0
					self.dyp = 0
					self.dxp = 0
			self.turned = True
		
	def draw(self):
		
		# Affichage des nouvelles positions
		global canvas
		currentTime = time.time()
		global NotInGame,WaitingToStart,inGame,startingTime,lastWinner,Alive
		if inGame:
			if currentTime > self.timeNextIte: 
				if self.ite%4==0:
					self.turned = False
				ask = '? ' + str(self.ite)
				#~ print 'send = ',ask
				self.sock.send(ask)
				tab = self.sock.recv(size).split()
				
				#~ print tab
				
				# Random Behaviour
				
				#~ if(np.random.random()<0.03):
					#~ if(np.random.random()<0.5):
						#~ self.change('right')
					#~ else:
						#~ self.change('left')
				
				if tab[0] == 'NoGame':
					global color
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
					color = params[12]
					self.begin()
				else :
					self.timeNextIte += self.speed*self.sp
					self.ite += 1
					self.lastdxp = self.dxp
					self.lastdxm = self.dxm
					self.lastdyp = self.dyp
					self.lastdym = self.dym
					i = 1
					while i < (len(tab)):
						h = tab[i].split(':')
						canvas.create_rectangle(int(h[1])*self.sp,int(h[2])*self.sp,(int(h[1])+1)*self.sp,(int(h[2])+1)*self.sp,fill=h[3])
						i += 1
			tell = 'move '+str(self.ite)+' '+str(self.Id)+' '+str(self.dxm)+' '+str(self.dxp)+' '+str(self.dym)+' '+str(self.dyp)
			
			self.sock.send(tell)
			#~ print 'send = ',tell
			a = self.sock.recv(size)
			if a[0] == 'NoGame':
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
			#~ print 'recv = ',a
			
			self.disp += 1
			if self.disp > 100:
				self.sock.send('alive hello')
				Alive = self.sock.recv(size)
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
		global canvas,col
		self.UI()
		sp = 16
		window.update()
	
	def newgame(self):
		
		# Reinitialisation des parametres
		def start():
			print ''
			print "Asking serveur to reset the game"
			self.sock.send('reset')
			#~ print 'send = reset'
			a = self.sock.recv(size)
			#~ print 'recv = ',a
		return start

def findGame(sock):
	
	# Recoit les parametres du joueur
	global NotInGame,WaitingToStart,inGame,color,Alive
	Alive = ' '
	Received = False
	while not Received:
		if color =='':
			data = 'name '+ player
		else:
			data  = 'name '+ player + ' '+ color
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
	print 'Localizing the server, please wait'
	while not Connected:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			essai = 'bs406-s31-'+str(random.randrange(28)+1)
			#~ print essai
			sock.connect((essai, port))
			
			# Dialogue avec le serveur via la classe GameClient
			params = findGame(sock)
			game = GameClient(params,sock)
			Connected = True
           
		except socket.error:
			#~ print 'Error : Connection failed !'
			time.sleep(0.02)
         
	

# Parametres du jeu

startingTime = 0
NotInGame = True
WaitingToStart = False 
inGame = False
Initialisation = True
mode = 0
color = ''
Alive = ''
listPlayer = []
lastWinner = 'None'

# Parametres socket

Connected = False
port = 3333
size = 1024


#~ host = '127.0.0.1'
#~ host = 'bs406-s31-23.insa-lyon.fr' #4BIM
#~ host = '134.214.159.30'
#~ player = 'insert_name_here'

host = sys.argv[1]
player = sys.argv[2]
Initialisation = False


terminaldisplay()
while True:
	try:
		print('How many buttons do you want to use to move the snake ?')
		print('- For the old method : Left,Right , enter "2" ')
		print('- For the new method : Left,Right,Up,Down , enter "4" ')
		print ''
		s = raw_input("")
		if(s=='2'):
			mode = 2
			Initialisation = False
			break	
		elif(s=='4'):
			mode = 4
			Initialisation = False
			break
	except ValueError:
		print("Please enter 2 or 4 ... *facepalm* ")

# Creation de la fenetre graphique
window = Tk()
window.title('TRON')

# Connexion et demarrage du jeu
ConnectionServer()

canvas = Canvas(window,bg='black',height=game.he*game.sp,width=game.wi*game.sp+200)
canvas.create_rectangle(game.sp*game.wi,0,game.sp*game.wi+5,game.sp*game.he,fill='white')
canvas.pack(side=TOP)


col=[]
col.append(['slategray','#6f8090',10])
col.append(['cornsilk3','#cdc7b0',10])
#~ col.append(['burlywood2','#edc591',10])
col.append(['lightpink','#ffadb8',10])
#~ col.append(['palegreen','#97fa97',10])
col.append(['paleturquoise','#baffff',10])
#~ col.append(['thistle2','#cac3ca',10])
col.append(['slateblue3','#6958cd',10])
col.append(['steelblue3','#4f93cd',10])
col.append(['tomato','#ff6246',10])
col.append(['orangered1','#ff4500',10])
col.append(['orange','#ffa400',10])
col.append(['firebrick3','#cd2525',10])
#~ col.append(['brown2','#ed3a3a',10])
#~ col.append(['yellow1','#ffff00',10])
col.append(['gold2','#edc800',10])
col.append(['deeppink2','#ed1288',10])
col.append(['mediumpurple','#926fdb',10])
col.append(['chartreuse2','#7eff00',10])
col.append(['green2','#00cd00',10])
#~ col.append(['olivedrab3','#9acd31',10])
#~ col.append(['limegreen','#31cd31',10])
col.append(['royalblue2','#436ded',10])
col.append(['seagreen3','#43cd80',10])
col.append(['skyblue3','#6ca6cd',10])
col.append(['darkmagenta','#8a008a',10])
col.append(['hotpink1','#ff6db4',10])






#~ 
#~ b=Button(window,text="New Game")
#~ b.config(command=game.newgame())
#~ b.pack()

if mode ==2:
	window.bind('<Right>', lambda event: game.change('right'))
	window.bind('<Left>', lambda event: game.change('left'))
if mode ==4:
	window.bind('<Right>', lambda event: game.change2('right'))
	window.bind('<Left>', lambda event: game.change2('left'))
	window.bind('<Up>', lambda event: game.change2('up'))
	window.bind('<Down>', lambda event: game.change2('down'))


window.update()

game.begin()

window.mainloop()


####### TODO List :

# 1- Change the time management so it is based on UTC time and not local time

####### Optionnal :

# Color selecting ? Maybe depending of their number of wins ?

