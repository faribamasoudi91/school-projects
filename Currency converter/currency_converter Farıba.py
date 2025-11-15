
import tkinter as tk
import requests

# -------------------------------
# Fetch list of currencies
# -------------------------------
#  Get the list of codes from USD base.
url = "https://api.exchangerate-api.com/v4/latest/USD"
response = requests.get(url)
data = response.json()
currency_list = list(data["rates"].keys())

# -------------------------------
# Conversion logic
# -------------------------------
def convert_currency(*_):
    """
    Convert the typed amount from source to target.
    Updates the Exchange Rate label as required.
    Triggered by: Convert button, changing the dropdowns, or swap.
    """
    try:
        # Read current UI values
        amount_str = amount_entry.get().strip()
        if amount_str == "":
            amount_str = "0"
        amount = float(amount_str)

        source = source_currency_var.get()
        target = target_currency_var.get()

        # Get live rates for the selected source currency
        url = f"https://api.exchangerate-api.com/v4/latest/{source}"
        r = requests.get(url)
        rates = r.json()["rates"]

        # Specific pair rate and label update
        rate = rates[target]
        exchange_rate_label.config(text=f"Exchange Rate: {rate}")

        # Compute and show result
        result = amount * rate
        target_amount_entry.delete(0, tk.END)
        target_amount_entry.insert(0, f"{result:.6f}")

    except Exception:
        target_amount_entry.delete(0, tk.END)
        target_amount_entry.insert(0, "Error")

#  swap the two currencies
def swap_currencies():
    src = source_currency_var.get()
    tgt = target_currency_var.get()
    source_currency_var.set(tgt)
    target_currency_var.set(src)

    # If a result exists, move it to Amount so users can convert back
    current_result = target_amount_entry.get().strip()
    if current_result:
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, current_result)

    convert_currency()

# -------------------------------
# UI
# -------------------------------
myForm = tk.Tk()
myForm.title("Currency Converter (by Fariba)")   # <-- change to your name
myForm.geometry("500x260")

# Amount (input)
amount_label = tk.Label(myForm, text="Amount:")
amount_label.place(x=20, y=20)

amount_entry = tk.Entry(myForm, width=15)
amount_entry.place(x=100, y=20)

# From (source) dropdown
from_label = tk.Label(myForm, text="From:")
from_label.place(x=20, y=70)

source_currency_var = tk.StringVar(value="USD")
source_currency_dropdown = tk.OptionMenu(myForm, source_currency_var, *currency_list)
source_currency_dropdown.place(x=100, y=65)

# To (target) dropdown
to_label = tk.Label(myForm, text="To:")
to_label.place(x=20, y=120)

target_currency_var = tk.StringVar(value="EUR")
target_currency_dropdown = tk.OptionMenu(myForm, target_currency_var, *currency_list)
target_currency_dropdown.place(x=100, y=115)

# Result (output) textbox
target_amount_entry = tk.Entry(myForm, width=15)
target_amount_entry.place(x=250, y=115)

# Swap button
swap_button = tk.Button(myForm, text=chr(0x21C5), width=3, command=swap_currencies)
swap_button.place(x=200, y=115)

# Exchange Rate label
exchange_rate_label = tk.Label(myForm, text="Exchange Rate: ???")
exchange_rate_label.place(x=20, y=170)

# Convert button 
convert_button = tk.Button(myForm, text="Convert", command=convert_currency)
convert_button.place(x=100, y=210)

# Auto-convert when dropdown selections change 
source_currency_var.trace("w", convert_currency)
target_currency_var.trace("w", convert_currency)

# initialize the label/result when the app opens
convert_currency()

# auto-convert while typing
amount_entry.bind("<KeyRelease>", convert_currency)

myForm.mainloop()
