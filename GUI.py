import json
import queue
import time
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
import tkinter.font as tkfont
import threading

from appletNewUser import addUser
from appletYouthStudy import *

request_queue = queue.Queue()


# 处理队列中请求的线程函数
def process_request_queue():
    while True:
        data = request_queue.get()
        handle_row_data(data)
        request_queue.task_done()
        time.sleep(1)


threading.Thread(target=process_request_queue, daemon=True).start()


def delete_data(key):
    data = getDataFromFile()
    del data[key]
    with open("users.json", 'w', encoding='utf-8') as writer:
        json.dump(data, writer, indent=4)  # 处理完的json写入


def on_right_click(event):
    # 获取鼠标点击位置对应的行
    row_id = tree.identify_row(event.y)
    if row_id:
        # 如果有行被点击，显示菜单
        tree.selection_set(row_id)  # 选中行
        right_click_menu.post(event.x_root, event.y_root)


def del_data():
    selected_items = tree.selection()
    for selected_item in selected_items:
        delete_data(tree.item(selected_item, 'values')[2])
        tree.delete(selected_item)
    print("选中的数据已删除")


def add_new_user():
    sub_window = tk.Toplevel(root)
    sub_window.title("子窗口")

    # 在子窗口中添加一个输入框
    text_input = tk.Text(sub_window, height=10, width=50)
    text_input.pack(padx=20, pady=20)

    # 定义一个内部函数来处理确定按钮的点击事件
    def on_confirm_button_click():
        user_input = text_input.get("1.0", "end-1c")  # 获取输入框的内容
        addUser(user_input.split("\n"))
        # add_user_queue.put(user_input)
        # process_user_input(user_input)  # 处理用户输入
        readdata(tree)
        sub_window.destroy()  # 关闭子窗口

    # 在子窗口中添加一个确定按钮
    confirm_button = tk.Button(sub_window, text="确定", command=on_confirm_button_click)
    confirm_button.pack(pady=20)


def start_learning():
    print("开始学习")
    for child in tree.get_children():
        # 获取行的数据
        data = tree.item(child)["values"]
        print(data)
        display_in_output_text(str(data))

        request_queue.put(data)

        # request_thread = threading.Thread(target=handle_row_data, args=(data,))
        # request_thread.daemon = True  # 设置守护线程，确保程序能够完全退出
        # request_thread.start()


def readdata(t: Treeview):
    userlist = getDataFromFile()
    for item in t.get_children():
        t.delete(item)
    for item in userlist:
        t.insert("", "end", values=(
            f"{userlist[item]['cardNo']}", f"{userlist[item]['userid']}", f"{item}", f"{userlist[item]['nid']}"))


def on_item_double_click(event):
    # 获取选中的项
    item = tree.selection()[0]
    # 获取该行的数据
    values = tree.item(item, 'values')
    # 调用函数并传递行数据
    # handle_row_data(values)

    request_queue.put(values)

    # request_thread = threading.Thread(target=handle_row_data, args=(values,))
    # request_thread.daemon = True  # 设置守护线程，确保程序能够完全退出
    # request_thread.start()


# 这个函数将处理从行中获取的数据
def handle_row_data(values):
    # print("您选择的行数据是:", values)
    # display_in_output_text("您选择的行数据是:" + str(values))

    openid = values[2]
    name = values[0]
    userid = values[1]
    orgid = values[3]

    session = sessionBuilder(openid)
    print(name, end=" - ")

    try:
        tot = retakesList(session)
        print(f"获取到{len(tot)}条未学习记录")
        display_in_output_text(name + f"获取到{len(tot)}条未学习记录")
    except:
        print("获取学习信息失败, 已跳过")
        display_in_output_text("获取学习信息失败, 已跳过")

    for item in tot:
        time.sleep(1)
        print(name, end=" - ")
        try:
            learningRecords(session, openid=openid, yid=item['i'])
            time.sleep(1)
            addOrUpdateCourse(session, userid=userid, orgid=str(orgid), yid=item['i'], duration=item['d'])
            time.sleep(1)
            print(f"第{item['i']}期学习成功!")
            display_in_output_text(name + f"第{item['i']}期学习成功!")
        except:
            print(f"第{item['i']}期学习出现异常!")
            display_in_output_text(name + f"第{item['i']}期学习出现异常!")

    print(name, "- 学习完成")
    display_in_output_text(name + "- 学习完成")


def autosize_columns(treeview):
    fnt = tkfont.Font()
    for col in treeview['columns']:
        max_length = 0
        for row in treeview.get_children():
            value = treeview.set(row, col)
            max_length = max(max_length, fnt.measure(value))
        treeview.column(col, width=max_length + 10)


def display_in_output_text(values):
    # output_text.delete('1.0', tk.END)  # 清除文本框中的当前内容
    output_text.insert(tk.END, values + "\n")  # 插入新的内容
    output_text.see(tk.END)


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("用户管理界面")

    # 设置窗口大小
    root.geometry("800x400")

    # 创建表格
    columns = ("姓名", "编号", "OpenId", "组织ID")
    tree = Treeview(root, columns=columns, show='headings')

    # 定义表头
    for col in columns:
        tree.heading(col, text=col.title(), anchor='center')
        tree.column(col, anchor='center')

    # 生成示例数据
    readdata(tree)

    # 绑定双击事件到on_item_double_click函数
    tree.bind("<Double-1>", on_item_double_click)

    # 在插入所有数据后调整列宽
    autosize_columns(tree)
    # 添加复选框列
    # tree.column("#0", width=40)
    # tree.heading("#0", text='')

    tree.grid(row=0, column=0, sticky='nsew')

    # 创建输出文本框
    output_text = tk.Text(root, height=4)
    output_text.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

    # 创建滚动条
    scroll = ttk.Scrollbar(root, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=0, column=1, sticky='ns')

    # 创建右侧按钮
    btn_add = tk.Button(root, text="添加新用户", command=add_new_user)
    btn_start = tk.Button(root, text="开始学习", command=start_learning)

    btn_add.grid(row=0, column=2, padx=10, pady=10)
    btn_start.grid(row=1, column=2, padx=10)

    # 配置行列权重
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 创建右键菜单
    right_click_menu = tk.Menu(tree, tearoff=0)
    right_click_menu.add_command(label="删除", command=del_data)

    # 绑定右键点击事件
    tree.bind("<Button-3>", on_right_click)  # 注意: 在不同的操作系统中，右键点击事件可能有不同的表示方法

    # 运行主循环
    root.mainloop()
