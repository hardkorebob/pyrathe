#!/usr/bin/env python3.10
# Application: PyRathe3
# Version: v.1
# Filename: you.py
# Written: Roberto Rodriguez Jr & just me this time
# 0.02: This editor rulez! (python rapid app & txt handling env)
# Email: hardkorebob@gmail.com
# Web: https://HARDKOREBOB.github.io
# Warranty: FREE WARRANTY 4 LIFE
# License: This software is provided under PRIVATE LICENSE.

import tkinter as tk
import tkinter.font as font
import os
import sys
import re
import time
import datetime
import threading
import subprocess
import requests
import segno as qr
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

class App:
    def __init__(self, root):
        self.root = root
        self.bg_color="#444" 
        self.txtPad_frames = []
        self.root.bind_all("<Control-R>", self.rss_program)

        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=13)
        self.create_editor()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def rss_program(self, event=None):
        os.execv(sys.executable, ["python3"] + sys.argv)

    def create_editor(self, event=None):
        tab = tk.Frame(self.root, bg=self.bg_color)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        tab.grid(row=0, column=0, sticky='nsew')
        action = Editor(tab)
        return "break"


class Editor:
    def __init__(self, parent):
        self.parent = parent
        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=13)
        self.bg_color = "#444"
        self.s_name = 0
        self.s_filetype = "_txt"
        self.qr_file = "0qr.png"
        self.me_file = "editor3.py"
        self.timerSymbols = ["|", "/", "-", "\\"]
        self.currentSymbolIndex = 0
        self.make_action()
        self.setup_keybindings()
        self.timelineThread()

    def make_action(self):
        self.action_frame = tk.Frame(self.parent, bg=self.bg_color,)
        self.action_frame.rowconfigure(0, weight=0)
        self.action_frame.rowconfigure(1, weight=0)
        self.action_frame.rowconfigure(2, weight=0)
        self.action_frame.rowconfigure(3, weight=1)
        self.action_frame.columnconfigure(0, weight=0)
        self.action_frame.columnconfigure(1, weight=1)
        self.action_frame.columnconfigure(2, weight=1)
        self.action_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)


        self.loadMe_button = tk.Button(
            self.action_frame,
            bg="#444",
            fg="#000",
            text="😻",
            command=self.loadMe,
            highlightbackground="#444",
            font=self.font,
        )
        self.loadMe_button.grid(row=2, column=0)

        self.timerLabel = tk.Label(
            self.action_frame, 
            bg=self.bg_color, 
            fg="yellow", 
            font=self.font,
        )
        self.timerLabel.grid(row=2, column=0, sticky="new", pady=1, padx=1,)

        self.timerLabel2 = tk.Label(
            self.action_frame, 
            bg=self.bg_color, 
            fg="yellow", 
            font=self.font,
        )
        self.timerLabel2.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        self.timerBar = tk.Text(
            self.action_frame,
            fg="yellow",
            bg=self.bg_color,
            relief=tk.FLAT,
            highlightcolor="#555",
            insertbackground="white",
            font=self.font,
            cursor="shuttle",
            highlightbackground=self.bg_color,
            insertwidth=10,
            height=1,
        )
        self.timerBar.grid(row=0, column=1, sticky="nsew", pady=1, padx=1, columnspan=2)
        
        self.msgBuffer = tk.Text(
            self.action_frame,
            fg="#777",
            bg=self.bg_color,
            relief=tk.FLAT,
            highlightcolor="red",
            insertbackground="white",
            font=self.font,
            cursor="pirate",
            highlightbackground="#333",
            insertwidth=10,
            height=8,
            wrap=tk.WORD,
        )
        self.msgBuffer.grid(row=2, column=1, sticky="nsew", padx=1, pady=1, columnspan=2)
        
        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label = tk.Label(
            self.action_frame,
            image = img,
            bg=self.bg_color,
            cursor="cross",
        )
        self.qr_label.grid(row=1, column=0, sticky='ns', pady=1, padx=1)
        self.qr_label.image = img
        
        self.txtPad = tk.Text(
            self.action_frame,
            fg="orange",
            bg=self.bg_color,
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightcolor="orange",
            insertbackground="red",
            font=self.font,
            cursor="heart",
            highlightbackground="#333",
            insertwidth=3,
            spacing1=9,
            spacing3=9,
            padx=10,
            undo=True,
        )
        Percolator(self.txtPad).insertfilter(ColorDelegator())
        self.txtPad.grid(row=3, column=1, sticky="nsew", columnspan=2, pady=1, padx=1)

        self.line_numbers = tk.Text(
            self.action_frame,
            relief=tk.FLAT,
            bg=self.bg_color,
            fg="#777",
            font=self.font,
            highlightbackground=self.bg_color,
            highlightcolor=self.bg_color,
            cursor="spider",
            spacing1=9,
            spacing3=9,
            width=5,
        )
        self.line_numbers.grid(row=3, column=0, sticky="nse", pady=1, padx=1)

        self.cpos = tk.Label(
            self.action_frame,
            text="1,0", 
            bg=self.bg_color, 
            fg="#777", 
            font=self.font,
        )
        self.cpos.grid(row=2, column=0, sticky="s", padx=1, pady=1)

        self.url_entry = tk.Entry(
            self.action_frame,
            bg=self.bg_color,
            fg="#000",
            insertbackground="yellow",
            highlightbackground="#333",
            highlightcolor="#777",
            cursor="star",
            font=self.font,
            relief=tk.FLAT,
        )
        self.url_entry.grid(row=1, column=1, sticky="ew", padx=1, pady=1,)

        self.qr_Entry = tk.Entry(
            self.action_frame,
            bg=self.bg_color,
            fg="red",
            insertbackground="red",
            highlightbackground="#333",
            cursor="spraycan",
            font=self.font,
            relief=tk.FLAT,
        )
        self.qr_Entry.grid(row=1, column=2, sticky='ew', padx=1, pady=1,)
        self.txtPad.focus_set()
        
################### KEEP HERE #################

    def timelineThread(self):
        self.char_line = threading.Thread(target=self.update_timerSymbol)
        self.char_line.daemon = True
        self.char_line.start()
        self.char_line2 = threading.Thread(target=self.update_timerSymbolLine)
        self.char_line2.daemon = True
        self.char_line2.start()

    def update_timerLabel(self, event=None):
        cursor_position = self.timerBar.index(tk.INSERT)
        line, col = cursor_position.split(".")
        i = int(col)
        c = int(line) - 1
        self.timerLabel.configure(text=f"🕐\n{str(c)}{str(i)}m")

    def update_timerSymbolLine(self, event=None):
        while True:
            self.timerBar.insert("end", ">")
            self.update_timerLabel()
            time.sleep(60)

    def update_timerSymbol(self, event=None):
        while True:
            symbol = self.timerSymbols[self.currentSymbolIndex]
            self.timerLabel2.configure(text=symbol)
            time.sleep(1)  
            self.currentSymbolIndex = (self.currentSymbolIndex + 1) % len(self.timerSymbols)

##########################################

    def mkQr(self, event=None):
        entry = self.qr_Entry.get()
        self.qrcode = qr.make_qr(entry)
        self.qrcode.save(self.qr_file, scale=5, border=0, light=self.bg_color)       
        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {entry} _QR|code.generated +Displayn:-0\n")

    def get_fun_fact(self, event=None):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            fact = data.get("text", "")
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _fact? {fact}\n"
            )
        else:
            self.msgBuffer.insert("1.0", "#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _fact.fail\n")

    def get_url_data(self, event=None):
        focused = self.parent.focus_get()
        url = self.url_entry.get()
        try:
            response = requests.get(url, timeout=5)
            focused.insert("1.0", f"{response.text}\n")
            status_msg = f"GET {url} HTTP/1.1 {response.status_code} {response.reason}"
            self.msgBuffer.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{status_msg}\n",
            )
        except requests.exceptions.RequestException as e:
            self.msgBuffer.insert("1.0", f"Error: {str(e)}\n")

    def gethistData(self, event=None):
        focused = self.parent.focus_get()
        command = "find ~ -name \"places.sqlite\" -exec sqlite3 -line {} '.dump' \; | grep http | tr ',' ' ' | awk '{print $5$6}' | sed \"s/'//g\""
        try:
            hist = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if hist.returncode == 0:
                focused.insert("1.0", f"{hist.stdout}\n")
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _web.history\n",
                )
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{hist.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{str(e)}\n"
            )
        return "break"

    def full_weather(self, event=None):
        focused = self.parent.focus_get()
        command = "curl http://wttr.in > w ; perl ./fmtw.pl w"
        try:
            weather = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if weather.returncode == 0:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _weather.local\n",
                )
                focused.insert("1.0", f"{weather.stdout}\n")
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{weather.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{str(e)}\n"
            )
        return "break"

    def weather(self, event=None):
        command = "curl http://wttr.in > w ; perl ./fmtw.pl w | head -7"
        try:
            weather = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if weather.returncode == 0:
                self.msgBuffer.insert("1.0", f"{weather.stdout}\n")
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{weather.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{str(e)}\n"
            )
        return "break"

    def loadMe(self, event=None):
        focused = self.parent.focus_get()
        command = f"cat {self.me_file}"
        try:
            if isinstance(focused, tk.Text):
                self.txtPad.focus_set()
                me = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                )
                if me.returncode == 0:
                    focused.insert("1.0", f"{me.stdout}\n")
                    self.msgBuffer.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _loaded meow {self.me_file} \n",
                    )
                else:
                    self.msgBuffer.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{me.stderr}\n",
                    )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _{str(e)}\n"
            )
        return "break"


    def update_cursor_position(self, event=None):
        focused = self.parent.focus_get()
        try:
            if isinstance(focused, tk.Text):
                cursor_position = focused.index(tk.INSERT)
                line, col = cursor_position.split(".")
                self.cpos.configure(text=f"{line},{col}")

                self.line_numbers.configure(state="normal")
                self.line_numbers.delete("1.0", tk.END)
                first, last = focused.yview()
                first_line = int(first * float(focused.index("end").split(".")[0])) + 1
                last_line = int(last * float(focused.index("end").split(".")[0]))
                line_numbers = "\n".join(str(i) for i in range(first_line, last_line))
                self.line_numbers.insert("1.0", line_numbers)
                self.line_numbers.delete("end-1c", "end")
                self.line_numbers.configure(state="disabled")
                self.line_numbers.yview_moveto(first)
        except KeyError:
            pass

    def add_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")
        return "break"

    def select_all_text(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def top_of_buffer(self, event):
        event.widget.mark_set("insert", "1.0")
        return "break"

    def bottom_of_buffer(self, event):
        event.widget.mark_set("insert", "end")
        return "break"

    def kill_line(self, event):
        event.widget.delete("insert linestart", "insert lineend")
        return "break"

    def clear_buffer(self, event):
        focused = self.parent.focus_get()
        if isinstance(focused, tk.Text):
            focused.delete("1.0", "end")
        return "break"

    def save_focused_to_file(self, event):
        focused = self.parent.focus_get()
        content = focused.get("1.0", "end-1c")
        filename = f"{self.s_name}{self.s_filetype}"
        self.s_name += 1
        with open(filename, "w") as file:
            file.write(content)
        self.msgBuffer.insert(
            "1.0",
            f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Buffer Saved\n",
        )
        return "break"

    def save_me_to_file(self, event):
        focused = self.parent.focus_get()
        content = focused.get("1.0", "end-1c")
        filename = self.me_file
        with open(filename, "w") as file:
            file.write(content)
        self.msgBuffer.insert(
            "1.0",
            f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Myself & I Saved\n",
        )
        return "break"

    def execute_python_code(self, event):
        focused = self.parent.focus_get()
        code = focused.get("1.0", "end-1c")
        try:
            exec(code, globals())
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def eval_python_code(self, event):
        focused = self.parent.focus_get()
        code = focused.get("insert linestart", "insert lineend")
        try:
            output = eval(code, globals())
            self.msgBuffer.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} >>> {output}\n",
            )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def execute_sh_command(self, event):
        focused = self.parent.focus_get()
        command = focused.get("insert linestart", "insert lineend")
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                focused.insert(
                    "insert linestart",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ",
                )
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n",
                )
                focused.insert("1.0", f"{result.stdout}")
            else:
                focused.insert(
                    "insert linestart",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ",
                )
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {result.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"


    def setup_keybindings(self):
        # defaults
        # ctrl t = transpose char
        # ctrl b = cursor back
        # ctrl f = cursor fwd
        # ctrl k = delete from cursor to end of line
        # ctrl d = delete from front of insert
        # ctrl h = backspace
        # ctrl p = line up
        # ctrl i = insert tab
        # ctrl e = end of line
        # ctrl a = begin of line
        # ctrl o = add a newline
        # ctrl y = paste
        self.parent.bind_all("<Control-l>", self.clear_buffer)
        self.parent.bind_all("<Control-s>", self.save_focused_to_file)
        self.parent.bind_all("<Control-S>", self.save_me_to_file)
        self.parent.bind_all("<Control-Alt-a>", self.select_all_text)
        self.parent.bind_all("<Control-n>", self.top_of_buffer)
        self.parent.bind_all("<Control-m>", self.bottom_of_buffer)
        self.parent.bind_all("<Control-Shift-Return>", self.execute_python_code)
        self.parent.bind_all("<Control-Alt-Return>", self.eval_python_code)
        self.parent.bind_all("<Control-Return>", self.execute_sh_command)
        self.parent.bind_all("<Control-Alt-a>", self.select_all_text)
        self.parent.bind_all("<ButtonRelease-1>", self.update_cursor_position)
        self.parent.bind_all("<KeyRelease>", self.update_cursor_position)
        self.parent.bind_all("<Control-P>", self.loadMe)
        self.parent.bind_all("<Control-u>", self.kill_line)
        self.parent.bind_all("<Control-I>", self.add_indent)
        self.parent.bind_all("<Control-w>", self.weather)
        self.parent.bind_all("<Control-X>", self.get_fun_fact)
        self.parent.bind_all("<Control-C>", self.get_url_data)
        self.parent.bind_all("<Control-Z>", self.mkQr)
        self.parent.bind_all("<Control-W>", self.full_weather)
        self.parent.bind_all("<Control-H>", self.gethistData)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("999x666+100+100")
    root.title("#$%&*^  PyRathe3   #allerrorsmatter #codwolf")
    root.configure(background="#444")
    app = App(root)
    root.mainloop()


#$%&*^ 03:23 cat editor3.py

#$%&*^ 04:06 
