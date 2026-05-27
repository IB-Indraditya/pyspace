# ==========================================
# PYTHON MINI IDLE / IDE
# ==========================================

import tkinter as tk
import os
import subprocess
import re
import threading

# ==========================================
# WINDOW
# ==========================================

t = tk.Tk()

t.state("zoomed")

t.title("PythonSpace IDE")

t.configure(bg="#050510")

# ==========================================
# EDITOR
# ==========================================

textbox = tk.Text(

    t,

    font=("Consolas", 15),

    fg="white",

    bg="#0f172a",

    insertbackground="cyan",

    undo=True,

    padx=10,

    pady=10

)

textbox.place(

    x=0,

    y=0,

    relwidth=1,

    relheight=0.70

)

# ==========================================
# CONSOLE
# ==========================================

console = tk.Text(

    t,

    state="disabled",

    font=("Consolas", 13),

    bg="black",

    fg="lightgreen",

    insertbackground="white"

)

console.place(

    x=0,

    rely=0.75,

    relwidth=1,

    relheight=0.20

)

# ==========================================
# INPUT TERMINAL
# ==========================================

inputbox = tk.Entry(

    t,

    font=("Consolas", 14),

    bg="#18191B",

    fg="cyan",

    insertbackground="white"

)

inputbox.place(

    relx=0,

    rely=0.95,

    relwidth=1,

    relheight=0.05

)

# ==========================================
# CREATE FILE IF NOT EXISTS
# ==========================================

if not os.path.exists("test002.py"):

    with open("test002.py", "w") as f:

        f.write("print('Hello World')")

# ==========================================
# SMART AUTO INDENT
# ==========================================

def smart_indent(e):

    wid = e.widget

    line = wid.get(

        "insert linestart",

        "insert"

    )

    match = re.match(

        r'^(\s*)',

        line

    )

    current_indent = (

        match.group(0)

        if match else ""

    )

    if line.strip().endswith(":"):

        wid.insert(

            "insert",

            "\n" +

            current_indent +

            "\t"

        )

    else:

        wid.insert(

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
# FONT ZOOM
# ==========================================

fontsize = 15

def zoom_in(e):

    global fontsize

    fontsize += 1

    textbox.configure(

        font=(

            "Consolas",

            fontsize

        )

    )

    console.configure(

        font=(

            "Consolas",

            fontsize - 1

        )

    )

textbox.bind(

    "<Control-equal>",

    zoom_in

)

def zoom_out(e):

    global fontsize

    if fontsize > 10:

        fontsize -= 1

    textbox.configure(

        font=(

            "Consolas",

            fontsize

        )

    )

    console.configure(

        font=(

            "Consolas",

            fontsize - 1

        )

    )

textbox.bind(

    "<Control-minus>",

    zoom_out

)

# ==========================================
# CONSOLE WRITER
# ==========================================

def write_console(text):

    console.configure(

        state="normal"

    )

    console.insert(

        tk.END,

        text

    )

    console.see(tk.END)

    console.configure(

        state="disabled"

    )

# ==========================================
# SAVE FILE
# ==========================================

def savefile(e=None):

    with open(

        "test002.py",

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

textbox.bind(

    "<Control-S>",

    savefile

)

# ==========================================
# PROCESS VARIABLE
# ==========================================

process = None

# ==========================================
# READ LIVE OUTPUT
# ==========================================

def read_output():

    global process

    while True:

        output = process.stdout.readline()

        if (

            output == ""

            and process.poll() is not None

        ):

            break

        if output:

            write_console(output)

# ==========================================
# RUN INSIDE CONSOLE
# ==========================================

def run(e=None):

    global process

    savefile()

    console.configure(

        state="normal"

    )

    console.delete(

        1.0,

        tk.END

    )

    console.configure(

        state="disabled"

    )

    process = subprocess.Popen(

        ["python", "test002.py"],

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

t.bind(

    "<Control-F5>",

    run

)

# ==========================================
# SEND INPUT TO PYTHON FILE
# ==========================================

def send_input(e):

    global process

    if process:

        command = inputbox.get()

        process.stdin.write(

            command + "\n"

        )

        process.stdin.flush()

        write_console(

            ">>> " +

            command +

            "\n"

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
# OPEN CMD TERMINAL
# ==========================================

def open_terminal(e=None):

    savefile()

    os.system(

        "start cmd /k python test002.py"

    )

t.bind(

    "<F5>",

    open_terminal

)

# ==========================================
# DEFAULT SAMPLE CODE
# ==========================================

sample = '''
name = input("Enter name : ")

print("Hello", name)

for i in range(5):

    print("Number :", i)
'''

textbox.insert(

    1.0,

    sample

)

# ==========================================
# START APP
# ==========================================

t.mainloop()
