import numpy as np
import random as rnd
import matplotlib.pyplot as plt

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
<<<<<<< HEAD
    

    # Compute how different the dissatisfaction between the agent and all its network is
    def dissatisfaction_distance(self):
        weighted_average = (close_friends_af*self.close_friends_dissatisfaction() + friends_af*self.friends_dissatisfaction() + netwrok_af*self.network_dissatisfaction()) / (close_friends_af + friends_af+netwrok_af)
        return weighted_average - self.dissatisfaction
    
    # Change the agent's dissatisfaction based on how different it's friends dissatisfaction is
    def update_dissatisfaction(self):
        change = self.dissatisfaction_distance() * (1 / base_disstatisfaction)
        self.dissatisfaction *= (1 + change)
=======
        
    def dissatisfaction_distance(self):
        weighted_average = (4*self.close_friends_dissatisfaction() + 2*self.friends_dissatisfaction() + self.network_dissatisfaction()) / 7
        return weighted_average - self.affected_dissatisfaction
    def update_dissatisfaction(self):
        affect_rate = 0.05
        change = self.dissatisfaction_distance() * affect_rate
        self.affected_dissatisfaction += change
>>>>>>> c39879808a29729f13032770397ecad3f0e59116

        # Just to see:  give a 1/1000 possibility that one agent becomes wild, maximum dissatisfaction
        if rnd.randint(0,1000) <=5:
            if self.dissatisfaction != base_disstatisfaction:
                self.dissatisfaction = base_disstatisfaction
        if rnd.randint(0,10000) <= 1:
            if self.dissatisfaction != 0:
                self.dissatisfaction = 0

    


#how much each connection is affected per person
<<<<<<< HEAD
close_friends_af = 0.6
friends_af = 0
netwrok_af = 0
=======
close_friends_af = 0.8
friends_af = 0.5
netwrok_af = 0.1
public_af = 0.01
>>>>>>> c39879808a29729f13032770397ecad3f0e59116
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
a_dis = []
def run(agents):
    iterations = 3000


    for j in range(iterations):
        dissatisfaction.append(average_total_dissatisfaction(agents))

        # Iterate over the full array of agents and change their dissatisfaction based on their friends'
        for i in range(len(agents)):
            agents[i].update_dissatisfaction()
        

<<<<<<< HEAD
# print("Close friends average dissatisfaction: ",agents[0].close_friends_dissatisfaction())
# print("Friends average dissatisfaction: ",agents[0].friends_dissatisfaction())
# print("Network average dissatisfaction: ",agents[0].network_dissatisfaction())
run(agents)
# print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_dissatisfaction(), agents[0].dissatisfaction_distance()))
# agents[0].update_dissatisfaction()
# print("New dissatisfaction: ",agents[0].get_dissatisfaction() )

plt.plot(dissatisfaction)
plt.xlabel("Number of Iterations")
plt.ylabel("Average Dissatisfaction")
plt.show()
=======
print("Close friends average personal_dissatisfaction: ",agents[0].close_friends_dissatisfaction())
print("Friends average personal_dissatisfaction: ",agents[0].friends_dissatisfaction())
print("Network average personal_dissatisfaction: ",agents[0].network_dissatisfaction())
print("Agent 0 has a personal dissatisfaction of {0}, an affected dissatisfaction of {1} and a difference of affected and its overall network {2}".format(agents[0].get_personal_dissatisfaction(),agents[0].get_affected_dissatisfaction(), agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New affected dissatisfaction of agent 0: ",agents[0].get_affected_dissatisfaction() )
#for i in range(len(agents)):
#    print(len(agents[i].friends))
>>>>>>> c39879808a29729f13032770397ecad3f0e59116

