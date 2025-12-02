import random
import pickle
import os
import numpy as np
from game_utils import check_winner

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}  # Maps state (tuple) to action values
        # Use absolute path or relative to this file to avoid CWD issues
        self.q_table_file = os.path.join(os.path.dirname(__file__), "q_table.pkl")
        self.load_q_table()

    def state_to_tuple(self, board):
        return tuple(board)

    def choose_action(self, board, available):
        state = self.state_to_tuple(board)
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in available}

        if random.random() < self.epsilon:
            return random.choice(available)  # Explore
        else:
            q_values = self.q_table[state]
            # Filter q_values to only include available actions
            available_q_values = {a: q for a, q in q_values.items() if a in available}
            if not available_q_values:
                 return random.choice(available)
            max_q = max(available_q_values.values())
            best_actions = [a for a, q in available_q_values.items() if q == max_q]
            return random.choice(best_actions)  # Exploit

    def update(self, state, action, reward, next_state, next_available):
        state = self.state_to_tuple(state)
        next_state = self.state_to_tuple(next_state)
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in next_available}

        current_q = self.q_table[state].get(action, 0)
        max_next_q = max(self.q_table[next_state].values()) if next_available and self.q_table[next_state] else 0
        
        if action not in self.q_table[state]:
             self.q_table[state][action] = 0
             
        self.q_table[state][action] += self.alpha * (
            reward + self.gamma * max_next_q - current_q
        )

    def save_q_table(self):
        with open(self.q_table_file, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, "rb") as f:
                self.q_table = pickle.load(f)

    def train(self, episodes=10000):
        # check_winner is now imported from game_utils
        # But wait, game_utils check_winner returns 2 for player win, 
        # while the original train loop expected -1.
        # Let's adjust the train loop to handle the new return values.
        # 1 -> Agent wins (Reward 1)
        # 2 -> Player wins (Reward -1)
        # 0 -> Draw (Reward 0)

        for episode in range(episodes):
            board = [0] * 9
            while True:
                available = [i for i, val in enumerate(board) if val == 0]
                if not available:
                    break

                # Agent's move
                action = self.choose_action(board, available)
                next_board = board.copy()
                next_board[action] = 1
                winner = check_winner(next_board)

                # Reward
                if winner == 1:
                    reward = 1
                    self.update(board, action, reward, next_board, [])
                    break
                elif winner == 0:
                    reward = 0
                    self.update(board, action, reward, next_board, [])
                    break
                
                # If winner is 2 (Player wins), that shouldn't happen immediately after agent move unless agent made a losing move?
                # No, agent moves, checks winner. If agent wins, done.
                
                # Random opponent's move
                available = [i for i, val in enumerate(next_board) if val == 0]
                if available:
                    opponent_action = random.choice(available)
                    next_board[opponent_action] = -1
                    winner = check_winner(next_board)
                    if winner == 2: # Player wins
                        reward = -1
                        self.update(board, action, reward, next_board, [])
                        break
                    elif winner == 0:
                        reward = 0
                        self.update(board, action, reward, next_board, [])
                        break
                    else:
                        reward = 0 # Game continues

                self.update(board, action, reward, next_board, available)
                board = next_board

            if episode % 1000 == 0:
                print(f"Episode {episode} completed")
                self.save_q_table()

        self.save_q_table()
        print("Training completed")

if __name__ == "__main__":
    agent = QLearningAgent()
    agent.train(episodes=1000000)
    
    
