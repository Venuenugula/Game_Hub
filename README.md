# AI Game Hub

A collection of classic games played against Reinforcement Learning agents.

## Games

### 1. Tic-Tac-Toe
- **Agent**: Q-Learning (Table-based).
- **Description**: The classic 3x3 game. The agent learns from its mistakes and becomes unbeatable.

### 2. Connect 4
- **Agent**: Deep Q-Network (DQN) with PyTorch.
- **Description**: A strategy game on a 7x6 grid. The agent uses a Convolutional Neural Network to evaluate board states.

## Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/Venuenugula/Game_Hub.git
    cd Game_Hub
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python app.py
    ```
4.  Open your browser and go to `http://127.0.0.1:5000`.

## Deployment

This project is ready for deployment on **Render**.
- `Procfile` and `render.yaml` are included.
- Ensure you select the **Python** environment.

## Project Structure

- `app.py`: Main Flask application (Game Hub).
- `agent.py`: Tic-Tac-Toe Q-Learning agent.
- `connect4_agent.py`: Connect 4 DQN agent.
- `connect4_game.py`: Connect 4 game logic.
- `game_utils.py`: Shared utilities.
- `templates/`: HTML files for the Hub and games.
