import numpy as np

class Connect4Game:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.winner = None

    def reset(self):
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.winner = None
        return self.board

    def get_valid_moves(self):
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def make_move(self, col, player):
        """
        Player: 1 (AI), -1 (Human)
        """
        if self.winner is not None:
            return False
        
        if col not in self.get_valid_moves():
            return False

        # Find the lowest empty row in the column
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = player
                self.check_winner(r, col, player)
                return True
        return False

    def check_winner(self, r, c, player):
        # Check horizontal
        for i in range(max(0, c - 3), min(self.cols - 3, c) + 1):
            if all(self.board[r][i+k] == player for k in range(4)):
                self.winner = player
                return

        # Check vertical
        if r <= self.rows - 4:
            if all(self.board[r+k][c] == player for k in range(4)):
                self.winner = player
                return

        # Check diagonal (top-left to bottom-right)
        for k in range(-3, 1):
            if 0 <= r+k <= self.rows-4 and 0 <= c+k <= self.cols-4:
                if all(self.board[r+k+i][c+k+i] == player for i in range(4)):
                    self.winner = player
                    return

        # Check anti-diagonal (top-right to bottom-left)
        for k in range(-3, 1):
            if 0 <= r+k <= self.rows-4 and 3 <= c-k < self.cols:
                if all(self.board[r+k+i][c-k-i] == player for i in range(4)):
                    self.winner = player
                    return
        
        if len(self.get_valid_moves()) == 0:
            self.winner = 0 # Draw
