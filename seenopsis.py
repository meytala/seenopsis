# -*- coding: utf-8 -*-
import seenopsis_data, paths, os, traceback
import tkinter as tk
from tkinter import ttk, filedialog

class Seenopsis(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.report_callback_exception = self.callback_error
        self.input_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.output_dir_path.set(paths.SCRIPT_DIR)
        self.output_file_name = tk.StringVar()
        self.output_file_name.set("seenopsis_output.html")
        self.output_file_path = self.output_dir_path.get() + "\\" + self.output_file_name.get()
        self.split_binary = ["split_binary"]
        self.split_binary[0] = tk.BooleanVar() # that is a list because of a bug in tkinter.
        self.split_by_column = tk.StringVar()
        self.export_to_pdf = tk.BooleanVar()
        self.export_to_pdf.set(True)
     
    def new_window(self):
        try:
            self.current_window.destroy()
        except:
            pass
        self.current_window = tk.Toplevel()
        self.current_window.title("SEENOPSIS")
        
    def unpload_data(self):
        # check valid inputs:
        if not(os.path.isfile(self.input_file_path.get())):
            tk.messagebox.showwarning("Warning", "You did not choose a valid input file.")
        elif os.path.splitext(self.input_file_path.get())[1] != ".csv":
            tk.messagebox.showwarning("Warning", "Please choose a .csv file as an input.")
        elif not(os.path.isdir(self.output_dir_path.get())):
            tk.messagebox.showwarning("Warning", "You did not choose a valid output directory.")
        elif os.path.splitext(self.output_file_name.get())[1] != ".html":
            tk.messagebox.showwarning("Warning", "The output file name has to end with .html.")
        else:
            self.output_file_path = self.output_dir_path.get() + "\\" + self.output_file_name.get()
            self.sd = seenopsis_data.SeenopsisData(self.input_file_path.get(), self.output_file_path, export_to_pdf=self.export_to_pdf.get())
            self.build_options_gui()
    
    def close_window(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
        
    def ask_output_dir(self):
        input_val = filedialog.askdirectory()
        self.output_dir_path.set(input_val.replace("/", "\\"))
        
    def ask_input_file(self):
        input_val = filedialog.askopenfilename()
        self.input_file_path.set(input_val.replace("/", "\\"))
        
    def end(self):
        tk.messagebox.showinfo("Success!", "Your output files are at: {}".format(self.output_dir_path.get()))
        self.root.destroy()
    
    def run(self):
        # check valid inputs:
        if self.split_binary[0].get() and self.split_by_column.get() == "":
            tk.messagebox.showwarning("Warning", "If you chose to split by binary, you have to choose a column.")
        else:
            self.sd.export_to_html()
            if self.split_binary[0].get():
                res = self.sd.split_by_binary(self.split_by_column.get())
            self.end()
        
    def open_column_options(self, binary_columns):
        global temp_lbl
        global temp_menu
        if self.split_binary[0].get():
            temp_lbl = tk.Label(master=self.current_window, text="Choose column name from the following list:")
            temp_lbl.grid(row=4, column=0, sticky=tk.W)
            binary_columns_names = [c.name for c in binary_columns]
            temp_menu = tk.OptionMenu(self.current_window, self.split_by_column, *binary_columns_names)
            temp_menu.grid(row=5, column=0, sticky=tk.W)
        else:
            try:
                temp_lbl.destroy()
                temp_menu.destroy()
            except:
                pass
            
    def build_options_gui(self):
        # build new window
        self.new_window()
        # show all binary columns in sd
        binary_columns = self.sd.get_columns(filter_by_var_type="Binary Variable")
        if len(binary_columns) > 0:
            lbl1 = tk.Label(master=self.current_window, text="We uploaded your data.\nThese are the binary columns we found:", anchor='w', justify=tk.LEFT)
            lbl1.grid(row=1, column=0, sticky=tk.W)
            # create a "table" to show the columns details:
            columns = ('name', 'index', 'type')
            table = ttk.Treeview(master=self.current_window, columns=columns, show="headings")
            for c in columns:
                table.heading(c, text=c)
            for bc in binary_columns:
                table.insert("", "end", values=(bc.name, bc.index, bc.var_type + " " + str(bc.np_type)))
            table.grid(row=2, column=0)
            # split_binary
            split_button = ttk.Checkbutton(self.current_window, text="I whould like to split results based on a binary feature.", variable=self.split_binary[0])
            split_button.grid(row=3, column=0, sticky=tk.W)
            self.split_binary[0].trace('w', lambda *args: self.open_column_options(binary_columns))
        else:
            lbl1 = tk.Label(master=self.current_window, text="We uploaded your data.\nThere are no binary columns.", anchor='w', justify=tk.LEFT)
            lbl1.grid(row=1, column=0, sticky=tk.W)
        # run
        tk.Button(self.current_window, text="Run", command=self.run).grid(row=6, column=0, sticky=tk.S)      
        self.current_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
    def build_main_gui(self):
        # build new window
        self.new_window()
        # input file path
        browse_input_button = ttk.Button(master=self.current_window, text="Choose input file", command=self.ask_input_file)
        browse_input_button.grid(row=1, column=0, sticky=tk.W)
        lbl1 = tk.Label(master=self.current_window, textvariable=self.input_file_path, justify=tk.LEFT)
        lbl1.grid(row=1, column=1, sticky=tk.W)
        # output dir path
        browse_output_button = ttk.Button(master=self.current_window, text="Choose output directory", command=self.ask_output_dir)
        browse_output_button.grid(row=2, column=0, sticky=tk.W)
        lbl2 = tk.Label(master=self.current_window, textvariable=self.output_dir_path, justify=tk.LEFT)
        lbl2.grid(row=2, column=1, sticky=tk.W)
        # output file name
        lbl3 = tk.Label(master=self.current_window, text="Choose output file name (.html):", justify=tk.LEFT)
        lbl3.grid(row=3, column=0, sticky=tk.W)
        file_name_ent = tk.Entry(master=self.current_window, textvariable=self.output_file_name)
        file_name_ent.grid(row=3, column=1, sticky=tk.W)
        # export to pdf
        export_pdf_button = ttk.Checkbutton(self.current_window, text="I whould like to export my results as a PDF file.", variable=self.export_to_pdf)
        export_pdf_button.grid(row=4, column=0, sticky=tk.W)
        # upload data
        tk.Button(self.current_window, text="Upload Data", command=self.unpload_data).grid(row=6, column=0, sticky=tk.W + tk.E)
        self.current_window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()
        
    def callback_error(self, *args):
        tk.messagebox.showerror("Error!", "The process has failed:\n {}".format(traceback.format_exc()))
                
def run_seenposis():
    s = Seenopsis()
    s.build_main_gui()