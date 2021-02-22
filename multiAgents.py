#Since there is only one Pacman_Agent (agent0) out of all agents in the game
        #number of ghosts will be numAgents - 1
        num_of_agents = gameState.getNumAgents()
        num_of_ghosts = num_of_agents - 1
        pacman_agent_index = 0

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        def minimaxFunc(gameState, agent_index, depth):
            optimal_action = None
            if agent_index == 0 and depth == self.depth:
                return None, self.evaluationFunction(gameState)
            elif agent_index == 0:
                optimal_value = float("-inf")
            else:
                optimal_value = float("inf")

            if agent_index == num_of_ghosts:
                depth = depth + 1

            for action in gameState.getLegalActions(agent_index):
                next_action, nextValue = minimaxFunc(gameState.generateSuccessor(agent_index, action), depth, agent_index % (num_of_agents-1))

                if agent_index > 0:
                    if nextValue < optimal_value:
                        _, optimal_action = nextValue, action
                else:
                    if(agent_index == 0):
                        if nextValue > optimal_value:
                            optimal_value, optimal_action = nextValue, action
                    else:
                        print("agent index cannot be less than zero")
            return optimal_action, optimal_value
        return minimaxFunc(gameState, 0, pacman_agent_index)
