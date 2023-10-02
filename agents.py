import numpy as np
import random as rnd
class agent:
    def __init__(self, dissatisfaction,id):
        self.dissatisfaction = dissatisfaction 
        self.close_friends = np.array([])
        self.friends = np.array([])
        self.network = np.array([])
        self.id = id
    def add_close_friend(self,close_friend):
        self.close_friends = np.append(self.close_friends,close_friend)
    def add_friend(self,friend):
        self.friends = np.append(self.friends,friend)
    def add_to_network(self,network_friend):
        self.network = np.append(self.network,network_friend)

def event(tick):
    if tick%7 == 0 :
        return (random.randint(-5, 5))
    if tick%30 == 0 :
        return (random.randint(-30, 30))
    if tick%90 == 0 :
        return (random.randint(-100, 100))
#close friends 4
#friends 10
#network 30
agents = np.array([])
base_disstatisfaction = 20
for i in range(100):
    agents = np.append(agents, agent(rnd.randint(0,base_disstatisfaction),i))

for i in range(25):
    close_friendgroup = np.array([agents[0+i*4],agents[1+i*4],agents[2+i*4],agents[3+i*4]])
    agents[(0+i*4)].add_close_friend(np.array([agents[1+i*4],agents[2+i*4],agents[3+i*4]]))
    agents[(1+i*4)].add_close_friend(np.array([agents[0+i*4],agents[2+i*4],agents[3+i*4]]))
    agents[(2+i*4)].add_close_friend(np.array([agents[0+i*4],agents[1+i*4],agents[3+i*4]]))
    agents[(3+i*4)].add_close_friend(np.array([agents[0+i*4],agents[1+i*4],agents[2+i*4]]))

for i in range(100):
    j=0
    while len(agents[j].friends) != 10:
        current_agent = agents[rnd.randint(0,99)]
        if not(np.any(agents[i].close_friends == current_agent)) and not(np.any(agents[i].friends == current_agent)):
            agents[j].friends = np.append(agents[j].friends,current_agent)
    while len(agents[j].network) != 30:
        current_agent = agents[rnd.randint(0,99)]
        if not(np.any(agents[i].close_friends == current_agent)) and not(np.any(agents[i].friends == current_agent) and not(np.any(agents[i].network == current_agent))):
            agents[j].network = np.append(agents[j].network,current_agent)
print(agents)


