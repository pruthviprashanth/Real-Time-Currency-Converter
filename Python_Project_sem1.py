import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ------------------ CURRENCY → COUNTRY MAP ------------------
currency_country = {
    "USD": "United States",
    "INR": "India",
    "EUR": "European Union",
    "GBP": "United Kingdom",
    "JPY": "Japan",
    "AUD": "Australia",
    "CAD": "Canada",
    "CNY": "China",
    "CHF": "Switzerland",
    "SGD": "Singapore"
}

# ------------------ FETCH CURRENCY CODES ------------------
def get_currency_list():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()

        if "rates" not in data:
            return []

        return sorted(list(data["rates"].keys()))
    except:
        return []

# ------------------ FETCH CONVERSION RATE ------------------
def get_conversion_rate(from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        if "rates" not in data:
            return None

        return data["rates"].get(to_currency)
    except:
        return None

# ------------------ CONVERT FUNCTION ------------------
def convert_currency():
    amount = entry_amount.get()

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    from_curr = combo_from.get().split("(")[-1].replace(")", "")
    to_curr = combo_to.get().split("(")[-1].replace(")", "")

    rate = get_conversion_rate(from_curr, to_curr)

    if rate is None:
        messagebox.showerror("Error", "Could not fetch conversion rate.")
        return

    result = amount * rate
    label_result.config(
        text=f"{amount} {from_curr} = {round(result, 2)} {to_curr}"
    )

# ------------------ CLEAR FUNCTION ------------------
def clear_result():
    entry_amount.delete(0, tk.END)
    label_result.config(text="")
    combo_from.set("United States (USD)")
    combo_to.set("India (INR)")

# ================= GUI =================
root = tk.Tk()
root.title("Real-Time Currency Converter")
root.geometry("450x360")

tk.Label(
    root,
    text="Real-Time Currency Converter",
    font=("Arial", 16, "bold")
).pack(pady=10)

#Fetch currencies
currency_codes = get_currency_list()
if not currency_codes:
    messagebox.showwarning("Offline ", "no internet connection")


# Create display list with country names
display_list = [
    f"{currency_country.get(code, code)} ({code})"
    for code in currency_codes
]

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Amount: ").grid(row=0, column=0, sticky="w")
entry_amount = tk.Entry(frame, width=18)
entry_amount.grid(row=0, column=1)

tk.Label(frame, text="From Country: ").grid(row=1, column=0, sticky="w")
combo_from = ttk.Combobox(frame, values=display_list, width=25)
combo_from.grid(row=1, column=1)
combo_from.set("United States (USD)")

tk.Label(frame, text="To Country: ").grid(row=2, column=0, sticky="w")
combo_to = ttk.Combobox(frame, values=display_list, width=25)
combo_to.grid(row=2, column=1)
combo_to.set("India (INR)")

# Buttons
tk.Button(root, text="Convert", command=convert_currency, width=15).pack(pady=10)
tk.Button(root, text="Clear", command=clear_result, width=15).pack(pady=5)

label_result = tk.Label(root, text="", font=("Arial", 14))
label_result.pack(pady=10)

root.mainloop()
