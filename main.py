import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Stack to keep track of operations
history_stack = []


def rename_files(dir_path, new_name, name_position):
    if not dir_path or not new_name:
        messagebox.showwarning("Warning", "Please select a directory and input a new name first.")
        return

    files = os.listdir(dir_path)
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if name_position.get() == "prefix":
            new_name_full = new_name + file_name + file_extension
        else:
            new_name_full = file_name + new_name + file_extension
        old_file_path = os.path.join(dir_path, file)
        new_file_path = os.path.join(dir_path, new_name_full)
        shutil.move(old_file_path, new_file_path)
        # Push operation details onto the stack
        history_stack.append((old_file_path, new_file_path))

    messagebox.showinfo("Success", "Files renamed successfully.")


def undo_operation():
    if history_stack:
        while history_stack:
            old_file_path, new_file_path = history_stack.pop()
            # Reverse the operation
            shutil.move(new_file_path, old_file_path)
        messagebox.showinfo("Success", "Operation undone successfully.")
    else:
        messagebox.showwarning("Warning", "No operations to undo.")


def select_directory(dir_label):
    dir_path = filedialog.askdirectory()
    if dir_path:  # Only update label if a directory was selected
        dir_label.config(text=f"Selected Directory: {dir_path}")
    return dir_path


def input_new_name(name_label):
    new_name = simpledialog.askstring("Input", "Enter new name")
    if new_name:  # Only update label if a name was inputted
        name_label.config(text=f"New Name: {new_name}")
    return new_name


def confirm_exit(window):
    if messagebox.askokcancel("Quit", "Do you really want to exit? If you exit, you can't undo the changes you've made."):
        window.destroy()


def main():
    window = tk.Tk()
    window.title("File Renamer")

    dir_path = tk.StringVar()
    new_name = tk.StringVar()
    name_position = tk.StringVar(value="prefix")

    dir_label = tk.Label(window, text="Selected Directory: None")
    dir_label.pack()

    name_label = tk.Label(window, text="New Name: None")
    name_label.pack()

    prefix_radio = tk.Radiobutton(window, text="Prefix", variable=name_position, value="prefix")
    prefix_radio.pack()

    suffix_radio = tk.Radiobutton(window, text="Suffix", variable=name_position, value="suffix")
    suffix_radio.pack()

    select_dir_button = tk.Button(window, text="Select Directory",
                                  command=lambda: dir_path.set(select_directory(dir_label)))
    select_dir_button.pack()

    input_name_button = tk.Button(window, text="Input New Name",
                                  command=lambda: new_name.set(input_new_name(name_label)))
    input_name_button.pack()

    rename_button = tk.Button(window, text="Execute Operation",
                              command=lambda: rename_files(dir_path.get(), new_name.get(), name_position))
    rename_button.pack()

    undo_button = tk.Button(window, text="Undo Operation", command=undo_operation)
    undo_button.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: confirm_exit(window))

    window.mainloop()


if __name__ == "__main__":
    main()
