import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import math

# Global variables

# how much each connection is affected per person
SELV = -30
CLOSE_FRIENDS_AF = -10
FRIENDS_AF = -1
NETWORK_AF = 0
PUBLIC_AF = 0  # yet to be determined

# Agent base level of dissatisfaction.
BASE_DISSATISFACTION = 100

# Agent's network size
NUMBER_OF_CLOSE_FRIENDS = 4
NUMBER_OF_FRIENDS = 10
NUMBER_OF_SOCIAL_NETWORK_FRIENDS = 30


class Agent:
    """Agent that interacts with agents in its network"""

    def __init__(self, personal_dissatisfaction, id):
        """
        Initialize an Agent object.

        :param personal_dissatisfaction: Initial personal dissatisfaction level of the agent.
        :param id: Unique identifier for the agent.
        """
        self.personal_dissatisfaction = personal_dissatisfaction
        self.close_friends = np.array([])
        self.friends = np.array([])
        self.network = np.array([])
        self.id = id
        self.affected_dissatisfaction = personal_dissatisfaction

    def get_personal_dissatisfaction(self):
        """
        Get the agent's personal dissatisfaction level.

        :return: Personal dissatisfaction level of the agent.
        """
        return self.personal_dissatisfaction

    def get_affected_dissatisfaction(self):
        """
        Get the agent's affected dissatisfaction level.

        :return: Affected dissatisfaction level of the agent.
        """
        return self.affected_dissatisfaction

    def set_affected_dissatisfaction(self,dissatisfaction):
        """
        Get the agent's affected dissatisfaction level.

        :return: Affected dissatisfaction level of the agent.
        """
        self.affected_dissatisfaction = dissatisfaction
    
    def get_close_friends(self):
        return self.close_friends
    def get_friends(self):
        return self.friends
    def get_network(self):
        return self.network
    
    def cap(self):
        # cap currently not used outside BLM
        if self.affected_dissatisfaction>100:
            self.affected_dissatisfaction = 100
        if self.affected_dissatisfaction<0:
            self.affected_dissatisfaction = 0


    def event_update_affected_dissatisfaction(self,amount):
        self.affected_dissatisfaction += amount[0]
        self.cap()
        for close_friend in self.close_friends:
            close_friend.set_affected_dissatisfaction(close_friend.get_affected_dissatisfaction() + amount[1])
            close_friend.cap()
        for friend in self.friends:
            friend.set_affected_dissatisfaction(friend.get_affected_dissatisfaction() + amount[2])
            friend.cap()
        for net_agent in self.network:
            net_agent.set_affected_dissatisfaction(net_agent.get_affected_dissatisfaction() + amount[3])
            net_agent.cap()
    
    def add_close_friend(self, close_friend):
        """
        Add a close friend to the agent's list of close friends.

        :param close_friend: Another agent considered a close friend.
        """
        self.close_friends = np.append(self.close_friends, close_friend)

    def add_friend(self, friend):
        """
        Add a friend to the agent's list of friends.

        :param friend: Another agent considered a friend.
        """
        self.friends = np.append(self.friends, friend)

    def add_to_network(self, network_friend):
        """
        Add an agent to the agent's network.

        :param network_friend: Another agent in the network.
        """
        self.network = np.append(self.network, network_friend)

    def close_friends_dissatisfaction(self):
        """
        Calculate the average dissatisfaction level of close friends.

        :return: The average dissatisfaction level of close friends.
        """
        average_friend_dis = 0
        for i in range(len(self.close_friends)):
            average_friend_dis += self.close_friends[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.close_friends)

    def friends_dissatisfaction(self):
        """
        Calculate the average dissatisfaction level of friends.

        :return: The average dissatisfaction level of friends.
        """
        average_friend_dis = 0
        for i in range(len(self.friends)):
            average_friend_dis += self.friends[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.friends)

    def network_dissatisfaction(self):
        """
        Calculate the average dissatisfaction level of network connections.

        :return: The average dissatisfaction level of network connections.
        """
        average_friend_dis = 0
        for i in range(len(self.network)):
            average_friend_dis += self.network[i].get_affected_dissatisfaction()
        return average_friend_dis / len(self.network)

    def dissatisfaction_distance(self):
        """
        Calculate the weighted average of dissatisfaction differences with different types of friends.

        :return: Weighted average of dissatisfaction differences.
        """
        weighted_average = (CLOSE_FRIENDS_AF * (
                self.close_friends_dissatisfaction() - self.affected_dissatisfaction) + FRIENDS_AF * (
                                    self.friends_dissatisfaction() - self.affected_dissatisfaction) + NETWORK_AF * (
                                    self.network_dissatisfaction() - self.affected_dissatisfaction)) / (
                                   CLOSE_FRIENDS_AF + FRIENDS_AF + NETWORK_AF)
        return weighted_average

    def update_dissatisfaction(self):
        """
        Update the agent's affected dissatisfaction level based on their social interactions.

        This method calculates a change in dissatisfaction level and applies it to the agent's affected dissatisfaction.

        It also includes random events where an agent can become "wild" or revert towards a base dissatisfaction level.

        :return: None
        """
        affect_rate = 2
        # change =  self.dissatisfaction_distance() * math.exp((self.dissatisfaction_distance / 100)-1)
        change = self.dissatisfaction_distance() ** 3 / 100 ** 2
        self.affected_dissatisfaction += change

        # Just to see:  give a 1/1000 possibility that one agent becomes wild, maximum dissatisfaction
        if rnd.randint(0, 100) <= 5:
            if self.affected_dissatisfaction != BASE_DISSATISFACTION:  # Note: 'BASE_DISSATISFACTION' is not defined in this code.
                self.affected_dissatisfaction += (BASE_DISSATISFACTION - self.affected_dissatisfaction) / 10
        if rnd.randint(0, 100) <= 3:
            if self.affected_dissatisfaction != 0:
                self.affected_dissatisfaction -= self.affected_dissatisfaction / 10


def event(tick):
    if tick % 7 == 0:
        affect = (rnd.randint(-7, 7) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))
    if tick % 29 == 0:
        affect = (rnd.randint(-29, 29) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))
    if tick % 89 == 0:
        affect = (rnd.randint(-89, 89) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))
    return affect

def per_group(dissatisfaction):
    affect = np.array([0,0,0,0,0])
    if dissatisfaction[0]:
        affect[0] += (rnd.randint(-30, 30) * SELV)
    if dissatisfaction[1]:
        affect[1] += (rnd.randint(-20, 20) * CLOSE_FRIENDS_AF)
    if dissatisfaction[2]:
        affect[2] += (rnd.randint(-10, 10) * FRIENDS_AF)
    if dissatisfaction[3]:
        affect[3] += (rnd.randint(-5, 5) * NETWORK_AF)
    if dissatisfaction[4]:
        affect[4] += (rnd.randint(-1, 1) * PUBLIC_AF)
    return affect

def BLM_simulation(agents):
    """
    Simulate the evolution of agent dissatisfaction over time.

    Args:
    agents (np.array): An array of Agent objects.

    Returns:
    list: A list of dissatisfaction values for each iteration.
    """
    iterations = 3285 # 9 years
    dissatisfaction = []

    for tick in range(iterations):
        if tick%365 == 0 :
            print(tick/365 + 2013,"year")
        dissatisfaction_update = BLM_even_list(tick)
        if dissatisfaction_update != [0, 0, 0, 0, 0]:
            rng_agent = agents[rnd.randint(0, agents.size-1)]
            rng_agent.event_update_affected_dissatisfaction(dissatisfaction_update)
            for agent in agents:
                agent.set_affected_dissatisfaction(agent.get_affected_dissatisfaction() + dissatisfaction_update[4])
            print(dissatisfaction_update, " ",tick)

        dissatisfaction.append(average_total_dissatisfaction(agents))
        for agent in agents:
            agent.update_dissatisfaction()

    return dissatisfaction

def BLM_even_list(tick):
    dissatisfaction = [0,0,0,0,0]
    if tick<365:              #2013-2014
        if 0 == rnd.randint(0,30): # 12 deaths 
            dissatisfaction = [100,100,70,10,1]
        if tick == 240: # one 500 african american protest
            dissatisfaction[4] += 1

    if tick>=365 and tick<730:#2014-2015
        if 0 == rnd.randint(0,24): # 15 deaths 
            dissatisfaction = [100,100,70,10,1]
        if 0 == rnd.randint(0,36): # 10 protests 
            dissatisfaction[4] += 1

    if tick>=730 and tick<1095:#2015-2016
        if 0 == rnd.randint(0,33): # 15 deaths 
            dissatisfaction = [100,100,70,10,1]
        if tick == 760: # hundreads of protests in january 
            dissatisfaction[4] += 15
     
    if tick>=1095 and tick<1460:#2016-2017
        if 0 == rnd.randint(0,365): # 1 death 
            dissatisfaction = [100,100,70,10,1]
        if tick == 1200: # month long BLM art exhibition 
            dissatisfaction[4] += 10
        if tick == 1300: # protest
            dissatisfaction[4] += 1
    if tick>=1460 and tick<1825:#2017-2018
        if 0 == rnd.randint(0,182): # 2 deaths 
            dissatisfaction = [100,100,70,10,1]
        if tick == 1700: # BLM fb page scam
            dissatisfaction[4] -= 5

    if tick>=1825 and tick<2190: #2018-2019 no data  
        None
    
    if tick>=2190 and tick<2555: #2019-2020
        if 0 == rnd.randint(0,182): # 2 deaths 
            dissatisfaction = [100,100,70,10,1]
        if tick == 2330: # George Floyd protests (450 major protests)
            dissatisfaction[4] += 40
        if tick == 2400: # Goverment intrvention
            dissatisfaction[4] -= 60

    if tick>=2555: #2020-2023
         if 0 == rnd.randint(0,182): # court cases settlements about BLM deaths
            dissatisfaction = [-100,-100,-70,-10,-1]
    return dissatisfaction



def create_agents_0(amount):
    """
    Create an array of Agent objects.

    Returns:
    np.array: An array of Agent objects.
    """
    agents = np.array([])
    for i in range(amount):
        agents = np.append(agents, Agent(0, i))
    return agents

def create_agents():
    """
    Create an array of Agent objects.

    Returns:
    np.array: An array of Agent objects.
    """
    agents = np.array([])
    for i in range(100):
        agents = np.append(agents, Agent(rnd.randint(0, BASE_DISSATISFACTION), i))
    return agents


def create_close_friendships(agents):
    """
    Establish close friendships among agents.

    Args:
    agents (np.array): An array of Agent objects.
    """
    for i in range(int(agents.size/4)):
        close_friendgroup = np.array([agents[0 + i * 4], agents[1 + i * 4], agents[2 + i * 4], agents[3 + i * 4]])
        for j in range(4):
            agents[(j + i * 4)].add_close_friend(np.array([agents[(k + i * 4)] for k in range(4) if k != j]))


def create_friendships(agents):
    """
    Establish friendships among agents.

    Args:
    agents (np.array): An array of Agent objects.
    """
    for i in range(agents.size):
        while len(agents[i].friends) != NUMBER_OF_FRIENDS:
            current_agent = agents[rnd.randint(0, 99)]
            if not (np.any(agents[i].close_friends == current_agent)) and not (
            np.any(agents[i].friends == current_agent)):
                agents[i].friends = np.append(agents[i].friends, current_agent)


def create_networks(agents):
    """
    Establish social networks among agents.

    Args:
    agents (np.array): An array of Agent objects.
    """
    for i in range(agents.size):
        while len(agents[i].network) != NUMBER_OF_SOCIAL_NETWORK_FRIENDS:
            current_agent = agents[rnd.randint(0, agents.size-1)]
            if not (np.any(agents[i].close_friends == current_agent)) and not (
                    np.any(agents[i].friends == current_agent) and not (np.any(agents[i].network == current_agent))):
                agents[i].network = np.append(agents[i].network, current_agent)


def average_total_dissatisfaction(agents):
    """
    Calculate the average total dissatisfaction of agents.

    Args:
    agents (np.array): An array of Agent objects.

    Returns:
    float: The average total dissatisfaction.
    """
    total = 0
    for agent in agents:
        total += agent.get_affected_dissatisfaction()
    average = total / len(agents)
    return average


def run_simulation(agents):
    """
    Simulate the evolution of agent dissatisfaction over time.

    Args:
    agents (np.array): An array of Agent objects.

    Returns:
    list: A list of dissatisfaction values for each iteration.
    """
    iterations = 5000
    dissatisfaction = []

    for j in range(iterations):
        if j%50 == 0 :
            print(j/50,"%")

        dissatisfaction.append(average_total_dissatisfaction(agents))


        for agent in agents:
            agent.update_dissatisfaction()

    return dissatisfaction


def print_agent_information(agent):
    """
    Print information about an agent's dissatisfaction.

    :param agent: The Agent object whose information will be printed.
    """
    print("Close friends average dissatisfaction: ", agent.close_friends_dissatisfaction())
    print("Friends average dissatisfaction: ", agent.friends_dissatisfaction())
    print("Network average dissatisfaction: ", agent.network_dissatisfaction())
    print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agent.get_affected_dissatisfaction(),
                                                                              agent.dissatisfaction_distance()))
    agent.update_dissatisfaction()
    print("New dissatisfaction: ", agent.get_affected_dissatisfaction())


def plot_dissatisfaction(dissatisfaction):
    """
    Plot the average dissatisfaction over iterations.

    :param dissatisfaction: An array containing the average dissatisfaction at each iteration.
    """
    plt.plot(dissatisfaction)
    plt.xlabel("Number of Iterations")
    plt.ylabel("Average Dissatisfaction")
    plt.show()


def main():
    agents = create_agents_0(1000)
    create_close_friendships(agents)
    create_friendships(agents)
    create_networks(agents)

    # Print information about the first agent
    print_agent_information(agents[0])
    print(average_total_dissatisfaction(agents))

    dissatisfaction = BLM_simulation(agents)

    # Print information about the first agent again after running the simulation
    print_agent_information(agents[0])
    print(average_total_dissatisfaction(agents))

    plot_dissatisfaction(dissatisfaction)


if __name__ == "__main__":
    main()
