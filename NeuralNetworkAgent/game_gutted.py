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
    '"right"':0
}

Agent_Input_List = [0,0,0,0,0]

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

        Agent_Input_List[0] = 0 # forward
        Agent_Input_List[1] = 0 # backward
        Agent_Input_List[2] = 0 # left
        Agent_Input_List[3] = 0 # right
        Agent_Input_List[4] = 0 # reset player

        self.game_over_next_turn = False

        # is stands for is there ground
        self.ground_check_1 = 0
        self.ground_check_2 = 0
        self.ground_check_3 = 0
        self.ground_check_4 = 0
        self.ground_check_5 = 0
        self.ground_check_6 = 0
        self.ground_check_7 = 0
        self.ground_check_8 = 0

        # now define directional data for the goal
        self.goal_direction_1 = 0
        self.goal_direction_2 = 0
        self.goal_direction_3 = 0
        self.goal_direction_4 = 0
        self.goal_direction_5 = 0
        self.goal_direction_6 = 0
        self.goal_direction_7 = 0
        self.goal_direction_8 = 0

        # additional checks to reset the simulation
        self.reset_game = 0
        self.is_closer_to_goal = 0
        self.distanse = 1000

        # imported from the last model
        self._hours_spent = 0
        self._score = 0
        self.number_of_games = 0
        self.reward = 0
        self.tick = 0
        self._simulation_duration = 150

    def reset(self, new_sim_duration):  # creates new player for new iteration
        # tracked game tick, idk why we use this but i guess its for like "how many moves it made" or whatever
        Agent_Input_Map['"forward"']=0
        Agent_Input_Map['"backward"']=0
        Agent_Input_Map['"left"']=0
        Agent_Input_Map['"right"']=0

        Agent_Input_List[0] = 0 # forward
        Agent_Input_List[1] = 0 # backward
        Agent_Input_List[2] = 0 # left
        Agent_Input_List[3] = 0 # right
        Agent_Input_List[4] = 0 # reset player

        self.game_over_next_turn = False

        # is stands for is there ground
        self.ground_check_1 = 0
        self.ground_check_2 = 0
        self.ground_check_3 = 0
        self.ground_check_4 = 0
        self.ground_check_5 = 0
        self.ground_check_6 = 0
        self.ground_check_7 = 0
        self.ground_check_8 = 0

        # now define directional data for the goal
        self.goal_direction_1 = 0
        self.goal_direction_2 = 0
        self.goal_direction_3 = 0
        self.goal_direction_4 = 0
        self.goal_direction_5 = 0
        self.goal_direction_6 = 0
        self.goal_direction_7 = 0
        self.goal_direction_8 = 0

        # additional checks to reset the simulation
        self.reset_game = 0
        self.is_closer_to_goal = 0
        self.distanse = 1000

        # imported from the last model
        self._hours_spent = 0
        self._score = 0
        self.number_of_games = 0
        self.reward = 0
        self.tick = 0
        self._simulation_duration = 150

    def check_game_over(self):
        if self.tick > 40000:
            return True
        return False

    def move_forward(self):
        print("forward")
        
        Agent_Input_Map['"forward"']=1
        Agent_Input_List[0] = 1 # forward
        self.reward = 5


    def move_backwards(self):
        print("backward")
        Agent_Input_Map['"backward"']=1
        Agent_Input_List[1] = 1 # backward
        self.reward = 5


    def move_left(self):
        print("left")
        Agent_Input_Map['"left"']=1
        Agent_Input_List[2] = 1 # left
        self.reward = 5


    def move_right(self):
        print("right")
        Agent_Input_Map['"right"']=1
        Agent_Input_List[3] = 1 # right
        self.reward = 5
    
    def idle(self):
        print("idle")
        self.reward = 1

    

    def play_step(self, action):
        
        # a move was made, increase the tick
        self.tick += 1

        self._hours_spent +=1
        # make a play
        self.move(action)

        '''
        HERE we send the command to unity to make a move
        
        then we get the ouput and update the init variables to reflect it
        
        '''
        # convert the movement action to a dict
        data_package = str(Agent_Input_List)

        # send a thank you message to the client. encoding to send byte type.
        c.send(data_package.encode())

        # print what we receive from unity
        damn = c.recv(1024).decode()
        
        damn = damn.replace("'",'"')

        damn = damn.replace("{",'{"')
        damn = damn.replace(" : ",'" : "')
        damn = damn.replace(", ",'","')
        damn = damn.replace("}",'"}')
        #print(damn)
        damn = json.loads(damn)
        #print(damn)
        #print(damn["goal_direction_0"])

        # here we go through the laborious process of setting akk the results to their self values
        self.goal_direction_1 = int(damn["goal_direction_0"])
        self.goal_direction_2 = int(damn["goal_direction_0"])
        self.goal_direction_3 = int(damn["goal_direction_0"])
        self.goal_direction_4 = int(damn["goal_direction_0"])
        self.goal_direction_5 = int(damn['goal_direction_4'])
        self.goal_direction_6 = int(damn['goal_direction_5'])
        self.goal_direction_7 = int(damn['goal_direction_6'])
        self.goal_direction_8 = int(damn['goal_direction_7'])

        self.ground_check_1 = int(damn['ground_check_0'])
        self.ground_check_2 = int(damn['ground_check_1'])
        self.ground_check_3 = int(damn['ground_check_2'])
        self.ground_check_4 = int(damn['ground_check_3'])
        self.ground_check_5 = int(damn['ground_check_4'])
        self.ground_check_6 = int(damn['ground_check_5'])
        self.ground_check_7 = int(damn['ground_check_6'])
        self.ground_check_8 = int(damn['ground_check_7'])
        
        self.reset_game = int(damn["reset_agent"])

        self.distanse = int(damn["AgentDistance"])
        if self.distanse == 0:
            self.distanse = 1
        # we also check if the agent is moving towards the goal, and if so then we reward it
        if int(damn['agent_closer']) == 1:
            self.is_closer_to_goal = 1
            self.reward = 10
            # the agents reward is an inverse function of its distance towards the goal
        
        self.reward += 10000* (1/self.distanse)

        
        
        print("SCORE",self.distanse)
        self._score = 100* (1/self.distanse)
        
        
        

        

        # check if game is over (ie if it has exceeded the allocated time to simulate)
        game_over = False
        if self.game_over_next_turn:
            game_over = True
            Agent_Input_List[4] = 0


        if self.check_game_over():
            #game_over = True
            self.game_over_next_turn = True
            Agent_Input_List[4] = 1

        if self._hours_spent > self._simulation_duration:
            # here we exceed the moves limit
            #game_over = True
            self.game_over_next_turn = True
            Agent_Input_List[4] = 1

        if self.reset_game:
            self.reward = -100
            # here the player has fallen off the map, and should die
            game_over = True

        return self.reward, game_over, self._score

    def move(self, action):
        # get the action as a numpy thing:
        '''
        action map:

        left = [1,0,0,0,0]
        right = [0,1,0,0,0] 
        forward = [0,0,1,0,0]
        backward = [0,0,0,1,0]
        idle = [0,0,0,0,1]
        
        '''
        #print(action)

        # check the action passed and then make a move
        if np.array_equal(action, [1, 0, 0, 0]):
            #print(self._hours_spent,"Agent Explores")
            self.move_forward()
        elif np.array_equal(action, [0, 1, 0, 0]):
            #print(self._hours_spent,"Agent Goes On Expedition")
            self.move_backwards()
        elif np.array_equal(action, [0, 0, 1, 0]):
            #print(self._hours_spent,"Agent Sells Resources")
            self.move_right()
        elif np.array_equal(action, [0, 0, 0, 1]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.move_left()
        
        
        #else:  # [0,0,0,0,0,0,0,1] agent idles
            #print(self._hours_spent,"Agent chooses to idle")
        #    self.idle(None)
