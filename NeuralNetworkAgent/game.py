import mysql.connector
import names
import json
import secrets
import numpy as np
import random

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port='3306',
    password="admin",
    database="sys"
)
mycursor = mydb.cursor()

'''
THE GOAL FOR AGENT IS TO TRY GET MAXIMUM XP AND CREDITS POSSIBLE WITHIN THE ALLOCATED LIFETIME OF 1000 HOURS
'''

# a generation class for generating events and colonists


class generation():
    def genColonist(self):
        # creates a new random colonist
        colonist_data = {
            "colonistID": secrets.token_hex(4),
            "colonistName": names.get_full_name(),
            "colonistOccupation": "unemployed"

        }
        return colonist_data

# backend is resposible for dealing with the database

class backendLogic():
    def fetch_score(self, id):
        mycursor.execute("SELECT * FROM user_data WHERE UserID = " + str(id))
        myresult = mycursor.fetchall()
        print(myresult)

    def createNewUser(self):
        new_id = 1
        resources_data = {
            "bones": 0,
            "common_rock": 0,
            'interesting_rock': 0,
            'stellar_soil': 0,
            'fertile_stellar_soil': 0,
            'credits': 0,
            'shards': 0,
            'life_samples': 0
        }
        # generate 3 new colonists
        colonistz = []
        for i in range(0, 3):
            colonistz.append(generation.genColonist(generation))

        colony_data = {
            "data": {
                "colonyName": "my_arse_hurts",
                "colonists": colonistz
            }
        }
        sql = "INSERT INTO user_data (UserID, Resources, ColonyData) VALUES (%s, %s, %s)"
        val = (str(new_id), json.dumps(resources_data), json.dumps(colony_data))
        mycursor.execute(sql, val)
        mydb.commit()


# define the bulk of the variables and conditions for the game that is avaliable to the agent to see
item_xp_table = {
    "common_rock": 1,
    "interesting_rock": 2,
    "stellar_soil": 1,
    "fertile_stellar_soil": 2,
    "bones": 5
}

# for now the items will just be 'resource' and will hgave a flat exchange of 1 credit and 1 xp
item_table = {
    "resource": {
        "xp": 1,
        "credits": 1
    }
}




# the interface is basically functions called that interact with the game and simulate events such as explore
class RedBoiAI():
    def __init__(self):
        # set the highest score for it to try reach
        self._highest_score = 0
        self.previous_score = 0
        # define all of the variables that need to be referenced
        self._simulation_duration = 150  # hours to run the sim for
        # variables for the agent to use
        self._credits = 0
        self._scouts = 1
        self._farmers = 1
        self._score = 0
        self._farm_level = 1
        self._recruit_cost = 500
        self._farm_upgrade_cost = 1000
        self._expedition_cost = 1000
        # track the agents resources here since i dont wanna dable with the database quite yet
        self._resources = 0
        # tracked variables that the agent shouldnt worry about
        self._number_expeditions = 0
        self._number_explores = 0
        self._hours_spent = 0
        # progression data lists
        self.hours_progression = []
        self.farm_level_prorgession = []
        self.resources_list = []
        self.credits_list = []
        self.scouts_list = []
        self.farmers_list = []
        self.score_list = []
        self.recruit_cost_list = []
        self.farm_cost_list = []
        self.expedition_cost_list = []

        # tracked game tick, idk why we use this but i guess its for like "how many moves it made" or whatever
        self.tick = 0

    def reset(self, new_sim_duration):  # creates new player for new iteration
        # basically just init the damn thing again and rest all the users items and score
        self._simulation_duration = new_sim_duration
        self._credits = 0
        self._scouts = 1
        self._farmers = 1
        self._score = 0
        self._farm_level = 1
        self._recruit_cost = 500
        self._farm_upgrade_cost = 1000
        self._expedition_cost = 1000
        # track the agents resources here since i dont wanna dable with the database quite yet
        self._resources = 0
        # tracked variables that the agent shouldnt worry about
        self._number_expeditions = 0
        self._number_explores = 0
        self._hours_spent = 0
        # progression data lists, reset them
        self.hours_progression = []
        self.farm_level_prorgession = []
        self.resources_list = []
        self.credits_list = []
        self.scouts_list = []
        self.farmers_list = []
        self.score_list = []
        self.recruit_cost_list = []
        self.farm_cost_list = []
        self.expedition_cost_list = []

        # tracked game tick, idk why we use this but i guess its for like "how many moves it made" or whatever
        self.tick = 0

    def explore(self):
        # perform the explore function
        # get the number of scouts and the number of farmers owned
        multiplier = (self._farmers * self._farm_level) + self._scouts 
        # Imported from discord bot so atm im not sure of the variables names
        itemNUMBER = [1, 2, 3] 
        randomList = random.choices(itemNUMBER, weights=(90, 50, 5), k=1)
        # print(randomList)
        sampleList = ['bones', 'common_rock', 'interesting_rock',
                      'stellar_soil', 'fertile_stellar_soil']
        randomList = random.choices(sampleList, weights=(
            3, 80, 3, 70, 3), k=int(randomList[0]))
        # generate the quantity of items found
        randomQUANITITY = [2, 3, 4, 6]
        items_found = {}
        for i in randomList:
            items_found[i] = random.choices(
                randomQUANITITY, weights=(90, 50, 30, 10), k=1)

        # then at the end we find items, for the agent we convert all resource types to type 'resource'
        resources_found = 0
        for item in items_found:
            new_item_ammount = items_found[item]
            resources_found = resources_found + (1 * new_item_ammount[0])
        # then update the agents data to show they found resources
        self._resources += (resources_found * multiplier)
        # and give them some score as the user does get xp for exploring
        self._score += (5 * multiplier)
        self.reward = (5 * multiplier)

    def expedition(self):
        # for now do nothing...
        # actually maybe degrade the agents score so they learn to avoid this since i dont feel like removing it at the moment

        self.reward = 1

    def sell(self):
        # TODO: to simplify, just sell all resources
        self._credits += self._resources
        self._resources = 0
        self.reward = 2
        

    def buy(self, item_type, quantity):
        # TODO: add the logic, for now it just does nothing
        self.reward = 1

    def study(self, item_type, quantity):
        # TODO: add the logic, for now it just does nothing
        self.reward = 1

    def upgrade(self):
        # check if agent has enough resources to upgrade the farm
        if(self._resources > self._farm_upgrade_cost):
            # here the agent can afford it
            self._farm_level += 1
            self.reward = 10
            self._resources -= self._farm_upgrade_cost
            self._farm_upgrade_cost = self._farm_upgrade_cost * 1.2
            
        self.reward = 1

    def recruit_farmer(self):  # to make it easier on the ai at the start, must specify job that you want to recruit for so either farmer or scout
        # check the agents credits and check if they can affoerd to upgrade
        if(self._credits >= self._recruit_cost):
            
            # in this case the agent can afford to upgrade
            self.reward = 10
            # now get a new colonist, so deduct the funds required
            self._credits -= self._recruit_cost
            self._farmers += 1
            self._recruit_cost = self._recruit_cost * 1.2

        self.reward = 1

    def recruit_scout(self):  # to make it easier on the ai at the start, must specify job that you want to recruit for so either farmer or scout
        # check the agents credits and check if they can affoerd to upgrade
        if(self._credits >= self._recruit_cost):
            # in this case the agent can afford to upgrade
            self.reward = 10
            # now get a new colonist, so deduct the funds required
            self._credits -= self._recruit_cost
            self._scouts += 1
            self._recruit_cost = self._recruit_cost * 1.2

        self.reward = 1

    def check_game_over(self):
        # check if the max number of hours has been reached yet
        if(self._hours_spent >= self._simulation_duration):
            self.reward = -1
            return True
        else:
            return False

    def idle(self, duration):
        # TODO: add the logic, for now it just does nothing
        self.reward = 1

    def play_step(self, action):
        # a move was made, increase the tick
        self.tick += 1
        # make a play
        self.move(action)
        # check if game is over (ie if it has exceeded the allocated time to simulate)
        game_over = False
        if self.check_game_over():
            game_over = True
            
            # game is over! so now save to a local file
            interesting_data = {
                "resources": self.resources_list,
                "credits": self.credits_list,
                "scouts": self.scouts_list,
                "farmers": self.farmers_list,
                "score": self.score_list,
                "recruit_cost": self.recruit_cost_list,
                "farm_cost": self.farm_cost_list,
                "expedition_cost": self.expedition_cost_list,
                "hours": self.hours_progression,
                "farm_level": self.farm_level_prorgession
            }

            f = open("./data/data_man.js", "w")
            f.write("var data_man = " + str(interesting_data))
            f.close()
            
            ## check if agent beat highest score
            #if(self._score > self._highest_score):
            #    self._highest_score = self._score
            #    return 2000, game_over, self._score
            ## check if the agent performed better than previous run
            #if(self._score > self.previous_score):
            #    self.previous_score = self._score
            #    return 500, game_over, self._score
            return 0, game_over, self._score
        # each time ticks are more than multiple of 60 then add another hour
        if self.tick/60 > self._hours_spent:
            # every hour worth of gameplay
            self._hours_spent += 1
            # here we will save the current paramaters of the progression
            self.resources_list.append(self._resources)
            self.credits_list.append(self._credits)
            self.scouts_list.append(self._scouts)
            
            self.farmers_list.append(self._farmers)
            self.score_list.append(self._score)
            self.recruit_cost_list.append(self._recruit_cost)
            self.farm_cost_list.append(self._farm_upgrade_cost)
            self.expedition_cost_list.append(self._expedition_cost)
            self.hours_progression.append(self._hours_spent)
            self.farm_level_prorgession.append(self._farm_level)

            


        return self.reward, game_over, self._score

    def move(self, action):
        # get the action as a numpy thing:
        '''
        action map:

        explore = [1,0,0,0,0,0,0,0,0]
        expedition = [0,1,0,0,0,0,0,0,0] IGNORED FOR NOW
        sell = [0,0,1,0,0,0,0,0,0]
        buy = [0,0,0,1,0,0,0,0,0]
        study = [0,0,0,0,1,0,0,0,0]
        upgrade = [0,0,0,0,0,1,0,0,0]
        recruit_farmer = [0,0,0,0,0,1,0,0]
        recruit_scout = [0,0,0,0,0,0,0,1,0]
        idle = [0,0,0,0,0,0,0,0,1]

        state map:

        [number_credits, number_resources,
        can_afford_scout,can_afford_farm,can_afford_expedition,
        number_farmers,number_scouts,farm_level,
        recruit_cost, farm_cost
        ]
        }
        '''
        #print(action)

        # check the action passed and then make a move
        if np.array_equal(action, [1, 0, 0, 0, 0, 0, 0, 0, 0]):
            #print(self._hours_spent,"Agent Explores")
            self.explore()
        elif np.array_equal(action, [0, 1, 0, 0, 0, 0, 0, 0, 0]):
            #print(self._hours_spent,"Agent Goes On Expedition")
            self.expedition()
        elif np.array_equal(action, [0, 0, 1, 0, 0, 0, 0, 0, 0]):
            #print(self._hours_spent,"Agent Sells Resources")
            self.sell()
        elif np.array_equal(action, [0, 0, 0, 1, 0, 0, 0, 0, 0]):
            #print(self._hours_spent,"Agent Buys Resources")
            self.buy(None, None)
        elif np.array_equal(action, [0, 0, 0, 0, 1, 0, 0, 0, 0]):
            #print(self._hours_spent,"Agent Studies")
            self.study(None, None)
        elif np.array_equal(action, [0, 0, 0, 0, 0, 1, 0, 0, 0]):
            #print(self._hours_spent,"Agent Upgrades")
            self.upgrade()
        elif np.array_equal(action, [0, 0, 0, 0, 0, 0, 1, 0, 0]):
            #print(self._hours_spent,"Agent Recruits farmer")
            self.recruit_farmer()
        elif np.array_equal(action, [0, 0, 0, 0, 0, 0, 0, 1, 0]):
            #print(self._hours_spent,"Agent Recruits scout")
            self.recruit_scout()
        else:  # [0,0,0,0,0,0,0,1] agent idles
            #print(self._hours_spent,"Agent chooses to idle")
            self.idle(None)
