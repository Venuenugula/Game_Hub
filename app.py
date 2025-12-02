from flask import Flask, render_template, request, jsonify
from agent import QLearningAgent
from game_utils import validate_board, check_winner
from connect4_game import Connect4Game
from connect4_agent import DQNAgent
import logging
import os
import numpy as np

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize Agents
ttt_agent = QLearningAgent()
connect4_game = Connect4Game()
connect4_agent = DQNAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tictactoe")
def tictactoe():
    return render_template("tictactoe.html")

@app.route("/connect4")
def connect4():
    return render_template("connect4.html")

# --- Tic-Tac-Toe API ---

@app.route("/api/tictactoe/move", methods=["POST"])
def ttt_move():
    try:
        data = request.json
        board = data.get("board")
        if board is None or not validate_board(board):
            return jsonify({"error": "Invalid board state"}), 400

        board = [int(val) for val in board]
        winner = check_winner(board)
        if winner is not None:
            return jsonify({"board": board, "winner": winner})

        available = [i for i, val in enumerate(board) if val == 0]
        if not available:
             return jsonify({"board": board, "winner": 0})

        action = ttt_agent.choose_action(board, available)
        board[action] = 1
        winner = check_winner(board)
        return jsonify({"board": board, "winner": winner})
    except Exception as e:
        logging.error(f"TTT Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tictactoe/reset", methods=["POST"])
def ttt_reset():
    return jsonify({"message": "Game reset"})

# --- Connect 4 API ---

@app.route("/api/connect4/move", methods=["POST"])
def connect4_move():
    try:
        data = request.json
        col = data.get("col")
        if col is None or not (0 <= col < 7):
            return jsonify({"error": "Invalid column"}), 400

        # Player move (-1)
        if not connect4_game.make_move(col, -1):
             return jsonify({"error": "Invalid move"}), 400
        
        if connect4_game.winner is not None:
             return jsonify({"board": connect4_game.board.tolist(), "winner": connect4_game.winner})

        # Agent move (1)
        valid_moves = connect4_game.get_valid_moves()
        if not valid_moves:
             return jsonify({"board": connect4_game.board.tolist(), "winner": 0}) # Draw

        action = connect4_agent.act(connect4_game.board, valid_moves)
        connect4_game.make_move(action, 1)
        
        return jsonify({"board": connect4_game.board.tolist(), "winner": connect4_game.winner})

    except Exception as e:
        logging.error(f"Connect4 Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/connect4/reset", methods=["POST"])
def connect4_reset():
    connect4_game.reset()
    return jsonify({"message": "Game reset"})

@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
