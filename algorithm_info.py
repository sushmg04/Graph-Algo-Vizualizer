import tkinter as tk
from tkinter import messagebox

class AlgorithmInfoWindow:
    def __init__(self, master, algorithm_name):
        self.master = master
        self.master.title("Algorithm Information: " + algorithm_name)
        self.master.geometry("400x300")

        info_label = tk.Label(master, text="Algorithm Information: " + algorithm_name, font=("Arial", 14, "bold"))
        info_label.pack(pady=10)

        info_text = tk.Text(master, width=40, height=15)
        info_text.pack(pady=10)

        # Insert actual information about the algorithm here
        algorithm_info = get_algorithm_info(algorithm_name)
        info_text.insert(tk.END, algorithm_info)

        close_button = tk.Button(master, text="Close", command=self.close_window)
        close_button.pack(pady=10)

    def close_window(self):
        self.master.destroy()

def get_algorithm_info(algorithm_name):
    # Replace this with actual information about each algorithm
    algorithm_info_dict = {
        "Linear Search": "Linear search is a simple search algorithm that finds the position of a target value within a list.",
        "Binary Search": "Binary search is a fast search algorithm that works on sorted arrays or lists.",
        # Add information for other algorithms here...
    }
    return algorithm_info_dict.get(algorithm_name, "Information not available.")

def create_info_window(algorithm_name):
    root = tk.Tk()
    app = AlgorithmInfoWindow(root, algorithm_name)
    root.mainloop()

def main():
    algorithms = [
        "Linear Search", "Binary Search", "Selection Sort", "Insertion Sort",
        "Bubble Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort",
        "Radix Sort", "Backtracking", "N-Queens", "Knight's Tour"
    ]

    root = tk.Tk()
    root.title("Algorithm Information")
    root.geometry("300x500")

    for algorithm in algorithms:
        button = tk.Button(root, text=algorithm, command=lambda algo=algorithm: create_info_window(algo))
        button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
