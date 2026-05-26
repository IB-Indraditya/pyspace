#code for python IDLE  <<-----
import tkinter as tk
import os, subprocess, re
##from tkinter.filedialog import askopenfilename, asksavefilename 
t=tk.Tk()
# t.geometry("900x750")
# textbox=tk.Text(t,font=("arial", 14), width=85, height=20,bg="white",fg="darkblue")
# textbox.place(x=0,y=0)
# console=tk.Text(t,state="disabled", font=("fixedsys", 16, "bold"), insertbackground="red", width=90, height=12,bg="black",fg="lightgreen")
# console.place(x=0,y=500)
t.state("zoomed")
t.title("Pythonspace for practice")
# Textbox
textbox = tk.Text(
    t,
    font=("arial", 14),
    fg="gold",
    bg="darkblue"
)

textbox.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=0.7
)

# Console
console = tk.Text(
    t,
    state="disabled",
    font=("fixedsys", 16, "bold"),
    insertbackground="red",
    bg="black",
    fg="lightgreen"
)

console.place(
    x=0,
    rely=0.7,
    relwidth=1,
    relheight=0.3
)
if os.path.exists("test002.py"):
    pass
#for colon (:)
def indenting(e):
    wid=e.widget
    l=wid.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', l)
    ci=len(match.group(0)) if match else 0
    ni=ci+1
    wid.insert("insert", e.char+"\n"+"\t"*ni)
    return "break"
textbox.bind(":<Return>", indenting)
#for enter key 
def indentspace(e):
    wid=e.widget
    l=wid.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', l)
    ci=len(match.group(0)) if match else 0
    ni=ci+0
    wid.insert("insert", "\n"+"\t"*ni)
    return "break"

textbox.bind("<Return>", indentspace)
pl=14
h=14
w=79
#manipulate size like in notepad  ctrl+plus, ctrl+minus
def inc(p):
    global pl,h,w
    p=0
    pl+=1
    if pl<=28:
        h=h-h/pl
        w=w-w/pl
    else:
        pl-=1
        h=h-0
        w=w-0
    textbox.configure(font=("consolas", int(pl)), height=int(h),width=int(w))
textbox.bind("<Control-equal>", inc)

def dec(p):
    global pl,h,w
    p=0
    pl-=1
    if pl>=11:
        h=h+h/pl
        w=w+w/pl
    else:
        pl+=1
        h=h+0
        w=w+0
    textbox.configure(font=("consolas", int(pl)), height=int(h),width=int(w))
textbox.bind("<Control-minus>", dec)
    

def savefile(t_file):
    with open("test002.py", "w") as t_file:
        t_file.write(textbox.get(1.0, tk.END))
textbox.bind("<Control-s>", savefile)
textbox.bind("<Control-S>", savefile)

def compiler(c):
    c=0
    os.system("python test002.py & pause>nul")
t.bind("<F5>", compiler)

def run(p):
    p=0
    console.configure(state="normal")
    pr=subprocess.Popen("python test002.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o, e= pr.communicate()
    console.delete(1.0, tk.END)
    console.insert(1.0, o)
    console.insert(1.0, e)
    console.configure(state="disabled")
t.bind("<Control-F5>", run)
t.mainloop()