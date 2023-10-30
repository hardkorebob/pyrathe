#!/usr/bin/env python3
# Written by Roberto Rodriguez Jr <hardkorebob@gmail.com>
import tkinter as tk
import tkinter.font as font
import threading
import os
import sys
import re
import time
import datetime
import subprocess
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator


class App:

    def __init__(self, root):
        self.root = root
        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=11)
        self.pyrathe_init()
        self.setup_keybindings()

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
        self.root.bind_all('<ButtonRelease-1>', self.update_cursor_position)
        self.root.bind_all("<KeyRelease>", self.update_cursor_position)
        self.root.bind_all("<Control-r>", self.rss_program)
        self.root.bind_all("<Control-Q>", self.quit_program)
        self.root.bind_all("<Control-D>", self.add_new_tab)
        self.root.bind_all("<Control-C>", self.del_new_tab)
        self.root.bind_all("<Control-X>", self.add_term_tab)
        self.root.bind_all("<Control-Z>", self.add_py_tab)
        self.root.bind_all("<Control-u>", self.backkill)
        self.root.bind_all("<Control-z>", self.add_indent)

    def pyrathe_init(self):
        self.s_name = 0
        self.s_filetype = "_txt"
        self.create()
        self.timeline()
        self.txtPad_frames = []

    def create(self):
        self.onover = tk.Frame(self.root, padx=18, pady=18, bg="black")
        self.onover.grid(row=0, column=0, sticky='nsew')
        self.msgBar = tk.Text(self.onover, fg="red", bg="black", relief=tk.FLAT, highlightcolor="red", insertbackground="orange", padx=10, pady=10, font=self.font, cursor="pirate", highlightbackground="black", height=4, insertwidth=6)
        self.msgBar.grid(row=0, column=0, sticky='nsew')
        self.overtop = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=18, cursor="spider", bg="black")
        self.overtop.grid(row=1, column=0, sticky='nsew')
        self.top = tk.Frame(self.overtop, padx=18, pady=18, bg="black")
        self.top.grid(row=0, column=0, sticky='nsew')
        self.txtPad = tk.Text(self.top, fg="orange", bg="black", wrap=tk.WORD, relief=tk.FLAT, highlightcolor="orange", insertbackground="red", padx=10, pady=10, font=self.font, cursor="heart", highlightbackground="black", spacing1=10, spacing3=10, spacing2=10, insertwidth=6)
        Percolator(self.txtPad).insertfilter(ColorDelegator())
        self.txtPad.grid(row=0, column=0, sticky='nsew')
        self.cposFrame = tk.Frame(self.root, bg="black")
        self.cposFrame.grid(row=2, column=0, sticky='se')
        self.cpos = tk.Label(self.cposFrame, text='1,0', bg="black", fg="orange", font=self.font)
        self.cpos.grid(row=0, column=0, padx=18, pady=10)
        self.overtop.add(self.top)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.overtop.rowconfigure(0, weight=1)
        self.overtop.columnconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        self.onover.rowconfigure(0, weight=1)
        self.onover.columnconfigure(0, weight=1)
        self.txtPad.focus_set()

    def add_py_tab(self, event=None):
        self.py_frame = tk.Frame(self.overtop, padx=18, pady=18, bg="black")
        self.py_frame.grid(row=0, column=0, sticky='nsew')
        wid = self.py_frame.winfo_id()
        os.system('xterm -into %d -geometry 180x50 -e python3 &' % wid)
        self.py_frame.columnconfigure(0, weight=1)
        self.py_frame.rowconfigure(0, weight=1)
        self.txtPad_frames.append(self.py_frame)
        self.overtop.add(self.py_frame)

    def add_term_tab(self, event=None):
        self.term_frame = tk.Frame(self.overtop, padx=18, pady=18, bg="black")
        self.term_frame.grid(row=0, column=0, sticky='nsew')
        wid = self.term_frame.winfo_id()
        os.system('xterm -into %d -geometry 180x50 &' % wid)
        self.term_frame.columnconfigure(0, weight=1)
        self.term_frame.rowconfigure(0, weight=1)
        self.txtPad_frames.append(self.term_frame)
        self.overtop.add(self.term_frame)

    def add_new_tab(self, event=None):
        new_frame = tk.Frame(self.overtop, padx=18, pady=18, bg="black")
        new_frame.grid(row=0, column=0, sticky='nsew')
        new_txtPad = tk.Text(new_frame, fg="orange", bg="black", wrap=tk.WORD, relief=tk.FLAT, highlightcolor="orange", insertbackground="red", padx=10, pady=10, font=self.font, cursor="heart", highlightbackground="black", spacing1=10, spacing3=10, spacing2=10, insertwidth=6)
        new_txtPad.grid(row=0, column=1, sticky='nsew')
        new_frame.columnconfigure(1, weight=1)
        new_frame.rowconfigure(0, weight=1)
        self.overtop.add(new_frame)
        self.txtPad_frames.append((new_frame, new_txtPad))
        new_txtPad.focus_set()

    def del_new_tab(self, event=None):
        if self.txtPad_frames:
            last_frame, last_txtPad = self.txtPad_frames.pop()
            self.overtop.forget(last_frame)
            last_frame.destroy()
        return "break"

    def update_cursor_position(self, event):
        focused = self.root.focus_get()
        if isinstance(focused, tk.Text):
            cursor_position = focused.index(tk.INSERT)
            line, col = cursor_position.split('.')
            self.cpos.configure(text=f"{line},{col}")

    def select_all_text(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def top_of_buffer(self, event):
        event.widget.mark_set("insert", "1.0")
        return "break"

    def bottom_of_buffer(self, event):
        event.widget.mark_set("insert", "end")
        return "break"

    def backkill(self, event):
        event.widget.delete("insert linestart", "insert lineend")
        return "break"

    def clear_buffer(self, event):
        event.widget.delete("1.0", "end")
        return "break"

    def save_focused_to_file(self, event):
        focused = self.root.focus_get()
        content = focused.get("1.0", "end-1c")
        filename = f"{self.s_name}{self.s_filetype}"
        self.s_seq += 1
        with open(filename, "w") as file:
            file.write(content)
        self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Buffer Saved\n")
        return "break"

    def save_me_to_file(self, event):
        focused = self.root.focus_get()
        content = focused.get("1.0", "end-1c")
        filename = "me"
        with open(filename, "w") as file:
            file.write(content)
        self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Myself & I Saved\n")
        return "break"

    def execute_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("1.0", "end-1c")
        try:
            exec(code, globals())
        except Exception as e:
            self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"

    def eval_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("insert linestart", "insert lineend")
        try:
            output = eval(code, globals())
            self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n# >>>{output}\n")
        except Exception as e:
            self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"

    def execute_sh_command(self, event):
        focused = self.root.focus_get()
        command = focused.get("insert linestart", "insert lineend")
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ")
                self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n")
                focused.insert("1.0", f"{result.stdout}")
            else:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ")
                self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n{result.stderr}\n")
        except Exception as e:
            self.msgBar.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n{str(e)}\n")
        return "break"

    def quit_program(self, event=None):
        command = "pkill xterm"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.root.quit()
        return "break"

    def rss_program(self, event=None):
        os.execv(sys.executable, ['python3'] + sys.argv)

    def timeline(self):
        self.char_line = threading.Thread(target=self.update_timeline)
        self.char_line.daemon = True
        self.char_line.start()

    def update_timeline(self):
        sym = ">"
        while True:
            self.update_buffer(sym)
            time.sleep(60)

    def update_buffer(self, sym):
        self.msgBar.insert("end", sym)

    def add_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r'^(\s+)', line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="black")
    app = App(root)
    root.mainloop()

#$%&*^ 02:44 cat me
