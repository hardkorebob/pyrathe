#!/usr/bin/env python3
# Written by Roberto Rodriguez Jr & ChatGPT
# hardkorebob@gmail.com
# Zettlekastenrhok v.999 [r.t.h.a.d.e]
# Rapid Text Handling And Dev Environment
# ratde.py: Rapid App & Text Dev Env
# codwolf_Software HARDKOREBOB.github.io
# Warranty: FREE WARRANTY 4 LIFE
# License: This software is provided under PRIVATE LICENSE
# PyRathe v.0(python rapid app & txt handling env by RoberRodri hardkorebob@gmail.com <customer service is NOT free>
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import tkinter.font as font
import threading, os, sys, re, time, datetime
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
class App:
    def __init__(self, root):
        self.root = ttk.Notebook(root, takefocus=False)
        self.font = font.nametofont("TkFixedFont")
        self.style = ttk.Style()
        self.font.configure(size=11)
        self.root.pack(fill=tk.BOTH, expand=1)
        self.zkr_init()
        self.setup_keybindings()
        self.style.configure("TNotebook", background="#696969");
        self.style.map("TNotebook.Tab", background=[("selected", "#696969")], foreground=[("selected", "orange")]);
        self.style.configure("TNotebook.Tab", background="#696969", foreground="#000");
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
        self.root.bind_all("<Control-Shift-Return>", self.execute_python_code)
        self.root.bind_all("<Control-Alt-Return>", self.eval_python_code)
        self.root.bind_all("<Control-Return>", self.execute_sh_command)
        self.root.bind_all("<Control-Alt-a>", self.select_all_text)
        self.root.bind_all("<KeyRelease>", self.update_cursor_position)
        self.root.bind_all("<Control-r>", self.rss_program)
        self.root.bind_all("<Control-D>", self.create_grid)
        self.root.bind_all("<Control-Q>", self.quit_program)
        self.root.bind_all("<Control-u>", self.backkill)
        self.root.bind_all("<Control-z>", self.add_indent)
        self.root.bind_all('<ButtonRelease-1>', self.update_cursor_position)
    def zkr_init(self):
        self.theme_bg = "#23252E"
        self.theme_fg = "#E9B96E"
        self.s_file_sequence = 0
        self.s_filename = "s"
        self.z_tabFrame()
        self.create_top_bar()
        self.textPaned()
        self.create_bot_bar()
        self.timeline()
    def z_tabFrame(self):
        self.primary_frame = tk.Frame(self.root, bd=0, bg="#000")
        self.primary_frame.grid(row=0, column=0, sticky='nsew')        
        self.primary_frame.grid_rowconfigure(0, weight=0) 
        self.primary_frame.grid_rowconfigure(1, weight=1) 
        self.primary_frame.grid_rowconfigure(2, weight=0) 
        self.root.add(self.primary_frame, text="PyRathe")
    def create_top_bar(self):
        self.top_bar = tk.Frame(self.primary_frame, bg="#000", height=24, bd=0)   
        self.top_bar.grid(row=0, column=0, sticky='nsew')
        self.shell_label = tk.Text(self.top_bar, fg="red", bg="#000", relief=tk.FLAT, highlightcolor="#000", insertbackground="#000", height=3, padx=10, pady=10, font=self.font, cursor="pirate", inactiveselectbackground="#000")
        self.shell_label.pack(fill=tk.BOTH, expand=1)
    def textPaned(self):
        self.horizontal_split = tk.PanedWindow(self.primary_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=18, cursor="spider")
        self.horizontal_split.grid(row=1, column=0, sticky='nsew') 
        self.primary_frame.grid_columnconfigure(0, weight=1)
        self.primary_frame.grid_rowconfigure(1, weight=1)
        self.term2 = tk.Frame(self.horizontal_split, bg="#000", relief=tk.FLAT, width=900, bd=0)
        self.term2.grid(row=0, column=0, sticky='nsew')
        wid = self.term2.winfo_id()
        os.system('xterm -into %d -geometry 150x50 &' % wid)
        self.horizontal_split.add(self.term2)
        self.term = tk.Frame(self.horizontal_split, bg="#000", relief=tk.FLAT, width=900, bd=0)
        self.term.grid(row=0, column=0, sticky='nsew')
        wid = self.term.winfo_id()
        os.system('xterm -into %d -geometry 150x50 -e python3 &' % wid)
        self.horizontal_split.add(self.term)
        self.text0 = tk.Frame(self.horizontal_split, bd=0, padx=18, pady=18, bg="#000")
        self.text1 = tk.Text(self.text0, bg=self.theme_bg, fg=self.theme_fg, highlightcolor="orange", insertbackground="red", bd=0, font=self.font, spacing1=9, spacing3=9, spacing2=9, padx=9, pady=9, wrap=tk.WORD, cursor="heart")
        Percolator(self.text1).insertfilter(ColorDelegator())
        self.text0.grid_rowconfigure(0, weight=1)
        self.text0.grid_columnconfigure(0, weight=1)
        self.text1.grid(row=0, column=0, sticky='nsew')
        self.horizontal_split.add(self.text0)
    def create_grid(self, event):
        self.grid_frame = tk.Frame(self.horizontal_split, bd=0, padx=18, pady=18, bg="#000")
        self.text_widgets = []
        self.my_grid()
        self.horizontal_split.add(self.grid_frame)
    def my_grid(self):
        row_var = int(self.gridr_entry.get())        
        col_var = int(self.gridc_entry.get())
        for i in range(row_var):
            row_widgets = []
            for j in range(col_var):
                text_widget = tk.Text(self.grid_frame, bg=self.theme_bg, fg=self.theme_fg, highlightcolor="orange", insertbackground="red", bd=0, font=self.font, spacing1=9, spacing3=9, spacing2=9, padx=9, pady=9, wrap=tk.WORD, cursor="heart", )
                Percolator(text_widget).insertfilter(ColorDelegator())
                text_widget.grid(row=i, column=j, sticky='nsew')
                row_widgets.append(text_widget)
                self.grid_frame.grid_columnconfigure(j, weight=1)
                self.grid_frame.grid_rowconfigure(i, weight=1)
            self.text_widgets.append(row_widgets)
    def create_bot_bar(self):
        self.status_bar = tk.Frame(self.primary_frame, bg="#000", height=15, bd=0, padx=18, pady=5)    
        self.status_bar.grid(row=2, column=0, sticky='nsew')
        self.status_bar.grid_columnconfigure(0, weight=1)
        self.status_bar.grid_columnconfigure(1, weight=0)
        self.status_bar.grid_columnconfigure(2, weight=0)
        self.status_bar.grid_columnconfigure(3, weight=0)
        self.status_bar.grid_columnconfigure(4, weight=0)
        self.status_bar.grid_columnconfigure(5, weight=0)
        self.status_bar.grid_columnconfigure(6, weight=0)
        self.status_bar.grid_columnconfigure(7, weight=0)
        self.status_bar.grid_columnconfigure(8, weight=0)
        self.status_bar.grid_columnconfigure(9, weight=0)
        self.status_bar.grid_columnconfigure(10, weight=0)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_bar, variable=self.progress_var, maximum=20*60, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.timer_label = tk.Label(self.status_bar, text='20:00', bg="#000", fg="#089143")
        self.timer_label.grid(row=0, column=1, padx=2, pady=2)
        self.start_button_20min = tk.Button(self.status_bar, text="Work", command=self.start_timer, takefocus=False, bg="#089143", fg="orange")
        self.start_button_20min.grid(row=0, column=2, padx=5, pady=5)
        self.progress_var_5min = tk.DoubleVar()
        self.progress_bar_5min = ttk.Progressbar(self.status_bar, variable=self.progress_var_5min, maximum=5*60, mode='determinate')
        self.progress_bar_5min.grid(row=0, column=5, padx=10, pady=10, sticky='nsew')
        self.timer_label_5min = tk.Label(self.status_bar, text='05:00', bg="#000", fg="#910813")
        self.timer_label_5min.grid(row=0, column=4, padx=2, pady=2)
        self.start_button_5min = tk.Button(self.status_bar, text="Break", command=self.start_timer_5min, takefocus=False, bg="red", fg="black")
        self.start_button_5min.grid(row=0, column=3, padx=2, pady=2)      
        self.cpos = tk.Label(self.status_bar, text='1,0', bg="#000", fg="orange", width=14)
        self.cpos.grid(row=0, column=6, padx=2, pady=2)
        self.gridr_label = tk.Label(self.status_bar, text='R', bg="#000", fg="#d9d9d9")
        self.gridr_label.grid(row=0, column=7, padx=2, pady=8)    
        self.row_var = tk.StringVar()
        self.gridr_entry = tk.Entry(self.status_bar, relief=tk.FLAT, width=3, bg="#000", fg="red", textvariable=self.row_var, cursor="target")
        self.gridr_entry.grid(row=0, column=8, padx=2, pady=5)
        self.gridc_label = tk.Label(self.status_bar, text='C', bg="#000", fg="#d9d9d9")
        self.gridc_label.grid(row=0, column=9, padx=2, pady=8)
        self.col_var = tk.StringVar()
        self.gridc_entry = tk.Entry(self.status_bar, relief=tk.FLAT, width=3, bg="#000", fg="orange", textvariable=self.col_var, cursor="target")
        self.gridc_entry.grid(row=0, column=10, padx=2, pady=5)     
    def start_timer(self):
        self.start_time = time.time()
        self.update_progress_bar()
    def update_progress_bar(self):
        elapsed_time = time.time() - self.start_time
        self.progress_var.set(elapsed_time)
        mins, secs = divmod(20*60 - int(elapsed_time), 60)
        self.timer_label.config(text=f'{mins:02}:{secs:02}')
        if elapsed_time < 20*60:
            self.root.after(1000, self.update_progress_bar)
    def start_timer_5min(self):
        self.start_time_5min = time.time()
        self.update_progress_bar_5min()
    def update_progress_bar_5min(self):
        elapsed_time = time.time() - self.start_time_5min
        self.progress_var_5min.set(elapsed_time)
        mins, secs = divmod(5*60 - int(elapsed_time), 60)
        self.timer_label_5min.config(text=f'{mins:02}:{secs:02}')
        if elapsed_time < 5*60:
           self.root.after(1000, self.update_progress_bar_5min)
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
        filename = f"{self.s_filename}{self.s_file_sequence}"
        self.s_file_sequence += 1
        with open(filename, "w") as file:
            file.write(content)
        self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {filename} _Buffer Saved\n")
        return "break"
    def execute_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("1.0", "end-1c")
        try:
            exec(code, globals())
        except Exception as e:
            self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"     
    def eval_python_code(self, event):
        focused = self.root.focus_get()
        code = focused.get("insert linestart", "insert lineend")
        try:
            output = eval(code, globals())
            self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n# >>>{output}\n")
        except Exception as e:
            self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {str(e)}\n")
        return "break"
    def execute_sh_command(self, event):
        focused = self.root.focus_get()
        command = focused.get("insert linestart", "insert lineend")  
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ")
                self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} {command}\n")
                focused.insert("1.0", f"{result.stdout}")
            else:
                focused.insert("insert linestart", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')} ")
                self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n{result.stderr}\n")
        except Exception as e:
            self.shell_label.insert("1.0", f"#$%&*^ {datetime.datetime.now().strftime('%H:%M')}\n{str(e)}\n")
        return "break"
    def quit_program(self, event=None):
        command = "pkill xterm"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.root.quit()
        return "break"
    def rss_program(self, event=None):
        command = "pkill xterm"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.execv(sys.executable, ['python3'] + sys.argv)
    def timeline(self):
        self.char_line = threading.Thread(target=self.update_timeline) 
        self.char_line.daemon = True
        self.char_line.start()
    def update_timeline(self):
        sym = f">"
        while True:
            self.update_buffer(sym)
            time.sleep(60)
    def update_buffer(self, sym):
        self.shell_label.insert("end", sym)
    def add_indent(self, event):
        text = event.widget
        line = text.get("insert linestart", "insert")
        match = re.match(r'^(\s+)', line)
        whitespace = match.group(0) if match else ""
        text.insert("insert", f"\n{whitespace}")
if __name__ == "__main__":
    root = tk.Tk()
    root.title("#$%&*^  [Zettlekastenrhok]    (PyRathe) {#allerrorsmatter #0xfu #dfc #ghd #rthade}")
    app = App(root)
    root.mainloop()
