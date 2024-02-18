import tkinter as tk
import os
import re

# Function to handle dragging items
def start_drag(event, index):
    global selected_index
    selected_index = index
    canvas.tag_raise(items[index])  # Raise the selected item
    canvas.itemconfig(items[index], fill="red")  # Change item color when dragged

def stop_drag(event):
    global selected_index
    if selected_index is not None:
        canvas.itemconfig(items[selected_index], fill="blue")  # Revert item color when drag ends
    selected_index = None
    sort_items()  # Sort items after drag ends

def on_drag(event):
    if selected_index is not None:
        x, y = event.x, event.y
        # Restrict horizontal movement, only update vertical position
        canvas.coords(items[selected_index], canvas.coords(items[selected_index])[0], y - 10)
        sort_items()  # Sort items while dragging

# Sort items based on their positions on the canvas
def sort_items():
    item_positions = [(canvas.coords(item)[1], item) for item in items]
    item_positions.sort(key=lambda x: x[0])

    for i, (_, item) in enumerate(item_positions):
        canvas.move(item, 0, 30 * i + 50 - canvas.coords(item)[1])

# Update the list based on the current order of items
def update_list():
    global item_names
    # get item positions and sort them by y coord
    item_positions = [(canvas.coords(item)[1], item) for item in items]
    item_positions.sort(key=lambda x: x[0])
    # use item id stored in item_positions to get item names
    names = [item_names[item_positions[i][1]//2] for i in range(len(item_names))]
    return names

# Capture and print the current ordering of items
def capture_order():
    names = update_list()
    write_to_file()
    load_items()
    print("Current ordering of items:", names)

def write_to_file():
    names = update_list()
    filename = "test.tex"
    with open(filename, "w") as f:
        f.write("% !TeX root = Liederbuchtest.tex\n")
        f.write("\n")
        for name in names:
            f.write("\\myinput[]{" + name +"}\n")

    # run tex and then run toc.py
    os.system("xelatex -synctex=1 -interaction=nonstopmode -output-directory=build -shell-escape Liederbuchtest.tex")
    os.system("python toc.py")
    os.system("xelatex -synctex=1 -interaction=nonstopmode -output-directory=build -shell-escape Liederbuchtest.tex")

def load_items():
    content = os.listdir("./texsongs/")
    # filter for .tex songs and get song names
    songs = [s[:-4] for s in content if re.search(r'.*\.tex', s)]

    return songs

# List of items
# item_names = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
item_names = load_items()

root = tk.Tk()
root.title("Movable Items")

canvas = tk.Canvas(root, width=400, height=1000, bg="white")
canvas.pack()

items = []
selected_index = None

# Create movable items with bounding boxes on canvas
for i, name in enumerate(item_names):
    item = canvas.create_text(50, 30 * i + 50, text=name, fill="blue", font=("Arial", 12), anchor="w")
    items.append(item)

    # Create bounding box around the item
    x0, y0, x1, y1 = canvas.bbox(item)
    bounding_box = canvas.create_rectangle(x0 - 5, y0 - 5, x1 + 5, y1 + 5, outline="black", dash=(3, 3))
    canvas.tag_lower(bounding_box, item)

    canvas.tag_bind(item, "<Button-1>", lambda event, index=i: start_drag(event, index))
    canvas.tag_bind(item, "<B1-Motion>", on_drag)
    canvas.tag_bind(item, "<ButtonRelease-1>", stop_drag)

# Button to capture and print the current ordering of items
capture_button = tk.Button(root, text="Capture Order", command=capture_order)
capture_button.pack(side=tk.RIGHT)

root.mainloop()
