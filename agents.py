import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import math

# Global variables

# how much each connection is affected per person
CLOSE_FRIENDS_AF = -10
FRIENDS_AF = -1
NETWORK_AF = 0
PUBLIC_AF = None  # yet to be determined

# Agent base level of dissatisfaction.
BASE_DISSATISFACTION = 100

# Agent's network size
NUMBER_OF_CLOSE_FRIENDS = 4
NUMBER_OF_FRIENDS = 10
NUMBER_OF_SOCIAL_NETWORK_FRIENDS = 30

class Agent:
    class Agent:
        """Agent that interacts with agents in its network. """

        def __init__(self, personal_dissatisfaction, id):
            """
            Initialize an Agent object.

            :param personal_dissatisfaction: Initial personal dissatisfaction level of the agent.
            :param close_friends:
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
        return (rnd.randint(-7, 7) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))
    if tick % 30 == 0:
        return (rnd.randint(-30, 30) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))
    if tick % 90 == 0:
        return (rnd.randint(-90, 90) * np.array([CLOSE_FRIENDS_AF, FRIENDS_AF, NETWORK_AF, PUBLIC_AF]))


agents = np.array([])

for i in range(100):
    agents = np.append(agents, Agent(rnd.randint(0, BASE_DISSATISFACTION), i))

for i in range(25):
    close_friendgroup = np.array([agents[0 + i * 4], agents[1 + i * 4], agents[2 + i * 4], agents[3 + i * 4]])
    agents[(0 + i * 4)].add_close_friend(np.array([agents[1 + i * 4], agents[2 + i * 4], agents[3 + i * 4]]))
    agents[(1 + i * 4)].add_close_friend(np.array([agents[0 + i * 4], agents[2 + i * 4], agents[3 + i * 4]]))
    agents[(2 + i * 4)].add_close_friend(np.array([agents[0 + i * 4], agents[1 + i * 4], agents[3 + i * 4]]))
    agents[(3 + i * 4)].add_close_friend(np.array([agents[0 + i * 4], agents[1 + i * 4], agents[2 + i * 4]]))

for i in range(100):
    while len(agents[i].friends) != NUMBER_OF_FRIENDS:
        current_agent = agents[rnd.randint(0, 99)]
        if not (np.any(agents[i].close_friends == current_agent)) and not (np.any(agents[i].friends == current_agent)):
            agents[i].friends = np.append(agents[i].friends, current_agent)
    while len(agents[i].network) != NUMBER_OF_SOCIAL_NETWORK_FRIENDS:
        current_agent = agents[rnd.randint(0, 99)]
        if not (np.any(agents[i].close_friends == current_agent)) and not (
                np.any(agents[i].friends == current_agent) and not (np.any(agents[i].network == current_agent))):
            agents[i].network = np.append(agents[i].network, current_agent)


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


print("Close friends average dissatisfaction: ", agents[0].close_friends_dissatisfaction())
print("Friends average dissatisfaction: ", agents[0].friends_dissatisfaction())
print("Network average dissatisfaction: ", agents[0].network_dissatisfaction())
print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_affected_dissatisfaction(),
                                                                          agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New dissatisfaction: ", agents[0].get_affected_dissatisfaction())
print(average_total_dissatisfaction(agents))
run(agents)
print("Close friends average dissatisfaction: ", agents[0].close_friends_dissatisfaction())
print("Friends average dissatisfaction: ", agents[0].friends_dissatisfaction())
print("Network average dissatisfaction: ", agents[0].network_dissatisfaction())
print("Agent has a dissatisfaction of {0} and a difference of {1}".format(agents[0].get_affected_dissatisfaction(),
                                                                          agents[0].dissatisfaction_distance()))
agents[0].update_dissatisfaction()
print("New dissatisfaction: ", agents[0].get_affected_dissatisfaction())
print(average_total_dissatisfaction(agents))
plt.plot(dissatisfaction)
plt.xlabel("Number of Iterations")
plt.ylabel("Average Dissatisfaction")
plt.show()
