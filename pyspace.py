# ==========================================
# PYTHONSPACE IDE ULTRA
# ==========================================

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import re

# ==========================================
# WINDOW
# ==========================================

t = tk.Tk()

t.state("zoomed")

t.title("PythonSpace IDE Ultra")

t.configure(bg="#050510")

# ==========================================
# VARIABLES
# ==========================================

fontsize = 15

process = None

current_file = "test002.py"

# ==========================================
# TOPBAR
# ==========================================

topbar = tk.Frame(

    t,

    bg="#111827",

    height=45

)

topbar.pack(

    fill="x",

    side="top"

)

# ==========================================
# MAIN FRAME
# ==========================================

editorframe = tk.Frame(

    t,

    bg="#050510"

)

editorframe.place(

    relx=0,

    rely=0.05,

    relwidth=1,

    relheight=0.65

)

# ==========================================
# LINE NUMBERS
# ==========================================

linenumbers = tk.Text(

    editorframe,

    width=5,

    bg="#1e293b",

    fg="#facc15",

    font=("Consolas", fontsize),

    bd=15,

    state="disabled",

    padx=0

)

linenumbers.pack(

    side="left",

    fill="y"

)

# ==========================================
# EDITOR
# ==========================================

textbox = tk.Text(

    editorframe,

    font=("Consolas", fontsize),

    fg="white",

    bg="#0f172a",

    insertbackground="cyan",

    undo=True,

    padx=10,

    pady=0,

    bd=15

)

textbox.pack(

    side="left",

    fill="both",

    expand=True

)

# ==========================================
# EDITOR SCROLLBAR
# ==========================================

editor_scroll = tk.Scrollbar(

    editorframe,

    command=textbox.yview,

    bg="#111827",

    troughcolor="#050510",

    activebackground="#00ffff",

    relief="flat",

    width=14

)

editor_scroll.pack(

    side="right",

    fill="y"

)

textbox.config(

    yscrollcommand=editor_scroll.set

)

# ==========================================
# CONSOLE
# ==========================================

consoleframe = tk.Frame(

    t,

    bg="#000000"

)

consoleframe.place(

    relx=0,

    rely=0.72,

    relwidth=1,

    relheight=0.23

)

console = tk.Text(

    consoleframe,

    font=("Consolas", 13),

    fg="lightgreen",

    bg="black",

    insertbackground="white",

    bd=25,

    padx=10,

    pady=10

)

console.pack(

    side="left",

    fill="both",

    expand=True

)

# ==========================================
# CONSOLE SCROLLBAR
# ==========================================

console_scroll = tk.Scrollbar(

    consoleframe,

    command=console.yview,

    bg="#111827",

    troughcolor="#000000",

    activebackground="#00ff88",

    relief="flat",

    width=14

)

console_scroll.pack(

    side="right",

    fill="y"

)

console.config(

    yscrollcommand=console_scroll.set
    

)

# ==========================================
# INPUT BOX
# ==========================================

inputbox = tk.Entry(

    t,

    font=("Consolas", 13),

    bg="#111827",

    fg="cyan",

    insertbackground="white",

    bd=10

)

inputbox.place(

    relx=0,

    rely=0.95,

    relwidth=1,

    relheight=0.05

)

# ==========================================
# CREATE FILE
# ==========================================

if not os.path.exists(current_file):

    with open(current_file, "w") as f:

        f.write("print('Hello World')")

# ==========================================
# UPDATE LINE NUMBERS
# ==========================================

def update_lines(e=None):

    linenumbers.config(state="normal")

    linenumbers.delete(

        1.0,

        tk.END

    )

    total_lines = int(

        textbox.index(

            "end-1c"

        ).split(".")[0]

    )

    line_text = "\n".join(

        str(i)

        for i in range(

            1,

            total_lines + 1

        )

    )

    linenumbers.insert(

        "1.0",

        line_text

    )

    linenumbers.config(

        state="disabled"

    )

textbox.bind(

    "<KeyRelease>",

    update_lines

)

# ==========================================
# SYNC SCROLL
# ==========================================

def sync_scroll(*args):

    textbox.yview(*args)

    linenumbers.yview(*args)

textbox.config(

    yscrollcommand=lambda *args: (

        editor_scroll.set(*args),

        linenumbers.yview_moveto(args[0])

    )

)

editor_scroll.config(

    command=sync_scroll

)

# ==========================================
# WRITE CONSOLE
# ==========================================

def write_console(text):

    console.insert(

        tk.END,

        text

    )

    console.see(tk.END)

# ==========================================
# SMART INDENT
# ==========================================

def smart_indent(e):

    line = textbox.get(

        "insert linestart",

        "insert"

    )

    match = re.match(

        r'^(\s*)',

        line

    )

    current_indent = match.group(0)

    if line.strip().endswith(":"):

        textbox.insert(

            "insert",

            "\n" +

            current_indent +

            "\t"

        )

    else:

        textbox.insert(

            "insert",

            "\n" +

            current_indent

        )

    return "break"

textbox.bind(

    "<Return>",

    smart_indent

)

# ==========================================
# SAVE FILE
# ==========================================

def savefile(e=None):

    with open(

        current_file,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(

            textbox.get(

                1.0,

                tk.END

            )

        )

    write_console(

        "\n[SAVED SUCCESSFULLY]\n"

    )

textbox.bind(

    "<Control-s>",

    savefile

)

# ==========================================
# OPEN FILE
# ==========================================

def open_file():

    global current_file

    file = filedialog.askopenfilename(

        filetypes=[

            ("Python Files", "*.py")

        ]

    )

    if file:

        current_file = file

        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:

            code = f.read()

        textbox.delete(

            1.0,

            tk.END

        )

        textbox.insert(

            1.0,

            code

        )

        update_lines()

# ==========================================
# EXPORT FILE
# ==========================================

def export_file():

    file = filedialog.asksaveasfilename(

        defaultextension=".py",

        filetypes=[

            ("Python Files", "*.py")

        ]

    )

    if file:

        with open(

            file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(

                textbox.get(

                    1.0,

                    tk.END

                )

            )

        messagebox.showinfo(

            "Export",

            "File Exported Successfully"

        )

# ==========================================
# CLEAR CONSOLE
# ==========================================

def clear_console():

    console.delete(

        1.0,

        tk.END

    )

# ==========================================
# COMMENT FEATURE
# ==========================================

def toggle_comment(e=None):

    try:

        start = textbox.index(

            "sel.first linestart"

        )

        end = textbox.index(

            "sel.last lineend"

        )

    except:

        return

    lines = textbox.get(

        start,

        end

    ).split("\n")

    new_lines = []

    for line in lines:

        if line.strip().startswith("#"):

            idx = line.find("#")

            line = line[:idx] + line[idx+1:]

        else:

            line = "#" + line

        new_lines.append(line)

    textbox.delete(

        start,

        end

    )

    textbox.insert(

        start,

        "\n".join(new_lines)

    )

textbox.bind(

    "<Control-slash>",

    toggle_comment

)

# ==========================================
# RUN PROGRAM
# ==========================================

def read_output():

    global process

    while True:

        output = process.stdout.readline()

        if output == "" and process.poll() is not None:

            break

        if output:

            console.after(

                0,

                lambda o=output:
                write_console(o)

            )

def run(e=None):

    global process

    savefile()

    clear_console()

    process = subprocess.Popen(

        ["python", "-u", current_file],

        stdin=subprocess.PIPE,

        stdout=subprocess.PIPE,

        stderr=subprocess.STDOUT,

        text=True,

        bufsize=1

    )

    threading.Thread(

        target=read_output,

        daemon=True

    ).start()

textbox.bind(

    "<Control-F5>",

    run

)

# ==========================================
# SEND INPUT
# ==========================================

def send_input(e=None):

    global process

    if process:

        command = inputbox.get()

        process.stdin.write(

            command + "\n"

        )

        process.stdin.flush()

        write_console(

            command + "\n"

        )

        inputbox.delete(

            0,

            tk.END

        )

inputbox.bind(

    "<Return>",

    send_input

)

# ==========================================
# TERMINAL WINDOW
# ==========================================

def open_terminal(e=None):

    savefile()

    os.system(

        f"start cmd /k python {current_file}"

    )

textbox.bind(

    "<F5>",

    open_terminal

)

# ==========================================
# FONT ZOOM
# ==========================================

def zoom_in(e=None):

    global fontsize

    fontsize += 1

    textbox.config(

        font=(

            "Consolas",

            fontsize

        )

    )

    linenumbers.config(

        font=(

            "Consolas",

            fontsize

        )

    )

textbox.bind(

    "<Control-equal>",

    zoom_in

)

def zoom_out(e=None):

    global fontsize

    if fontsize > 10:

        fontsize -= 1

    textbox.config(

        font=(

            "Consolas",

            fontsize

        )

    )

    linenumbers.config(

        font=(

            "Consolas",

            fontsize

        )

    )

textbox.bind(

    "<Control-minus>",

    zoom_out

)

# ==========================================
# BUTTONS
# ==========================================
# ==========================================
# NEW PYSPACE WINDOW
# ==========================================

def newtab(e=None):

    os.system("python pyspace.py")
buttons = [
    ("PYSPACE", newtab, "white"),

    ("📂 OPEN", open_file, "#2563eb"),

    ("⬇ EXPORT", export_file, "#9333ea"),

    ("🗑 CLEAR", clear_console, "#ef4444"),

    ("# COMMENT", toggle_comment, "#facc15"),

    ("💾 SAVE", savefile, "#22c55e"),

    ("▶ RUN", run, "#00ffff")
    

]

for text, cmd, color in buttons:

    btn = tk.Button(

        topbar,

        text=text,

        command=cmd,

        font=("Consolas", 11, "bold"),

        bg=color,

        fg="black",

        relief="flat",

        cursor="hand2",
        width="24"
        

    )

    btn.pack(

        side="left",

        padx=10,

        pady=5

    )

# ==========================================
# SAMPLE CODE
# ==========================================
name=os.getenv("USERNAME")
sample = f'''print("Hello, {name}")
'''

textbox.insert(

    1.0,

    sample

)

update_lines()

# ==========================================
# START
# ==========================================

t.mainloop()
