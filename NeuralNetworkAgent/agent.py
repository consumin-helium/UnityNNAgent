from typing import Deque
import torch
import numpy as np
import random

from game_gutted import RedBoiAI

from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 10
LR = 0.001


class Agent:

    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate (must be smaller than 1)
        self.memory = Deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(17, 256, 4) # state / hidden / output moves
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # TODO: model, trainer

    def get_state(self, game):
        # in example, here they checked the snake to see if it was in danger or something. basically this is the agents eyes
        # get all of the state variables from the game and then tabulate them here
        '''
        [number_credits, number_resources,
        can_afford_scout,can_afford_farm,can_afford_expedition,
        number_farmers,number_scouts,farm_level,
        recruit_cost, farm_cost
        ]
        '''
        state = [
            # get the ground checks
            game.ground_check_1,
            game.ground_check_2,
            game.ground_check_3,
            game.ground_check_4,
            game.ground_check_5,
            game.ground_check_6,
            game.ground_check_7,
            game.ground_check_8,


            # get the direction of the goal
            game.goal_direction_1,
            game.goal_direction_2,
            game.goal_direction_3,
            game.goal_direction_4,
            game.goal_direction_5,
            game.goal_direction_6,
            game.goal_direction_7,
            game.goal_direction_8,

            # get if user is closer to goal
            game.is_closer_to_goal
            

        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory()

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradoff exploration / exploitation
        self.epsilon = 500 - self.number_of_games
        final_move = [0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).cuda() 
            prediction = self.model(state0).cuda() 
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0  # best score
    agent = Agent()
    game = RedBoiAI()
    while True:
        # get the old state
        state_old = agent.get_state(game)

        # get the move based on current state
        final_move = agent.get_action(state_old)
        
        
        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train the short memory (for only one step)
        agent.train_short_memory(
            state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        print("Agent has made ", game._hours_spent, "moves out of ",game._simulation_duration,"for generation", agent.number_of_games)

        if done:
            # train the long memory (all experience / past life), plot the results live
            #game.reset(100*1.005**(agent.number_of_games + 1)) # also set the new number of hours to simulate
            game.reset(150)
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            
            print('Game', agent.number_of_games,"Score",score,'Record',record)

            # plotting begin
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
