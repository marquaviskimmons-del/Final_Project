import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wayne Manor Private Table")
        self.root.geometry("700x600") 
        self.root.configure(bg="#1a3e1a")
        
        self.save_file = "savegame.json"
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.suits = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}
        
        # --- Load Save Data or Set Default ---
        self.money = self.load_game()

        self.alfred_quotes = {
            "start": "Care for a hand, Master Bruce? I’ve prepared the table.",
            "win": ["Splendid hand, sir. Shall I put the winnings toward the Batmobile's repairs?", 
                    "Precisely played, Master Bruce. Even the Joker couldn't read that face."],
            "loss": ["A temporary setback, sir. Even a Dark Knight must occasionally stumble.", 
                     "Perhaps we should stick to crime-fighting for the remainder of the evening?"],
            "tie": "A stalemate. Much like your encounters with Mr. Dent, I suppose.",
            "broke": "It seems the Wayne fortune has run dry. I'll go pack our bags for the poorhouse.",
            "save": "I have secured the ledgers, sir. Your progress is recorded."
        }

        # --- UI Elements ---
        self.alfred_frame = tk.Frame(root, bg="#222", bd=2, relief="sunken")
        self.alfred_frame.pack(fill="x", padx=20, pady=10)
        self.alfred_label = tk.Label(self.alfred_frame, text=f"ALFRED: {self.alfred_quotes['start']}", 
                                     font=("Georgia", 11, "italic"), bg="#222", fg="#e0e0e0", wraplength=600)
        self.alfred_label.pack(pady=10)

        self.balance_label = tk.Label(root, text=f"Wealth: ${self.money:,}", font=("Arial", 18, "bold"), bg="#1a3e1a", fg="#ffd700")
        self.balance_label.pack(pady=10)

        self.card_frame = tk.Frame(root, bg="#1a3e1a")
        self.card_frame.pack(pady=20)
        self.card_slots = []
        for i in range(5):
            lbl = tk.Label(self.card_frame, text="?", font=("Arial", 24, "bold"), width=5, height=3, relief="raised", bg="white")
            lbl.grid(row=0, column=i, padx=8)
            self.card_slots.append(lbl)

        self.info_label = tk.Label(root, text="Place your wager, sir.", font=("Arial", 12), bg="#1a3e1a", fg="white")
        self.info_label.pack()

        self.bet_entry = tk.Entry(root, font=("Arial", 14), width=10, justify='center')
        self.bet_entry.insert(0, "1000")
        self.bet_entry.pack(pady=5)

        # Buttons
        self.deal_btn = tk.Button(root, text="DEAL HAND", command=self.play_round, font=("Arial", 12, "bold"), bg="#ffd700", width=20)
        self.deal_btn.pack(pady=10)

        self.save_btn = tk.Button(root, text="SAVE & EXIT", command=self.save_and_quit, font=("Arial", 10), bg="#444", fg="white", width=15)
        self.save_btn.pack(pady=5)

    # --- Save/Load Logic ---
    def save_game(self):
        try:
            with open(self.save_file, "w") as f:
                json.dump({"money": self.money}, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save game: {e}")

    def load_game(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    return data.get("money", 10000000)
            except:
                return 10000000
        return 10000000

    def save_and_quit(self):
        self.save_game()
        messagebox.showinfo("Alfred", self.alfred_quotes["save"])
        self.root.destroy()

    def get_deck(self):
        deck = [(rank, suit) for rank in self.ranks for suit in self.suits.keys()]
        random.shuffle(deck)
        return deck

    def evaluate_hand(self, hand):
        vals = sorted([self.ranks.index(c[0]) for c in hand], reverse=True)
        hand_suits = [c[1] for c in hand]
        is_flush = len(set(hand_suits)) == 1
        is_straight = len(set(vals)) == 5 and (max(vals) - min(vals) == 4)
        counts = sorted([vals.count(v) for v in set(vals)], reverse=True)
        
        if is_flush and is_straight: return (8, "Straight Flush")
        if counts == [4, 1]: return (7, "Four of a Kind")
        if counts == [3, 2]: return (6, "Full House")
        if is_flush: return (5, "Flush")
        if is_straight: return (4, "Straight")
        if counts == [3, 1, 1]: return (3, "Three of a Kind")
        if counts == [2, 2, 1]: return (2, "Two Pair")
        if counts == [2, 1, 1, 1]: return (1, "One Pair")
        return (0, "High Card")

    def play_round(self):
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Alfred: 'I'm afraid that isn't a number, sir.'")
            return

        if bet > self.money:
            self.alfred_label.config(text="ALFRED: 'Master Bruce, your ambition outweighs your current liquidity.'")
            return
        if bet <= 0: return

        deck = self.get_deck()
        player_hand = [deck.pop() for _ in range(5)]
        cpu_hand = [deck.pop() for _ in range(5)]

        for i in range(5):
            rank, suit_key = player_hand[i]
            suit_symbol = self.suits[suit_key]
            color = "red" if suit_key in ['H', 'D'] else "black"
            self.card_slots[i].config(text=f"{rank}\n{suit_symbol}", fg=color)

        p_val, p_name = self.evaluate_hand(player_hand)
        c_val, c_name = self.evaluate_hand(cpu_hand)

        if p_val > c_val:
            self.money += bet
            comment = random.choice(self.alfred_quotes["win"])
            result_text = f"WINNER! {p_name} beats {c_name}"
        elif p_val < c_val:
            self.money -= bet
            comment = random.choice(self.alfred_quotes["loss"])
            result_text = f"LOSS! {c_name} beats your {p_name}"
        else:
            comment = self.alfred_quotes["tie"]
            result_text = f"TIE! Both held {p_name}"

        self.alfred_label.config(text=f"ALFRED: {comment}")
        self.balance_label.config(text=f"Wealth: ${self.money:,}")
        self.info_label.config(text=result_text)

        # Auto-save after every round so Bruce never loses his progress
        self.save_game()

        if self.money <= 0:
            if os.path.exists(self.save_file):
                os.remove(self.save_file) # Remove save if you go broke
            messagebox.showinfo("Bankruptcy", f"ALFRED: {self.alfred_quotes['broke']}")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = PokerGUI(root)
    root.mainloop()
