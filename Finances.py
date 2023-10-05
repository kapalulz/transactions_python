import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def process_csv_file(file_path, transaction_name):
    total_amount = 0
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 6:
                    status = row[0]
                    date = row[1]
                    description = row[2]
                    amount = row[3]
                    payee = row[5]

                    if transaction_name in description:
                        try:
                            amount = float(amount)
                            total_amount += amount
                        except ValueError:
                            print(f"Invalid amount format for record: {description}")
        return total_amount
    except Exception as e:
        return 0

def capitalize_transaction_name():
    transaction_name = transaction_name_entry.get().upper()
    transaction_name_entry.delete(0, tk.END)
    transaction_name_entry.insert(0, transaction_name)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        transaction_name = transaction_name_entry.get()
        total_amount = process_csv_file(file_path, transaction_name)
        messagebox.showinfo("Result", f"Total amount of transactions with '{transaction_name}': ${total_amount:.2f}")

# Create a graphical window
root = tk.Tk()
root.title("Transaction Analysis")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x = (screen_width - 200) // 2
y = (screen_height - 150) // 2

# Set the window size to 200x150 pixels and position it in the center of the screen
root.geometry("200x150+{}+{}".format(x, y))

# Create a label and an entry field for entering the transaction name
transaction_name_label = tk.Label(root, text="Transaction Name:")
transaction_name_label.pack()
transaction_name_entry = tk.Entry(root)
transaction_name_entry.pack()

# Create a button to convert the entered transaction name to uppercase
capitalize_button = tk.Button(root, text="Uppercase", command=capitalize_transaction_name)
capitalize_button.pack()

# Create a button for selecting a CSV file
browse_button = tk.Button(root, text="Select CSV File", command=browse_file)
browse_button.pack(pady=20)

root.mainloop()
