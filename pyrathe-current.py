#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as font
import tkinter.filedialog as tkf
import os
import sys
import re
import time 
import datetime
import threading
import subprocess
import requests
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
from geopy.geocoders import Nominatim


class RootWindow(tk.Tk):
    def __init__(_):
        super().__init__()
        _.fpList = []
        _.fl=None
        _.btnC='#555'
        _.btnFC='white'
        _.hbC='#444'
        _.fpbgC='#444'
        _.font = font.nametofont("TkFixedFont")
        _.font.configure(size=12)
        _.sW=10

        _.bind("<Control-r>", _.restart_program)
        _.bind("<Control-Q>", _.quit_program)

        _.fp = tk.PanedWindow(_, orient=tk.HORIZONTAL, sashwidth=_.sW, relief=tk.RAISED, bg="gray", showhandle=True, sashpad=5)
        _.fp.pack(expand=1, fill='both')

        f = tk.Frame(_.fp, padx=10, bg=_.fpbgC)
        f.pack(expand=1, fill='both')

        logo = tk.PhotoImage(file="palnet0.png")
        logol = tk.Label(f, image = logo, padx=3, pady=3,
                                bg="#444", cursor="pirate", )
        logol.pack(expand=1, fill=_.fl)
        logol.image = logo

        weatherBtn = tk.Button(f, text=' ☀ ️', command=_.showWeather, padx=10, 
                       pady=10, bg=_.btnC, fg=_.btnFC, highlightbackground=_.hbC, font=_.font, )
        weatherBtn.pack(expand=1, fill=_.fl)

        me = tk.Button(f, text='ᕕ( ᐛ )ᕗ', command=_.showMe, padx=10, pady=10,
                       bg=_.btnC,  fg=_.btnFC, highlightbackground=_.hbC, font=_.font,  )
        me.pack(expand=1, fil=_.fl)
        
        txtpad = tk.Button(f, text="'͜▭▭ι═══════ﺤ", command=_.showPad, padx=10, pady=10,
                        bg=_.btnC, fg=_.btnFC, highlightbackground=_.hbC, font=_.font, )
        txtpad.pack(expand=1, fill=_.fl)

        pyrepl = tk.Button(f, text='╾━╤デ╦︻', command=_.showRepl, padx=10, pady=10, bg=_.btnC, fg=_.btnFC, highlightbackground=_.hbC, font=_.font, )
        pyrepl.pack(expand=1, fill=_.fl)

        terminal = tk.Button(f, text='─=≡Σʕっ•ᴥ•ʔっ', command=_.showTerm, padx=10, pady=10, bg=_.btnC, fg=_.btnFC, highlightbackground=_.hbC, font=_.font, )
        terminal.pack(expand=1, fill=_.fl)

        deleteWindowBtn = tk.Button(f, text='X', command=_.delFp, padx=10, pady=10, bg=_.btnC, fg='red', highlightbackground=_.hbC, font=_.font, )
        deleteWindowBtn.pack(expand=1, fill=_.fl)

        _.fp.add(f)

    def quit_program(self, event):
        quit()

    def restart_program(self, event):
        os.execv(sys.executable, ["python3"] + sys.argv)

    def showWeather(_, event=None):
        x = WPad(_, 'black', 'yellow', 'white', )
        command = "curl http://wttr.in > w ; perl ./fmtw.pl w"
        try:
            weather = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,)
            if weather.returncode == 0:
                x.tp.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n {weather.stdout}\n")
            else:
                x.tp.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stderr}\n")
        except Exception as e:
            x.tp.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        _.fpList.append(x)
        _.fp.add(x)

    def showMe(_, event=None):
        x = TxtPad(_, '#444', '#EEE', 'red',)
        x.timelineThread()
        f = open("project0.py", "r")
        me = f.read()
        x.tp.insert("1.0", me)
        _.fpList.append(x)
        _.fp.add(x)
        x.tp.focus_set()

    def showPad(_, event=None):
        x = TxtPad(_, '#444', '#EEE', 'red', )
        x.tp.focus_set()
        x.timelineThread()
        _.fpList.append(x)
        _.fp.add(x)

    def showRepl(_, event=None):
        x = PyRepl(_)
        _.fpList.append(x)
        _.fp.add(x)

    def showTerm(_, event=None):
        x = Xterm(_)
        _.fpList.append(x)
        _.fp.add(x)

    def delFp(_, event=None):
        if not _.fpList:
            return
        else:
            nlast_frame = _.fpList.pop()
            _.fp.forget(nlast_frame)
            nlast_frame.destroy()            

        
class TxtPad(tk.Frame): 

    def __init__(_, ap, bC, fC, iC,):
        super().__init__(ap)

        f = tk.Frame(_, bg=bC, padx=10, pady=10,)
        f.pack(expand=1, fill='both')

        _.font = font.nametofont("TkFixedFont")
        _.font.configure(size=12)

        _.timerSymbols = ["|", "/", "-", "\\"]
        _.currentSymbolIndex = 0

        ff = tk.Frame(f, bg=bC)
        ff.pack(expand=0, fill='both')

        _.timer_label_total = tk.Label(ff, text="", padx=10, pady=10, bg=bC, fg='orange', font=_.font, )
        _.timer_label_total.pack(expand=0, side='left')

        _.timer_anim = tk.Label(ff, text="", padx=10, pady=10, bg=bC, fg='yellow', font=_.font, )
        _.timer_anim.pack(expand=0, fill='both', side='left')

        _.timerBar = tk.Text(ff, bg=bC, fg='yellow', insertbackground='green', font=_.font, cursor="shuttle", 
                             highlightbackground=bC, highlightcolor='green', height=1, relief='flat', padx=3, pady=3,)
        _.timerBar.pack(expand=1, fill='x')

        _.msg = tk.Label(f, text="", bg="#444", fg="red", font=_.font,)
        _.msg.pack()

        _.tp = tk.Text(f, bg=bC, fg=fC, insertbackground=iC, font=_.font, cursor="heart", 
                       spacing1=5, spacing3=5, insertwidth=5, padx=10, pady=10,
                       highlightcolor='orange', undo=True, wrap='word',)
        Percolator(_.tp).insertfilter(ColorDelegator())
        _.tp.pack(expand=1, fill='both')

        _.pos = tk.Label(f, text="1,0", bg="#444", fg="#BBB", font=_.font, padx=10, pady=10, )
        _.pos.pack(expand=0, fill='both')

        _.tp.bind("<Control-l>", _.clear_buffer)
        _.tp.bind("<Control-Alt-a>", _.select_all_text)
        _.tp.bind("<Control-n>", _.top_of_buffer)
        _.tp.bind("<Control-m>", _.bottom_of_buffer)
        _.tp.bind("<Control-u>", _.kill_line)
        _.tp.bind("<Control-I>", _.add_indent)
        _.tp.bind("<Control-U>", _.stay_indent)
        _.tp.bind("<Control-s>", _.save)
        _.tp.bind("<Control-S>", _.save_myself)
        _.tp.bind("<Control-Return>", _.exe_sh_command)
        _.tp.bind("<ButtonRelease-1>", _.update_cursor_position)
        _.tp.bind("<KeyRelease>", _.update_cursor_position)

    def timelineThread(_):
        _.char_line = threading.Thread(target=_.update_timerSymbol)
        _.char_line.daemon = True
        _.char_line.start()
        _.char_line2 = threading.Thread(target=_.update_timerSymbolLine)
        _.char_line2.daemon = True
        _.char_line2.start()

    def update_timer_total(_, event=None):
        cursor_position = _.timerBar.index(tk.INSERT)
        line, col = cursor_position.split(".")
        i = int(col)
        c = int(line) - 1
        _.timer_label_total.configure(text=f"{str(c)}{str(i)}m")

    def update_timerSymbolLine(_, event=None):
        while True:
            _.timerBar.insert("end", ">")
            _.update_timer_total()
            time.sleep(60)

    def update_timerSymbol(_, event=None):
        while True:
            symbol = _.timerSymbols[_.currentSymbolIndex]
            _.timer_anim.configure(text=symbol)
            time.sleep(1)  
            _.currentSymbolIndex = (_.currentSymbolIndex + 1) % len(_.timerSymbols)

    def update_cursor_position(_, event=None):
        focused = _.tp.focus_get()
        cursor_position = focused.index(tk.INSERT)
        line, col = cursor_position.split(".")
        _.pos.configure(text=f"{line},{col}")

    def clear_buffer(_, event):
        event.widget.delete('1.0', 'end')
        return "break"

    def stay_indent(_, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")
        return "break"

    def add_indent(_, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}    ")
        return "break"

    def select_all_text(_, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def top_of_buffer(_, event):
        event.widget.mark_set("insert", "1.0")
        return "break"

    def bottom_of_buffer(_, event):
        event.widget.mark_set("insert", "end")
        return "break"

    def kill_line(_, event):
        event.widget.delete("insert linestart", "insert lineend")
        return "break"

    def save(_, event):
        f = tkf.asksaveasfile(mode='w')
        text2save = event.widget.get('1.0', 'end-1c')
        f.write(text2save)
        f.close()
        return "break"

    def save_myself(_, event):
        focused = _.tp.focus_get()
        if focused is None:
            return
        content = focused.get("1.0", "end-1c")
        filename = "project0.py"
        with open(filename, "w") as file:
            file.write(content)
        _.msg.configure(text=f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Saved!\n")
        return "break"

    def exe_sh_command(_, event):
        focused = _.tp.focus_get()
        command = focused.get("insert linestart", "insert lineend")
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, )
            if result.returncode == 0:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ")
                focused.insert("1.0", f"{result.stdout}\n")
            else:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {result.stderr}\n")
        except Exception as e:
            focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"


class WPad(tk.Frame): 
    def __init__(_, ap, bC, fC, iC, ):
        super().__init__(ap)
        f = tk.Frame(_)
        f.pack(expand=1, fill='both')
        _.tp = tk.Text(f, bg=bC, fg=fC, insertbackground=iC, cursor="star", padx=20, pady=20,)
        _.tp.pack(expand=1, fill='both')
       
    
class PyRepl(tk.Frame):
    def __init__(_, ap):
        super().__init__(ap)
        _.f = tk.Frame(_, bg='black', padx=10, pady=10)
        _.f.pack(expand=1, fill='both')
        wid = _.f.winfo_id()
        pyRepl = os.system("st -w %d -g 100x40 -e python3 &" % wid)


class Xterm(tk.Frame):
    def __init__(_, ap):
        super().__init__(ap)
        _.f = tk.Frame(_, bg='black', padx=10, pady=10)
        _.f.pack(expand=1, fill='both')
        wid = _.f.winfo_id()
        xterm = os.system("st -w %d -g 130x58 &" % wid)


if __name__ == '__main__':
    go = RootWindow()
    go.title("Pyrathe  #allerrorsmatter")
    go.mainloop()








