from game import Agent
from game import Directions
import random
import util

class ReflexAgent(Agent):
    def __init__(self):
        self.previous_positions = []

    def getAction(self, state):
        food = state.getFood()
        pacman_position = state.getPacmanPosition()
        legal_actions = state.getLegalPacmanActions()
        ghost_positions = state.getGhostPositions()

        if Directions.STOP in legal_actions:
            legal_actions.remove(Directions.STOP)

        if not food.asList():  
            if self.current_direction not in legal_actions:
                self.current_direction = random.choice(legal_actions)
            return self.current_direction

        best_direction = None
        min_distance = float('inf')

        for action in legal_actions:
            successor_state = state.generatePacmanSuccessor(action)
            successor_position = successor_state.getPacmanPosition()
            distance = self.getClosestFoodDistance(successor_position, food)
            if distance < min_distance and successor_position not in self.previous_positions:
                min_distance = distance
                best_direction = action

        for ghost_position in ghost_positions:
            if self.getGhostDistance(pacman_position, ghost_position) <= 3:
                legal_actions = [action for action in legal_actions if state.generatePacmanSuccessor(action).getPacmanPosition() != ghost_position]

        if best_direction is not None and best_direction in legal_actions:
            self.current_direction = best_direction
        elif self.current_direction in legal_actions:
            pass
        else:
            self.current_direction = random.choice(legal_actions)

        self.previous_positions.append(pacman_position)
        if len(self.previous_positions) > 10:  
            self.previous_positions.pop(0)

        return self.current_direction

    def getClosestFoodDistance(self, position, food):
        food_positions = food.asList()
        return min([util.manhattanDistance(position, food_pos) for food_pos in food_positions])

    def getGhostDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class BetterRandomAgent(Agent):
    def getAction(self, state):
        legal_actions = state.getLegalPacmanActions()
        if Directions.STOP in legal_actions:
            legal_actions.remove(Directions.STOP)
        return random.choice(legal_actions)

class RandomAgent(Agent):
    def getAction(self, state):
        random_numbers = [random.randint(1, 4) for _ in range(1)]
        randomKey = {1: 'WEST', 2: 'EAST', 3: 'SOUTH', 4: 'NORTH'}
        print(randomKey[random.randint(1, 4)])
        if randomKey[random.randint(1, 4)] == 'WEST' and Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        elif randomKey[random.randint(1, 4)] == 'SOUTH' and Directions.SOUTH in state.getLegalPacmanActions():
            return Directions.SOUTH
        elif randomKey[random.randint(1, 4)] == 'EAST' and Directions.EAST in state.getLegalPacmanActions():
            return Directions.EAST
        else:
            print("Stopping.")
            return Directions.STOP


class DumbAgent(Agent):
    "an agent that goes west until it can't"
    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        print("Location: ", state.getPacmanPosition())
        print("Actions available: ", state.getLegalPacmanActions())
        if Directions.SOUTH in state.getLegalPacmanActions():
            print("Going West.")
            return Directions.SOUTH
        else:
            print("Stopping.")
            return Directions.STOP

