import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import os

class DQN(nn.Module):
    def __init__(self, rows, cols, output_size):
        super(DQN, self).__init__()
        self.rows = rows
        self.cols = cols
        
        # Simple CNN for board state
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * rows * cols, 128)
        self.fc2 = nn.Linear(128, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 1, self.rows, self.cols) # (Batch, Channel, H, W)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1) # Flatten
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class DQNAgent:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.action_size = cols
        self.device = torch.device("cpu") # Use CPU for inference
        self.model = DQN(rows, cols, self.action_size).to(self.device)
        self.model_path = os.path.join(os.path.dirname(__file__), "connect4_dqn.pth")
        
        # Load pre-trained model if exists, otherwise random initialization
        if os.path.exists(self.model_path):
            try:
                self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                self.model.eval()
            except Exception as e:
                print(f"Failed to load model: {e}")

    def act(self, board, valid_moves):
        # Epsilon-greedy not needed for inference, just take best valid move
        # But maybe add small noise for variety? No, let's be deterministic for now.
        
        state = torch.FloatTensor(board).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state)
        
        q_values = q_values.cpu().numpy()[0]
        
        # Mask invalid moves
        for col in range(self.cols):
            if col not in valid_moves:
                q_values[col] = -float('inf')
        
        return int(np.argmax(q_values))

    def save(self):
        torch.save(self.model.state_dict(), self.model_path)
