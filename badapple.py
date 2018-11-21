

import pygame,sys,random
from collections import deque



# Note: some of the codes are not mine , code snippet from pygame user (susah) were used.

pygame.init()
size = 800,600
textcolor = 255,255,255
speed = -3
up = right = True 
down = left = False
screen = pygame.display.set_mode(size)
bg = pygame.image.load("file/bg.png")
bgrect = bg.get_rect()
pygame.key.set_repeat(65,65)

# sounds effects
sound = pygame.mixer.Sound("file/move.wav")
sound1 = pygame.mixer.Sound("file/crash.wav")
	
class Apple:
    	
    	def __init__(self,path):
        	self.img = pygame.image.load("file/apple.png")
        	self.rect = self.img.get_rect()

		if path == 1:
			self.rect = self.rect.move(731,196)
		elif path == 2:
			self.rect = self.rect.move(731,271)
		elif path == 3:
			self.rect = self.rect.move(731,356)
    	
	def left(self):
        	return self.rect.left
    	
	def right(self):
        	return self.rect.right
    	
	def top(self):
        	return self.rect.top
    	
	def bottom(self):
        	return self.rect.bottom
    	
	def move(self,x,y):
        	self.rect = self.rect.move(x,y)
    	
	def render(self):
        	screen.blit(self.img,self.rect)

	def get_rectangle(self):
		return self.rect


class Ant:
	def __init__(self):
		self.img = pygame.image.load("file/ant.png")
		self.rect = self.img.get_rect()
		self.rect = self.rect.move(30,270)
		self.path = 2
	
	def left(self):
		return self.rect.left
	
	def right(self):
		return self.rect.right
	
	def top(self):
		return self.rect.top
	
	def bottom(self):
		return self.rect.bottom
	
	
	def move(self,key):
	
		if key == up  and self.path == 1:
			
			self.path = 1
		
		elif key == up and self.path == 2:
			self.rect = self.rect.move(0,-75)
			self.path = 1
		
		elif key == up and self.path == 3:
			self.rect = self.rect.move(0,-85)
			self.path = 2
		
		elif key == down and self.path == 1:
			self.rect = self.rect.move(0,75)
			self.path = 2
		
		elif key == down and self.path == 2:
			self.rect = self.rect.move(0,85)
			self.path = 3
		
		elif key == down and self.path == 3:
			
			self.path = 3

	def render(self):
		screen.blit(self.img,self.rect)
	
	def shift(self, d):
		
		if d == right:
			if self.rect.right < 750:
				self.rect = self.rect.move(10,0)
		elif d == left:
			if self.rect.left > 20:
				self.rect = self.rect.move(-10,0)

	def get_path(self):
		return self.path

def re_play():
	gover = pygame.image.load("file/endgame.png")
	grect = gover.get_rect()

	#Play agai
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		screen.fill((75,200,44))
		screen.blit(gover,grect)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE]: break
		pygame.display.flip()
	begin()


# gameover 
def gameover(x,y):
	tempscreen = pygame.image.load("file/endgame.png")
	trect = tempscreen.get_rect()
	boom = pygame.image.load("file/rottenapple.png")
	brect = boom.get_rect()
	brect = brect.move(x,y)
	sound1.play()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		screen.blit(tempscreen,trect)
		screen.blit(boom,brect)
		
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE]:break
		pygame.display.flip()

	re_play()

#Begin
def begin():

	#queues of apples in different paths
	apple1 = deque()
	apple2 = deque()
	apple3 = deque()
	
	#your ant
	ant = Ant()

	score = 0
	timer = 32

	myfont = pygame.font.SysFont("monospace.ttf",40)	
	
	
	while 1:
        	for event in pygame.event.get():
            		if event.type == pygame.QUIT: sys.exit()
        
		screen.blit(bg,bgrect)

		#scoreboard
		if pygame.time.get_ticks()%200: score = score + 1
		scoreline = "SCORE: "+str(score)
		scoreboard = myfont.render(scoreline,1,textcolor)
		screen.blit(scoreboard,scoreboard.get_rect())
		 
		#apple AI
		
		if pygame.time.get_ticks() % (100*random.randint(2,6)) == 0:
			apple1.append(Apple(1))
		if pygame.time.get_ticks() % (100*random.randint(3,5)) == 0:
			apple2.append(Apple(2))
		if pygame.time.get_ticks() % (100*random.randint(1,5)) == 0:
			apple3.append(Apple(3))

        	#move and render apples in diff paths
		for apple in apple1:
            		apple.move(speed,0)
            		apple.render()
		for apple in apple2:
			apple.move(speed,0)
			apple.render()
		for apple in apple3:
			apple.move(speed-1,0)
			apple.render()
			
		moved = 0

		#User Input
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_UP:
					ant.move(up)
					sound.play()
			
				elif event.key == pygame.K_DOWN:
					ant.move(down)
					sound.play()
			
				
				elif event.key == pygame.K_RIGHT:
					ant.shift(right)
					sound.play()
			
	
				elif event.key == pygame.K_LEFT:
					ant.shift(left)
					sound.play()

		ant.render()

		#Collision Detection
		
		for apple in apple1:
			if ant.get_path()==1:
				if apple.left() < ant.left() < apple.right():
					pygame.image.save(screen,"file/gameover.jpeg")
					x = apple.get_rectangle()
					gameover(x[0],x[1])
					
				
				if apple.left() in range(ant.right()-2,ant.right()+2,1): 
					pygame.image.save(screen,"file/gameover.jpeg")
					x = apple.get_rectangle()
					gameover(x[0],x[1])
					
		
				if apple.right() == ant.left()+1:
					pygame.image.save(screen,"file/gameover.jpeg")
					x = apple.get_rectangle()
					gameover(x[0],x[1])
					
		
		for apple in apple2:
			if ant.get_path()==2:
		 		if apple.left() < ant.left() < apple.right():
					pygame.image.save(screen,"file/gameover.jpeg")
					x = apple.get_rectangle()
					gameover(x[0],x[1])
					

				if apple.left() in range(ant.right()-2,ant.right()+2,1):
                                	pygame.image.save(screen,"file/gameover.jpeg")
                                	x = apple.get_rectangle()
                                	gameover(x[0],x[1])
                                	

                        	if apple.right() == ant.left()+1:
                                	pygame.image.save(screen,"file/gameover.jpeg")
                                	x = apple.get_rectangle()
                                	gameover(x[0],x[1])
                                	
		
		for apple in apple3:
			if ant.get_path()==3:
		 		if apple.left() < ant.left() < apple.right():
					pygame.image.save(screen,"file/gameover.jpeg")
					x = apple.get_rectangle()
					gameover(x[0],x[1])
					

				if apple.left() in range(ant.right()-2,ant.right()+2,1):
                                	pygame.image.save(screen,"file/gameover.jpeg")
                                	x = apple.get_rectangle()
                                	gameover(x[0],x[1])
                                	

                        	if apple.right() == ant.left()+1:
                                	pygame.image.save(screen,"file/gameover.jpeg")
                                	x = apple.get_rectangle()
                                	gameover(x[0],x[1])

		#memory cleanup
		
		if apple1:
			if apple1[0].right() < 0: apple1.popleft()
		if apple2:
			if apple2[0].right() < 0: apple2.popleft()
		if apple3:
			if apple3[0].right() < 0: apple3.popleft()
	
		pygame.display.flip()

def main():

	#draw the start screen
	startscrn = pygame.image.load("file/startscreen.png")
	wrect = startscrn.get_rect()
	wrect = wrect.move(80,40)

	soundtrack = pygame.mixer.Sound('file/soundtrack.wav')
	soundtrack.set_volume(.1)
	soundtrack.play(-1)	
	

	#waiting for user to press enter
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		screen.fill((55,200,44))
 		screen.blit(startscrn,wrect)
		pressed = pygame.key.get_pressed()
		
		if pressed[pygame.K_s]: break
	
		pygame.display.flip()
	
	# Start Game
	begin()

if __name__ == "__main__":
	main()
