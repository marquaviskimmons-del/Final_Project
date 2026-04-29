import tkinter as tk
from tkinter import messagebox
import random

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Poker GUI")
        self.root.geometry("600x450")
        self.root.configure(bg="#2e7d32") # Poker green background

        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.suits = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}
        self.money = 100

        # --- UI Elements ---
        self.balance_label = tk.Label(root, text=f"Balance: ${self.money}", font=("Arial", 18, "bold"), bg="#2e7d32", fg="white")
        self.balance_label.pack(pady=10)

        self.card_frame = tk.Frame(root, bg="#2e7d32")
        self.card_frame.pack(pady=30)

        self.card_slots = []
        for i in range(5):
            lbl = tk.Label(self.card_frame, text="?", font=("Arial", 24, "bold"), width=5, height=3, relief="raised", bg="white")
            lbl.grid(row=0, column=i, padx=10)
            self.card_slots.append(lbl)

        self.info_label = tk.Label(root, text="Enter bet and deal!", font=("Arial", 12), bg="#2e7d32", fg="white")
        self.info_label.pack()

        self.bet_entry = tk.Entry(root, font=("Arial", 14), width=10, justify='center')
        self.bet_entry.insert(0, "10")
        self.bet_entry.pack(pady=5)

        self.deal_btn = tk.Button(root, text="DEAL CARDS", command=self.play_round, font=("Arial", 14, "bold"), bg="#ffc107", width=15)
        self.deal_btn.pack(pady=20)

    def get_deck(self):
        deck = [(rank, suit) for rank in self.ranks for suit in self.suits.keys()]
        random.shuffle(deck)
        return deck

    def evaluate_hand(self, hand):
        # Value mapping for comparison
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
        # Validate Bet
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        if bet > self.money:
            messagebox.showwarning("Warning", "Insufficient funds!")
            return
        if bet <= 0: return

        # Deal Hands
        deck = self.get_deck()
        player_hand = [deck.pop() for _ in range(5)]
        cpu_hand = [deck.pop() for _ in range(5)]

        # Update Visuals
        for i in range(5):
            rank, suit_key = player_hand[i]
            suit_symbol = self.suits[suit_key]
            color = "red" if suit_key in ['H', 'D'] else "black"
            self.card_slots[i].config(text=f"{rank}\n{suit_symbol}", fg=color)

        # Determine Winner
        p_val, p_name = self.evaluate_hand(player_hand)
        c_val, c_name = self.evaluate_hand(cpu_hand)

        if p_val > c_val:
            self.money += bet
            msg = f"WINNER! You: {p_name} | CPU: {c_name}"
        elif p_val < c_val:
            self.money -= bet
            msg = f"LOST! You: {p_name} | CPU: {c_name}"
        else:
            msg = f"TIE! Both had {p_name}"

        # Refresh UI
        self.balance_label.config(text=f"Balance: ${self.money}")
        self.info_label.config(text=msg)

        if self.money <= 0:
            messagebox.showinfo("Game Over", "You're broke! House wins.")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = PokerGUI(root)
    root.mainloop()
