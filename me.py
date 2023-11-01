#!/usr/bin/env python3
# Application: PyRathe
# Version: v.1
# Filename: me.py
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
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator


class App:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.rootConfig()
        self.setup_keybindings()
        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=11)
        self.pyrathe_init()
        self.timelineThread()

    def rootConfig(self):
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=0)

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
        self.root.bind_all("<Control-g>", self.goto_next_search)
        self.root.bind_all("<Control-j>", self.goto_previous_search)

    def pyrathe_init(self):
        self.s_name = 0
        self.s_filetype = "_txt"
        self.txtPad_frames = []
        self.myTimer()
        self.wtrFrame()
        self.msgBar()
        self.textPad()
        self.createUtilBar()
        self.weather()
        self.get_fun_fact()

    def myTimer(self):
        self.timerFrame = tk.Frame(self.root, bg="black", pady=2, padx=10)
        self.timerFrame.columnconfigure(0, weight=0)
        self.timerFrame.columnconfigure(1, weight=1)
        self.timerFrame.rowconfigure(0, weight=1)
        self.timerFrame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.timerLabel = tk.Label(
            self.timerFrame, bg="black", fg="green", text="000", font=self.font
        )
        self.timerLabel.grid(row=0, column=0, sticky="new")
        self.timerBar = tk.Text(
            self.timerFrame,
            fg="green",
            bg="black",
            relief=tk.FLAT,
            highlightcolor="green",
            insertbackground="green",
            font=self.font,
            cursor="shuttle",
            highlightbackground="black",
            insertwidth=10,
            height=2,
        )
        self.timerBar.grid(row=0, column=1, sticky="nsew")

    def timelineThread(self):
        self.char_line = threading.Thread(target=self.update_timerSymbol)
        self.char_line.daemon = True
        self.char_line.start()

    def update_timerLabel(self, event=None):
        cursor_position = self.timerBar.index(tk.INSERT)
        line, col = cursor_position.split(".")
        i = int(col)
        c = int(line) - 1
        self.timerLabel.configure(text=f"{str(c)}{str(i)}min")

    def update_timerSymbol(self, event=None):
        while True:
            self.timerBar.insert("end", ">")
            self.update_timerLabel()
            time.sleep(60)

    def wtrFrame(self):
        self.wtrFrame = tk.Frame(self.root, padx=10, bg="black")
        self.wtrFrame.rowconfigure(0, weight=0)
        self.wtrFrame.columnconfigure(0, weight=0)
        self.wtrFrame.grid(row=1, column=0, sticky="nsew")

        self.fullW_button = tk.Button(
            self.wtrFrame,
            bg="black",
            fg="#777",
            text="🌞",
            command=self.full_weather,
            highlightbackground="black",
        )
        self.fullW_button.grid(row=0, column=0, sticky="wens")

    def msgBar(self):
        self.msgBarFrame = tk.Frame(self.root, bg="black", padx=10)
        self.msgBarFrame.rowconfigure(0, weight=1)
        self.msgBarFrame.columnconfigure(0, weight=1)
        self.msgBarFrame.grid(row=1, column=1, sticky="nsew", columnspan=2)
        self.msgBar = tk.Text(
            self.msgBarFrame,
            fg="red",
            bg="black",
            relief=tk.FLAT,
            highlightcolor="red",
            insertbackground="orange",
            font=self.font,
            cursor="pirate",
            highlightbackground="black",
            insertwidth=10,
            height=12,
            wrap=tk.WORD,
        )
        self.msgBar.grid(row=0, column=0, sticky="nsew")

    def textPad(self):
        self.paned = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=10,
            cursor="target",
            bg="black",
        )
        self.paned.rowconfigure(0, weight=1)
        self.paned.columnconfigure(0, weight=1)
        self.paned.grid(row=2, column=1, sticky="nsew", columnspan=2)

        self.mainTxtFrame = tk.Frame(self.paned, bg="black", padx=10)
        self.mainTxtFrame.rowconfigure(0, weight=1)
        self.mainTxtFrame.columnconfigure(0, weight=1)
        self.mainTxtFrame.grid(row=0, column=0, sticky="nsew")
        self.txtPad = tk.Text(
            self.mainTxtFrame,
            fg="orange",
            bg="black",
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightcolor="orange",
            insertbackground="red",
            font=self.font,
            cursor="heart",
            highlightbackground="black",
            insertwidth=4,
            spacing1=9,
            spacing3=10,
            padx=5,
            undo=True,
        )
        Percolator(self.txtPad).insertfilter(ColorDelegator())
        self.txtPad.grid(row=0, column=0, sticky="nsew")
        self.paned.add(self.mainTxtFrame)
        self.txtPad.focus_set()

        self.lineFrame = tk.Frame(self.root, bg="black", padx=10, pady=8)
        self.lineFrame.rowconfigure(0, weight=1)
        self.lineFrame.columnconfigure(0, weight=0)
        self.lineFrame.grid(row=2, column=0, sticky="nesw")
        self.line_numbers = tk.Text(
            self.lineFrame,
            relief=tk.FLAT,
            bg="#000",
            fg="#666",
            font=self.font,
            highlightbackground="black",
            cursor="spider",
            spacing1=10,
            spacing3=10,
            width=5,
        )
        self.line_numbers.grid(row=0, column=0, sticky="nswe")

    def createUtilBar(self):
        self.utilFrame = tk.Frame(self.root, bg="black", pady=15, padx=10)
        self.utilFrame.rowconfigure(0, weight=1)
        self.utilFrame.columnconfigure(0, weight=1)
        self.utilFrame.columnconfigure(1, weight=0)
        self.utilFrame.columnconfigure(2, weight=0)
        self.utilFrame.columnconfigure(3, weight=0)
        self.utilFrame.columnconfigure(4, weight=0)
        self.utilFrame.columnconfigure(5, weight=0)
        self.utilFrame.columnconfigure(6, weight=1)
        self.utilFrame.columnconfigure(7, weight=0)
        self.utilFrame.columnconfigure(8, weight=0)
        self.utilFrame.grid(row=3, column=0, sticky="nsew", columnspan=2)
        self.cpos = tk.Label(
            self.utilFrame, text="1,0", bg="black", fg="#777", font=self.font,
        )
        self.cpos.grid(row=0, column=0, sticky="nsew")
        self.search_entry = tk.Entry(
            self.utilFrame, bg="black", fg="red", insertbackground="red"
        )
        self.search_entry.grid(row=0, column=1, sticky="nsw", padx=2)
        self.replace_entry = tk.Entry(
            self.utilFrame, bg="black", fg="red", insertbackground="red"
        )
        self.replace_entry.grid(row=0, column=2, sticky="nsw", padx=2)
        self.search_button = tk.Button(
            self.utilFrame, bg="black", fg="#777", text="Search", command=self.search
        )
        self.search_button.grid(row=0, column=3, sticky="nsw", padx=2)
        self.replace_button = tk.Button(
            self.utilFrame, bg="black", fg="#777", text="Replace", command=self.replace
        )
        self.replace_button.grid(row=0, column=4, sticky="nsw", padx=2)
        self.replace_all_button = tk.Button(
            self.utilFrame,
            bg="black",
            fg="#777",
            text="Replace All",
            command=self.replace_all,
        )
        self.replace_all_button.grid(row=0, column=5, sticky="nsw", padx=3)

        self.url_entry = tk.Entry(
            self.utilFrame,
            bg="black",
            fg="red",
            insertbackground="red",
        )
        self.url_entry.grid(row=0, column=6, sticky="ewns", padx=3)
        self.url_button = tk.Button(
            self.utilFrame, bg="black", fg="#777", text="Go", command=self.getUrldata
        )
        self.url_button.grid(row=0, column=7, sticky="wens", padx=3)
        self.hist_button = tk.Button(
            self.utilFrame, bg="black", fg="#777", text="H", command=self.gethistData
        )
        self.hist_button.grid(row=0, column=8, sticky="wens", padx=3)

    def add_new_tab(self, event=None):
        self.new_frame = tk.Frame(self.paned, bg="black", padx=10)
        self.new_frame.columnconfigure(0, weight=1)
        self.new_frame.rowconfigure(0, weight=1)
        self.new_frame.grid(row=0, column=0, sticky="nsew")
        self.new_txtPad = tk.Text(
            self.new_frame,
            fg="orange",
            bg="black",
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightcolor="orange",
            insertbackground="red",
            font=self.font,
            cursor="heart",
            highlightbackground="black",
            padx=5,
            undo=True,
        )
        self.new_txtPad.grid(row=0, column=0, sticky="nsew")
        self.paned.add(self.new_frame)
        self.txtPad_frames.append((self.new_frame, self.new_txtPad))
        self.new_txtPad.focus_set()

    def add_py_tab(self, event=None):
        self.py_frame = tk.Frame(self.paned, bg="black")
        self.py_frame.columnconfigure(0, weight=1)
        self.py_frame.rowconfigure(0, weight=1)
        self.py_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.py_frame.winfo_id()
        py_xterm = os.system("xterm -into %d -geometry 100x50 -e python3 &" % wid)
        self.txtPad_frames.append((self.py_frame, py_xterm))
        self.paned.add(self.py_frame)

    def add_term_tab(self, event=None):
        self.term_frame = tk.Frame(self.paned, bg="black")
        self.term_frame.columnconfigure(0, weight=1)
        self.term_frame.rowconfigure(0, weight=1)
        self.term_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.term_frame.winfo_id()
        xterm = os.system("xterm -into %d -geometry 200x50 &" % wid)
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
            self.paned.forget(last_frame)
            last_frame.destroy()
        return "break"

    def add_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")
        return "break"

    def get_fun_fact(self, event=None):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            fact = data.get("text", "")
            self.msgBar.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {fact}\n"
            )
        else:
            self.msgBar.insert("1.0", "Failed to fetch the fact.\n")

    def getUrldata(self, event=None):
        focused = self.root.focus_get()
        url = self.url_entry.get()
        try:
            response = requests.get(url, timeout=5)
            focused.insert("1.0", f"{response.text}\n")
            status_msg = f"GET {url} HTTP/1.1 {response.status_code} {response.reason}"
            self.msgBar.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {status_msg}\n",
            )
        except requests.exceptions.RequestException as e:
            self.msgBar.insert("1.0", f"Error: {str(e)}\n")

    def gethistData(self, event=None):
        focused = self.root.focus_get()
        command = "find . -name \"places.sqlite\" -exec sqlite3 -line {} '.dump' \; | grep http | tr ',' ' ' | awk '{print $5$6}' | sed \"s/'//g\""
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
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} Printed Mozilla History\n",
                )
            else:
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {hist.stderr}\n",
                )
        except Exception as e:
            self.msgBar.insert(
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
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} Full Weather Report\n",
                )
                focused.insert("1.0", f"{weather.stdout}\n")
            else:
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stderr}\n",
                )
        except Exception as e:
            self.msgBar.insert(
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
                self.msgBar.insert("1.0", f"{weather.stdout}\n")
            else:
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stderr}\n",
                )
        except Exception as e:
            self.msgBar.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def search(self, event=None):
        focused = self.root.focus_get()
        if isinstance(focused, tk.Text):
            focused.tag_remove("found", "1.0", tk.END)
            self.search_text = self.search_entry.get()
            if self.search_text:
                idx = "1.0"
                while True:
                    idx = focused.search(
                        self.search_text, idx, nocase=1, stopindex=tk.END
                    )
                    if not idx:
                        break
                    lastidx = f"{idx}+{len(self.search_text)}c"
                    focused.tag_add("found", idx, lastidx)
                    focused.tag_config("found", background="green")
                    idx = lastidx
                self.occurrences = list(focused.tag_ranges("found"))
            else:
                self.msgBar.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {self.search_text} Not Found!\n",
                    )
                if self.occurrences:
                    self.last_index = 0
                    focused.mark_set("insert", self.occurrences[0])
                    focused.see(self.occurrences[0])

    def goto_next_search(self, event=None):
        focused = self.root.focus_get()
        if self.occurrences and self.last_index is not None:
            self.last_index = (self.last_index + 1) % len(self.occurrences)
            focused.mark_set("insert", self.occurrences[self.last_index])
            focused.see(self.occurrences[self.last_index])
            return "break"

    def goto_previous_search(self, event=None):
        focused = self.root.focus_get()
        if self.occurrences and self.last_index is not None:
            self.last_index = (self.last_index - 1) % len(self.occurrences)
            focused.mark_set("insert", self.occurrences[self.last_index])
            focused.see(self.occurrences[self.last_index])
            return "break"

    def replace(self):
        focused = self.root.focus_get()
        if isinstance(focused, tk.Text):
            search_text = self.search_entry.get()
            replace_text = self.replace_entry.get()
            if search_text and replace_text:
                idx = focused.index(tk.INSERT)
                idx = focused.search(search_text, idx, nocase=1)
                if idx:
                    lastidx = f"{idx}+{len(search_text)}c"
                    focused.delete(idx, lastidx)
                    focused.insert(idx, replace_text)
                    focused.tag_remove("found", "1.0", tk.END)
                    focused.tag_add("found", idx, f"{idx}+{len(replace_text)}c")
                    focused.tag_config("found", background="green")
                    self.msgBar.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} Replaced_ {search_text} {replace_text}\n",
                    )
                else:
                    self.msgBar.insert(
                        "1.0",
                        f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {search_text} Not Found!\n",
                    )

    def replace_all(self):
        focused = self.root.focus_get()
        if isinstance(focused, tk.Text):
            search_text = self.search_entry.get()
            replace_text = self.replace_entry.get()
            content = self.txtPad.get("1.0", tk.END)
            replaced_content = content.replace(search_text, replace_text)
            self.txtPad.delete("1.0", tk.END)
            self.txtPad.insert("1.0", replaced_content)
            self.msgBar.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ALL*Replaced_ {search_text} {replace_text}\n",
            )

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
                first_line = int(first * float(focused.index("end").split(".")[0]))
                last_line = int(last * float(focused.index("end").split(".")[0]))
                line_numbers = "\n".join(
                    str(i) for i in range(first_line + 1, last_line)
                )
                self.line_numbers.insert("1.0", line_numbers)
                self.line_numbers.configure(state="disabled")
                self.line_numbers.yview_moveto(first)
        except KeyError:
            pass

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
        focused = self.txtPad.focus_get()
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
        self.msgBar.insert(
            "1.0",
            f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Buffer Saved\n",
        )
        return "break"

    def save_me_to_file(self, event):
        focused = self.root.focus_get()
        content = focused.get("1.0", "end-1c")
        filename = "me.py"
        with open(filename, "w") as file:
            file.write(content)
        self.msgBar.insert(
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
            self.msgBar.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def eval_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("insert linestart", "insert lineend")
        try:
            output = eval(code, globals())
            self.msgBar.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} >>> {output}\n",
            )
        except Exception as e:
            self.msgBar.insert(
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
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n",
                )
                focused.insert("1.0", f"{result.stdout}")
            else:
                focused.insert(
                    "insert linestart",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ",
                )
                self.msgBar.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {result.stderr}\n",
                )
        except Exception as e:
            self.msgBar.insert(
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
    root.title("#$%&*^  PyRathe   #allerrorsmatter")
    root.configure(background="black")
    app = App(root)
    root.mainloop()


#$%&*^ 17:47 cat me.py
