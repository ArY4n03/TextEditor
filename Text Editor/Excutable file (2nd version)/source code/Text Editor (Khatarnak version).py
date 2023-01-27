#Text Editor
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pickle
import os
import os.path

class Menu():
    def __init__(self,parent):
        self.menu = tk.Menu(parent.master)
        parent.master.config(menu=self.menu)
        self.parent = parent
        self.file = tk.Menu(self.menu,tearoff=0)
        self.file.add_command(label="New",command=parent.new_file)
        self.file.add_command(label="Open File",command=parent.open_file)
        self.file.add_command(label="Save",command=parent.save)
        self.file.add_command(label="Save as",command=parent.save_as)
        self.menu.add_cascade(menu =self.file,label = "File")
        
        self.customize = tk.Menu(self.menu,tearoff=0)
        self.customize.add_command(label="Font",command=parent.customizeFont)
        self.customize.add_command(label="Background and text color",
                                   command=parent.customize_text_and_background_color)
        self.customize.add_command(label="Transparency",command=parent.customize_transparency)
        self.menu.add_cascade(menu=self.customize,label="Customize")

        self.Help = tk.Menu(self.menu,tearoff=0)
        self.Help.add_command(label="About",command=parent.about)
        self.menu.add_cascade(menu=self.Help,label="Help")
        
class TextEditor():
    def __init__(self,master):
        master.title("TEXT EDITOR")
        master.geometry("1200x700")
        self.master = master
        self.menu = Menu(self)
        self.data = {"font":"Arial",
                           "fontsize": 14,
                           "bg color":"white",
                           "text color":"black",
                           "transparency":1.0
                          }
        
        self.filename= None
        self.make_Window1 = True
        self.make_Window2 = True
        self.make_Window3 = True
        self.textarea = tk.Text(master,font=(self.data["font"],self.data["fontsize"]),bg=self.data["bg color"],fg=self.data["text color"])
        master.attributes("-alpha",self.data["transparency"])
        self.scrollBar = tk.Scrollbar(master,command=self.textarea.yview)
        self.textarea.configure(yscrollcommand = self.scrollBar.set)
        self.scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.textarea.pack(side= tk.LEFT,fill=tk.BOTH,expand=True)
        self.load()
        self.change_cursorColor()

    def change_cursorColor(self):
        if self.data["bg color"] == "black":
            self.textarea.configure(insertbackground="white")
        else:
            self.textarea.configure(insertbackground="black")
            
    def load(self):
        if os.path.exists("Data"):
            dataFile = open("Data","rb")
            self.data = pickle.load(dataFile)
            dataFile.close()
            
            self.textarea.config(font=(self.data["font"],self.data["fontsize"]),bg=self.data["bg color"],fg=self.data["text color"])
            master.attributes("-alpha",self.data["transparency"])
        else:
            self.save_data()

    def save_data(self):
        file = "data"
        saveFile = open(file,"wb")
        pickle.dump(self.data,saveFile)
        saveFile.close()
    
    def new_file(self):
        self.textarea.delete(1.0,tk.END)
        self.filename = None
        
    def open_file(self):
        try:
            self.filename = filedialog.askopenfilename(defaultextension="*.txt",
                                                                         filetypes =[("Text files", "*.txt"),
                                                                                         ("Python files","*.py"),
                                                                                         ("CCS Documents","*.css"),
                                                                                         ("HTML","*.html"),
                                                                                         ("JavaScipt","*.js"),
                                                                                         ("C++","*.cpp"),
                                                                                         ("Java","*.java"),
                                                                                         ("All Files","*.*")
                                                                                        ]
                                                                         )
        except:
            self.filename = None
            
        if self.filename != None:
            self.textarea.delete(1.0,tk.END)
            with open(self.filename,"r") as file:
                self.textarea.insert(1.0 ,file.read())
                

    def save(self):
        if self.filename != None:
            text_area_content = self.textarea.get(1.0,tk.END)
            with open(self.filename,"w") as file:
                file.write(text_area_content)

        else:
            self.save_as()
            
    def save_as(self):
        try:
            self.filename = filedialog.asksaveasfilename(initialfile = "untitled.txt",
                                                                        defaultextension="*.txt",
                                                                         filetypes =[("Text files", "*.txt"),
                                                                                         ("Python files","*.py"),
                                                                                         ("CCS Documents","*.css"),
                                                                                         ("HTML","*.html"),
                                                                                         ("JavaScipt","*.js"),
                                                                                         ("C++","*.cpp"),
                                                                                         ("Java","*.java"),
                                                                                         ("All Files","*.*")                                                                                 
                                                                                        ]
                                                                         )
        except:
            self.filename = None

        if self.filename != None:
            text_area_content = self.textarea.get(1.0,tk.END)
            with open(self.filename, "w") as file:
                file.write(text_area_content)
                
    def customize_text_and_background_color(self):
        if self.make_Window1:
            win = tk.Toplevel()
            win.title("customization")
            win.geometry("300x200")
            win.resizable(False,False)
            bg = "skyblue"
            win.configure(bg=bg)
            tk.Label(win,text="Background Color",bg=bg).grid(column=0,row=0,sticky=tk.W)
            tk.Label(win,text="Font Color",bg=bg).grid(column=0,row=1,pady=50,sticky=tk.W)
            
            bgColorCombobox = ttk.Combobox(win)
            bgColorCombobox['values'] = ("black","white","red","green","blue","lightblue",
                                                        "lightgreen","dark blue","dark green","yellow",
                                                        "orange","purple","grey","skyblue","lime","pink","cyan")
            bgColorCombobox.grid(column =1,row= 0)
            bgColorCombobox.current(0)
            
            fontColorCombobox = ttk.Combobox(win)
            fontColorCombobox['values'] = ("black","white","red","green","blue","lightblue",
                                                        "lightgreen","dark blue","dark green","yellow",
                                                        "orange","purple","grey","skyblue","lime","pink","cyan")
            fontColorCombobox.grid(column =1,row= 1)
            fontColorCombobox.current(1)
            
            def Exit():
                self.make_Window1 = True
                win.destroy()
                
            def Ok():
                fontColor = fontColorCombobox.get()
                bgColor = bgColorCombobox.get()
                self.textarea.configure(bg=bgColor,fg=fontColor)
                self.data["bg color"] = bgColor
                self.data["text color"] = fontColor
                self.save_data()
                self.change_cursorColor()
                self.make_Window1 = True
                win.destroy()

            win.protocol("WM_DELETE_WINDOW",Exit)
            OkButton = tk.Button(win,text="OK",command=Ok)
            OkButton.grid(column=1,row=2,sticky=tk.W)
            self.make_Window1 = False

    def customizeFont(self):
        if self.make_Window2:
            win = tk.Toplevel()
            win.geometry("300x200")
            win.resizable(False,False)
            bg = "lime"
            win.configure(bg=bg)
            tk.Label(win,text="Font",bg=bg).grid(column=0,row=0,sticky=tk.W)
            tk.Label(win,text="Font Size",bg=bg).grid(column=0,row=1,pady=50,sticky=tk.W)
            
            FontCombobox = ttk.Combobox(win)
            FontCombobox['values'] = ("Default","Arial")
            FontCombobox.grid(column =1,row= 0)
            FontCombobox.current(0)
            
            FontSizeCombobox = ttk.Combobox(win)
            FontSizeCombobox['values'] = (14,20,30,32,33,45,34,40,50,64)
            FontSizeCombobox.grid(column =1,row= 1)
            FontSizeCombobox.current(0)

            def Exit():
                self.make_Window2 = True
                win.destroy()
                
            def Ok():
                Font = FontCombobox.get()
                fontSize = FontSizeCombobox.get()
                if Font == "Default":
                    self.textarea.configure(font = (None,fontSize))
                    self.data["font"] = None
                else:
                    self.textarea.configure(font = (Font,fontSize))
                    self.data["font"] = Font
                    
                self.data["fontsize"] = fontSize
                self.save_data()
                self.make_Window2 = True
                win.destroy()
                
            win.protocol("WM_DELETE_WINDOW",Exit)
            OkButton = tk.Button(win,text="OK",command=Ok)
            OkButton.grid(column=1,row=2,sticky=tk.W)
            self.make_Window2 = False

    def customize_transparency(self):
        if self.make_Window3:
            win = tk.Toplevel()
            win.title("Customization")
            win.geometry("300x200")
            win.resizable(False,False)
            bg = "pink"
            win.configure(bg=bg)
            def Exit():
                self.make_Window3 = True
                win.destroy()

            def Ok():
                self.save_data()
                self.make_Window3 =True
                win.destroy()

            def slide(e):
                self.data["transparency"] = slider.get()
                self.master.attributes("-alpha",self.data["transparency"])
                               
            tk.Label(win,text="Transparency",bg=bg).grid(columnspan=5,row=0,padx=100)
            slider = ttk.Scale(win,from_=0.1,to=1.0,value=self.data["transparency"],orient=tk.HORIZONTAL,command=slide)
            slider.grid(column=0,row=1,padx=100,pady=30)


            OkButton = tk.Button(win,text="OK",command=Ok).grid(column=0,row=2,padx=100,pady=30)
            win.protocol("WM_DELETE_WINDOW",Exit)
            self.make_Window3 = False

    def about(self):
    	messagebox.showinfo(title="About",message="version 1.1")
    	
if __name__ == "__main__":
    master = tk.Tk()
    text_editor = TextEditor(master)
    master.mainloop()
