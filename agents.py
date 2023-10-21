import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import math

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
    
    def get_close_friends(self):
        return self.close_friends
    def get_friends(self):
        return self.friends
    def get_network(self):
        return self.network

    def event_update_affected_dissatisfaction(self,amount):
        self.affected_dissatisfaction += amount

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
        weighted_average = (close_friends_af*(self.close_friends_dissatisfaction() - self.affected_dissatisfaction) + friends_af*(self.friends_dissatisfaction() - self.affected_dissatisfaction)+ netwrok_af*(self.network_dissatisfaction() - self.affected_dissatisfaction)) / (close_friends_af + friends_af + netwrok_af)
        return weighted_average
    def update_dissatisfaction(self):
        affect_rate = 2
        # change =  self.dissatisfaction_distance() * math.exp((self.dissatisfaction_distance / 100)-1)
        change = self.dissatisfaction_distance()**3/100**2
        self.affected_dissatisfaction += change

        # # Just to see:  give a 1/1000 possibility that one agent becomes wild, maximum dissatisfaction
        if rnd.randint(0,100) <=5:
            if self.affected_dissatisfaction != base_disstatisfaction:
                self.affected_dissatisfaction += (base_disstatisfaction - self.affected_dissatisfaction)/10
        if rnd.randint(0,100) <= 3:
            if self.affected_dissatisfaction != 0:
                self.affected_dissatisfaction -= self.affected_dissatisfaction / 10

    


#how much each connection is affected per person
person = 10
close_friends_af = 9
friends_af = 3
netwrok_af = 1
public_af = 0.1
def event(tick):
    if tick%7 == 0 :
        return (rnd.randint(-7, 7)*np.array([person,close_friends_af,friends_af,netwrok_af,public_af]))
    elif tick%29 == 0 :
        return (rnd.randint(-30, 30)*np.array([person,close_friends_af,friends_af,netwrok_af,public_af]))
    elif tick%89 == 0 :
        return (rnd.randint(-90, 90)*np.array([person,close_friends_af,friends_af,netwrok_af,public_af]))
    else: return np.array([0,0,0,0,0])

#close friends 4
#friends 10
#network 30
agents = np.array([])
base_disstatisfaction = 100
for i in range(100):
    agents = np.append(agents, agent(rnd.randint(0,base_disstatisfaction),i))

for i in range(25):
    close_friendgroup = np.array([agents[0+i*4],agents[1+i*4],agents[2+i*4],agents[3+i*4]])
    agents[(0+i*4)].add_close_friend(np.array([agents[1+i*4],agents[2+i*4],agents[3+i*4]]))
    agents[(1+i*4)].add_close_friend(np.array([agents[0+i*4],agents[2+i*4],agents[3+i*4]]))
    agents[(2+i*4)].add_close_friend(np.array([agents[0+i*4],agents[1+i*4],agents[3+i*4]]))
    agents[(3+i*4)].add_close_friend(np.array([agents[0+i*4],agents[1+i*4],agents[2+i*4]]))

for i in range(100):
    while len(agents[i].friends) <= 10:
        rnumber = rnd.randint(0,99)
        if not(np.any(agents[i].close_friends == agents[rnumber])) and not(np.any(agents[i].friends == agents[rnumber])):
            agents[i].friends = np.append(agents[i].friends,agents[rnumber])
            agents[rnumber].friends = np.append(agents[rnumber],agents[i].friends)
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
a_dis = []
def run(agents):
    iterations = 5000

    for j in range(iterations):
        dissatisfaction.append(average_total_dissatisfaction(agents))

        # Iterate over the full array of agents and change their dissatisfaction based on their friends'
        for i in range(len(agents)):
            agents[i].update_dissatisfaction()
        

        rnumber = rnd.randint(0,99)
        eve = event(j)
        agents[rnumber].event_update_affected_dissatisfaction(eve[0])
        for close_friend in agents[rnumber].get_close_friends():
            close_friend.event_update_affected_dissatisfaction(eve[1])
        for friend in agents[rnumber].get_friends():
            friend.event_update_affected_dissatisfaction(eve[2])
        for network in agents[rnumber].get_network():
            network.event_update_affected_dissatisfaction(eve[3])
        for agent in agents:
            if agent != agents[rnumber] and not(np.any(agent == agents[rnumber].get_close_friends())) and not(np.any(agent == agents[rnumber].get_friends())) and not(np.any(agent == agents[rnumber].get_network())):
                agent.event_update_affected_dissatisfaction(eve[4])
        #if j%7 == 0:
        #    print(eve)
        #    print(agents[rnumber])

print("Close friends average dissatisfaction: ",agents[0].close_friends_dissatisfaction())
print("Friends average dissatisfaction: ",agents[0].friends_dissatisfaction())
print("Network average dissatisfaction: ",agents[0].network_dissatisfaction())
print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_affected_dissatisfaction(), agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New dissatisfaction: ",agents[0].get_affected_dissatisfaction() )
print(average_total_dissatisfaction(agents))
run(agents)
print("Close friends average dissatisfaction: ",agents[0].close_friends_dissatisfaction())
print("Friends average dissatisfaction: ",agents[0].friends_dissatisfaction())
print("Network average dissatisfaction: ",agents[0].network_dissatisfaction())
print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_affected_dissatisfaction(), agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New dissatisfaction: ",agents[0].get_affected_dissatisfaction() )
print(average_total_dissatisfaction(agents))
plt.plot(dissatisfaction)
plt.xlabel("Number of Iterations")
plt.ylabel("Average Dissatisfaction")
plt.show()

