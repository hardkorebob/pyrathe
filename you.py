#!/usr/bin/env python3.10
# Application: PyRathe2
# Version: v.1
# Filename: you.py
# Written: Roberto Rodriguez Jr & ChatGPT
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
        super().__init__()
        self.root = root
        self.rootConfig()
        self.setup_keybindings()
        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=13)
        self.pyrathe_init()
        self.timelineThread()

    def rootConfig(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

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
        self.root.bind_all("<Control-l>", self.clear_buffer)
        self.root.bind_all("<Control-s>", self.save_focused_to_file)
        self.root.bind_all("<Control-S>", self.save_me_to_file)
        self.root.bind_all("<Control-Alt-a>", self.select_all_text)
        self.root.bind_all("<Control-n>", self.top_of_buffer)
        self.root.bind_all("<Control-m>", self.bottom_of_buffer)
        self.root.bind_all("<Control-Shift-Return>", self.execute_python_code)
        self.root.bind_all("<Control-Alt-Return>", self.eval_python_code)
        self.root.bind_all("<Control-Return>", self.execute_sh_command)
        self.root.bind_all("<Control-Alt-a>", self.select_all_text)
        self.root.bind_all("<ButtonRelease-1>", self.update_cursor_position)
        self.root.bind_all("<KeyRelease>", self.update_cursor_position)
        self.root.bind_all("<Control-r>", self.rss_program)
        self.root.bind_all("<Control-Q>", self.quit_program)
        self.root.bind_all("<Control-D>", self.add_new_tab)
        self.root.bind_all("<Control-C>", self.del_new_tab)
        self.root.bind_all("<Control-X>", self.add_term_tab)
        self.root.bind_all("<Control-Z>", self.add_py_tab)
        self.root.bind_all("<Control-u>", self.kill_line)
        self.root.bind_all("<Control-I>", self.add_indent)
        self.root.bind_all("<Control-f>", self.get_fun_fact)
        self.root.bind_all("<Control-w>", self.weather)
        self.root.bind_all("<Control-W>", self.full_weather)
        self.root.bind_all("<Control-H>", self.gethistData)

    def pyrathe_init(self):
        self.s_name = 0
        self.s_filetype = "_txt"
        self.qr_file = "0qr.png"
        self.me_file = "you.py"
        self.txtPad_frames = []
        self.timerSymbols = ["|", "/", "-", "\\"]
        self.currentSymbolIndex = 0
        self.action()
        self.get_fun_fact()

    def action(self):
        self.paned = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=10,
            cursor="target",
            bg="#444",
        )
        self.paned.rowconfigure(0, weight=1)
        self.paned.columnconfigure(0, weight=1)
        self.paned.grid(row=0, column=0, sticky="nsew")
 
        self.action_frame = tk.Frame(self.paned, bg="#444", padx=1, pady=1)
        self.action_frame.rowconfigure(0, weight=0)
        self.action_frame.rowconfigure(1, weight=0)
        self.action_frame.rowconfigure(2, weight=0)
        self.action_frame.rowconfigure(3, weight=1)
        self.action_frame.rowconfigure(4, weight=0)

        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=0)
        self.action_frame.grid(row=0, column=0, sticky="nsew")

        self.timerBar = tk.Text(
            self.action_frame,
            fg="yellow",
            bg="#444",
            relief=tk.FLAT,
            highlightcolor="#555",
            insertbackground="white",
            font=self.font,
            cursor="shuttle",
            highlightbackground="#444",
            insertwidth=10,
            height=1,
        )
        self.timerBar.grid(row=0, column=0, sticky="nsew", pady=1, padx=1, columnspan=5)

        self.timerLabel = tk.Label(
            self.action_frame, 
            bg="#444", 
            fg="yellow", 
            font=self.font,
        )
        self.timerLabel.grid(row=1, column=4, sticky="nesw", pady=1, padx=1)
        
        self.url_entry = tk.Entry(
            self.action_frame,
            bg="#444",
            fg="#000",
            insertbackground="#000",
            highlightbackground="#333",
            cursor="star",
            font=self.font,
            relief=tk.FLAT,
            width=100,
        )
        self.url_entry.grid(row=4, column=2, sticky="nsew", padx=1, pady=1)

        self.url_button = tk.Button(
            self.action_frame, 
            bg="#444", 
            fg="#000",
            text="🕷",
            #text="✅",
            #text="🕸", 
            command=self.getUrldata,           	
            highlightbackground="#444",
            font=self.font,
        )
        self.url_button.grid(row=4, column=1, sticky="w", padx=1, pady=1)

        self.hist_button = tk.Button(
            self.action_frame, 
            bg="#444", 
            fg="#777", 
            text="🔎", 
            command=self.gethistData,             
            highlightbackground="#444",
            font=self.font,
        )
        self.hist_button.grid(row=4, column=3, sticky="w", padx=1, pady=1)

        self.qr_Entry = tk.Entry(
            self.action_frame,
            bg="#444",
            fg="red",
            insertbackground="red",
            highlightbackground="#333",
            cursor="spraycan",
            font=self.font,
            relief=tk.FLAT,
        )
        self.qr_Entry.grid(row=4, column=3, sticky='nesw', padx=1, pady=1)

        self.qr_Button = tk.Button(
            self.action_frame,
            bg="#444", 
            fg="#777", 
            text="📷", 
            command=self.mkQr,             
            highlightbackground="#444",
            font=self.font,
        )    
        self.qr_Button.grid(row=4, column=4, sticky='nwse', padx=1, pady=1,)

        self.msgBuffer = tk.Text(
            self.action_frame,
            fg="#777",
            bg="#444",
            relief=tk.FLAT,
            highlightcolor="red",
            insertbackground="white",
            font=self.font,
            cursor="pirate",
            highlightbackground="#444",
            insertwidth=10,
            height=12,
            wrap=tk.WORD,
        )
        self.msgBuffer.grid(row=2, column=0, sticky="nsew", padx=1, pady=1, columnspan=3)
        
        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label = tk.Label(
            self.action_frame,
            image = img,
            bg="#444",
            cursor="cross",
        )
        self.qr_label.grid(row=2, column=3, sticky='nsw', pady=1, padx=1, columnspan=2)
        self.qr_label.image = img
        
        self.txtPad = tk.Text(
            self.action_frame,
            fg="orange",
            bg="#444",
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
        self.txtPad.grid(row=3, column=0, sticky="nsew", columnspan=5, pady=1, padx=1)

        self.line_numbers = tk.Text(
            self.action_frame,
            relief=tk.FLAT,
            bg="#444",
            fg="#777",
            font=self.font,
            highlightbackground="orange",
            highlightcolor="#555",
            cursor="spider",
            spacing1=9,
            spacing3=9,
            width=5,
        )
        self.line_numbers.grid(row=3, column=4, sticky="nsew", pady=1, padx=1)

        self.cpos = tk.Label(
            self.action_frame,
            text="1,0", 
            bg="#444", 
            fg="#777", 
            font=self.font,
        )
        self.cpos.grid(row=3, column=4, sticky="s", padx=1, pady=1)

        self.timerLabel2 = tk.Label(
            self.action_frame, 
            bg="#444", 
            fg="yellow", 
            font=self.font,
        )
        self.timerLabel2.grid(row=0, column=1, sticky="nse", padx=1, pady=1)

        self.fullWeather_button = tk.Button(
            self.action_frame,
            bg="#444",
            text="🌞",
            command=self.full_weather,
            highlightbackground="#444",
            font=self.font,
        )
        self.fullWeather_button.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)

        self.loadMe_button = tk.Button(
            self.action_frame,
            bg="#444",
            fg="black",
            text="😻",
            command=self.loadMe,
            highlightbackground="#444",
            font=self.font,
            pady=1,
        )
        self.loadMe_button.grid(row=4, column=0, sticky="nswe", padx=1, pady=1)

        self.py_button = tk.Button(
            self.action_frame,
            bg="#444",
            text="🐍",
            command=self.add_py_tab,
            highlightbackground="#444",
            font=self.font,
            pady=1,
        )
        self.py_button.grid(row=0, column=3, sticky="nsw", padx=1, pady=1)

        self.term_button = tk.Button(
            self.action_frame,
            bg="#444",
            fg="black",
            text="⊡⁁",
            command=self.add_term_tab,
            highlightbackground="#444",
            font=self.font,
            pady=1,
        )
        self.term_button.grid(row=2, column=4, sticky="nsew", padx=1)

        self.addtab_button = tk.Button(
            self.action_frame,
            bg="#444",
            fg="green",
            text="⊞", #◫", 
            command=self.add_new_tab,
            highlightbackground="#444",
            font=self.font,
            pady=1,
        )
        self.addtab_button.grid(row=0, column=3, sticky="nse", padx=1, pady=1)

        self.kill_button = tk.Button(
            self.action_frame,
            bg="#444",
            fg="red",
            text="⊟", #⚠□", #
            command=self.del_new_tab,
            highlightbackground="#444",
            font=self.font,
            pady=1,
        )
        self.kill_button.grid(row=0, column=4, sticky="nswe", padx=1)

        self.paned.add(self.action_frame)
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

    def add_new_tab(self, event=None):
        self.new_frame = tk.Frame(self.paned, bg="#444", padx=1)
        self.new_frame.columnconfigure(0, weight=1)
        self.new_frame.rowconfigure(0, weight=1)
        self.new_frame.grid(row=0, column=0, sticky="nsew")

        self.new_txtPad = tk.Text(
            self.new_frame,
            fg="orange",
            bg="#444",
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightcolor="blue",
            insertbackground="#000",
            font=self.font,
            cursor="heart",
            highlightbackground="#333",
            padx=1,
            undo=True,
        )
        self.new_txtPad.grid(row=0, column=0, sticky="nsew")
        self.txtPad_frames.append((self.new_frame, self.new_txtPad))
        self.paned.add(self.new_frame)
        self.new_txtPad.focus_set()

    def add_py_tab(self, event=None):
        self.py_frame = tk.Frame(self.paned, bg="#444")
        self.py_frame.columnconfigure(0, weight=1)
        self.py_frame.rowconfigure(0, weight=1)
        self.py_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.py_frame.winfo_id()
        py_xterm = os.system("xterm -into %d -geometry 150x50 -e python3 &" % wid)
        self.txtPad_frames.append((self.py_frame, py_xterm))
        self.paned.add(self.py_frame)

    def add_term_tab(self, event=None):
        self.term_frame = tk.Frame(self.paned, bg="#444")
        self.term_frame.columnconfigure(0, weight=1)
        self.term_frame.rowconfigure(0, weight=1)
        self.term_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.term_frame.winfo_id()
        xterm = os.system("xterm -into %d -geometry 150x50 &" % wid)
        self.txtPad_frames.append((self.term_frame, xterm))
        self.paned.add(self.term_frame)

    def del_new_tab(self, event=None):
        command = "pkill xterm"
        subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if self.txtPad_frames:
            last_frame, last_txtPad = self.txtPad_frames.pop()
            last_frame.destroy()
        return "break"
       
    def mkQr(self):
        entry = self.qr_Entry.get()
        self.qrcode = qr.make_qr(entry)
        self.qrcode.save(self.qr_file, scale=5, border=0, light="#444")       
        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {entry} _QR code.generated +Displayn:-0\n")

    def get_fun_fact(self, event=None):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            fact = data.get("text", "")
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {fact}\n"
            )
        else:
            self.msgBuffer.insert("1.0", "Failed to fetch the fact.\n")

    def getUrldata(self, event=None):
        focused = self.root.focus_get()
        url = self.url_entry.get()
        try:
            response = requests.get(url, timeout=5)
            focused.insert("1.0", f"{response.text}\n")
            status_msg = f"GET {url} HTTP/1.1 {response.status_code} {response.reason}"
            self.msgBuffer.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {status_msg}\n",
            )
        except requests.exceptions.RequestException as e:
            self.msgBuffer.insert("1.0", f"Error: {str(e)}\n")

    def gethistData(self, event=None):
        focused = self.root.focus_get()
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
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} Printed Mozilla History\n",
                )
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {hist.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def full_weather(self, event=None):
        focused = self.root.focus_get()
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
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} Full Weather Report\n",
                )
                focused.insert("1.0", f"{weather.stdout}\n")
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
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
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stderr}\n",
                )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def loadMe(self):
        focused = self.root.focus_get()
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
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} meow {self.me_file} _loaded\n",
                    )
                else:
                    self.msgBuffer.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {me.stderr}\n",
                    )
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"


    def update_cursor_position(self, event=None):
        focused = self.root.focus_get()
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
        focused = self.root.focus_get()
        if isinstance(focused, tk.Text):
            focused.delete("1.0", "end")
        return "break"

    def save_focused_to_file(self, event):
        focused = self.root.focus_get()
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
        focused = self.root.focus_get()
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
        focused = self.root.focus_get()
        code = focused.get("1.0", "end-1c")
        try:
            exec(code, globals())
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def eval_python_code(self, event):
        focused = self.root.focus_get()
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
        focused = self.root.focus_get()
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

    def quit_program(self, event=None):
        self.root.quit()
        return "break"

    def rss_program(self, event=None):
        os.execv(sys.executable, ["python3"] + sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("999x666+100+100")
    root.title("#$%&*^  PyRathe2   #allerrorsmatter #codwolf")
    root.configure(background="#444")
    app = App(root)
    root.mainloop()

 
