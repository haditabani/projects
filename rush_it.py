################## Rush It - in 2D ###############

########################WARNING##########################
# This Game was built in Codeskulptor.org for a Comp160 project.
# I scored an A in the class for this game. To play, paste
# code in www.codeskulptor.org and and press play.


# The Pitch Sheet can be found at:

## http://dl.dropbox.com/u/51611948/RushIt/PitchSheet.png

# The Controls:
## arrow Keys to move and Space to shoot

# Also you have a Mini Map that will have your current position on the map,
# And Finally you ARE driving a Bugatti Veyron... Damn Right Son.
# So please stay on the road and drive safely because the other guy is 
# only on a Koenigsegg CCR.

####### Keep In Mind #######
## The game gets harder as you play more.



## Also you finish the game by going to the start point, that is
## is the red line at the end.

## the faster cars have lesser health. kill them quick.

#### One piece of advice: do try game after lap 13:
#### insanely fun, you gotta have a strategy to win.


# Importing important stuff
import simplegui
import math
import random

# Setting the Width and the Height of the frame 
width = 600
height = 400
backGroundColor = "silver"

# Track of location of the camera
camera_offset = [0,0]

## Keep Track of the three high Scores:
HighScores= [["", 0], ["",0], ["",0]]
game_at = 0


# time that will be given for each race.
tot_time = 60

# Globals
TURN = 0
car_speed = 5
car_pos = [width / 2, height / 2]
car_mini_pos = [5,6]
score = 0
curr_text = 0
CoinsCollected = 0

# this is the follower car and i need to write an AI to build it better.
car2_pos = [width *4/5, height*2/3 -2 ]

# globals
go = False
left = False
right = False
started = False
AIStarted = False
showHow = False
showHigh = False

RecordHigh = []
velocity = [0,0] 

# Information Regarding images
car2_info = [450,318]
veyron_info = [150,83]
RACE_CAR_CENTER = [67.5, 82]
RACE_CAR_SIZE = [135, 164]
missile_info = [10,10]
splash_info = [600,400]
tree_info = [35,33]
missile_group = set()

# Importing all the images
backGround = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/backgorund.png")
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
race_car_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/Race-Car.png")
splash_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/Splash.png")
car2_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/Car2.png")
veyron_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/Veyron%20.png")
tree_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/Tree.png")
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
howToPlay_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/HowToPlay%20copy.png")
highscore_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/HighScore.png")
coin_image = simplegui.load_image("http://dl.dropbox.com/u/51611948/RushIt/Coin.png")


# Importing Sounds
start_sound = simplegui.load_sound("http://dl.dropbox.com/u/51611948/gmenstar.wav")
start_sound.set_volume(1)
driving_sound = simplegui.load_sound("http://dl.dropbox.com/u/51611948/gphorse.wav")
driving_sound.set_volume(.3)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
back_sound = simplegui.load_sound("http://dl.dropbox.com/u/51611948/RushIt/07%20Around%20The%20World.wav")
back_sound.set_volume(.3)

# Right now we only have one map and this is it.

myMap = [(0, 200), (158, 200), (1000, 200), (1277, 300), (1424, 600), (1700, 900), (2003, 1200), (2300, 1400), (2600, 1700), (2900, 2100), (3200, 2400), (3500, 2700), (3800, 3000), (4500, 3200),(4450,3700), (4200,4100), (3800,  4100), (3600,4500), (3300,4800), (3000,5100), (2500,5500), (2100, 5600), (1800,5650), (1200, 5100), (900, 4000), (700, 3000), (500, 2000),(300,1000), (100, 500), (-50 , 300), (0,200)]

####################----------Map Class-------------##################


# This is the map class that is needed to build and change the map every draw fram
# Notice how the map is moved and not the car.
class Map:
    
    def __init__(self, car_pos, car_speed, myMap):
        back_sound.play()
        global start_sound
        self.car_pos = car_pos
        self.speed = car_speed
        self.myMap = myMap
        self.unalteredMap = myMap
        self.miniMap = []
        self.road = []
        self.road2 = []
        start_sound.play()
       
        
        
        
#     This creates the miniMap on the top right corner    
    def create_mini_map(self):
        for i in range(len(self.myMap)):
            new = [0,0]
            new[0] = self.myMap[i][0]*50/4500 +540
            new[1] = self.myMap[i][1]*50/5600 +340
            self.miniMap.append(new)
            
    

        
        
            
            
    def make_road(self):
        ## first find angle of two points add 2pi calculate angle to vector to that and make a point there
        global Trees, tree_image, tree_info, RecordHigh
        for i in range(len(self.myMap)-1):
            y = self.myMap[i + 1][1] - self.myMap[i][1]
            x = self.myMap[i + 1][0] - self.myMap[i][0]
            angle = math.atan2(y,x) + math.pi/2
            angle2 = math.atan2(y,x) - math.pi/2
            self.road.append([self.myMap[i][0]+70*math.cos(angle) +10, self.myMap[i][1] + 70*math.sin(angle) +10] )
            self.road2.append([self.myMap[i][0]+70*math.cos(angle2) , self.myMap[i][1] + 70*math.sin(angle2)])
            Trees.add( Sprite([self.myMap[i][0]+100*math.cos(angle) +10, self.myMap[i][1] + 100*math.sin(angle) +10], [0,0], 0, 0, tree_image , tree_info))
            Coins.add(Sprite(self.myMap[i],[0,0], 0, 0 ,coin_image,[25,25]) )
            RecordHigh.append(False)
            
            
            
    # this makes the map mutable
    def set_map(self):
        myMapR = []
        for i in range(len(self.myMap)):
            new = [0,0]
            new[0] = self.myMap[i][0]
            new[1] = self.myMap[i][1]
            myMapR.append(new)
        self.myMap = myMapR
        
    def get_map(self):
        return self.myMap
    
    # updates the position of the map regarding the car    
    def update(self,car_pos):
        global go, TURN, camera_offset, car_speed
        self.speed = myCar.speed
        if go == True:
            if car_pos[0]> 200 + camera_offset[0]:
                camera_offset[0] += self.speed*math.cos(TURN)
            if car_pos[1]> 200 + camera_offset[1]:
                camera_offset[1] += self.speed*math.sin(TURN) 
            if car_pos[0]< 100 + camera_offset[0]:
                camera_offset[0] += self.speed*math.cos(TURN)
            if car_pos[1]< 100 + camera_offset[1]:
                camera_offset[1] += self.speed*math.sin(TURN)     
                
    def car_at(self):
        return self.car_pos
    
    def get_speed(self):
        return self.speed
      
    # Drawing the maps.    
    def draw(self, canvas): 
        tempmap = []
        tempRoad = []
        tempRoad2 = []
        for i in self.myMap:
            tempmap.append(list(i))
        for i in range(len(tempmap)):
            tempmap[i][0] -= camera_offset[0]
            tempmap[i][1] -= camera_offset[1]
        for j in self.road:
            tempRoad.append(list(j))
        for n in self.road2:
            tempRoad2.append(list(n))    
        for k in range(len(tempRoad)):
            tempRoad[k][0] -= camera_offset[0]
            tempRoad[k][1] -= camera_offset[1]
            tempRoad2[k][0] -= camera_offset[0]
            tempRoad2[k][1] -= camera_offset[1]
        
        canvas.draw_polyline(tempmap, 12,"Red")
        ## Drawing Road
        for l in range(len(self.myMap)-2):
            canvas.draw_polygon([tempmap[l], tempmap[l+1],tempRoad[l+1], tempRoad[l], tempmap[l] ], 6, "Black","Grey")
            canvas.draw_polygon([tempmap[l], tempmap[l+1],tempRoad2[l+1], tempRoad2[l], tempmap[l] ], 6, "Black","Grey")
            
        ## Drawing MiniMap
        canvas.draw_polygon([(530,335),(598,335),(598,398),(530,398)],3,"White")
        canvas.draw_polyline(self.miniMap,2, "aqua")

####################----------Player CAR CLASS-------------##################        

class Player:
    def __init__(self, pos, angle, speed, image, image_info,sound = None):
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.image = image
        self.info = image_info 
        self.car_at = 0
        self.win = False
        self.Now = True
        self.nit = False
        self.Once = True
        self.nitTime = 0
        
    def update(self):
        global CoinsCollected, num1, score, go, TURN, camera_offset, driving_sound,myMap,RecordHigh, started, computer_car, HighScores, game_at
        #print RecordHigh
        for n in range(len(RecordHigh)):
            dist_n = dist(self.pos,myMap[n])
            if dist_n <200:
                RecordHigh[n] = True    
        if tot_time < 57:
            dist1 = dist(self.pos, myMap[0])
            if len(computer_car)<= 1:
                if game_at > 1:
                    computer_car.add(AICar([140,200],5 + game_at*.2, myMap, car2_image ,car2_info))
        if tot_time < 50:
            if dist1 < 100:
               
                started = False
                self.win = True
                if self.Now == True:
                    score += 5*CoinsCollected +5*tot_time
                    sortHigh()
                    self.Now =False
                    
        if self.nitTime > 5:
            self.nit = False
            self.speed = 5
            self.nitTime = 0 
            
        self.angle =TURN
        if go == True:
            driving_sound.play()
            self.pos[0] += self.speed*math.cos(self.angle)
            self.pos[1] += self.speed*math.sin(self.angle)
        else:
            driving_sound.rewind()
    
    # Adding nitrous to help with higher levels.
    def Nitrous(self):
        global game_at
        if self.nit == True:
            if self.Once == True:
                self.speed = 9 + .2*game_at
                self.Once = False
            
        
    
    # deals with the action in the game
    def shoot(self):
        global missile_group, TURN
        vel = angle_to_vector(TURN)
        pos = [self.pos[0], self.pos[1]]
        pos[0] += vel[0] * 40
        pos[1] += vel[1] * 50
        vel[0] = self.speed*math.cos(self.angle) + (vel[0] *3)
        vel[1] = self.speed*math.sin(self.angle) + (vel[1] *3)
        
        missile_group.add(Sprite(pos, vel, TURN, 0, missile_image, missile_info, missile_sound))

    def get_position(self):
        return self.pos  
    
    def get_radius(self):
        return 40
    
    def draw(self, canvas):
        temppos = list(self.pos)
        temppos[0] -= camera_offset[0]
        temppos[1] -= camera_offset[1]
        canvas.draw_image(self.image, [self.info[0]/2, self.info[1]/2],self.info,[self.pos[0]*50/4500 + 540, self.pos[1]*50/5600 +340], [8,5] , self.angle )
        canvas.draw_image(self.image,[self.info[0]/2,self.info[1]/2], self.info, temppos, self.info, self.angle  )
          
        
        
####################----------AI CAR CLASS-------------##################
def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class AICar:
    
    def __init__(self, car_pos,speed, myMap, image,image_info):
        self.car_pos = car_pos
        self.myMap = myMap
        self.image = image
        self.info = image_info
        self.myTurn = 0
        self.car_at = 0
        self.speed = speed
        self.health= 30
        self.explosion = False
        self.explosion_time = 0
        
        
    def position_car(self, myMap):   
        global tot_time, score        
        if tot_time < 30:
            #print tot_time
            dist2 = dist(self.car_pos, self.myMap[0])
            #print dist2
            if dist2 < 5:
                score -= 100
        self.myTurn = math.atan2(self.myMap[self.car_at + 1][1] - self.myMap[self.car_at ][1], self.myMap[self.car_at + 1][0] - self.myMap[self.car_at][0])
        dist1 = dist(self.car_pos, self.myMap[self.car_at + 1])
        if AIStarted == True:
            if dist1 >6:
                self.car_pos[0] += self.speed*math.cos(self.myTurn)
                self.car_pos[1] += self.speed*math.sin(self.myTurn)      
            else:
                self.car_at += 1
                if self.car_at > len(self.myMap)-2:
                    self.car_at = 0
        if self.health < 1:
            self.explosion = True

            
    def get_position(self):
        return self.car_pos
    
    def get_radius(self):
        return 50
        
    def draw(self,canvas):
        global camera_offset, explosion_sound, explosion_image, tot_time, score        
        #print self.finished
        if self.explosion == True:
            explosion_sound.play()
            if self.explosion_time < 24:
                explosion_image_size = [128,128]
                explosion_image_center = [64,64]
                temppos1 = list(self.car_pos)
                temppos1[0] -= camera_offset[0]
                temppos1[1] -= camera_offset[1]
                
                canvas.draw_image(explosion_image, [explosion_image_center[0] + explosion_image_size[0]*self.explosion_time, explosion_image_center[1]], explosion_image_size, temppos1, [120,90] , self.myTurn)
                self.explosion_time += 1 
            elif self.explosion_time == 24:
                explosion_sound.pause()
        else:
            temppos = list(self.car_pos)
            temppos[0] -= camera_offset[0]
            temppos[1] -= camera_offset[1]
            canvas.draw_image(self.image, [self.info[0]/2, self.info[1]/2],self.info, [self.car_pos[0]*50/4500 + 540, self.car_pos[1]*50/5600 +340], [8,6], self.myTurn )
            canvas.draw_image(self.image, [self.info[0]/2, self.info[1]/2],self.info, temppos, [120,90], self.myTurn )
       
####################----------Sprite Class-------------##################


# This sprite is taken from the asteroids game and basically helps with the missiles        
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = vel
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = [info[0]/2, info[1]/2]
        self.image_size = info
        self.radius = 3
        self.lifespan = 50
        self.animated = False
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
   
    def draw(self, canvas):
        global camera_offset
        temppos = list(self.pos)
        temppos[0] -= camera_offset[0]
        temppos[1] -= camera_offset[1]
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          temppos, self.image_size, self.angle)
    
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        self.age += .5
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) 
        self.pos[1] = (self.pos[1] + self.vel[1])
        if self.age >= self.lifespan:
            return False
        else:
            return True
    
    def explosion(self):
        self.age = 0
        self.vel = [0, 0]
        self.angle_vel = 0
        self.lifespan = explosion_info.get_lifespan()
        self.image = explosion_image
        self.animated = True
        self.image_size = [128, 128]
        self.image_center = [64, 64]
        explosion_sound.rewind()
        explosion_sound.play()
   
    def collide(self,another_sprite):
        dist1 = dist(self.pos,another_sprite.get_position())
        dist1  = dist1 - (self.radius + another_sprite.get_radius())
        if dist1 < 0:
            return True
        else:
            return False
 
############################      Initializing Objects    #######################################        
# Create the new Object map, make it mutable and then create the mini map
myNewMap = Map(car_pos,car_speed,myMap)        
myNewMap.set_map()
myNewMap.create_mini_map()
Trees = set()
Coins = set()
myNewMap.make_road()

myCar = Player(car_pos, TURN, car_speed, veyron_image, veyron_info)

computer_car = set()





####################----------Draw Handler-------------##################


# Handler to draw on canvas
def draw(canvas):
    global CoinsCollected,ScoreColour,score , TURN, car2_info, car_pos,car_angle,velocity,go, left,right, car_speed, started, car_mini_pos, AIStarted, Trees
    canvas.draw_image(backGround, [300,200],[600,400],[300,200],[600,400])
    if go ==True:
        if left ==True:
            TURN -= .03
        if right == True:
            TURN += .03
    #    if go == True:
#       car_mini_pos[0] = (car_mini_pos[0] + math.cos(TURN)/18)
#       car_mini_pos[1] = (car_mini_pos[1] + math.sin(TURN)/20)
    myNewMap.update(myCar.get_position())
    myNewMap.draw(canvas)
    for j in computer_car:
        j.position_car(myNewMap.get_map())
        j.draw(canvas)
    for l in Trees:
        l.draw(canvas)
    for n in Coins:
        n.draw(canvas)
    myCar.update()
    myCar.draw(canvas)
    
    
    ScoreColour = ""
    if tot_time >30:
        ScoreColour = "White"
    elif tot_time >10:
        ScoreColour = "Yellow"
    elif tot_time > -2:
        ScoreColour = "Red" 
    canvas.draw_text("Time Remaining: " + str(tot_time), [5, 20], 15, ScoreColour ) 
    canvas.draw_text("Score: " + str(score), [450,20] ,15, "White" )
    canvas.draw_text("Coins: " + str(CoinsCollected), [250,20] ,15, "White" )
    if started == True:
        if tot_time < 10:
            canvas.draw_text("You Gotta Hurry Buddy", [100,70],15,"Red")    
    
    if tot_time <0:
        started = False
        AIStarted = False
        score = 0
    if started == False:
        canvas.draw_image(splash_image, [300,200],[600,400], [300,200], [600,400])
    if showHow ==True:
        canvas.draw_image(howToPlay_image, [300,200],[600,400], [300,200], [600,400])
    if showHigh == True:
        canvas.draw_image(highscore_image, [300,200],[600,400], [300,200], [600,400])	
        for i in range(len(HighScores)):
            canvas.draw_text(str(HighScores[i]), [250  ,250+i*30], 20,"Silver")
    for m in Coins:
        if m.collide(myCar):
            CoinsCollected += 1
            Coins.remove(m)
            break
    
    for i in missile_group:
        if i.update() == True:
            i.update()
            i.draw(canvas)
        else:
            missile_group.remove(i)
        for j in computer_car:
            if i.collide(j) == True:
                j.health -= 4
                missile_group.remove(i)
                score +=1
                break
        for e in computer_car:	
            if e.explosion_time > 22:
                computer_car.remove(e)
                break
    if myCar.win and (not showHigh) and (not showHow):
        canvas.draw_text("You win, press Start or Check HighScore", [100 ,170], 20,"Red")
    ## Tutorial    
    if started == True:        
        if game_at == 1:
            if tot_time >56:
               canvas.draw_text("UpKey to accelarate...", [250,100],15,"Red")
               canvas.draw_text("Finish Lap within 60 Seconds to get a HighScore.",[200,130],15,"red")
            elif tot_time > 52:
               canvas.draw_text("Car can only turn when accelerating..", [250,100],15,"Red")
            elif tot_time > 45:
               canvas.draw_text("Enjoy it while its easy.. gear up!", [250,100],15,"Red")
            elif tot_time > 40:
               canvas.draw_text("Keep shooting the car with spacebar for points..", [210,100],15,"Red")
               canvas.draw_text("These guys will get faster and tougher", [250,130],15,"Red")
            elif tot_time > 30:
               canvas.draw_text("Score in the end will be 5*CoinsCollected", [250,100],15,"Red")
               canvas.draw_text("plus 5*remaining time and the score " , [250,130],15,"Red")
               canvas.draw_text("you gained from killing cars.", [250,160],15,"Red") 
            elif tot_time > 25:
               canvas.draw_text("Collect Coins to increase score...", [250,100],15,"Red")
            elif tot_time >15:
               canvas.draw_text("Press n for nitrous,", [250,100],15,"Red")
               canvas.draw_text("it lasts only for 5 seconds so choose wisely...", [230,130],15,"Red")
            elif tot_time > 0:
               canvas.draw_text("Get to the Red line to win.", [250,100],15,"Red")
               canvas.draw_text("Score gets a -200 if a computer car", [250,130],15,"Red")
               canvas.draw_text("beats you to the finish .." , [250,160],15,"Red")
    
        my_comp_car = []
        for f in computer_car:
            my_comp_car.append(f)
        for w in range(len(my_comp_car)):
            if my_comp_car[w].health > 0:
                CarColour = "Red"
                if my_comp_car[w].health > 10:
                    CarColour = "Green"
                if my_comp_car[w].speed == 5:
                    canvas.draw_text("car" + str(w+1)  +": ", [450,50 +w*20],15 ,"White")
                    canvas.draw_line([490,45 + w*20], [490 + my_comp_car[w].health*100/ (30 +10*game_at), 45 +w*20], 8, CarColour)
                else:
                    canvas.draw_text("car" + str(w+1)  +": ", [450,50 +w*20],15 ,"White")
                    canvas.draw_line([490,45 + w*20], [490 + my_comp_car[w].health*100/ 30, 45 +w*20], 8, CarColour)
  
        
     

####################----------Game Logic-------------##################            
# gets the angle of the given vector            
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


# key handlers     
def keydown(key):
    global go,left,right, started, myCar
    if key == simplegui.KEY_MAP["up"]:
        if started == True:
            go = True
    if key == simplegui.KEY_MAP["left"]:
        left = True
    if key == simplegui.KEY_MAP["right"]:
        right = True
    if key == simplegui.KEY_MAP["space"]:
        if started == True:
            myCar.shoot()
    if key == simplegui.KEY_MAP["n"]:
        if started == True:
            myCar.nit = True
            myCar.Nitrous()
            
     

def keyup(key):
    global go,left,right
    if key == simplegui.KEY_MAP["up"]:
        go = False
    if key == simplegui.KEY_MAP["left"]:
        left = False
    if key == simplegui.KEY_MAP["right"]:
        right = False

        
        
write = False

def sortHigh():
    global HighScores, game_at, score, started, curr_text, write, RecordHigh
    #print HighScores
    #print RecordHigh 
    Now = True
    for i in RecordHigh:
        if i == False:
            Now=False
            write = False
    if Now ==True:	        
        if score > HighScores[0][1]:
            write =True
            HighScores[2] = list(HighScores[1])
            HighScores[1] = list(HighScores[0])
            HighScores[0][1] = score
            HighScores[0][0] = ""
            curr_text = 0
            score = 0
        elif score > HighScores[1][1]:
            write =True
            HighScores[2] = list(HighScores[1])
            HighScores[1][1] = score
            HighScores[1][0] = ""
            curr_text = 1
            score = 0
        elif score > HighScores[2][1]:
            write =True
            HighScores[2][1] = score
            curr_text = 2
            score = 0
        else:
            write =False
            score = 0
        
                
        
def HighScoreInput(text):
    global HighScores,game_at, curr_text, write
    if write != False:
        HighScores[curr_text][0] = text
    
def buttonPause():
    global AIStarted , started
    AIStarted = False
    started = False
    
def buttonPlay():
    global AIStarted , started
    AIStarted = True
    started = True

    
## Start frame here, because need to change label.    
frame = simplegui.create_frame("RushIt", width, height)
label = frame.add_label("You are on Lap " + str(game_at))

#To start the game        
def click(pos):
    global CoinsColleced, Coins, score,camera_offset, Now, write, game_at, started, splash_info, tot_time, AIStarted,showHow, showHigh, TURN, RecordHigh, Coins, myMap
    center = [width / 2, height / 2]
    inheight = (center[1] - splash_info[1] / 2) < pos[1] < (center[1] + splash_info[1] / 2)
    inwidth = (center[0] - splash_info[0] / 2) < pos[0] < (center[0] + splash_info[0] / 2)
    back = [500,360]
    if showHow == True:
        if pos[0] > back[0] and pos[1]> back[1]:
            showHow = False
    if showHigh == True:
        if pos[0] > back[0] and pos[1]> back[1]:
            showHigh = False
    startpos1 = [200,200]
    startpos2 = [300,245]
    startTrue = startpos1[0] < pos[1] and  pos[0]> startpos1[0] and  startpos2[1]>pos[1]> startpos1[1]
    HowtoPlay1 = [130,250]
    HowtoPlay2 = [470,310]
    HowtoPlayTrue = HowtoPlay1[0] < pos[0] < HowtoPlay2[0] and  HowtoPlay2[1]> pos[1] > HowtoPlay1[1]
    high1 = [170,315]
    high2 = [430,370]
    highTrue = high1[0] < pos[0] < high2[0] and  high2[1]> pos[1] > high1[1]
    if highTrue and (not showHigh) and (not showHow):
        showHigh = True
    if HowtoPlayTrue and (not showHigh) and (not showHow):
        showHow = True
        
    if (not started) and inwidth and inheight:
        if (not showHigh) and (not showHow) and startTrue:
            if game_at > 0:
                Coins =set()
                #print Coins
                for i in range(len(myMap)-1):
                    Coins.add(Sprite(myMap[i],[0,0], 0, 0 ,coin_image,[25,25]) )
                    RecordHigh[i] = False
                #print Coins
            Now = True
            write = False
            score = 0
            CoinsCollected = 0
            game_at += 1
            label.set_text("You are on Lap " + str(game_at))
            myCar.win = False
            myCar.Now = True
            myCar.Once =True
            started = True
            AIStarted = True
            tot_time = 60 
            myCar.pos = [200,200]
            camera_offset = [0,0]
            myCar.angle = 0 
            TURN = 0
            for i in computer_car:	
                computer_car.remove(i)
            if game_at <3:    
                computer_car.add(AICar([0,200], 4 ,  myMap, car2_image ,car2_info))
            else:
                computer_car.add(AICar([0,200], 5 ,  myMap, car2_image ,car2_info))
            for q in computer_car:
                q.finished = False
                if game_at > 0:
                    q.health += 10*game_at
                
                
def level(text):
    global game_at, started
    if started == False:
        game_at = int(text)
               
# To time the Game
def timer():
    global tot_time
    if myCar.nit == True:
        myCar.nitTime += 1
    if started == True:
       tot_time-=1

# Create a frame and assign callbacks to event handlers

frame.set_canvas_background(backGroundColor)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.add_input("Enter Name and press Enter", HighScoreInput, 100)
frame.add_input("Level Select", level, 100)
frame.add_button("Pause Game" , buttonPause, 100)
frame.add_button("Play", buttonPlay, 100 )

    


frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, timer)
# Start the frame animation and timer
frame.start()
timer.start()
