import numpy as np
import random as rnd
class agent:
    def __init__(self, dissatisfaction,id):
        self.dissatisfaction = dissatisfaction 
        self.close_friends = np.array([])
        self.friends = np.array([])
        self.network = np.array([])
        self.id = id

    def get_dissatisfaction(self):
        return self.dissatisfaction
    def add_close_friend(self,close_friend):
        self.close_friends = np.append(self.close_friends,close_friend)
    def add_friend(self,friend):
        self.friends = np.append(self.friends,friend)
    def add_to_network(self,network_friend):
        self.network = np.append(self.network,network_friend)
    def close_friends_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.close_friends)):
            average_friend_dis += self.close_friends[i].get_dissatisfaction()
        return average_friend_dis / len(self.close_friends)
    def friends_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.friends)):
            average_friend_dis += self.friends[i].get_dissatisfaction()
        return average_friend_dis / len(self.friends)
    def network_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.network)):
            average_friend_dis += self.network[i].get_dissatisfaction()
        return average_friend_dis / len(self.network)
    def dissatisfaction_distance(self):
        weighted_average = (4*self.close_friends_dissatisfaction() + 2*self.friends_dissatisfaction() + self.network_dissatisfaction()) / 7
        return weighted_average - self.dissatisfaction
    def update_dissatisfaction(self):
        change = self.dissatisfaction_distance() * 0.05
        self.dissatisfaction *= (1 + change)

    


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
# print(agents)

# def run(agents):
#     iterations = 200
#     for j in range(iterations):
#         for i in range(len(agents)):





print("Close friends average dissatisfaction: ",agents[0].close_friends_dissatisfaction())
print("Friends average dissatisfaction: ",agents[0].friends_dissatisfaction())
print("Network average dissatisfaction: ",agents[0].network_dissatisfaction())
print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_dissatisfaction(), agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New dissatisfaction: ",agents[0].get_dissatisfaction() )

