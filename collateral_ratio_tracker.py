import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Define ratio calculation
def compute_ratios(l_amt, c_val, t):
    dates = pd.date_range(start="2023-01-01", end="2025-03-06", freq="ME")
    periods = min(t, len(dates))
    loan_vals = np.linspace(l_amt, l_amt * 0.9, periods)  # Gradual loan reduction
    coll_vals = np.linspace(c_val, c_val * 0.95, periods)  # Slight collateral decline
    df = pd.DataFrame({"Loan": loan_vals, "Collateral": coll_vals}, index=dates[:periods])
    return df["Collateral"] / df["Loan"]

# Step 2: Define breach detection
def detect_breaches(rat, th):
    return rat[rat < th].index

# Step 3: Define GUI update logic
def refresh_gui():
    try:
        l_amt = float(e1.get())  # Loan amount
        c_val = float(e2.get())  # Collateral value
        t = int(e3.get())  # Periods
        th = float(e4.get())  # Threshold

        # Step 4: Validate inputs
        if l_amt <= 0 or c_val <= 0 or t <= 0 or th <= 0:
            raise ValueError("All inputs must be positive")

        # Step 5: Compute ratios and breaches
        rat = compute_ratios(l_amt, c_val, t)
        breach_dates = detect_breaches(rat, th)
        lbl_avg.config(text=f"Avg Ratio: {rat.mean():.4f}")

        # Step 6: Update plot
        ax.clear()
        ax.plot(rat.index, rat, color="#FF6B6B", lw=2, label="Coverage Ratio")
        ax.axhline(th, color="#4ECDC4", ls="--", alpha=0.6, label=f"Threshold={th}")
        if len(breach_dates) > 0:
            ax.plot(breach_dates, rat[breach_dates], "o", color="#FF6B6B", ms=8, label="Breaches")
        ax.set_xlabel("Date", color="white")
        ax.set_ylabel("Ratio", color="white")
        ax.set_title("Collateral Coverage Ratio", color="white")
        ax.set_facecolor("#2B2B2B")
        fig.set_facecolor("#1E1E1E")
        ax.grid(True, ls="--", color="#555555", alpha=0.5)
        ax.legend(facecolor="#333333", edgecolor="white", labelcolor="white")
        ax.tick_params(colors="white")
        canv.draw()

    except ValueError as err:
        messagebox.showerror("Error", str(err))

# Step 7: Initialize GUI
root = tk.Tk()
root.title("Collateral Ratio Tracker")
root.configure(bg="#1E1E1E")

frm = ttk.Frame(root, padding=10)
frm.pack()
frm.configure(style="Dark.TFrame")

# Step 8: Set up plot
fig, ax = plt.subplots(figsize=(7, 5))
canv = FigureCanvasTkAgg(fig, master=frm)
canv.get_tk_widget().pack(side=tk.LEFT)

# Step 9: Build input panel
pf = ttk.Frame(frm)
pf.pack(side=tk.RIGHT, padx=10)
pf.configure(style="Dark.TFrame")

# Dark theme styling
style = ttk.Style()
style.theme_use("default")
style.configure("Dark.TFrame", background="#1E1E1E")
style.configure("Dark.TLabel", background="#1E1E1E", foreground="white")
style.configure("TButton", background="#333333", foreground="white")
style.configure("TEntry", fieldbackground="#333333", foreground="white")

ttk.Label(pf, text="Loan Amount:", style="Dark.TLabel").pack(pady=3)
e1 = ttk.Entry(pf); e1.pack(pady=3); e1.insert(0, "100000")
ttk.Label(pf, text="Collateral Value:", style="Dark.TLabel").pack(pady=3)
e2 = ttk.Entry(pf); e2.pack(pady=3); e2.insert(0, "130000")
ttk.Label(pf, text="Periods:", style="Dark.TLabel").pack(pady=3)
e3 = ttk.Entry(pf); e3.pack(pady=3); e3.insert(0, "26")
ttk.Label(pf, text="Threshold:", style="Dark.TLabel").pack(pady=3)
e4 = ttk.Entry(pf); e4.pack(pady=3); e4.insert(0, "1.2")

ttk.Button(pf, text="Update", command=refresh_gui).pack(pady=10)
lbl_avg = ttk.Label(pf, text="Avg Ratio: ", style="Dark.TLabel")
lbl_avg.pack(pady=2)

# Step 10: Run initial display and start GUI
refresh_gui()
root.mainloop()