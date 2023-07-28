import os
import pyperclip
import pytesseract
from utils import *
import tkinter as tk
from PIL import ImageTk, Image

FILE_PATH = "./images"
OUT_PATH = "./files"

def root():
    window = tk.Tk()
    ip = get_private_ip()
    get_qr_code(ip)

    window.title("OCR :)")
    window.geometry("300x400")
    window.resizable(False, False)

    top_frame = tk.Frame(window)

    txt_label = tk.Label(
        top_frame, text=f"Visit http://{ip}:8080/update on your phone.",
        wraplength=200, justify=tk.CENTER
        )
    img = ImageTk.PhotoImage(Image.open("./images/qr_code/0.png"))
    img_label = tk.Label(top_frame, image=img)

    txt_label.pack(pady=5)
    img_label.pack(pady=5)

    bottom_frame = tk.Frame(window)

    button = tk.Button(
        bottom_frame, text="Choose Image",
        command=lambda: choose_image(window)
        )
    button.pack(pady=5)

    top_frame.pack(anchor='n', expand=True, fill=tk.BOTH)
    bottom_frame.pack(anchor='s', expand=True, fill=tk.BOTH)

    window.mainloop()

def choose_image(root):
    def update(e):
        selectedFile.set(listbox.get(listbox.curselection()))
        preview_button.configure(state="active")
        text_button.configure(state="active")

    top = tk.Toplevel(root)
    top.title("Choose Image")
    top.geometry("300x300")
    top.resizable(False, False)
    top.grab_set()

    files = get_file_names(FILE_PATH)
    selectedFile = tk.StringVar()

    label = tk.Label(top, text="Files", font=("lucida", 30))
    label.pack(anchor='w', padx=7)

    file_frame = tk.Frame(top)
    scroll = tk.Scrollbar(file_frame)
    scroll.pack(side=tk.RIGHT, fill="y")

    listbox = tk.Listbox(file_frame, yscrollcommand=scroll.set, selectmode="SINGLE")
    for file in files:
        listbox.insert(tk.END, file)

    listbox.pack(expand=True, fill=tk.BOTH, padx=5)
    file_frame.pack(expand=True, fill=tk.BOTH)
    listbox.bind("<<ListboxSelect>>", update)

    button_frame = tk.Frame(top)
    preview_button = tk.Button(
        button_frame, text="Preview",
        state="disabled", command=lambda: preview(top, selectedFile)
        )
    text_button = tk.Button(
        button_frame, text="Text",
        state="disabled", command=lambda: generate_text(top, selectedFile)
        )

    preview_button.grid(row=0, column=0, pady=10)
    text_button.grid(row=0, column=1, pady=10)
    button_frame.pack(expand=True, fill='y')


def preview(root, var):
    global img
    top = tk.Toplevel(root)
    top.title("Preview")
    top.grab_set()

    # img = ImageTk.PhotoImage(Image.open(os.path.join(FILE_PATH, var.get())))
    img = ImageTk.PhotoImage(scale_image(os.path.join(FILE_PATH, var.get())))
    img_label = tk.Label(top, image=img)

    text_button = tk.Button(
        top, text="Text",
        command=lambda: generate_text(top, var)
        )
    img_label.pack(padx=5, pady=5)
    text_button.pack(pady=5)

def generate_text(root, var):
    def copy(data):
        pyperclip.copy(data)

    def save(data, name):
        name = name[:name.rfind('.')] + ".txt"
        with open(name, 'w') as f:
            f.write(data)

    top = tk.Toplevel(root)
    top.title("Text")
    top.geometry("400x400")
    top.resizable(False, False)
    top.grab_set()

    img = Image.open(os.path.join(FILE_PATH, var.get()))
    text = pytesseract.image_to_string(img)

    text_frame = tk.Frame(top)
    scroll = tk.Scrollbar(text_frame)
    scroll.pack(side=tk.RIGHT, fill='y')

    text_box = tk.Text(text_frame, wrap=tk.WORD)
    text_box.insert(tk.END, text)
    text_box.pack(padx=5)

    text_frame.pack()

    button_frame = tk.Frame(top)
    copy_btn = tk.Button(
        button_frame, text="Copy",
        command=lambda: copy(text)
        )
    save_btn = tk.Button(
        button_frame, text="Save",
        command=lambda: save(text, os.path.join(OUT_PATH, var.get())))

    copy_btn.grid(row=0, column=0)
    save_btn.grid(row=0, column=1)

    button_frame.pack()


if __name__ == "__main__":
    root()