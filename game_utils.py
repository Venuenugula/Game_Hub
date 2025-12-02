import logging

def validate_board(board):
    """
    Validates the board structure and values.
    """
    if not isinstance(board, list):
        logging.error(f"Board is not a list: {board} (type: {type(board)})")
        return False
    if len(board) != 9:
        logging.error(f"Board length is not 9: {len(board)}")
        return False
    try:
        # Convert board values to integers
        board_converted = [int(val) for val in board]
        if not all(val in [0, 1, -1] for val in board_converted):
            logging.error(f"Board contains invalid values: {board_converted}")
            return False
        return True
    except (ValueError, TypeError) as e:
        logging.error(f"Failed to convert board values to integers: {board}, Error: {str(e)}")
        return False

def check_winner(board):
    """
    Checks for a winner on the board.
    Returns:
        1: Agent wins
        2: Player wins (mapped from -1 internally if needed, but logic usually uses -1 for O)
        # Wait, the original app.py returned 2 for player win (-3 sum).
        # Let's stick to the logic: 1 for Agent (X), -1 for Player (O), 0 for Draw, None for ongoing.
        # However, the original app.py returned:
        # 1 -> Agent wins
        # 2 -> Player wins
        # 0 -> Draw
        # None -> No winner
        
        Let's standardize this.
        Agent (1) -> Sum 3
        Player (-1) -> Sum -3
    """
    combos = [
        [0,1,2], [3,4,5], [6,7,8],  # Rows
        [0,3,6], [1,4,7], [2,5,8],  # Columns
        [0,4,8], [2,4,6]            # Diagonals
    ]
    for combo in combos:
        s = sum([board[i] for i in combo])
        if s == 3:
            return 1   # Agent wins
        if s == -3:
            return 2   # Player wins
    if 0 not in board:
        return 0   # Draw
    return None    # No winner yet
