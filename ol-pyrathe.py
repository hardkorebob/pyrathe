#!/usr/bin/env python3
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
from geopy.geocoders import Nominatim


class App:

    def __init__(self, root):
        self.root = root
        self.rootConfig()
        self.pyrathe_init()
        self.timelineThread()

    def rootConfig(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.setup_keybindings()
        self.font = font.nametofont("TkFixedFont")
        self.font.configure(size=12)

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
        self.root.bind_all("<Control-Alt-a>", self.select_all_text)
        self.root.bind_all("<Control-n>", self.top_of_buffer)
        self.root.bind_all("<Control-m>", self.bottom_of_buffer)
        self.root.bind_all("<Control-Shift-Alt-Return>", self.execute_python_code)
        self.root.bind_all("<Control-Alt-Return>", self.eval_python_code)
        self.root.bind_all("<Control-Shift-Return>", self.exe_sh_command)
        self.root.bind_all("<Control-Return>", self.execute_sh_command)
        self.root.bind_all("<Control-Alt-a>", self.select_all_text)
        self.root.bind_all("<ButtonRelease-1>", self.update_cursor_position)
        self.root.bind_all("<KeyRelease>", self.update_cursor_position)
        self.root.bind_all("<Control-r>", self.rss_program)
        self.root.bind_all("<Control-Q>", self.quit_program)
        self.root.bind_all("<Control-G>", self.create_grid)
        self.root.bind_all("<Control-D>", self.add_new_tab)
        self.root.bind_all("<Control-C>", self.del_grid)
        self.root.bind_all("<Control-X>", self.add_term_tab)
        self.root.bind_all("<Control-Z>", self.add_py_tab)
        self.root.bind_all("<Control-u>", self.kill_line)
        self.root.bind_all("<Control-I>", self.add_indent)
        self.root.bind_all("<Control-U>", self.stay_indent)
        self.root.bind_all("<Control-f>", self.get_fun_fact)
        self.root.bind_all("<Control-w>", self.weather)
        self.root.bind_all("<Control-W>", self.full_weather)
        self.root.bind_all("<Control-A>", self.getAddr)
        self.root.bind_all("<Control-T>", self.mkQr)
        self.root.bind_all("<Control-H>", self.gethistData)





    def pyrathe_init(self):
        self.s_name = 0
        self.s_filetype = "@"
        self.text_widgets = []
        self.timerSymbols = ["|", "/", "-", "\\"]
        self.currentSymbolIndex = 0
        self.qr_file = "qr.png"
        self.mainF()
        self.panedF()
        self.utilF()
        self.create_grid()
        self.add_new_tab()
        self.text_widgets[0]

    def mainF(self):
        self.mainFrame = tk.Frame(self.root, bg='#444', pady=10, padx=5, bd=0)
        self.mainFrame.rowconfigure(0, weight=0)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure((1,2), weight=0)
        self.mainFrame.grid(row=0, column=0, sticky='nsew')

        self.msgBuffer = tk.Text(
            self.mainFrame,
            fg="red",
            bg="#444",
            relief=tk.FLAT,
            highlightcolor="red",
            insertbackground="orange",
            font=self.font,
            cursor="pirate",
            highlightbackground="#555",
            insertwidth=10,
            height=12,
            wrap=tk.WORD,
            padx=10,
            pady=10,)
        self.msgBuffer.grid(row=0, column=0, sticky="nsew")

        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label = tk.Label(
            self.mainFrame,
            image = img,
            bg="#444",
            cursor="cross",
        )
        self.qr_label.grid(row=0, column=1, sticky='nswe', padx=15,)
        self.qr_label.image = img
        
        img2 = tk.PhotoImage(file="palnet0.png")
        self.pl_label = tk.Label(
            self.mainFrame,
            image = img2,
            bg="#444",
            cursor="cross",
        )
        self.pl_label.grid(row=0, column=2, sticky='nswe', padx=5, pady=5,)
        self.pl_label.image = img2
        
    def panedF(self):
        self.paned = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=15,
            cursor="target",
            bg="#666", bd=0)
        self.paned.rowconfigure(0, weight=1)
        self.paned.columnconfigure(0, weight=1)
        self.paned.grid(row=1, column=0, sticky="nsew")

    def utilF(self):
        self.statusBarFrame = tk.Frame(self.root, bg="#444", pady=5, bd=0)
        self.statusBarFrame.columnconfigure(0, weight=0)
        self.statusBarFrame.columnconfigure(1, weight=0)
        self.statusBarFrame.columnconfigure(2, weight=1)
        self.statusBarFrame.rowconfigure(0, weight=0)
        self.statusBarFrame.rowconfigure(1, weight=1)
        self.statusBarFrame.grid(row=2, column=0, sticky="nsew")

        self.timer_label = tk.Label(
            self.statusBarFrame, 
            bg="#444", 
            fg="orange", 
            font=self.font,
        )
        self.timer_label.grid(row=0, column=1, sticky="nsew")

        self.timer_label2 = tk.Label(
            self.statusBarFrame, 
            bg="#444", 
            fg="yellow", 
            font=self.font,
	    padx=10,
        )
        self.timer_label2.grid(row=0, column=0, sticky="nsew")

        self.timerBar = tk.Text(
            self.statusBarFrame,
            fg="yellow",
            bg="#444",
            relief=tk.FLAT,
            highlightcolor="green",
            insertbackground="green",
            font=self.font,
            cursor="shuttle",
            highlightbackground="#555",
            insertwidth=10,
            height=1,
            padx=5
        )
        self.timerBar.grid(row=0, column=2, sticky="nsew", pady=5)

        self.cpos = tk.Label(
            self.root, 
            text="1,0", 
            bg="#444", 
            fg="#BBB", 
            font=self.font,)
        self.cpos.grid(row=3, column=0, sticky="nesw", padx=5, pady=5)

        self.row_var = tk.StringVar()
        self.gridr_entry = tk.Entry(self.statusBarFrame, relief=tk.FLAT, width=3, font=self.font, bg="#444", fg="red", 
                                    textvariable=self.row_var, cursor="target", highlightbackground="#555",)
        self.gridr_entry.insert(0, "1")
        self.gridr_entry.grid(row=0, column=6, padx=5, pady=5, sticky='e')

        self.col_var = tk.StringVar()
        self.gridc_entry = tk.Entry(self.statusBarFrame, relief=tk.FLAT, width=3, bg="#444", fg="orange", 
                                    font=self.font, textvariable=self.col_var, cursor="target", highlightbackground="#555",)
        self.gridc_entry.insert(0, "2")
        self.gridc_entry.grid(row=0, column=7, padx=5, pady=5, sticky='e')

        self.gps_Entry = tk.Entry(
            self.statusBarFrame,
            bg="#444",
            fg="red",
            insertbackground="red",
            highlightbackground="#555",
            cursor="dotbox",
            font=self.font,
            relief=tk.FLAT,
            takefocus=False,)
        self.gps_Entry.grid(row=0, column=3, sticky='nswe', pady=5, padx=5,)

        self.qr_Entry = tk.Entry(
            self.statusBarFrame,
            bg="#444",
            fg="red",
            insertbackground="red",
            highlightbackground="#555",
            cursor="spraycan",
            font=self.font,
            relief=tk.FLAT,
            takefocus=False,)
        self.qr_Entry.grid(row=0, column=4, sticky='nswe', pady=5, padx=5,)





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
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _Mozilla History\n",)
                 
                focused.insert("1.0", f"{hist.stdout}\n")
            else:
                self.msgBuffer.insert(
                    "1.0",
                    f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {hist.stderr}\n",)
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n"
            )
        return "break"

    def get_gps_coordinates(self, address):
        geolocator = Nominatim(user_agent="uniqueName")
        location = geolocator.geocode(address)
    
        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude
            return self.latitude, self.longitude
        else:
            return None

    def getAddr(self, event=None):
        address = self.gps_Entry.get()
        coordinates = self.get_gps_coordinates(address)   
        if coordinates:
            self.latitude, self.longitude = coordinates
            self.msgBuffer.insert("1.0", f"#$%&*^ Latitude: {self.latitude}, Longitude: {self.longitude} {address}\n")
        else:
            self.msgBuffer.insert("1.0", "#$%&*^ Location not found.\n")
        self.gps_Entry.delete(0, 'end')

    def mkQr(self, event=None):
        entry = self.qr_Entry.get()
        self.qrcode = qr.make_qr(entry)
        self.qrcode.save(self.qr_file, scale=5, border=0, light="#444") 
        img = tk.PhotoImage(file=self.qr_file)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} _code _{entry}_ generated :-) -->\n")
        self.qr_Entry.delete(0, "end")

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
                self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {weather.stdout}\n")
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
            self.msgBuffer.insert("1.0", "#$%&*^ {datetime.datetime.now().strftime('%H:%M')} !Failed to fetch the fact.\n")

    def timelineThread(self):
        self.char_line = threading.Thread(target=self.update_timerSymbol)
        self.char_line.daemon = True
        self.char_line.start()
        self.char_line2 = threading.Thread(target=self.update_timerSymbolLine)
        self.char_line2.daemon = True
        self.char_line2.start()

    def update_timer_label(self, event=None):
        cursor_position = self.timerBar.index(tk.INSERT)
        line, col = cursor_position.split(".")
        i = int(col)
        c = int(line) - 1
        self.timer_label.configure(text=f"{str(c)}{str(i)}m")

    def update_timerSymbolLine(self, event=None): # Dont move these funcs
        while True:
            self.timerBar.insert("end", ">")
            self.update_timer_label()
            time.sleep(60)

    def update_timerSymbol(self, event=None):
        while True:
            symbol = self.timerSymbols[self.currentSymbolIndex]
            self.timer_label2.configure(text=symbol)
            time.sleep(1)  
            self.currentSymbolIndex = (self.currentSymbolIndex + 1) % len(self.timerSymbols)
        
    def create_grid(self, event=None):
        self.grid_frame = tk.Frame(self.paned, bg="#444", bd=0, padx=5)
        self.my_grid()
        self.paned.add(self.grid_frame)

    def my_grid(self):
        row_var = int(self.gridr_entry.get())        
        col_var = int(self.gridc_entry.get())
        for i in range(row_var):
            row_widgets = []
            for j in range(col_var):
                text_widget = tk.Text(self.grid_frame, bg="#444", 
                    fg="#BBB", 
                    highlightcolor="orange",
                    insertbackground="red",
                    relief=tk.FLAT,
                    font=self.font, 
                    padx=10,
                    pady=10, 
                    wrap=tk.WORD, 
                    cursor="heart", 
                    undo=True,
                    highlightbackground="#555",
                    spacing1=5, bd=0)
                text_widget.grid(row=i, column=j, sticky='nsew')
                row_widgets.append(text_widget)
                self.grid_frame.grid_columnconfigure(j, weight=1)
                self.grid_frame.grid_rowconfigure(i, weight=1)
                Percolator(text_widget).insertfilter(ColorDelegator())
            self.text_widgets.append((self.grid_frame, row_widgets))
    
    def del_grid(self, event=None):
        if self.text_widgets:
            nlast_frame, nlast_txtPad = self.text_widgets.pop()
            self.paned.forget(nlast_frame)
            nlast_frame.destroy()
        return "break"

    def add_new_tab(self, event=None):
        self.new_frame = tk.Frame(self.paned, bg="#444", padx=5)
        self.new_frame.columnconfigure(0, weight=1)
        self.new_frame.rowconfigure(0, weight=1)
        self.new_frame.grid(row=0, column=0, sticky="nsew")

        self.new_txtPad = tk.Text(
            self.new_frame,
            fg="orange",
            bg="#444",
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightcolor="orange",
            insertbackground="red",
            font=self.font,
            cursor="heart",
            highlightbackground="#333",
            undo=True,
            padx=10,
            pady=10,)
        self.new_txtPad.grid(row=0, column=0, sticky="nsew")
        self.paned.add(self.new_frame)
        self.text_widgets.append((self.new_frame, self.new_txtPad))
        
    def add_py_tab(self, event=None):
        self.py_frame = tk.Frame(self.paned, bg="#444")
        self.py_frame.columnconfigure(0, weight=1)
        self.py_frame.rowconfigure(0, weight=1)
        self.py_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.py_frame.winfo_id()
        py_xterm = os.system("st -w %d -g 200x30 -e python3 &" % wid)
        self.text_widgets.append((self.py_frame, py_xterm))
        self.paned.add(self.py_frame)

    def add_term_tab(self, event=None):
        self.term_frame = tk.Frame(self.paned, bg="#444")
        self.term_frame.columnconfigure(0, weight=1)
        self.term_frame.rowconfigure(0, weight=1)
        self.term_frame.grid(row=0, column=0, sticky="nsew")
        wid = self.term_frame.winfo_id()
        xterm = os.system("st -w %d -g 200x30 &" % wid)
        self.text_widgets.append((self.term_frame, xterm))
        self.paned.add(self.term_frame)

    def update_cursor_position(self, event=None):
        focused = self.root.focus_get()
        try:
            if isinstance(focused, tk.Text):
                cursor_position = focused.index(tk.INSERT)
                line, col = cursor_position.split(".")
                self.cpos.configure(text=f"{line},{col}")
        except KeyError:
            pass

    def stay_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")
        return "break"

    def add_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}    ")
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
            f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Buffer Saved!\n",
        )
        return "break"

    def execute_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("1.0", "end-1c")
        try:
            exec(code, globals())
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"

    def eval_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("insert linestart", "insert lineend")
        try:
            output = eval(code, globals())
            self.msgBuffer.insert(
                "1.0",
                f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} >>> {output}\n")
        except Exception as e:
            self.msgBuffer.insert(
                "1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
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
                self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n")
                self.new_txtPad.insert("1.0", f"{result.stdout}")
                focused.delete("insert linestart", "insert lineend")
            else:
                self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {result.stderr}\n")
        except Exception as e:
            self.msgBuffer.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"

    def exe_sh_command(self, event):
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
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n")
                focused.insert("1.0", f"{result.stdout}\n")
                focused.delete("insert linestart", "insert lineend")
            else:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {result.stderr}\n")
        except Exception as e:
            focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"

    def quit_program(self, event=None):
        self.root.quit()
        return "break"

    def rss_program(self, event=None):
        os.execv(sys.executable, ["python3"] + sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("999x666+100+100")
    root.title("#$%&*^  PyRathe   #allerrorsmatter #0xFu    ~dislux-hapfyl")
    root.configure(background="#444")
    app = App(root)
    root.mainloop()

