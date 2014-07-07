# H1.py
# Author: Paul Talaga
# Programmer: Aarthi Raghavendra
# Co-Worker: Abhyudaya Upadhyay
# This file demonstrates how to implement various kinds of Roomba robot agents
# and run them in GUI or non-gui mode using the roomba_sim library.
#

from roomba_sim import *
from roomba_concurrent import *
from queue import PriorityQueue

# Each robot below should be a subclass of ContinuousRobot, RealisticRobot, or DiscreteRobot.
# All robots need to implement the runRobot(self) member function, as this is where
# you will define that specific robot's characteristics.

# All robots perceive their environment through self.percepts (a class variable) and 
# act on it through self.action.  The specific percepts received and actions allowed
# are specific to the superclass.  See roomba_sim for details.

# TunedRobot - Robot that acceps a chromosome parameter and can store limited state
#               (a single number).  Continuous and dynamic environment.
      
      

# the chromosome will contains the course of actions which it performs 
# chromosome = String 
# string will contain - Hurdle-right, degree to turn -82,88,108, 157, which keep on changing on every hurdle, with addition of 0.5
# on dirt perform a suck opration 
# on no - bump and no- dirt - move forward  
# HRt82t88t108t157|DS|Forward
#

# Stupid Robot
class TunedRobot1(RealisticRobot):
  """ The ReflexRobotState robot is similar to the ReflexRobot, but some
    state is allowed in the form of a number.
  """
  def __init__(self,room,speed, start_location = -1, chromosome = None):
    super(TunedRobot1, self).__init__(room,speed, start_location)
    # Set initial state here you may only store a single number.
    self.state = 0
    # Save chromosome value
    self.degrees = 0 # choromosome value is coming as null and its causing problems
      
    
  def runRobot(self):
    (bstate, dirt) = self.percepts
    if(bstate == 'Bump'):
      self.action = ('TurnRight',135 + self.degrees)
    elif(dirt == 'Dirty'):
      self.action = ('Suck',None)
    else:
      self.action = ('Forward',None)


class TunedRobot(RealisticRobot):
  """ The ReflexRobotState robot is similar to the ReflexRobot, but some
    state is allowed in the form of a number.
  """
  def __init__(self,room,speed, start_location = -1, chromosome = None):
    super(TunedRobot, self).__init__(room,speed, start_location)
    # Set initial state here you may only store a single number.
    self.state = 0
    # Save chromosome value
    #print("chromo = ", chromosome)
    self.degrees = chromosome
    #print("degrees = ", self.degrees)
      
    
  def runRobot(self):
    degree = 0
    deg = parseChromosome(self.degrees)
    if(self.state%4 ==0):
      degree = deg[0]
    elif(self.state%4 ==1):
      degree = deg[1]
    elif(self.state%4 ==2):
      degree = deg[2]
    elif(self.state%4 ==3):
      degree = deg[3]
    self.state += 1
    
    (bstate, dirt) = self.percepts
    if(bstate == 'Bump'):
      self.action = ('TurnRight',degree )
    elif(dirt == 'Dirty'):
      self.action = ('Suck',None)
    else:
      self.action = ('Forward',None)


def getOldChromosome(rooms, start_location, min_clean):

    rooms = rooms
    wallcount = calculatewalls(rooms)
    print(wallcount ,'wall count')

    
    if(wallcount == 0):
      return 'HRt82t86t132t157|D|F'
    elif (wallcount > 20):
      return  'HRt84t88t102t117|D|F'
    elif(wallcount >50):
      return 'HRt81t76t142t127|D|F'
    else :
      return 'HRt82t86t132t157|D|F'
    
def getChromosome(rooms, start_location, min_clean):

        
  ###New function

    priority = PriorityQueue()
    #old chromo  HRt84t88t102t117|D|F
    first = 81
    second = 84
    third = 106
    fourth = 121

    for k in range(10):
      testIt = makechromosome(first + k, second + k, third -k, fourth -k)
      priority.put(  (resultValue(rooms, testIt, minclean = 0.20), testIt)  )
    chromosomerecent = priority.get()[1]
    print("transferreing chromomsmme ", chromosomerecent)
    return chromosomerecent

def calculatewalls(rooms):
  countwalls = 0
  for i in range(len(rooms)):
    wallsnumber = len(getWallsValue(rooms[i]))
    countwalls = countwalls + wallsnumber
  print('Number of walls ',countwalls)  
  return countwalls 
                                                                                                                      


def getWallsValue(room):
      #width = self.getRoomWidth();
      #height =  self.getRoomHeight();
      #dirtyList =  self.getDirty()
      #wallList = rooms[1].getWalls()
      insidewall = []
      countnumberofWalls = 0 
      width = room.getWidth()
      height = room.getHeight()       
      walllist = room.getWalls()
      #for k in range(len(walllist)):
      while(len(walllist)>0):
          #print(walllist[k])
          (x,y) = walllist.pop()
          if(not(x == width or  x == -1 or y == -1  or y == height)):
               insidewall.append((x,y))

      return insidewall
         #countnumberofWalls = countnumberofWalls+ len(rooms[i].getWalls());



def testAllMaps2(robot, rooms, numtrials = 10, minclean = 0.95, start_location = -1, chromosome = None):
  """ Runs the specified robot over the list of rooms, optionally with a specified
  number of trials per map, and starting location (x,y).
  Prints status to the screen and returns the average performance over all maps and 
  trials."""
  score = 0
  for room in rooms:
    runscore, runstd = runSimulation(num_robots = 1,
                    speed = 1,
                    min_clean = minclean,
                    num_trials = numtrials,
                    room = room,
                    robot_type = robot,
                    start_location = start_location,
                    #debug = True,
                    chromosome = chromosome,
                    ui_enable = False)
    score += runscore
    #print("Room %d of %d done (score: %d std: %d)" % (rooms.index(room)+1, len(rooms), runscore, runstd))
  #print("Average score over %d trials: %d" % (numtrials * len(rooms), score / len(rooms)))
  return score / len(rooms)



#Results value for a chromosome
'''
def resultValue(robot,rooms,chromosome):
   #robot = TunedRobot
   startLoc = (5,5)
   minclean = 0.2
   numtrials = 20
   chromosome = getChromosome(rooms, startLoc, minclean)
   result =testAllMaps(TunedRobot, rooms, numtrials, minclean, chromosome )

   testAllMaps(TunedRobot, rooms, numtrials = 20, minclean = minClean, chromosome = getChromosome(rooms, startLoc, minClean)))
   print(result)
   return result
'''

def makechromosome(first,second,third,fourth):
    firstdegree = str(first)
    seconddegree = str(second)
    thirddegree = str(third)
    fourthdegree = str(fourth)
    
    s = 'HR'+'t'+firstdegree+'t'+seconddegree+'t'+thirddegree+'t'+ fourthdegree + '|D|F'
    #print ("make chromo -- ", s)
    return s

def resultValue(rooms, chromosome, numtrials = 3, minclean = 0.20, startLoc = (5,5) ):
   result = testAllMaps2(TunedRobot, rooms, numtrials, minclean, start_location = startLoc ,chromosome = chromosome)
   return result
#result =testAllMaps(TunedRobot, rooms, numtrials = 20, minclean = minClean, chromosome = getChromosome(rooms, startLoc, minClean))
  

   
#parse chromosome
def parseChromosome(s):
    #s= 'HRt82t86t132t157|D|F'
    #s= 'HRt84t84t82t87|D|F'
    a = s.split('|')
    degree = a[0].split('t') 
    #print(a)
    #print(degree)
    first = int(degree[1])
    second = int(degree[2])
    third = int(degree[3])
    fourth = int(degree[4])  
    return(first,second,third,fourth)



    
     



############################################
## A few room configurations

allRooms = []

smallEmptyRoom = RectangularRoom(10,10)
allRooms.append(smallEmptyRoom)  # [0]

largeEmptyRoom = RectangularRoom(10,10)
allRooms.append(largeEmptyRoom) # [1]

mediumWalls1Room = RectangularRoom(30,30)
mediumWalls1Room.setWall((5,5), (25,25))
allRooms.append(mediumWalls1Room) # [2]

mediumWalls2Room = RectangularRoom(30,30)
mediumWalls2Room.setWall((5,25), (25,25))
mediumWalls2Room.setWall((5,5), (25,5))
allRooms.append(mediumWalls2Room) # [3]

mediumWalls3Room = RectangularRoom(30,30)
mediumWalls3Room.setWall((5,5), (25,25))
mediumWalls3Room.setWall((5,15), (15,25))
mediumWalls3Room.setWall((15,5), (25,15))
allRooms.append(mediumWalls3Room) # [4]

mediumWalls4Room = RectangularRoom(30,30)
mediumWalls4Room.setWall((7,5), (26,5))
mediumWalls4Room.setWall((26,5), (26,25))
mediumWalls4Room.setWall((26,25), (7,25))
allRooms.append(mediumWalls4Room) # [5]

mediumWalls5Room = RectangularRoom(30,30)
mediumWalls5Room.setWall((7,5), (26,5))
mediumWalls5Room.setWall((26,5), (26,25))
mediumWalls5Room.setWall((26,25), (7,25))
mediumWalls5Room.setWall((7,5), (7,22))
allRooms.append(mediumWalls5Room) # [6]

#############################################    
def TunedTest1():
  print(runSimulation(num_robots = 1,
                    min_clean = 0.95,
                    num_trials = 1,
                    room = allRooms[6],
                    robot_type = TunedRobot1,
                    #ui_enable = True,
                    ui_delay = 0.1,
                    chromosome = getChromosome(rooms, startLoc, minClean)))
                    
def TunedTest2():
  print(runSimulation(num_robots = 1,
                    min_clean = 0.95,
                    num_trials = 1,
                    room = allRooms[6],
                    robot_type = TunedRobot,
                    #ui_enable = True,
                    ui_delay = 0.1,
                    chromosome = 2))                  



if __name__ == "__main__":
  # This is an example of how we will test your program.  Our rooms will not be those listed above, but similar.
  #rooms = [allRooms[1]]
  #rooms = [allRooms[1], allRooms[5]]
  rooms = allRooms

  startLoc = (5,5)

  minClean = 0.20

  #chromosome = getChromosome(rooms, startLoc, minClean)

  #print('some chromosome ',chromosome)

  # testAllMaps

 

  # Concurrent test execution.
  
  print("***********************")

  print("And Stupid  robot")

  print("***********************")

  #print(concurrent_test(TunedRobot1, rooms, num_trials = 20, min_clean = minClean, chromosome = chromosome))

  print(testAllMaps(TunedRobot1, rooms, numtrials = 20, minclean = minClean, chromosome = 'chromosome'))

  print("***********************")

  print("And now your robot")

  print("***********************")

  #print(concurrent_test(TunedRobot, rooms, num_trials = 20, min_clean = minClean, chromosome = chromosome))

  print(testAllMaps(TunedRobot, rooms, numtrials = 20, minclean = minClean, chromosome = getChromosome(rooms, startLoc, minClean)))
  #print('Test map results ' + testAllMaps(TunedRobot, rooms, numtrials = 20, minclean = minClean, chromosome = getChromosome(rooms, startLoc, minClean)))
  #print('before the result function',chromosome)
  #print ("old chromo ", getOldChromosome(rooms, startLoc, minClean))
  #result =testAllMaps(TunedRobot, rooms, numtrials = 20, minclean = minClean, chromosome = getOldChromosome(rooms, startLoc, minClean))
#  res = resultValue(rooms,chromosome=getChromosome(rooms, startLoc, minClean))
  #print(result)
#  print(res)

  # This code will be run if this file is called on its own
  #TunedTest1()
  
  #TunedTest2()
  
  # This is an example of how we will test your program.  Our rooms will not be those listed above, but similar.
  #rooms = [allRooms[1], allRooms[5]]
  #startLoc = (5,5)
  #minClean = 0.2
  #chromosome = getChromsome(rooms, startLoc, minClean)
  
  # Concurrent test execution.
  #print(concurrent_test(TunedRobot, rooms, num_trials = 20, min_clean = minClean, chromosome = chromosome))


