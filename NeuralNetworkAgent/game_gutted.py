import mysql.connector
import names
import json
import secrets
import numpy as np
import random
import socket			
import time

'''
THE GOAL FOR AGENT IS TO TRY GET MAXIMUM XP AND CREDITS POSSIBLE WITHIN THE ALLOCATED LIFETIME OF 1000 HOURS
'''

Agent_Input_Map = {
    '"forward"':0,
    '"backward"':0,
    '"left"':0,
    '"right"':0,
    '"forward_left"':0,
    '"forward_right"':0,
    '"backward_left"':0,
    '"backward_right"':0
}

Agent_Input_List = [0,0,0,0,0,0,0,0,0]

s = socket.socket()		
print ("Socket successfully created")



# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 8052		

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

# a forever loop until we interrupt it or
# an error occurs

# Establish connection with client.
c, addr = s.accept()

# the interface is basically functions called that interact with the game and simulate events such as explore
class RedBoiAI():
    def __init__(self):
        Agent_Input_Map['"forward"']=0
        Agent_Input_Map['"backward"']=0
        Agent_Input_Map['"left"']=0
        Agent_Input_Map['"right"']=0
        Agent_Input_Map['"forward_left"']=0
        Agent_Input_Map['"forward_right"']=0
        Agent_Input_Map['"backward_left"']=0
        Agent_Input_Map['"backward_right"']=0

        Agent_Input_List[0] = 0 # forward
        Agent_Input_List[1] = 0 # backward
        Agent_Input_List[2] = 0 # left
        Agent_Input_List[3] = 0 # right
        Agent_Input_List[4] = 0 # forward left
        Agent_Input_List[5] = 0 # forward right
        Agent_Input_List[6] = 0 # backward left
        Agent_Input_List[7] = 0 # backward right
        Agent_Input_List[8] = 0 # reset player

        self.game_over_next_turn = False

        # is stands for is there ground
        self.gr1 = 0
        self.gr2 = 0
        self.gr3 = 0
        self.gr4 = 0
        self.gr5 = 0
        self.gr6 = 0
        self.gr7 = 0
        self.gr8 = 0

        # now define directional data for the goal
        self.gd1 = 0
        self.gd2 = 0
        self.gd3 = 0
        self.gd4 = 0
        self.gd5 = 0
        self.gd6 = 0
        self.gd7 = 0
        self.gd8 = 0
        self.gd9 = 0
        self.gd10 = 0
        self.gd11 = 0
        self.gd12 = 0
        self.gd13 = 0
        self.gd14 = 0
        self.gd15 = 0
        self.gd16 = 0
        self.gd17 = 0
        self.gd18 = 0
        self.gd19 = 0
        self.gd20 = 0
        self.gd21 = 0
        self.gd22 = 0
        self.gd23 = 0
        self.gd24 = 0
        self.gd25 = 0
        self.gd26 = 0
        self.gd27 = 0
        self.gd28 = 0
        self.gd29 = 0
        self.gd30 = 0
        self.gd31 = 0
        self.gd32 = 0
        self.gd33 = 0
        self.gd34 = 0
        self.gd35 = 0
        self.gd36 = 0
        self.gd37 = 0
        self.gd38 = 0
        self.gd39 = 0
        self.gd40 = 0
        self.gd41 = 0
        self.gd42 = 0
        self.gd43 = 0
        self.gd44 = 0
        self.gd45 = 0

        # additional checks to reset the simulation
        self.reset_game = 0
        self.is_closer_to_goal = 0
        self.distanse = 1000
        self.initial_distance_from_goal = 21
        self.last_data = {}

        # imported from the last model
        self._hours_spent = 0
        self._score = 0
        self.number_of_games = 0
        self.reward = 0
        self.tick = 0
        self._simulation_duration = 40

        self.temp_clamped_distance = 21

    def reset(self, new_sim_duration):  # creates new player for new iteration
        # tracked game tick, idk why we use this but i guess its for like "how many moves it made" or whatever
        Agent_Input_Map['"forward"']=0
        Agent_Input_Map['"backward"']=0
        Agent_Input_Map['"left"']=0
        Agent_Input_Map['"right"']=0
        Agent_Input_Map['"forward_left"']=0
        Agent_Input_Map['"forward_right"']=0
        Agent_Input_Map['"backward_left"']=0
        Agent_Input_Map['"backward_right"']=0

        Agent_Input_List[0] = 0 # forward
        Agent_Input_List[1] = 0 # backward
        Agent_Input_List[2] = 0 # left
        Agent_Input_List[3] = 0 # right
        Agent_Input_List[4] = 0 # forward left
        Agent_Input_List[5] = 0 # forward right
        Agent_Input_List[6] = 0 # backward left
        Agent_Input_List[7] = 0 # backward right
        Agent_Input_List[8] = 0 # reset player

        self.game_over_next_turn = False

        # is stands for is there ground
        self.gr1 = 0
        self.gr2 = 0
        self.gr3 = 0
        self.gr4 = 0
        self.gr5 = 0
        self.gr6 = 0
        self.gr7 = 0
        self.gr8 = 0

        # now define directional data for the goal
        self.gd1 = 0
        self.gd2 = 0
        self.gd3 = 0
        self.gd4 = 0
        self.gd5 = 0
        self.gd6 = 0
        self.gd7 = 0
        self.gd8 = 0
        self.gd9 = 0
        self.gd10 = 0
        self.gd11 = 0
        self.gd12 = 0
        self.gd13 = 0
        self.gd14 = 0
        self.gd15 = 0
        self.gd16 = 0
        self.gd17 = 0
        self.gd18 = 0
        self.gd19 = 0
        self.gd20 = 0
        self.gd21 = 0
        self.gd22 = 0
        self.gd23 = 0
        self.gd24 = 0
        self.gd25 = 0
        self.gd26 = 0
        self.gd27 = 0
        self.gd28 = 0
        self.gd29 = 0
        self.gd30 = 0
        self.gd31 = 0
        self.gd32 = 0
        self.gd33 = 0
        self.gd34 = 0
        self.gd35 = 0
        self.gd36 = 0
        self.gd37 = 0
        self.gd38 = 0
        self.gd39 = 0
        self.gd40 = 0
        self.gd41 = 0
        self.gd42 = 0
        self.gd43 = 0
        self.gd44 = 0
        self.gd45 = 0

        # additional checks to reset the simulation
        self.reset_game = 0
        self.is_closer_to_goal = 0
        self.distanse = 1000
        
        self.initial_distance_from_goal = abs(int(self.last_data['init_goal']))

        # imported from the last model
        self._hours_spent = 0
        self._score = 0
        self.number_of_games = 0
        self.reward = 0
        self.tick = 0
        self._simulation_duration = 40

    def check_game_over(self):
        if self.tick > 40000:
            return True
        return False

    def move_forward(self):
        print("forward")
        
        Agent_Input_Map['"forward"']=1
        Agent_Input_List[0] = 1 # forward
        self.reward = 1


    def move_backwards(self):
        print("backward")
        Agent_Input_Map['"backward"']=1
        Agent_Input_List[1] = 1 # backward
        self.reward = 1


    def move_left(self):
        print("left")
        Agent_Input_Map['"left"']=1
        Agent_Input_List[2] = 1 # left
        self.reward = 1


    def move_right(self):
        print("right")
        Agent_Input_Map['"right"']=1
        Agent_Input_List[3] = 1 # right
        self.reward = 1
    
    def move_forward_left(self):
        print("forward left")
        
        Agent_Input_Map['"forward_left"']=1
        Agent_Input_List[4] = 1 # forward
        self.reward = 1
    
    def move_forward_right(self):
        print("forward right")
        
        Agent_Input_Map['"forward_right"']=1
        Agent_Input_List[5] = 1 # forward
        self.reward = 1

    def move_backward_left(self):
        print("backward left")
        
        Agent_Input_Map['"backward_left"']=1
        Agent_Input_List[6] = 1 # forward
        self.reward = 1

    def move_backward_right(self):
        print("backward right")
        
        Agent_Input_Map['"backward_right"']=1
        Agent_Input_List[7] = 1 # forward
        self.reward = 1
    

    def play_step(self, action):
        
        # a move was made, increase the tick
        self.tick += 1

        self._hours_spent +=1

        # Here we reset the moves list
        Agent_Input_List[0] = 0
        Agent_Input_List[1] = 0
        Agent_Input_List[2] = 0
        Agent_Input_List[3] = 0
        Agent_Input_List[4] = 0
        Agent_Input_List[5] = 0
        Agent_Input_List[6] = 0
        Agent_Input_List[7] = 0
        # make a play
        self.move(action)


        # wait 1 second
        #time.sleep(0.5)

        '''
        HERE we send the command to unity to make a move
        
        then we get the ouput and update the init variables to reflect it
        
        '''
        # convert the movement action to a dict
        data_package = str(Agent_Input_List)

        # debug send the instructions list
        #print("Instructions sent :",data_package)

        # Decide on a move and then send the instructions to the agent in unity
        c.send(data_package.encode())
        #time.sleep(0.5)

        # print what we receive from unity
        damn = c.recv(1024).decode()
        #print(damn)
        damn = damn.replace("'",'"')

        damn = damn.replace("{",'{"')
        damn = damn.replace(" : ",'" : "')
        damn = damn.replace(", ",'","')
        damn = damn.replace("}",'"}')
        #print(damn)
        damn = json.loads(damn)

        self.last_data = damn
        #print(damn)
        #print(damn["gd0"])

        # here we go through the laborious process of setting akk the results to their self values
        # goal direction checks
        self.gd1 = int(damn["gd0"])
        self.gd2 = int(damn["gd1"])
        self.gd3 = int(damn["gd2"])
        self.gd4 = int(damn["gd3"])
        self.gd5 = int(damn['gd4'])
        self.gd6 = int(damn["gd5"])
        self.gd7 = int(damn["gd6"])
        self.gd8 = int(damn["gd7"])
        self.gd9 = int(damn["gd8"])
        self.gd10 = int(damn['gd9'])
        self.gd11 = int(damn["gd10"])
        self.gd12 = int(damn["gd11"])
        self.gd13 = int(damn["gd12"])
        self.gd14 = int(damn["gd13"])
        self.gd15 = int(damn['gd14'])
        self.gd16 = int(damn["gd15"])
        #self.gd17 = int(damn["gd16"])
        #self.gd18 = int(damn["gd17"])
        #self.gd19 = int(damn["gd18"])
        #self.gd20 = int(damn['gd19'])
        #self.gd21 = int(damn["gd20"])
        #self.gd22 = int(damn["gd21"])
        #self.gd23 = int(damn["gd22"])
        #self.gd24 = int(damn["gd23"])
        #self.gd25 = int(damn['gd24'])
        #self.gd26 = int(damn["gd25"])
        #self.gd27 = int(damn["gd26"])
        #self.gd28 = int(damn["gd27"])
        #self.gd29 = int(damn["gd28"])
        #self.gd30 = int(damn['gd29'])
        #self.gd31 = int(damn["gd30"])
        #self.gd32 = int(damn["gd31"])
        #self.gd33 = int(damn["gd32"])
        #self.gd34 = int(damn["gd33"])
        #self.gd35 = int(damn['gd34'])
        #self.gd36 = int(damn["gd35"])
        #self.gd37 = int(damn["gd36"])
        #self.gd38 = int(damn["gd37"])
        #self.gd39 = int(damn["gd38"])
        #self.gd40 = int(damn['gd39'])
        #self.gd41 = int(damn["gd40"])
        #self.gd42 = int(damn["gd41"])
        #self.gd43 = int(damn["gd42"])
        #self.gd44 = int(damn["gd43"])
        #self.gd45 = int(damn['gd44'])

        

        # ground checks
        self.gr1 = int(damn['gr0'])
        self.gr2 = int(damn['gr1'])
        self.gr3 = int(damn['gr2'])
        self.gr4 = int(damn['gr3'])
        self.gr5 = int(damn['gr4'])
        self.gr6 = int(damn['gr5'])
        self.gr7 = int(damn['gr6'])
        self.gr8 = int(damn['gr7'])

        # get the spawn distance from goal
        #self.initial_distance_from_goal = int(damn['init_goal'])
        
        self.reset_game = int(damn["reset_agent"])
 
        self.distanse = int(damn["AgentDistance"])
        if self.distanse == 0:
            self.distanse = 1
        # we also check if the agent is moving towards the goal, and if so then we reward it
        #if int(damn['agent_closer']) == 1:
        #    self.is_closer_to_goal = 1
        #    self.reward = 10
        #    # the agents reward is an inverse function of its distance towards the goal
        
        #self.reward += 10000* (1/self.distanse)
        ## NEW METHOD TO GIVE ACTURATE AND FLAT REWARDS
        self.reward += (self.initial_distance_from_goal - self.distanse)*10

        
        if self.distanse > self.initial_distance_from_goal:
            self.temp_clamped_distance = self.initial_distance_from_goal
        else:
            self.temp_clamped_distance = self.distanse
        
        # whats going on here? ohhh its capping the score at 0 if the agent moves further than init position 
        # TODO NAHH G, there is some black magic here bruh got me deaaad
        self._score = ((self.initial_distance_from_goal - self.temp_clamped_distance)/self.initial_distance_from_goal)*100
        
        # TEST to update the initial distance from the goal to forcably promote moving towards the goal please TODO CHECK THIS AND MAYBE REMOVE IF ISSUES ARRISE
        #self.initial_distance_from_goal = self.distanse

        # Test why the agent keeps saying 1 move onyl when it dies for first time
        print("reset status from edge :",self.reset_game)

        # check if game is over (ie if it has exceeded the allocated time to simulate)
        game_over = False
        if self.game_over_next_turn:
            game_over = True
            Agent_Input_List[8] = 0


        if self.check_game_over():
            #game_over = True
            self.game_over_next_turn = True
            Agent_Input_List[8] = 1

        if self._hours_spent > self._simulation_duration:
            # here we exceed the moves limit
            #game_over = True
            self.game_over_next_turn = True
            Agent_Input_List[8] = 1

        if self.reset_game:
            self.reward = -1000
            self.distanse = 1000
            # here the player has fallen off the map, and should die
            game_over = True
            self.reset_game = 0

        return self.reward, game_over, self._score

    def move(self, action):
        # get the action as a numpy thing:
        '''
        action map:

        forward = [1,0,0,0,0,0,0,0]
        backward = [0,1,0,0,0,0,0,0] 
        left = [0,0,1,0,0,0,0,0]
        right = [0,0,0,1,0,0,0,0]
        forward left = [0,0,0,0,1,0,0,0]
        forward right = [0,0,0,0,0,1,0,0]
        backward left = [0,0,0,0,0,0,1,0]
        backward right = [0,0,0,0,0,0,0,1]
        
        '''
        #print(action)

        # check the action passed and then make a move
        if np.array_equal(action, [1,0,0,0,0,0,0,0]):
            #print(self._hours_spent,"Agent Explores")
            self.move_forward()
        elif np.array_equal(action, [0,1,0,0,0,0,0,0] ):
            #print(self._hours_spent,"Agent Goes On Expedition")
            self.move_backwards()
        elif np.array_equal(action, [0,0,1,0,0,0,0,0]):
            #print(self._hours_spent,"Agent Sells Resources")
            self.move_right()
        elif np.array_equal(action, [0,0,0,1,0,0,0,0]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_left()
        elif np.array_equal(action, [0,0,0,0,1,0,0,0]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_forward_left()
        elif np.array_equal(action, [0,0,0,0,0,1,0,0]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_forward_right()
        elif np.array_equal(action, [0,0,0,0,0,0,1,0]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_backward_left()
        elif np.array_equal(action, [0,0,0,0,0,0,0,1]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_backward_right()
        
        
        #else:  # [0,0,0,0,0,0,0,1] agent idles
            #print(self._hours_spent,"Agent chooses to idle")
        #    self.idle(None)
