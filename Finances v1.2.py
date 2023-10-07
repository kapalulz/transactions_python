import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import defaultdict

# Function to get the screen width and height
def get_screen_width_height(window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    return x, y

# Определите категории и ключевые слова
categories_and_keywords = {
    "Costco": ["COSTCO", "TARGET", "MARKET BASKET", "CVS", "PHARMACY"],  # Включаем "TARGET" и "MARKET BASKET" в Costco
    "Gas и Fuel": ["GAS", "PRESTIGE", "CAR", "GULF", "EXXON"],
    "FastFood": ["MCDONALDS", "BURGER KING", "STARBUCKS", "DUNKIN", "JAPAN", "WOK", "UNOCHICAGOGRILL#227", "STEAK", "SIP", "SWEET", "SUSHI"],
    "Makeup": ["ULTA", "SEPHORA", "PRIMARK"],
    "IKEA": ["IKEA"]
}

# Function to process the CSV file and automatically classify transactions
def process_csv_file(file_path):
    # Initialize category totals
    category_totals = defaultdict(float)

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

                    matched_category = "Other"  # Default category if no match is found

                    for keyword, category in categories_and_keywords.items():
                        if any(kw in description.upper() for kw in category):
                            matched_category = keyword
                            break

                    try:
                        amount = float(amount)
                        category_totals[matched_category] += amount
                    except ValueError:
                        print(f"Invalid amount format for record: {description}")

        return category_totals
    except Exception as e:
        return None

# Function to capitalize the transaction name
def capitalize_transaction_name():
    transaction_name = transaction_name_entry.get().upper()
    transaction_name_entry.delete(0, tk.END)
    transaction_name_entry.insert(0, transaction_name)

# Function to close the application
def exit_application():
    root.destroy()

# Function to close the result window
def close_result_window():
    result_window.destroy()

# Function to show the result
def show_result():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        # Process the CSV file and classify transactions
        category_totals = process_csv_file(file_path)

        if category_totals is not None:
            # Create a result window
            global result_window
            result_window = tk.Toplevel(root)
            result_window.title("Result")

            # Set the result window size
            result_window_width = 400
            result_window_height = 200
            x, y = get_screen_width_height(result_window_width, result_window_height)
            result_window.geometry(f"{result_window_width}x{result_window_height}+{int(x)}+{int(y)}")

            # Display category totals
            result_label = tk.Label(result_window, text="Category Totals:")
            result_label.pack(padx=20, pady=10)

            for category, total_amount in category_totals.items():
                result_label = tk.Label(result_window, text=f"{category}: ${total_amount:.2f}")
                result_label.pack(padx=20, pady=5)

            # Determine the figure size based on the number of labels
            figure_size = (8, 8) if len(category_totals) <= 5 else (10, 10)

            # Create a pie chart
            plt.figure(figsize=figure_size)
            labels = category_totals.keys()
            sizes = category_totals.values()
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})  # Adjust text size
            plt.title('Transaction Analysis')

            # Show the pie chart
            plt.show()

            # Add a "Close" button to close the result window
            close_button = tk.Button(result_window, text="Close", command=close_result_window)
            close_button.pack()

# Create the main graphical window
root = tk.Tk()
root.title("Transaction Analysis")

# Set the main window size
window_width = 400
window_height = 200
x, y = get_screen_width_height(window_width, window_height)
root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

# Create a label and an entry field for entering the transaction name
transaction_name_label = tk.Label(root, text="Transaction Name:")
transaction_name_label.pack()
transaction_name_entry = tk.Entry(root)
transaction_name_entry.pack()

# Create a button to convert the entered transaction name to uppercase
capitalize_button = tk.Button(root, text="Uppercase", command=capitalize_transaction_name)
capitalize_button.pack()

# Create a button to open a CSV file and show the result
browse_button = tk.Button(root, text="Open CSV File", command=show_result)
browse_button.pack(pady=20)

# Add an "Exit" button to exit the application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

root.mainloop()
