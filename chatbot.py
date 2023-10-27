import tkinter as tk
import socket
from datetime import datetime
import time
import random
import re

from tkinter import messagebox



global clearText
clearText = ''
global bot_locked
bot_locked = False

global howtouse
howtouse = 'how', 'do', 'i', 'use', 'this'

global python_info
python_info = 'All you can do in Python here is print.'

# Bot responses
def bot_response(user_input):
    
    
    global bot_locked
    # If the bot is locked, below can run
    if "/unlock" in user_input:
        bot_locked = False
        return "The bot can now answer"
    
    elif "/clear" in user_input:
        return "SCROLL DOWN\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    
    user_input = user_input.lower()
    # Can't run:
    if bot_locked:
        return "The bot is currently locked!"
    
    elif user_input.startswith("python:"):
        try:
            exec(user_input.replace("python: ", ""))
            return "Python code executed successfully."
        except Exception as e:
            return f"Python code execution error: {str(e)}"
        
    elif 'hello' in user_input:
        return "Hello! I'm OzzyChat. Made by Ozzy, obviously."
    
    elif "ip" in user_input:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Your current IP is: {ip_address}"

    elif "internet" in user_input:
        if check_internet_connection():
                return "You have an active internet connection."
        else:
            return "You are not connected to the internet."

    elif "search" in user_input:
        query = user_input.replace("search", "").strip()
        if query:
            search_results = search(query)
            if search_results:
                return "Search Results:\n" + "\n".join(search_results)
            else:
                return "No search results found."

    elif "math" in user_input:
        try:
            result = str(eval(user_input.replace("math", "").replace("=", "")))
            return f"The result of the math operation is {result}."
        except:
            return "Sorry, I couldn't understand the math expression."
        
    elif 'use' in user_input:
        return "Please type '/?', to learn about OzzyChat!"
        
    elif "/?" in user_input:
        return "All info about OzzyBot: Lock feature, '/lock', '/unlock' to undo. /clear to clear. 'time' for bot to say the time. 'math' followed by problem to do math. Can run 1 line python. To run python, 'python:' followed by code. E.g: python:print('Hello World!')"

    elif "time" in user_input:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    elif "/exit" in user_input:
        root.destroy()
    
    elif "how" in user_input and "are" in user_input and "you" in user_input:
        return "Great! I'm called OzzyChat. Type 'info', to learn about me."

    elif user_input == 'info':
        return "You can ask me what time it is. I can do math, type 'math' followed by the problem. Type 'commands', to review all of the commands."
    
    elif "commands" in user_input:
            return "You can do '/exit' to destroy the window. You can use /lock to stop the bot from answering. You can do /unlock to unlock, locking the bot."
    
    elif user_input == '/lock':
        bot_locked = True
        return "The bot is now locked from answering. Type '/unlock' to undo."
    
    elif '/game' in user_input:
        def create_board():
            return [[' ' for _ in range(3)] for _ in range(3)]

    def check_win(board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True

        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def is_full(board):
        return all(board[i][j] != ' ' for i in range(3) for j in range(3))

    def minimax(board, depth, is_maximizing):
        scores = {
            'X': 1,
            'O': -1,
            'Tie': 0
        }

        if check_win(board, 'X'):
            return scores['X']
        if check_win(board, 'O'):
            return scores['O']
        if is_full(board):
            return scores['Tie']

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        eval = minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        eval = minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        min_eval = min(min_eval, eval)
            return min_eval

    def best_move(board):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, 0, False)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def update_board(row, col):
        if board[row][col] == ' ':
            buttons[row][col]['text'] = 'O'
            buttons[row][col]['state'] = 'disabled'
            board[row][col] = 'O'
            if check_win(board, 'O'):
                messagebox.showinfo("Tic Tac Toe", "You win!")
                reset_game()
                return
            if is_full(board):
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                reset_game()
                return

            ai_move = best_move(board)
            buttons[ai_move[0]][ai_move[1]]['text'] = 'X'
            buttons[ai_move[0]][ai_move[1]]['state'] = 'disabled'
            board[ai_move[0]][ai_move[1]] = 'X'
            if check_win(board, 'X'):
                messagebox.showinfo("Tic Tac Toe", "AI wins!")
                reset_game()
            elif is_full(board):
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                reset_game()

    def reset_game():
        for i in range(3):
            for j in range(3):
                buttons[i][j]['text'] = ' '
                buttons[i][j]['state'] = 'normal'
                board[i][j] = ' '

    window = tk.Tk()
    window.title("Unbeatable Tic Tac Toe AI")

    board = create_board()

    buttons = [[None, None, None] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(window, text=' ', font=('normal', 20), width=6, height=2,
                                    command=lambda row=i, col=j: update_board(row, col))
            buttons[i][j].grid(row=i, column=j)

    reset_button = tk.Button(window, text="Reset", font=('normal', 16), command=reset_game)
    reset_button.grid(row=3, column=0, columnspan=3)

    window.mainloop()

        
        
    
    responses = ["I'm not sure I understand. Can you rephrase that?", "Tell me more.", "That's interesting!"]
    return random.choice(responses)

# Function to check internet connection
def check_internet_connection():
    try:
        # Try to create a socket connection to a well-known website (e.g., Google)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

# Function to search for a query
def search(query):
    return []  # Modify this to perform a web search without requests if needed

# Function to send user messages and display bot responses
def send_message():
    user_message = entry.get()
    display_message(f"You: {user_message}")
    bot_reply = bot_response(user_message)
    display_message(f"Bot: {bot_reply}")
    entry.delete(0, tk.END)

# Function to display messages in the chat window
def display_message(message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + "\n")
    chat_history.config(state=tk.DISABLED)

def clear_chat():
    chat_history.delete(1.0, "end")

# Create the main window
root = tk.Tk()
root.title("ChatBot")
root.configure(bg='black')

# Create a chat history display area
chat_history = tk.Text(root, wrap=tk.WORD, width=40, height=10)
chat_history.config(state=tk.DISABLED)
chat_history.pack()

entry = tk.Entry(root, width=40)
entry.pack()

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Start the GUI event loop
root.mainloop()




