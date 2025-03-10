import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("待辦事項列表")

        self.tasks = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_input = tk.Entry(self.frame, width=35)
        self.task_input.pack(side=tk.LEFT, padx=10)

        self.add_task_button = tk.Button(self.frame, text="添加任務", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT)

        self.tasks_listbox = tk.Listbox(self.root, width=50, height=10)
        self.tasks_listbox.pack(pady=10)

        self.delete_task_button = tk.Button(self.root, text="刪除任務", command=self.delete_task)
        self.delete_task_button.pack(pady=10)

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append(task)
            self.update_tasks_listbox()
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "請輸入任務描述")

    def delete_task(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_tasks_listbox()
        except IndexError:
            messagebox.showwarning("警告", "請選擇一個任務刪除")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    todo_app = TodoApp(root)
    root.mainloop()
