import tkinter as tk
from tkinter import messagebox
from collections import deque
import random

# ======================== Sudoku Solver Functions ========================
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in shuffle_numbers():
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def shuffle_numbers():
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    return numbers

def generate_sudoku(difficulty):
    if difficulty == "Easy":
        empty_cells = random.randint(40, 45)
    elif difficulty == "Medium":
        empty_cells = random.randint(46, 50)
    elif difficulty == "Hard":
        empty_cells = random.randint(56, 60)
    else:
        raise ValueError("Invalid difficulty level")

    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)

    for _ in range(empty_cells):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board

# ======================== Sudoku Game ========================
class SudokuSolverUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E1E")

        self.title_font = ("Helvetica", 24, "bold")
        self.button_font = ("Helvetica", 14)
        self.cell_font = ("Helvetica", 18)

        self.difficulty_var = tk.StringVar(value="Easy")
        self.create_difficulty_selector()

        self.cells = []
        self.create_sudoku_grid()

        self.create_buttons()

    def create_difficulty_selector(self):
        difficulty_frame = tk.Frame(self.root, bg="#1E1E1E")
        difficulty_frame.pack(pady=10)

        tk.Label(difficulty_frame, text="Difficulty:", font=self.button_font, bg="#1E1E1E", fg="#00FF00").pack(side=tk.LEFT, padx=5)

        difficulties = ["Easy", "Medium", "Hard"]
        for diff in difficulties:
            tk.Radiobutton(
                difficulty_frame, text=diff, variable=self.difficulty_var, value=diff,
                font=self.button_font, bg="#1E1E1E", fg="#00FF00", selectcolor="#333333"
            ).pack(side=tk.LEFT, padx=5)

    def create_sudoku_grid(self):
        grid_frame = tk.Frame(self.root, bg="#1E1E1E")
        grid_frame.pack(pady=10)

        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(
                    grid_frame, width=2, font=self.cell_font, justify='center',
                    bg="#333333", fg="#00FF00", relief="solid", borderwidth=1
                )
                cell.grid(row=i, column=j, padx=2, pady=2)
                if (i // 3 + j // 3) % 2 == 0:
                    cell.config(bg="#262626")
                row.append(cell)
            self.cells.append(row)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#1E1E1E")
        button_frame.pack(pady=10)

        buttons = [
            ("Check", self.check_solution),
            ("Solution", self.show_solution),
            ("New Puzzle", self.new_puzzle),
            ("Back to Menu", self.back_to_menu)
        ]

        for text, command in buttons:
            button = tk.Button(
                button_frame, text=text, font=self.button_font, command=command,
                bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0
            )
            button.pack(side=tk.LEFT, padx=5)
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#00FF00", fg="#1E1E1E"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#333333", fg="#00FF00"))

    def check_solution(self):
        user_board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()
                if value == "":
                    row.append(0)
                else:
                    try:
                        row.append(int(value))
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input. Please enter numbers only.")
                        return
            user_board.append(row)

        if user_board == self.solution:
            messagebox.showinfo("Success", "Congratulations! Your solution is correct.")
        else:
            messagebox.showerror("Error", "Your solution is incorrect. Please try again.")

    def show_solution(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].insert(0, str(self.solution[i][j]))
                self.cells[i][j].config(state='disabled', bg="#262626")

    def new_puzzle(self):
        self.difficulty = self.difficulty_var.get()
        self.board = generate_sudoku(self.difficulty)
        self.solution = [row[:] for row in self.board]
        solve_sudoku(self.solution)
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state='normal', bg="#333333")
                self.cells[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.board[i][j]))
                    self.cells[i][j].config(state='disabled', bg="#262626")

    def back_to_menu(self):
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

# ======================== Gomoku Game ========================
class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E1E")

        self.board_size = 15
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.game_over = False
        self.move_history = []

        # Track the player's first move
        self.player_first_move = None

        self.canvas = tk.Canvas(root, width=500, height=500, bg="#333333")
        self.canvas.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

        self.button_frame = tk.Frame(root, bg="#1E1E1E")
        self.button_frame.pack(pady=10)

        self.regret_button = tk.Button(self.button_frame, text="Regret", font=("Helvetica", 12), command=self.regret_move, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.regret_button.pack(side=tk.LEFT, padx=5)
        self.regret_button.bind("<Enter>", lambda e, b=self.regret_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.regret_button.bind("<Leave>", lambda e, b=self.regret_button: b.config(bg="#333333", fg="#00FF00"))

        self.restart_button = tk.Button(self.button_frame, text="Restart", font=("Helvetica", 12), command=self.restart_game, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        self.restart_button.bind("<Enter>", lambda e, b=self.restart_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.restart_button.bind("<Leave>", lambda e, b=self.restart_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_button = tk.Button(self.button_frame, text="Back to Menu", font=("Helvetica", 12), command=self.back_to_menu, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_button.pack(side=tk.LEFT, padx=5)
        self.back_button.bind("<Enter>", lambda e, b=self.back_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_button.bind("<Leave>", lambda e, b=self.back_button: b.config(bg="#333333", fg="#00FF00"))

    def draw_board(self):
        cell_size = 500 // self.board_size
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#333333", outline="#1E1E1E")

    def on_click(self, event):
        if self.game_over:
            return

        cell_size = 500 // self.board_size
        col = event.x // cell_size
        row = event.y // cell_size

        if self.board[row][col] == 0:
            # Player's move (Player 1)
            self.board[row][col] = 1
            self.move_history.append((row, col))
            self.draw_piece(row, col, 1)  # Draw black piece for player

            # Track the player's first move
            if self.player_first_move is None:
                self.player_first_move = (row, col)

            if self.check_win(row, col, 1):
                self.game_over = True
                messagebox.showinfo("Game Over", "You win!")
                return

            # Switch to AI's turn
            self.current_player = 2
            self.ai_move()

    def draw_piece(self, row, col, player):
        """
        Draw a piece on the board.
        - Player 1 (Human): Black
        - Player 2 (AI): White
        """
        cell_size = 500 // self.board_size
        x = col * cell_size + cell_size // 2
        y = row * cell_size + cell_size // 2
        color = "black" if player == 1 else "white"  # Player 1 = black, Player 2 = white
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline="#1E1E1E")

    def check_win(self, row, col, player):
        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Diagonal (top-left to bottom-right)
            (1, -1)  # Diagonal (top-right to bottom-left)
        ]

        for dr, dc in directions:
            count = 1
            for d in [-1, 1]:
                r, c = row + dr * d, col + dc * d
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == player:
                    count += 1
                    r += dr * d
                    c += dc * d
            if count >= 5:
                return True
        return False

    def find_open_four_move(self):
        """
        Find a move to block four pieces in a line with two adjacent empty slots by the player.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    # Check horizontal
                    if self.check_open_four(i, j, 0, 1):
                        return (i, j)
                    # Check vertical
                    if self.check_open_four(i, j, 1, 0):
                        return (i, j)
                    # Check diagonal (top-left to bottom-right)
                    if self.check_open_four(i, j, 1, 1):
                        return (i, j)
                    # Check diagonal (top-right to bottom-left)
                    if self.check_open_four(i, j, 1, -1):
                        return (i, j)
        return None

    def check_open_four(self, row, col, dr, dc):
        """
        Check if placing a piece at (row, col) blocks four pieces in a line with two adjacent empty slots.
        """
        # Check in both directions
        count = 1  # Current empty slot
        for d in [-1, 1]:
            r, c = row + dr * d, col + dc * d
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 1:
                count += 1
                r += dr * d
                c += dc * d
            # Check if the end is empty
            if not (0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 0):
                return False
        # If the total count is 4 (four in a row with two open ends), block it
        return count == 4

    def ai_move(self):
        if self.game_over:
            return

        # Step 1: Check if AI can win in the next move
        winning_move = self.find_winning_move(2)  # AI is player 2
        if winning_move:
            row, col = winning_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)  # Draw white piece for AI
            if self.check_win(row, col, 2):
                self.game_over = True
                messagebox.showinfo("Game Over", "AI wins!")
            return

        # Step 2: Check if the player is about to win and block them
        blocking_move = self.find_winning_move(1)  # Player is player 1
        if blocking_move:
            row, col = blocking_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)  # Draw white piece for AI
            return

        # Step 3: Check if the player has four pieces in a line with two adjacent empty slots and block it
        open_four_move = self.find_open_four_move()
        if open_four_move:
            row, col = open_four_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)  # Draw white piece for AI
            return

        # Step 4: If it's the AI's first move, place a piece near the player's first move
        if len(self.move_history) == 1:  # AI's first move
            row, col = self.player_first_move
            adjacent_moves = self.get_adjacent_positions(row, col)
            if adjacent_moves:
                move = random.choice(adjacent_moves)
                self.board[move[0]][move[1]] = 2
                self.move_history.append(move)
                self.draw_piece(move[0], move[1], 2)  # Draw white piece for AI
                return

        # Step 5: Create opportunities to win (e.g., multiple threats)
        strategic_move = self.find_strategic_move()
        if strategic_move:
            row, col = strategic_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)  # Draw white piece for AI
            return

        # Step 6: Prioritize moves near the player's pieces
        adjacent_move = self.find_adjacent_move()
        if adjacent_move:
            row, col = adjacent_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)
            return

        # Step 7: Fallback to a random move near existing pieces
        fallback_move = self.find_fallback_move()
        if fallback_move:
            row, col = fallback_move
            self.board[row][col] = 2
            self.move_history.append((row, col))
            self.draw_piece(row, col, 2)  # Draw white piece for AI
            return

    def get_adjacent_positions(self, row, col):
        """
        Get all adjacent positions to (row, col) that are empty.
        """
        adjacent_moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r, c = row + i, col + j
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 0:
                    adjacent_moves.append((r, c))
        return adjacent_moves

    def find_adjacent_move(self):
        """
        Find a move near the player's pieces.
        """
        player_positions = self.get_player_positions()
        adjacent_moves = set()

        for row, col in player_positions:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    r, c = row + i, col + j
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 0:
                        adjacent_moves.add((r, c))

        if adjacent_moves:
            return random.choice(list(adjacent_moves))
        return None

    def get_player_positions(self):
        """
        Get all positions occupied by the player (player 1).
        """
        positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    positions.append((i, j))
        return positions

    def find_winning_move(self, player):
        """
        Check if the specified player can win in the next move.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    self.board[i][j] = player
                    if self.check_win(i, j, player):
                        self.board[i][j] = 0
                        return (i, j)
                    self.board[i][j] = 0
        return None

    def find_strategic_move(self):
        """
        Find a move that creates multiple threats (e.g., multiple lines of three or four).
        """
        best_move = None
        best_score = -float('inf')

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    # Simulate placing a piece
                    self.board[i][j] = 2
                    score = self.evaluate_position(i, j, 2)
                    self.board[i][j] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

    def evaluate_position(self, row, col, player):
        """
        Evaluate the strength of a position for the given player.
        """
        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Diagonal (top-left to bottom-right)
            (1, -1)  # Diagonal (top-right to bottom-left)
        ]

        score = 0
        for dr, dc in directions:
            count = 1
            for d in [-1, 1]:
                r, c = row + dr * d, col + dc * d
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == player:
                    count += 1
                    r += dr * d
                    c += dc * d
            if count >= 5:
                score += 100000  # Winning move
            elif count == 4:
                score += 10000  # Four in a row
            elif count == 3:
                score += 1000  # Three in a row
            elif count == 2:
                score += 100  # Two in a row
        return score

    def find_fallback_move(self):
        """
        Find a move near existing pieces if no strategic move is found.
        """
        player_positions = self.get_player_positions()
        ai_positions = self.get_ai_positions()
        all_positions = player_positions + ai_positions

        adjacent_moves = set()
        for row, col in all_positions:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    r, c = row + i, col + j
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 0:
                        adjacent_moves.add((r, c))

        if adjacent_moves:
            return random.choice(list(adjacent_moves))
        else:
            # If no adjacent moves, pick a random move
            return random.choice(self.get_possible_moves(self.board))

    def get_player_positions(self):
        """
        Get all positions occupied by the player (player 1).
        """
        positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    positions.append((i, j))
        return positions

    def get_ai_positions(self):
        """
        Get all positions occupied by the AI (player 2).
        """
        positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 2:
                    positions.append((i, j))
        return positions

    def get_possible_moves(self, board):
        """
        Get all possible moves on the board.
        """
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def is_game_over(self, board):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] != 0:
                    if self.check_win(i, j, board[i][j]):
                        return True
        return False

    def regret_move(self):
        if self.game_over or len(self.move_history) < 2:
            return

        for _ in range(2):
            row, col = self.move_history.pop()
            self.board[row][col] = 0
            self.redraw_board()

        self.current_player = 1

    def redraw_board(self):
        self.canvas.delete("all")
        self.draw_board()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 0:
                    self.draw_piece(i, j, self.board[i][j])

    def restart_game(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.move_history = []
        self.current_player = 1
        self.game_over = False
        self.redraw_board()

    def back_to_menu(self):
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

# ======================== Snake Game ========================
class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("500x730")
        self.root.configure(bg="#1E1E1E")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="#333333")
        self.canvas.pack()

        self.after_id = None

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.walls = []
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.diy_mode = False
        self.paused = False
        self.speed = 100
        self.speed_var = tk.IntVar(value=self.speed)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Helvetica", 14), bg="#1E1E1E", fg="#00FF00")
        self.score_label.pack()

        self.create_mode_buttons()

        self.root.bind("<Up>", self.change_direction)
        self.root.bind("<Down>", self.change_direction)
        self.root.bind("<Left>", self.change_direction)
        self.root.bind("<Right>", self.change_direction)

    def set_speed(self):
        self.speed_label = tk.Label(self.root, text="Speed:", font=("Helvetica", 12), bg="#1E1E1E", fg="#00FF00")
        self.speed_label.pack()
        speed_slider = tk.Scale(self.root, from_=150, to=10, orient="horizontal", variable=self.speed_var, command=self.update_speed, bg="#333333", fg="#00FF00")
        speed_slider.pack()

    def create_mode_buttons(self):
        mode_frame = tk.Frame(self.root, bg="#1E1E1E")
        mode_frame.pack(pady=10)

        self.start_original_button = tk.Button(mode_frame, text="Original", font=("Helvetica", 12), command=self.start_original_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.start_original_button.pack(side=tk.LEFT, padx=5)
        self.start_original_button.bind("<Enter>", lambda e, b=self.start_original_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.start_original_button.bind("<Leave>", lambda e, b=self.start_original_button: b.config(bg="#333333", fg="#00FF00"))

        self.start_diy_button = tk.Button(mode_frame, text="DIY", font=("Helvetica", 12), command=self.start_diy_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.start_diy_button.pack(side=tk.LEFT, padx=5)
        self.start_diy_button.bind("<Enter>", lambda e, b=self.start_diy_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.start_diy_button.bind("<Leave>", lambda e, b=self.start_diy_button: b.config(bg="#333333", fg="#00FF00"))

        self.start_random_button = tk.Button(mode_frame, text="Infinite", font=("Helvetica", 12), command=self.start_random_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.start_random_button.pack(side=tk.LEFT, padx=5)
        self.start_random_button.bind("<Enter>", lambda e, b=self.start_random_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.start_random_button.bind("<Leave>", lambda e, b=self.start_random_button: b.config(bg="#333333", fg="#00FF00"))

    def generate_random_walls(self):
        self.walls = []
        self.canvas.delete("wall")

        num_walls = random.randint(40, 120)
        for _ in range(num_walls):
            x = random.randint(0, 49) * 10
            y = random.randint(0, 49) * 10
            if (x, y) not in self.walls and (x, y) not in self.snake:
                self.walls.append((x, y))

        self.ensure_connectivity()
        self.draw_walls()

    def ensure_connectivity(self):
        grid_size = 50
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        for wall in self.walls:
            x, y = wall
            grid[y // 10][x // 10] = 1

        for segment in self.snake:
            x, y = segment
            grid[y // 10][x // 10] = 1

        start_x, start_y = self.snake[0]
        start_x //= 10
        start_y //= 10

        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        queue = deque([(start_x, start_y)])
        visited[start_y][start_x] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if not visited[ny][nx] and grid[ny][nx] == 0:
                        visited[ny][nx] = True
                        queue.append((nx, ny))

        for y in range(grid_size):
            for x in range(grid_size):
                if not visited[y][x] and grid[y][x] == 0:
                    if self.walls:
                        wall_to_remove = random.choice(self.walls)
                        self.walls.remove(wall_to_remove)
                        grid[wall_to_remove[1] // 10][wall_to_remove[0] // 10] = 0

                        self.ensure_connectivity()
                        return

    def start_random_game(self):
        self.set_speed()
        self.diy_mode = False
        self.canvas.unbind("<Button-1>")
        self.create_random_game_buttons()
        self.draw_food()
        self.move_snake()

    def create_random_game_buttons(self):
        game_frame = tk.Frame(self.root, bg="#1E1E1E")
        game_frame.pack(pady=10)

        self.pause_button = tk.Button(game_frame, text="Pause", font=("Helvetica", 12), command=self.toggle_pause, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.bind("<Enter>", lambda e, b=self.pause_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.pause_button.bind("<Leave>", lambda e, b=self.pause_button: b.config(bg="#333333", fg="#00FF00"))

        self.restart_button = tk.Button(game_frame, text="Restart", font=("Helvetica", 12), command=self.restart_game, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        self.restart_button.bind("<Enter>", lambda e, b=self.restart_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.restart_button.bind("<Leave>", lambda e, b=self.restart_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_menu_button = tk.Button(game_frame, text="Main Menu", font=("Helvetica", 12), command=self.back_to_menu, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_menu_button.pack(side=tk.LEFT, padx=5)
        self.back_to_menu_button.bind("<Enter>", lambda e, b=self.back_to_menu_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_menu_button.bind("<Leave>", lambda e, b=self.back_to_menu_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_mode_button = tk.Button(game_frame, text="Mode", font=("Helvetica", 12), command=self.back_to_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_mode_button.pack(side=tk.LEFT, padx=5)
        self.back_to_mode_button.bind("<Enter>", lambda e, b=self.back_to_mode_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_mode_button.bind("<Leave>", lambda e, b=self.back_to_mode_button: b.config(bg="#333333", fg="#00FF00"))

        self.regenerate_button = tk.Button(game_frame, text="Regenerate", font=("Helvetica", 12), command=self.restart_random_game, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.regenerate_button.pack(side=tk.LEFT, padx=5)
        self.regenerate_button.bind("<Enter>", lambda e, b=self.regenerate_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.regenerate_button.bind("<Leave>", lambda e, b=self.regenerate_button: b.config(bg="#333333", fg="#00FF00"))

    def restart_random_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.generate_random_walls()
        self.score_label.config(text=f"Score: {self.score}")
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()
        self.draw_walls()

        if hasattr(self, "after_id"):
            self.root.after_cancel(self.after_id)

        self.move_snake()

    def start_random_mode(self):
        self.generate_random_walls()
        self.root.geometry("500x780")
        self.start_original_button.forget()
        self.start_diy_button.forget()
        self.start_random_button.forget()
        self.diy_mode = False

        self.start_random_game()

    def start_original_mode(self):
        self.start_original_button.forget()
        self.start_diy_button.forget()
        self.start_random_button.forget()
        self.diy_mode = False
        self.walls = []
        self.start_game()

    def start_diy_mode(self):
        self.root.geometry("500x780")
        self.start_original_button.forget()
        self.start_diy_button.forget()
        self.start_random_button.forget()

        self.diy_mode = True
        self.walls = []

        self.canvas.bind("<Button-1>", self.place_wall)
        self.create_diy_buttons()

    def create_diy_buttons(self):
        diy_frame = tk.Frame(self.root, bg="#1E1E1E")
        diy_frame.pack(pady=10)

        self.finish_design_button = tk.Button(diy_frame, text="Finish", font=("Helvetica", 12), command=self.diy_start_game, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.finish_design_button.pack(side=tk.LEFT, padx=5)
        self.finish_design_button.bind("<Enter>", lambda e, b=self.finish_design_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.finish_design_button.bind("<Leave>", lambda e, b=self.finish_design_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_mode_button = tk.Button(diy_frame, text="Mode", font=("Helvetica", 12), command=self.back_to_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_mode_button.pack(side=tk.LEFT, padx=5)
        self.back_to_mode_button.bind("<Enter>", lambda e, b=self.back_to_mode_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_mode_button.bind("<Leave>", lambda e, b=self.back_to_mode_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_menu_button = tk.Button(diy_frame, text="Main Menu", font=("Helvetica", 12), command=self.back_to_menu, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_menu_button.pack(side=tk.LEFT, padx=5)
        self.back_to_menu_button.bind("<Enter>", lambda e, b=self.back_to_menu_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_menu_button.bind("<Leave>", lambda e, b=self.back_to_menu_button: b.config(bg="#333333", fg="#00FF00"))

    def place_wall(self, event):
        if self.diy_mode:
            x = (event.x // 10) * 10
            y = (event.y // 10) * 10
            if (x, y) not in self.walls and (x, y) not in self.snake:
                self.walls.append((x, y))
                self.draw_walls()

    def diy_start_game(self):
        self.finish_design_button.forget()
        self.back_to_mode_button.forget()
        self.back_to_menu_button.forget()
        self.set_speed()
        self.diy_mode = False
        self.canvas.unbind("<Button-1>")
        self.create_game_buttons()
        self.draw_food()
        self.move_snake()

    def start_game(self):
        self.set_speed()
        self.diy_mode = False
        self.canvas.unbind("<Button-1>")
        self.create_game_buttons()
        self.draw_food()
        self.move_snake()

    def create_game_buttons(self):
        game_frame = tk.Frame(self.root, bg="#1E1E1E")
        game_frame.pack(pady=10)

        self.pause_button = tk.Button(game_frame, text="Pause", font=("Helvetica", 12), command=self.toggle_pause, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.bind("<Enter>", lambda e, b=self.pause_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.pause_button.bind("<Leave>", lambda e, b=self.pause_button: b.config(bg="#333333", fg="#00FF00"))

        self.restart_button = tk.Button(game_frame, text="Restart", font=("Helvetica", 12), command=self.restart_game, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        self.restart_button.bind("<Enter>", lambda e, b=self.restart_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.restart_button.bind("<Leave>", lambda e, b=self.restart_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_menu_button = tk.Button(game_frame, text="Main Menu", font=("Helvetica", 12), command=self.back_to_menu, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_menu_button.pack(side=tk.LEFT, padx=5)
        self.back_to_menu_button.bind("<Enter>", lambda e, b=self.back_to_menu_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_menu_button.bind("<Leave>", lambda e, b=self.back_to_menu_button: b.config(bg="#333333", fg="#00FF00"))

        self.back_to_mode_button = tk.Button(game_frame, text="Mode", font=("Helvetica", 12), command=self.back_to_mode, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
        self.back_to_mode_button.pack(side=tk.LEFT, padx=5)
        self.back_to_mode_button.bind("<Enter>", lambda e, b=self.back_to_mode_button: b.config(bg="#00FF00", fg="#1E1E1E"))
        self.back_to_mode_button.bind("<Leave>", lambda e, b=self.back_to_mode_button: b.config(bg="#333333", fg="#00FF00"))

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.move_snake()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y, z = self.food
        if z % 10 == 0:
            self.canvas.create_oval(x, y, x + 10, y + 10, fill="yellow", tags="food")
        else:
            self.canvas.create_oval(x, y, x + 10, y + 10, fill="red", tags="food")

    def draw_walls(self):
        self.canvas.delete("wall")
        for wall in self.walls:
            x, y = wall
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="gray", tags="wall")

    def create_food(self):
        while True:
            x = random.randint(0, 49) * 10
            y = random.randint(0, 49) * 10
            z = random.randint(0, 99) % 10
            if (x, y) not in self.snake and (x, y) not in self.walls:
                return (x, y, z)

    def move_snake(self):
        if self.game_over or self.paused:
            return

        head = self.snake[0]
        x, y = head

        if self.direction == "Up":
            y -= 10
        elif self.direction == "Down":
            y += 10
        elif self.direction == "Left":
            x -= 10
        elif self.direction == "Right":
            x += 10

        new_head = (x, y)

        if (
            x < 0 or x >= 500 or
            y < 0 or y >= 500 or
            new_head in self.snake or
            new_head in self.walls
        ):
            self.game_over = True
            messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
            return

        self.snake.insert(0, new_head)

        if new_head == self.food[:2]:
            if self.food[2] == 0:
                self.score += 10
            else:
                self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()

        self.after_id = self.root.after(self.speed, self.move_snake)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if (
                (event.keysym == "Up" and self.direction != "Down") or
                (event.keysym == "Down" and self.direction != "Up") or
                (event.keysym == "Left" and self.direction != "Right") or
                (event.keysym == "Right" and self.direction != "Left")
            ):
                self.direction = event.keysym

    def update_speed(self, value):
        self.speed = int(value)

    def restart_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.paused = False

        self.speed = 100
        self.speed_var.set(self.speed)

        self.score_label.config(text=f"Score: {self.score}")
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()
        self.draw_walls()

        if hasattr(self, "after_id"):
            self.root.after_cancel(self.after_id)

        self.move_snake()

    def back_to_menu(self):
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()

    def back_to_mode(self):
        self.root.destroy()
        root = tk.Tk()
        SnakeGame(root)
        root.mainloop()


class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game")
        self.root.configure(bg="#1E1E1E")

        self.maze_size = 15  # Default medium size
        self.cell_size = 30
        self.player_pos = (0, 0)
        self.exit_pos = (14, 14)
        self.walls = {}
        self.revealed = []  # Track revealed cells
        self.visited = set()  # Track visited cells

        # Mode selection frame
        mode_frame = tk.Frame(root, bg="#1E1E1E")
        mode_frame.pack(pady=10)

        self.mode_var = tk.StringVar(value="Medium")
        modes = [("Small", 15), ("Medium", 25), ("Large", 35)]

        for text, size in modes:
            btn = tk.Radiobutton(mode_frame, text=text, variable=self.mode_var, value=text,
                                 command=lambda s=size: self.set_maze_size(s),
                                 font=("Helvetica", 12), bg="#1E1E1E", fg="#00FF00", selectcolor="#333333")
            btn.pack(side=tk.LEFT, padx=5)

        # Maze canvas
        self.canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Control buttons
        button_frame = tk.Frame(root, bg="#1E1E1E")
        button_frame.pack(pady=10)

        self.new_game_btn = tk.Button(button_frame, text="New Game", command=self.new_game,
                                      bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat")
        self.new_game_btn.pack(side=tk.LEFT, padx=5)

        self.menu_btn = tk.Button(button_frame, text="Main Menu", command=self.back_to_menu,
                                  bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat")
        self.menu_btn.pack(side=tk.LEFT, padx=5)

        # Add hover effects
        for btn in [self.new_game_btn, self.menu_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#00FF00", fg="#1E1E1E"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#333333", fg="#00FF00"))

        self.root.bind("<KeyPress>", self.move_player)
        self.new_game()

    def set_maze_size(self, size):
        self.maze_size = size
        self.exit_pos = (size - 1, size - 1)
        self.new_game()

    def generate_maze(self):
        cells = [(col, row) for row in range(self.maze_size) for col in range(self.maze_size)]
        stack = []
        visited = set()
        self.walls = {(x, y): {'top': True, 'right': True, 'bottom': True, 'left': True}
                      for x in range(self.maze_size) for y in range(self.maze_size)}

        current = (0, 0)
        visited.add(current)

        while len(visited) < len(cells):
            neighbors = self.get_unvisited_neighbors(current, visited)
            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(current)
                self.remove_wall(current, next_cell)
                current = next_cell
                visited.add(current)
            elif stack:
                current = stack.pop()

        # Initialize revelation matrix and visited set
        self.revealed = [[False for _ in range(self.maze_size)] for _ in range(self.maze_size)]
        self.visited = set()
        self.update_vision(*self.player_pos)

    def get_unvisited_neighbors(self, cell, visited):
        x, y = cell
        neighbors = []
        directions = {
            'left': (x - 1, y),
            'right': (x + 1, y),
            'up': (x, y - 1),
            'down': (x, y + 1)
        }
        for dir, (nx, ny) in directions.items():
            if 0 <= nx < self.maze_size and 0 <= ny < self.maze_size and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        return neighbors

    def remove_wall(self, current, next_cell):
        x1, y1 = current
        x2, y2 = next_cell

        if x2 == x1 + 1:  # Right
            self.walls[current]['right'] = False
            self.walls[next_cell]['left'] = False
        elif x2 == x1 - 1:  # Left
            self.walls[current]['left'] = False
            self.walls[next_cell]['right'] = False
        elif y2 == y1 + 1:  # Down
            self.walls[current]['bottom'] = False
            self.walls[next_cell]['top'] = False
        elif y2 == y1 - 1:  # Up
            self.walls[current]['top'] = False
            self.walls[next_cell]['bottom'] = False

    def update_vision(self, x, y):
        # Reveal current cell and adjacent cells
        vision_radius = 2
        for dx in range(-vision_radius, vision_radius + 1):
            for dy in range(-vision_radius, vision_radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze_size and 0 <= ny < self.maze_size:
                    self.revealed[nx][ny] = True

        # Add current position to visited
        self.visited.add((x, y))

    def draw_maze(self):
        self.canvas.delete("all")
        cell_size = self.cell_size
        self.canvas.config(width=self.maze_size * cell_size,
                           height=self.maze_size * cell_size)

        # Draw walls only for revealed cells
        for (x, y), walls in self.walls.items():
            if not self.revealed[x][y]:
                continue

            x0 = x * cell_size
            y0 = y * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            if walls['top']:
                self.canvas.create_line(x0, y0, x1, y0, fill="#00FF00", width=2)
            if walls['right']:
                self.canvas.create_line(x1, y0, x1, y1, fill="#00FF00", width=2)
            if walls['bottom']:
                self.canvas.create_line(x0, y1, x1, y1, fill="#00FF00", width=2)
            if walls['left']:
                self.canvas.create_line(x0, y0, x0, y1, fill="#00FF00", width=2)

        # Draw exit if revealed
        exit_x, exit_y = self.exit_pos
        #if self.revealed[exit_x][exit_y]:
        self.canvas.create_rectangle(exit_x * cell_size + cell_size // 4,
                                         exit_y * cell_size + cell_size // 4,
                                         exit_x * cell_size + 3 * cell_size // 4,
                                         exit_y * cell_size + 3 * cell_size // 4,
                                         fill="red", outline="")

        # Draw player
        self.player = self.canvas.create_oval(
            self.player_pos[0] * cell_size + cell_size // 4,
            self.player_pos[1] * cell_size + cell_size // 4,
            self.player_pos[0] * cell_size + 3 * cell_size // 4,
            self.player_pos[1] * cell_size + 3 * cell_size // 4,
            fill="#00FF00", outline="")

        # Draw visited path
        #for x, y in self.visited:
            #self.canvas.create_rectangle(
                #x * cell_size + cell_size // 4,
                #y * cell_size + cell_size // 4,
                #x * cell_size + 3 * cell_size // 4,
                #y * cell_size + 3 * cell_size // 4,
                #fill="#003300", outline="")

    def move_player(self, event):
        old_x, old_y = self.player_pos
        new_x, new_y = old_x, old_y
        key = event.keysym
        moved = False

        if key == "Up" and not self.walls[(old_x, old_y)]['top']:
            new_y -= 1
            moved = True
        elif key == "Down" and not self.walls[(old_x, old_y)]['bottom']:
            new_y += 1
            moved = True
        elif key == "Left" and not self.walls[(old_x, old_y)]['left']:
            new_x -= 1
            moved = True
        elif key == "Right" and not self.walls[(old_x, old_y)]['right']:
            new_x += 1
            moved = True

        if moved and 0 <= new_x < self.maze_size and 0 <= new_y < self.maze_size:
            dx = (new_x - old_x) * self.cell_size
            dy = (new_y - old_y) * self.cell_size
            self.canvas.move(self.player, dx, dy)
            self.player_pos = (new_x, new_y)
            self.update_vision(new_x, new_y)
            self.draw_maze()

            if (new_x, new_y) == self.exit_pos:
                messagebox.showinfo("Congratulations!", "You escaped the maze!")
                self.new_game()

    def new_game(self):
        self.player_pos = (0, 0)
        self.generate_maze()
        self.draw_maze()
        self.canvas.focus_set()

    def back_to_menu(self):
        self.root.destroy()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()


# ======================== Main Menu ========================
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Menu")
        self.root.geometry("300x350")
        self.root.configure(bg="#1E1E1E")

        self.title_font = ("Helvetica", 24, "bold")
        self.button_font = ("Helvetica", 14)

        tk.Label(root, text="Choose a Game", font=self.title_font, bg="#1E1E1E", fg="#00FF00").pack(pady=20)

        games = [
            ("Sudoku", self.start_sudoku),
            ("Gomoku", self.start_gomoku),
            ("Snake Game", self.start_snake_game),
            ("Maze Game", self.start_maze_game)  # Add this line
        ]

        for text, command in games:
            button = tk.Button(root, text=text, font=self.button_font, command=command, bg="#333333", fg="#00FF00", padx=10, pady=5, relief="flat", bd=0)
            button.pack(pady=10)
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#00FF00", fg="#1E1E1E"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#333333", fg="#00FF00"))

    def start_sudoku(self):
        self.root.destroy()
        root = tk.Tk()
        SudokuSolverUI(root)
        root.mainloop()

    def start_gomoku(self):
        self.root.destroy()
        root = tk.Tk()
        GomokuGame(root)
        root.mainloop()

    def start_snake_game(self):
        self.root.destroy()
        root = tk.Tk()
        SnakeGame(root)
        root.mainloop()

    def start_maze_game(self):
        self.root.destroy()
        root = tk.Tk()
        MazeGame(root)
        root.mainloop()

# ======================== Main Program ========================
if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()
