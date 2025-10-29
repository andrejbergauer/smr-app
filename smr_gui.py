#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

APP_TITLE = "SMR → NASCET (Windows GUI)"

def classify_stenosis(smr: float) -> str:
    if smr < 8:
        return "<50% stenosis"
    elif 8 <= smr <= 10:
        return "50–59% stenosis"
    elif 11 <= smr <= 13:
        return "60–69% stenosis"
    elif 14 <= smr <= 21:
        return "70–79% stenosis"
    elif 22 <= smr <= 29:
        return "80–89% stenosis"
    elif smr > 30:
        return ">90% stenosis (less than near-occlusion)"
    # borderline gaps (10<SMR<11 etc.)
    if 10 < smr < 11:
        return "≈50–69% (borderline)"
    if 13 < smr < 14:
        return "≈60–79% (borderline)"
    if 21 < smr < 22:
        return "≈70–89% (borderline)"
    return "≈80–90% (borderline)"

def compute():
    try:
        edv = float(entry_edv.get().strip())
        psv = float(entry_psv.get().strip())
    except ValueError:
        messagebox.showerror("Input error", "Please enter numeric values (use dot for decimals).")
        return

    if edv <= 0:
        messagebox.showerror("Input error", "EDV of CCA must be > 0 cm/s.")
        return
    if psv < 0:
        messagebox.showerror("Input error", "PSV of ICA cannot be negative.")
        return

    smr = psv / edv
    cat = classify_stenosis(smr)

    lbl_smr_val.config(text=f"{smr:.2f}")
    lbl_cat_val.config(text=cat)

def clear_fields():
    entry_edv.delete(0, tk.END)
    entry_psv.delete(0, tk.END)
    lbl_smr_val.config(text="—")
    lbl_cat_val.config(text="—")
    entry_edv.focus_set()

root = tk.Tk()
root.title(APP_TITLE)
root.resizable(False, False)
pad = {"padx": 10, "pady": 6}

frm = tk.Frame(root)
frm.grid(row=0, column=0, **pad)

# Inputs
tk.Label(frm, text="EDV (CCA) cm/s:").grid(row=0, column=0, sticky="e", **pad)
entry_edv = tk.Entry(frm, width=18)
entry_edv.grid(row=0, column=1, **pad)
entry_edv.focus_set()

tk.Label(frm, text="PSV (ICA) cm/s:").grid(row=1, column=0, sticky="e", **pad)
entry_psv = tk.Entry(frm, width=18)
entry_psv.grid(row=1, column=1, **pad)

# Buttons
btns = tk.Frame(frm)
btns.grid(row=2, column=0, columnspan=2, **pad)
tk.Button(btns, text="Calculate", command=compute).grid(row=0, column=0, padx=6)
tk.Button(btns, text="Clear", command=clear_fields).grid(row=0, column=1, padx=6)

# Outputs
tk.Label(frm, text="St. Mary's Ratio (SMR):").grid(row=3, column=0, sticky="e", **pad)
lbl_smr_val = tk.Label(frm, text="—", font=("Segoe UI", 10, "bold"))
lbl_smr_val.grid(row=3, column=1, sticky="w", **pad)

tk.Label(frm, text="Estimated NASCET range:").grid(row=4, column=0, sticky="e", **pad)
lbl_cat_val = tk.Label(frm, text="—", font=("Segoe UI", 10, "bold"))
lbl_cat_val.grid(row=4, column=1, sticky="w", **pad)

# Enter key = Calculate
root.bind("<Return>", lambda e: compute())

root.mainloop()