from Tkinter import *
import socket
import sys
import time
import numpy as np

# TRON Client version Alpha 0.0.6

version = "0.0.6"

# Network parameters

size = 1024
port = 3333

#~ host = '127.0.0.1'
#~ host = 'bs406-s31-20.insa-lyon.fr'
#~ host = '134.214.159.30'

#~ player = 'insert_name_here'

canvas= ''

# Method used to make a User Interface in the terminal 

def terminaldisplay():
	global NotInGame,WaitingToStart,inGame,version,game,listPlayer,lastWinner,Initialisation
	for i in range(15):
		print ''
	print "########## Welcome to TRON ###############"
	print ''
	print "Version "+version
	print ''
	if Initialisation:
		print ''
	else :
		print 'Last game winner : '+lastWinner # Print the winner of the last game
		print ''
		
		# Print the status of the game 
		if NotInGame:
			print " Waiting for game "
			for i in range(13):
				print ''
		if WaitingToStart:
			global startingTime
			numb=str(int(round(startingTime-time.time())))
			print 'Game starting in '+numb+' seconds' 
			print ' '
			print 'Players connected : '
			print ' '
			print 'Name'+'\t\t'+'Session wins'+'\t'+'All Time wins'
			nbPlayer=len(listPlayer)
			for p in listPlayer:
				print p[0]+'\t\t'+p[1]+'\t\t'+p[2]
			for i in range(10-nbPlayer):
				print ''
		if inGame :
			print 'Game started since '+str(int(game.ite*game.speed*game.sp))+' seconds.'
			print ' '
			print 'Players connected : '
			print ' '
			print 'Name'+'\t\t'+'Session wins'+'\t'+'All Time wins'
			nbPlayer=len(listPlayer)
			for p in listPlayer:
				print p[0]+'\t\t'+p[1]+'\t\t'+p[2]
			for i in range(10-nbPlayer):
				print ''
		
		
		

# Method used to keep make the game display itself on the player's screen
# Id Identifiant given by the server and used to communicate with him
# wi,he,sp parameters of the graphic window given by the server
# dxm, dxp, dym ,dyp current input of the player
# ite : current iteration of the game
# speed : parameter of the server
# disp : variable to know when to update the terminal display
# timeNextIte : Time of the next iteration
# 

class GameClient:
    def __init__(self,wi,he,sp,Id,startingTime,dxm,dxp,dym,dyp,speed):
		self.Id = Id
		self.wi = wi
		self.he = he
		self.sp = sp
		self.dxm = dxm
		self.dxp = dxp
		self.dym = dym
		self.dyp = dyp
		self.ite = 0
		self.speed = speed
		self.disp = 0
		self.timeNextIte = startingTime+speed*self.sp
		
	# Method that runs during the loading phase before a game
    def phase_init(self):
		global NotInGame,WaitingToStart,inGame,startingTime,listPlayer
		wait = True
		while wait:
			currentTime = time.time()
			if(currentTime < startingTime):
				# Each second a pixel art number is displayed on screen
				if round(startingTime-currentTime-round(startingTime-currentTime),5)==0:
					numb = str(int(round(startingTime-currentTime)))
					c=[0,0,0,0,0,0,0,0]
					c2=[0,0,0,0,0,0,0,0]
					num = int(numb)
					if (num>9):
						c2=[1,1,1,1,0,0,0,0]
					else:
						c2=[0,0,0,0,0,0,0,0]
					if (numb=='9' or numb=='19'):
						c=[1,1,0,0,1,1,1,1]	
					if (numb=='8' or numb=='18' or numb=='10'):
						c=[1,1,1,1,1,1,1,1]	
					if (numb=='7' or numb=='17'):
						c=[1,0,0,0,1,1,1,1]		
					if (numb=='6' or numb=='16'):
						c=[1,1,1,1,1,0,1,1]	
					if (numb=='5' or numb=='15'):
						c=[1,1,0,1,1,0,1,1]	
					if (numb=='4' or numb=='14'):
						c=[1,1,1,0,0,0,1,1]			
					if (numb=='3' or numb=='13'):
						c=[1,0,0,1,1,1,1,1]
					if (numb=='2' or numb=='12'):
						c=[1,0,1,1,1,1,0,1]
					if (numb=='1' or numb=='11'):
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
							canvas.create_rectangle((self.wi/2-2*(1-i))*self.sp,(self.he/2-2*(2-j))*self.sp,(self.wi/2+2*i)*self.sp,(self.he/2-2*(1-j))*self.sp,fill=col)
							canvas.create_rectangle((self.wi/2-2*(4-i))*self.sp,(self.he/2-2*(2-j))*self.sp,(self.wi/2-4+2*i)*self.sp,(self.he/2-2*(1-j))*self.sp,fill=col2)
					# Connect to the server and ask who is currently connected (waiting for the game)
					sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					sock.connect((host,port))
					sock.send('who')
					LP=sock.recv(size).split()
					listPlayer=[]
					# Store this information in the global variable listPlayer
					for lp in LP:
						p = lp.split(':')
						listPlayer.append([p[0],p[1],p[2]])
					sock.close()
					window.update()
					terminaldisplay()
					
					time.sleep(0.01)
			else :
				wait = False
				WaitingToStart = False
				inGame = True
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				sock.connect((host,port))
				sock.send('who')
				LP=sock.recv(size).split()
				listPlayer=[]
				for lp in LP:
					p = lp.split(':')
					listPlayer.append([p[0],p[1],p[2]])
				sock.close()
				
				terminaldisplay()
		
	
	# If the user press the Right or Left arrow key, direction is updated
    def change(self,c):
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
		
	# Method that is looped by the window and makes the game run
    def draw(self):
		currentTime=time.time() 
		# Gets the current computer time
		# Must be aligned on current network time else synchronisation 
		# problems may occur
		global NotInGame,WaitingToStart,inGame,startingTime,lastWinner
		if inGame: # If we are in a game
			if currentTime > self.timeNextIte:  #If an iteration has passed 
				# ask the server what happened last iteration
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				sock.connect((host,port))
				ask = '? '+str(self.ite)
				sock.send(ask)
				tab = sock.recv(size).split()
				
				# Decoment code below if you want a player to have a random behaviour
				
				#if(np.random.random()<0.05):
				#	if(np.random.random()<0.5):
				#		self.change('right')
				#	else:
				#		self.change('left')
				
				# If the server reply that no game is currently running
				# the procedure to reiniate the game is launched
				if tab[0]=='NoGame':
					sock.close()
					inGame = False
					NotInGame = True	
					self.reset() # Cleanse the canvas
					startingTime = float(tab[1]) # New starting time told by the server
					lastWinner = tab[2] # Get the winner of the last game
					self.timeNextIte = startingTime+self.speed*self.sp
					params=findGame() # Try to reconnect to the new game
					self.ite = 0
					# Store the parameters of the new game
					self.wi = int(params[1])
					self.he = int(params[2])
					self.sp = int(params[3])
					self.Id = int(params[5])
					self.dxm =  int(params[7])
					self.dxp =  int(params[8])
					self.dym =  int(params[9])
					self.dyp =  int(params[10])
					self.speed = float(params[11])
					# Launch new game procedure
					game.begin()
				else :
					sock.close()
					# If game is running update iteration variables and print 
					# what occured in the last iteration
					self.timeNextIte+=self.speed*self.sp
					self.ite+=1
					i=1
					while i<(len(tab)):
						h=tab[i].split(':')
						canvas.create_rectangle(int(h[1])*self.sp,int(h[2])*self.sp,(int(h[1])+1)*self.sp,(int(h[2])+1)*self.sp,fill=h[3])
						i+=1
				
			# Tell the server what direction the player is willing to go
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.connect((host,port))
			ask = 'move '+str(self.ite)+' '+str(self.Id)+' '+str(self.dxm)+' '+str(self.dxp)+' '+str(self.dym)+' '+str(self.dyp)
			sock.send(ask)
			sock.close()
			
			# Close to every second update the terminal display
			self.disp+=1
			if self.disp>100:
				terminaldisplay()
				self.disp=0	
				
    def begin(self):
		global NotInGame,WaitingToStart,inGame
		# Launch the ' waiting for the game to start' phase
		self.phase_init()
		# Every 10 ms, execute the self.draw() method and update canvas
		for i in range(100000):
			window.after(10,self.draw())
			window.update()			
				
	# Cleanse the canvas (liberate memory) and update canvas
    def reset(self):
		global canvas
		canvas.delete("all")
		#~ canvas = Canvas(window,bg='black',height=he*sp,width=wi*sp)
		window.update()

# If the user press the 'newgame' button, ask server to launch a new game
def newgame():
	def start():
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((host,port))
		print ''
		print "Asking serveur to reset the game"
		sock.send('reset')
		sock.close()
	return start

# Method used to periodicly ask the server if the player can join the game
def findGame():
	NotConnected = True
	global NotInGame,WaitingToStart,inGame
	while NotConnected:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((host,port))
		data = 'name '+player
		sock.send(data)
		s=sock.recv(size)
		# while nothing is recivied wait
		while sock.recv(size)!='':
			s=sock.recv(size)
		sock.close()
		# if the server tells us 'yes' the pass in the next phase
		if s.split()!=[]:
			if s.split()[0]=='accepted':
				NotInGame = False
				WaitingToStart = True
				params = s.split()
				NotConnected = False
		terminaldisplay()
		# Wait half a second between each attempt
		if NotConnected:
			time.sleep(0.5)
	return params

# Global variables used to know in which phase the client currenlty is
NotInGame = True
WaitingToStart = False 
inGame = False

Initialisation = True
terminaldisplay()

# Ask the user where is the server launched and what will be is username
while True:
	try:
		#~ print ('WARNING : Please execute this script from a real terminal ')
		print ''
		print ('Where is the server launched ?')
		print ('For example if it is on bs406-s31-15 enter 15')
		print ''
		x = raw_input()
		host = 'bs406-s31-'+x
		break
	except ValueError:
		print("Oops!  That was no valid number.  Try again...")
		
terminaldisplay()

while True:
	try:
		print('What is your username ?')
		print('Example : xXDarkRangerdu93Xx or John')
		print ''
		s = raw_input("")
		player = s
		Initialisation = False
		break
	except ValueError:
		print("Oops!  That was not a valid username.  Try again...")

# Initialisation of global variables
listPlayer=[]
game=''
startingTime = 0
lastWinner = 'None'

# Try to find a game
params=findGame()

# Store game parameters into global variables
wi = int(params[1])
he = int(params[2])
sp = int(params[3])
Id = int(params[5])
dxm =  int(params[7])
dxp =  int(params[8])
dym =  int(params[9])
dyp =  int(params[10])
speed = float(params[11])

startingTime = float(params[6])
# Get current time
currentTime = time.time()

game = GameClient(wi,he,sp,Id,startingTime,dxm,dxp,dym,dyp,speed)

# Launch a new window 
window = Tk()
window.title('TRON')
# Create a new canvas of the size dictated by the server
canvas = Canvas(window,bg='black',height=he*sp,width=wi*sp)
canvas.pack(side=TOP)

# Create a "New Game" button
b=Button(window,text="New Game")
b.config(command=newgame())
b.pack()

# Add listener to Left and Right Arrow keys to allow the player to input directions
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
