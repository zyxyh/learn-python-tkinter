# learn-python-tkinter
用tkinter库创建一个学习tkinter的程序

tkinter是python自带的GUI编程库，可实现常用的GUI应用程序，但对初学者来说，widget较多，每个widget的选项又较多，学习难度较大。

本程序用tkinter创建，包含了各种widget，和各自的option和说明，点击可显示说明，并创建了各个widget的样例，采用一个按钮点击可自动改变widget相应的属性。

widget列表存在一个excel文件里，每个widget的option也存在excel的一个sheet里，通过xlrd库调用，此excel文件可扩充更新

每个option后面跟着说明，说明可显示在程序界面上，后面跟着可选的几个设置，当点击按钮的时候，可以把样例widget的属性轮流改变

此程序欢迎更新扩充。
