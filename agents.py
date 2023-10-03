import numpy as np
import random as rnd

class agent:

    def __init__(self, personal_dissatisfaction,id):
        self.personal_dissatisfaction = personal_dissatisfaction 
        self.close_friends = np.array([])
        self.friends = np.array([])
        self.network = np.array([])
        self.id = id
        self.affected_dissatisfaction = personal_dissatisfaction

    def get_personal_dissatisfaction(self):
        return self.personal_dissatisfaction
    def get_affected_dissatisfaction(self):
        return self.affected_dissatisfaction

    def add_close_friend(self,close_friend):
        self.close_friends = np.append(self.close_friends,close_friend)
    def add_friend(self,friend):
        self.friends = np.append(self.friends,friend)
    def add_to_network(self,network_friend):
        self.network = np.append(self.network,network_friend)

    def close_friends_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.close_friends)):
            average_friend_dis += self.close_friends[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.close_friends)
    def friends_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.friends)):
            average_friend_dis += self.friends[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.friends)
    def network_dissatisfaction(self):
        average_friend_dis = 0
        for i in range(len(self.network)):
            average_friend_dis += self.network[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.network)
        
    def dissatisfaction_distance(self):
        weighted_average = (4*self.close_friends_dissatisfaction() + 2*self.friends_dissatisfaction() + self.network_dissatisfaction()) / 7
        return weighted_average - self.affected_dissatisfaction
    def update_dissatisfaction(self):
        affect_rate = 0.05
        change = self.dissatisfaction_distance() * affect_rate
        self.affected_dissatisfaction += change

    


#how much each connection is affected per person
close_friends_af = 0.8
friends_af = 0.5
netwrok_af = 0.1
public_af = 0.01
def event(tick):
    if tick%7 == 0 :
        return (rnd.randint(-7, 7)*np.array([close_friends_af,friends_af,netwrok_af,public_af]))
    if tick%30 == 0 :
        return (rnd.randint(-30, 30)*np.array([close_friends_af,friends_af,netwrok_af,public_af]))
    if tick%90 == 0 :
        return (rnd.randint(-90, 90)*np.array([close_friends_af,friends_af,netwrok_af,public_af]))

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
    while len(agents[i].friends) != 10:
        current_agent = agents[rnd.randint(0,99)]
        if not(np.any(agents[i].close_friends == current_agent)) and not(np.any(agents[i].friends == current_agent)):
            agents[i].friends = np.append(agents[i].friends,current_agent)
    while len(agents[i].network) != 30:
        current_agent = agents[rnd.randint(0,99)]
        if not(np.any(agents[i].close_friends == current_agent)) and not(np.any(agents[i].friends == current_agent) and not(np.any(agents[i].network == current_agent))):
            agents[i].network = np.append(agents[i].network,current_agent)

def average_total_dissatisfaction(agents):
    average = 0
    for i in range(len(agents)):
        average += agents[i].get_affected_dissatisfaction()
    return average / len(agents)

dissatisfaction = []
def run(agents):
    iterations = 200
    for j in range(iterations):
        for i in range(len(agents)):
            agents[i].update_dissatisfaction()
        np.append(dissatisfaction, average_total_dissatisfaction(agents))

print("Close friends average personal_dissatisfaction: ",agents[0].close_friends_dissatisfaction())
print("Friends average personal_dissatisfaction: ",agents[0].friends_dissatisfaction())
print("Network average personal_dissatisfaction: ",agents[0].network_dissatisfaction())
print("Agent 0 has a personal dissatisfaction of {0}, an affected dissatisfaction of {1} and a difference of affected and its overall network {2}".format(agents[0].get_personal_dissatisfaction(),agents[0].get_affected_dissatisfaction(), agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New affected dissatisfaction of agent 0: ",agents[0].get_affected_dissatisfaction() )
#for i in range(len(agents)):
#    print(len(agents[i].friends))

