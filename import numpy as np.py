import numpy as np
import random as rnd
class agent:
    close_friends = np.array([])
    friends = np.array([])
    network = np.array([])
    def __init__(self, dissatisfaction):
        self.dissatisfaction = dissatisfaction 
    def add_close_friend(close_friend):
        np.append(close_friends,close_friend)
    def add_friend(friend):
        np.append(friends,friend)
    def add_to_network(network_friend):
        np.append(network,network_friend)

def event(tick):
    if tick%7 == 0 :
        return (random.randint(-5, 5))
    if tick%30 == 0 :
        return (random.randint(-30, 30))
    if tick%90 == 0 :
        return (random.randint(-100, 100))
#close friends 4
agents = np.array([])
base_disstatisfaction = 20
for i in range(100):
    np.append(agents, agent(rnd.randint(0,base_disstatisfaction)))

for i in range(25):
    close_friendgroup = np.array([agents[0+i*4],agents[1+i*4],agents[2+i*4],agents[3+i*4]])
    agents[0+i*4].add_close_friend(close_friendgroup)

#for i in range(100):
#    while agents[i].friends != 10:
#        if agents[randint(0,100)]


