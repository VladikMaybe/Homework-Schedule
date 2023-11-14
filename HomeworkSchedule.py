import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox
from tkinter import ttk
import calendar
import datetime
import pickle

class HomeworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Homework App")
        # self.root.resizable(True, True)
        self.homework_list = self.load_homework()  # 用于存储作业列表
        self.completed_homework = []  # 用于存储已完成的作业

        # 创建左侧 Frame
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 创建菜单栏
        menubar = tk.Menu(root)
        self.root.config(menu=menubar)

        # 创建视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)

        # 添加月视图和列表视图到视图菜单
        view_menu.add_command(label="月视图", command=self.show_month_view)
        view_menu.add_command(label="列表视图", command=self.show_list_view)


        # # 创建月视图按钮
        # self.month_view_button = tk.Button(left_frame, text="月视图", command=self.show_month_view)
        # self.month_view_button.pack(pady=10)

        # # 创建列表视图按钮
        # self.list_view_button = tk.Button(left_frame, text="列表视图", command=self.show_list_view)
        # self.list_view_button.pack(pady=10)

        # 创建右侧 Frame
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # 初始显示月视图
        self.show_month_view()
    
    def has_homework(self, day):
        """检查指定的日期是否有作业"""
        for homework_day, _, _ in self.homework_list:
            if homework_day == day:
                return True
        return False

    def add_homework(self, day):
        """添加作业"""
        homework = tkinter.simpledialog.askstring("添加作业", "请输入作业信息：")
        if homework is not None:
            self.homework_list.append((day, homework, False))  # 添加作业时，完成状态为 False
            self.save_homework()  # 保存作业列表到文件
            self.show_list_view()  # 更新作业列表
            self.show_month_view()  # 更新月视图
    
    def update_month_view(self, day):
        """更新月视图中的按钮颜色"""
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] == day:
                if self.has_homework(day):
                    widget.config(bg="#FF0000")  # 如果有未完成的作业，背景色为红色
                    self.show_month_view()  # 更新月视图
                else:
                    widget.config(bg="#FFFFFF")  # 如果所有作业都已完成，背景色为白色
                    self.show_month_view()
                break

    def complete_homework(self, event):
        """完成作业"""
        treeview = event.widget
        selected_item = treeview.selection()[0]  # 获取被选中的行
        values = treeview.item(selected_item, "values")  # 获取被选中行的值
        day, homework = values[1], values[2]  # 获取日期和作业
        for i, (homework_day, homework_content, completed) in enumerate(self.homework_list):
            if homework_day == day and homework_content == homework:
                if completed:
                    # 如果作业已经完成，询问用户是否要将作业标记为未完成
                    if tkinter.messagebox.askyesno("未完成作业", "你确定这个作业还没有完成吗？"):
                        self.homework_list[i] = (day, homework, False)  # 更新作业的完成状态
                        treeview.set(selected_item, "完成", "否")  # 更新完成状态
                        treeview.item(selected_item, tags="")  # 移除标签
                else:
                    # 如果作业还没有完成，询问用户是否要将作业标记为已完成
                    if tkinter.messagebox.askyesno("完成作业", "你确定已经完成了这个作业吗？"):
                        self.homework_list[i] = (day, homework, True)  # 更新作业的完成状态
                        treeview.set(selected_item, "完成", "是")  # 更新完成状态
                        treeview.item(selected_item, tags="completed")  # 添加标签
                        treeview.tag_configure("completed", foreground="gray")  # 设置标签的颜色
                self.save_homework()  # 保存作业列表到文件
                self.update_month_view(day)  # 更新月视图中的按钮颜色
                break

    def save_homework(self):
        """将作业列表保存到文件"""
        with open("data/homework.pkl", "wb") as f:
            pickle.dump(self.homework_list, f)

    def load_homework(self):
        """从文件中加载作业列表"""
        try:
            with open("data/homework.pkl", "rb") as f:
                homework_list = pickle.load(f)
        except FileNotFoundError:
            homework_list = []
        return homework_list

    def get_month_days(self, year, month):
        """获取指定年月的日期"""
        month_days = calendar.monthcalendar(year, month)
        return month_days

    def show_month_view(self):
        # 删除右侧 Frame 中的所有组件
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 获取当前年月的日期
        now = datetime.datetime.now()
        year = now.year  # 获取当前年份
        month = now.month  # 获取当前月份
        month_days = self.get_month_days(year, month)

        # 创建月视图
        for i in range(7):
            for j in range(7):
                if i == 0:
                    # 第一行显示一周的每一天
                    text = calendar.day_abbr[j]
                    label = tk.Label(self.right_frame, text=text, width=5, height=1)
                    label.grid(row=i, column=j, padx=0, pady=0)
                else:
                    # 剩下的行显示月份的日期
                    if i-1 < len(month_days):
                        day = month_days[i-1][j]
                        text = str(day) if day != 0 else ""
                        if text != "":
                            if self.has_homework(text):
                                bg_color = "#FF0000"  # 如果有未完成的作业，背景色为红色
                            else:
                                bg_color = "#FFFFFF"  # 如果所有作业都已完成，背景色为白色
                            button = tk.Button(self.right_frame, text=text, width=5, height=1,
                                            command=lambda day=text: self.add_homework(day), bg=bg_color)
                            button.grid(row=i, column=j, padx=0, pady=0)
                        else:
                            label = tk.Label(self.right_frame, text=text, width=5, height=1)
                            label.grid(row=i, column=j, padx=0, pady=0)


    def show_list_view(self):
        # 删除右侧 Frame 中的所有组件
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # 创建表格
        treeview = ttk.Treeview(self.right_frame, columns=("完成", "日期", "作业"), show="headings")
        treeview.column("完成", width=50)
        treeview.column("日期", width=100)
        treeview.column("作业", width=200)
        treeview.heading("完成", text="完成")
        treeview.heading("日期", text="日期")
        treeview.heading("作业", text="作业")
        treeview.pack()

        # 显示作业列表
        for day, homework, completed in sorted(self.homework_list, key=lambda x: x[0]):
            completed_text = "是" if completed else "否"
            tags = ("completed",) if completed else ()
            treeview.insert('', 'end', values=(completed_text, day, homework), tags=tags)
        treeview.tag_configure("completed", foreground="gray")  # 设置标签的颜色

        # 绑定双击事件
        treeview.bind("<Double-1>", self.complete_homework)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeworkApp(root)
    root.mainloop()
