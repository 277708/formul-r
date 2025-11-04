import pandas as pd
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Načtení dat z Excelu
machines_df = pd.read_excel("zoznamy.xlsx", sheet_name="STROJE")
clients_df = pd.read_excel("zoznamy.xlsx", sheet_name="KLIENTI")

# Filtr dostupných strojů
machines_df = machines_df[machines_df['E'] == "ANO"].reset_index(drop=True)

# Funkce pro výpočet půjčovného
def calculate_rental():
    client_name = client_combobox.get()
    selected_indices = machine_listbox.curselection()
    days_str = days_entry.get()

    if not client_name:
        messagebox.showwarning("Chyba", "Vyberte klienta!")
        return
    if not selected_indices:
        messagebox.showwarning("Chyba", "Vyberte alespoň jeden stroj!")
        return
    if not days_str.isdigit() or int(days_str) <= 0:
        messagebox.showwarning("Chyba", "Zadejte platný počet dní!")
        return

    days = int(days_str)
    client_discount = clients_df.loc[clients_df['A'] == client_name, 'D'].values[0]

    total_price = sum(machines_df.iloc[i]['D'] * days for i in selected_indices)
    total_price = total_price * (1 - client_discount / 100)

    result_label.config(text=f"Celková cena: {total_price:.2f} Kč")

# Vytvoření GUI
root = ttk.Window(themename="cyborg")
root.title("Půjčovna strojů")
root.geometry("450x450")
root.resizable(False, False)

# Klient
ttk.Label(root, text="Vyberte klienta:", font=("Helvetica", 12)).pack(pady=(15,5))
client_combobox = ttk.Combobox(root, values=list(clients_df['A']), bootstyle="info")
client_combobox.pack(pady=5, fill=X, padx=20)

# Stroje
ttk.Label(root, text="Vyberte stroje:", font=("Helvetica", 12)).pack(pady=(15,5))
machine_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
for i, row in machines_df.iterrows():
    machine_listbox.insert(tk.END, f"{row['A']} - {row['C']} ({row['D']} Kč/den)")
machine_listbox.pack(pady=5, fill=X, padx=20)

# Počet dní
ttk.Label(root, text="Počet dní:", font=("Helvetica", 12)).pack(pady=(15,5))
days_entry = ttk.Entry(root)
days_entry.pack(pady=5, fill=X, padx=20)

# Tlačítko pro výpočet
ttk.Button(root, text="Spočítat půjčovné", command=calculate_rental, bootstyle="success").pack(pady=20)

# Výsledek
result_label = ttk.Label(root, text="", font=("Helvetica", 14, "bold"))
result_label.pack(pady=10)

root.mainloop()
