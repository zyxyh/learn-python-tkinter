from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
import xlrd 

class Application(Frame):  # 此为面向对象编程的通用写法
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.widget_list = [] # 用于widget列表框
        self.option_list = [] # 用于option列表框
        self.options = {}     # 用于option的字典，用来生成更新self.option_list
        self.sample_widget = {} # 用来存储widget样例的列表
        
        self.sample_labelVar0 = StringVar()
        self.current_option_labelVar0 = StringVar() 
        self.current_option_labelVar1 = StringVar() 
        # 联系标签文字的，标签文字可以自动根据选择的内容改变
        # 标签内容从self.options中来，self.options从excel表格读取
        
        self.widget_listVar = StringVar(value = self.widget_list) # 联系widget列表框
        self.option_listVar = StringVar(value = self.option_list) # 联系option列表框
        # option列表框的内容和self.option_listVar保持同步
        self.wb = xlrd.open_workbook("C:/Users/zyxyh/Documents/py/learntkinter/tkinter-widget.xlsx")
        self.widgetsheet = self.wb.sheet_by_name('widget')
        # widget 和 option 的内容保存在tkinter-widget.xlsx中，使用xlrd模块读取
        
        # 把widget_list的内容从excel文件中读取出来
        for i in range(1,self.widgetsheet.nrows):
            self.widget_list.append(self.widgetsheet.cell(i,0).value)
        self.currentindex = 0
        self.widget_listVar.set(self.widget_list)
        self.create_widgets()

    def create_widgets(self):
        # LabelFrame用来放置widget_listbox列表框
        self.widgetlabelframe = LabelFrame(self,text='Widget')
        self.widgetlabelframe.grid(row=0, column=0)
        
        # widget_listbox列表框放置在widgetlabelframe中
        # 内部数据和StringVar对象链接,必须设置exportselection=False才可以
        self.widget_listbox = Listbox(self.widgetlabelframe, 
                listvariable=self.widget_listVar, 
                exportselection=False,  
                font=('Arial',16,'bold'),selectmode = SINGLE) 
        
        # 滚动条和列表框相联系，下面几行是必须的
        self.scrollbar1 = Scrollbar(self.widgetlabelframe)
        self.scrollbar1.pack(side = RIGHT,fill = Y) 
        #指定Listbox的yscrollbar的回调函数为Scrollbar的set
        self.widget_listbox['yscrollcommand'] = self.scrollbar1.set
        self.scrollbar1.config(command=self.widget_listbox.yview)
        
        self.widget_listbox.pack()
        self.widget_listbox.selection_set(0)  # 初始选择第一个
        # <<ListboxSelect>>是虚拟事件，和self.widget_listbox_click回调函数绑定，
        # 当选择改变时产生此事件，调用self.widget_listbox_click回调函数
        self.widget_listbox.bind('<<ListboxSelect>>', self.widget_listbox_click)
        
        # 另一个LabelFrame用来放置option_listbox列表框
        self.optionlabelframe = LabelFrame(self,text='Option')
        self.optionlabelframe.grid(row=1, column=0)
        self.option_listbox = Listbox(self.optionlabelframe, \
            listvariable=self.option_listVar,exportselection=False,\
                font=('Arial',16,'bold'),selectmode = SINGLE) # 必须设置exportselection=False才可以
        
        self.scrollbar2 = Scrollbar(self.optionlabelframe)
        self.scrollbar2.pack(side = RIGHT,fill = Y) 
        #指定Listbox的yscrollbar的回调函数为Scrollbar的set
        self.option_listbox['yscrollcommand'] = self.scrollbar2.set
        self.option_listbox.pack()
        self.scrollbar2.config(command=self.option_listbox.yview)
        self.option_listbox.selection_set(0) # 初始选择第一个
        # 虚拟事件，和回调函数绑定，列表框需设置exportselection=False，不解
        self.option_listbox.bind('<<ListboxSelect>>', self.option_listbox_click)
        
        self.current_option_label0 = Label(self,font=('Arial',12,'bold'), width=30, justify=LEFT,
                wraplength=300, textvariable = self.current_option_labelVar0,relief='raised')        
        self.option_label_labelframe = LabelFrame(self,labelwidget = self.current_option_label0)
        self.option_label_labelframe.grid(row=0,column=1,sticky=N+E+S+W)
        
        self.current_option_label1 = Label(self.option_label_labelframe,font=('Arial',12,'bold'), width=30, justify=LEFT,
                wraplength=300, textvariable = self.current_option_labelVar1,relief='raised')
        self.current_option_label1.grid(sticky=N+E+S+W)
        
        self.create_menu() # 创建菜单
        
        self.sample_label0 = Label(self,font=('Arial',12,'bold'), width=30, justify=LEFT,
                wraplength=300, textvariable = self.sample_labelVar0,relief='raised')        
        self.sample_labelframe = LabelFrame(self,labelwidget = self.sample_label0)
        self.sample_labelframe.grid(row=1,column=1,sticky=N+E+S+W)
        self.sample_attr_button = Button(self.sample_labelframe,
                                         text='Change Attribute',
                                         command=self.changeattr)
        self.sample_attr_button.grid(row=0)
        
        self.create_sample_widget()  # 创建示例控件
        
        self.current_widget = self.sample_widget['Frame'] # 初始示例设置为第一个'Frame'
        self.current_widget.grid(row=1,rowspan=3)  # self.sample_widget是一个字典，为的是根据widget_listbox选择改变
        self.optionupdate()  # 读出option_listbox的数据
        self.current_option_labelVar1.set(self.options[self.option_listbox.get(0)]) # 先显示第一个数据
        self.current_option_labelVar0.set("Frame: Option: background")
        self.sample_labelVar0.set("Frame Sample")
        
    def create_sample_widget(self):
        self.sample_frame = Frame(self.sample_labelframe,relief=RAISED,bd=2,width=100,height=100,bg='red')
        self.sample_canvas = Canvas(self.sample_labelframe,relief=RAISED,bd=2,width=100,height=100,bg='green')
        self.sample_button = Button(self.sample_labelframe,text='sample_button')
        self.sample_label = Label(self.sample_labelframe,text='sample_label')
        self.sample_checkbutton = Checkbutton(self.sample_labelframe,text='sample_checkbutton')
        self.sample_entry = Entry(self.sample_labelframe,text='sample_entry')
        self.sample_radiobutton = Radiobutton(self.sample_labelframe,text='sample_radiobutton')
        # self.sample_combobox = Combobox(self,text='sample_label')
        self.sample_text = Text(self.sample_labelframe,bd=2,width=10,height=10,bg='green')
        self.sample_scale = Scale(self.sample_labelframe)
        # 把各个样例widget创建出来，但不显示出来，并放到self.sample_widget字典里
        self.sample_widget={'Frame':self.sample_frame, 
            'Button':self.sample_button, 
            'Canvas':self.sample_canvas,
            'Label':self.sample_label, 
            'Checkbutton':self.sample_checkbutton,
            'Radiobutton':self.sample_radiobutton,
            #'Combobox':self.sample_combobox,
            'Text':self.sample_text,
            'Scale':self.sample_scale,
            'Entry':self.sample_entry  }
        
    def create_menu(self):
        self.menubar = Menu(self)
        self.master['menu'] = self.menubar
        
        self.widget_menu = Menu(self.menubar,tearoff = 0)
        self.widget_option_menu = Menu(self.menubar,tearoff = 0)
        self.widget_method_menu = Menu(self.menubar,tearoff = 0)
        
        for k in self.widget_list:
            self.widget_menu.add_command(label = k,command = self.widgetmenu)
    
        self.menubar.add_cascade(label = 'widget',menu = self.widget_menu)
        self.menubar.add_cascade(label = 'widget_option',menu = self.widget_menu)
        self.menubar.add_cascade(label = 'widget_method',menu = self.widget_menu)
    def widgetmenu(self):  # 菜单命令
        pass
    def changeattr(self):
        self.current_widget = self.sample_widget[self.widgetname]
        
        index = self.option_listbox.curselection()[0]
        attrcount = int(self.optionsheet.cell(index+1,2).value)
        
        if attrcount == 0:
            self.currentindex = 0
            return
        optionname = self.option_listbox.get(index)
        attr = self.optionsheet.cell(index+1,3+self.currentindex).value
        print(self.currentindex, attrcount, attr)
        self.current_widget[optionname] =  attr    
        
        if self.currentindex < attrcount-1:
            self.currentindex += 1   
        else:
            self.currentindex = 0
            
    def option_listbox_click(self,event):
        s = self.option_listbox.get(self.option_listbox.curselection())
        self.current_option_labelVar1.set(self.options[s])
        self.current_option_labelVar0.set(self.widgetname+": Option: "+s)
        self.sample_labelVar0.set(self.widgetname+" Sample")
            
    def widget_listbox_click(self,event):
        self.optionupdate()
        
    def optionupdate(self):
        self.widgetname = self.widget_listbox.get(self.widget_listbox.curselection()[0])
        self.optionsheet = self.wb.sheet_by_name(self.widgetname)
        self.optionlabelframe['text'] = self.widgetname + ' Option'
        self.option_list.clear()
        self.options.clear()
        for i in range(1,self.optionsheet.nrows):
            self.options.setdefault(self.optionsheet.cell(i,0).value,\
                self.optionsheet.cell(i,1).value)
        #print(self.options)
        self.option_list=list(self.options.keys())
        #print(self.option_list)
        self.option_listbox.selection_set(0)
        self.option_listVar.set(self.option_list)
        self.current_option_labelVar1.set(self.options[self.option_listbox.get(0)])
        self.current_option_labelVar0.set(self.widgetname+" Option："+self.options[self.option_listbox.get(0)])
        self.sample_labelVar0.set(self.widgetname+" Sample")
        self.currentindex = 0
        if self.widgetname in ('Listbox','Scrollbar','Labelframe'):
            messagebox.showinfo('Sorry',self.widgetname+' widget参看左边')
        elif self.widgetname in ('Sizegrip','Progressbar','Spinbox','Combobox',
                                 'Separator','Panedwindow','Notebook','Treeview'):
            messagebox.showinfo('Sorry',self.widgetname+' 示例 待添加！')
        else:
            self.current_widget.grid_forget()
            self.current_widget = self.sample_widget[self.widgetname]
            self.current_widget.grid(row=1,column=1)

if __name__ == '__main__':
    root = Tk()
    root.geometry('600x600')
    root.title('tKinter速查手册 岳慧练习作品')
    app = Application(master=root)
    app.mainloop()