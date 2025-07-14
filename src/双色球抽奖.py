# -*- coding: utf-8 -*-
#python3.8
import random
import tkinter as tk
from tkinter import messagebox

class LotteryGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("双色球抽奖程序")
        self.master.geometry("500x400")
        
        self.prizes = {
            "一等奖": "5000万元",
            "二等奖": "10000元",
            "三等奖": "300 元",
            "四等奖": "200元",
            "五等奖": "10 元",
            "六等奖": "5元",
            "未中奖": "0 元"
        }
        
        self.create_start_widgets()

    def create_start_widgets(self):
        # 创建初始界面，供用户选择是否自己选号还是自动生成号码
        self.clear_widgets()
        
        self.label_intro = tk.Label(self.master, text="欢迎参加双色球抽奖！", font=("Helvetica", 16))
        self.label_intro.pack(pady=10)

        self.label_choice = tk.Label(self.master, text="请选择选号方式：", font=("Helvetica", 12))
        self.label_choice.pack(pady=10)

        self.button_manual = tk.Button(self.master, text="手动选号", width=15, command=self.create_widgets)
        self.button_manual.pack(pady=5)

        self.button_auto = tk.Button(self.master, text="自动生成号码", width=15, command=self.ask_number_of_auto_selections)
        self.button_auto.pack(pady=5)

    def ask_number_of_auto_selections(self):
        self.clear_widgets()
        
        self.label_auto = tk.Label(self.master, text="请输入自动生成号码的数量：", font=("Helvetica", 12))
        self.label_auto.pack(pady=10)

        self.entry_number = tk.Entry(self.master)
        self.entry_number.pack(pady=5)

        self.button_generate = tk.Button(self.master, text="生成号码", width=15, command=self.generate_auto_numbers)
        self.button_generate.pack(pady=10)

        self.button_back = tk.Button(self.master, text="返回", width=15, command=self.create_start_widgets)
        self.button_back.pack(pady=5)

    def generate_auto_numbers(self):
        try:
            number_of_auto = int(self.entry_number.get())
            if number_of_auto < 1:
                raise ValueError("数量必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", "请输入有效的数量：{}".format(e))
            return
        
        self.auto_generated_numbers = [self.generate_lottery_numbers() for _ in range(number_of_auto)]
        self.show_auto_generated_numbers()

    def show_auto_generated_numbers(self):
        self.clear_widgets()
        
        self.label_generated = tk.Label(self.master, text="自动生成的号码及其结果：", font=("Helvetica", 12))
        self.label_generated.pack(pady=10)

        # 生成一次中奖号码，所有自动生成号码都会与这次中奖号码比较
        winning_red_balls, winning_blue_ball = self.generate_lottery_numbers()

        for numbers in self.auto_generated_numbers:
            red_balls, blue_ball = numbers
            result = self.check_win(red_balls, blue_ball, winning_red_balls, winning_blue_ball)
            prize = self.prizes[result]
            text = "红色球：{} 蓝色球：{} - 结果：{} - 奖金：{}".format(sorted(red_balls), blue_ball, result, prize)
            label = tk.Label(self.master, text=text, font=("Helvetica", 10))
            label.pack(pady=2)

        # 显示中奖号码
        winning_text = "中奖号码如下：\n红色球：{} 蓝色球：{}".format(sorted(winning_red_balls), winning_blue_ball)
        winning_label = tk.Label(self.master, text=winning_text, font=("Helvetica", 10, "bold"), fg="blue")
        winning_label.pack(pady=10)

        self.button_back = tk.Button(self.master, text="返回", width=15, command=self.create_start_widgets)
        self.button_back.pack(pady=10)

    def create_widgets(self):
        self.clear_widgets()

        self.label_intro = tk.Label(self.master, text="请选择红色球（1-33）和蓝色球（1-16）号码：", font=("Helvetica", 12))
        self.label_intro.pack(pady=10)

        self.frame_red_balls = tk.Frame(self.master)
        self.frame_red_balls.pack(pady=5)

        # 使用Grid布局将红色球按钮分为两行显示
        self.red_balls = []
        self.red_buttons = []
        for i in range(1, 34):
            button = tk.Button(self.frame_red_balls, text=str(i), width=3, height=1, command=lambda num=i: self.select_red_ball(num))
            self.red_buttons.append(button)
            row = (i - 1) // 17  # 0或1
            column = (i - 1) % 17
            button.grid(row=row, column=column, padx=3, pady=3)

        self.frame_blue_ball = tk.Frame(self.master)
        self.frame_blue_ball.pack(pady=10)

        self.blue_balls = []
        self.blue_buttons = []
        for i in range(1, 17):
            button = tk.Button(self.frame_blue_ball, text=str(i), width=3, height=1, command=lambda num=i: self.select_blue_ball(num))
            button.pack(side=tk.LEFT, padx=3)
            self.blue_buttons.append(button)

        self.button_submit = tk.Button(self.master, text="提交选择", width=15, command=self.submit_selection)
        self.button_submit.pack(pady=20)

        self.button_clear = tk.Button(self.master, text="清除选择", width=15, command=self.clear_selection)
        self.button_clear.pack(pady=10)

        self.label_selection = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.label_selection.pack(pady=10)

        self.label_prize = tk.Label(self.master, text="", font=("Helvetica", 14, "bold"))
        self.label_prize.pack()

    def select_red_ball(self, num):
        if len(self.red_balls) < 6:
            if num not in self.red_balls:
                self.red_balls.append(num)
                self.red_buttons[num - 1].config(state=tk.DISABLED, relief=tk.SUNKEN)
        self.update_selection()

    def select_blue_ball(self, num):
        if hasattr(self, 'blue_ball'):
            self.blue_buttons[self.blue_ball - 1].config(state=tk.NORMAL, relief=tk.RAISED)
        self.blue_ball = num
        self.blue_buttons[num - 1].config(state=tk.DISABLED, relief=tk.SUNKEN)
        self.update_selection()

    def update_selection(self):
        self.label_selection.config(
            text="已选红色球：{}，蓝色球：{}".format(
                sorted(self.red_balls), 
                self.blue_ball if hasattr(self, 'blue_ball') else ''
            )
        )

    def submit_selection(self):
        if len(self.red_balls) != 6 or not hasattr(self, 'blue_ball'):
            messagebox.showerror("错误", "请先选择6个红色球和1个蓝色球！")
            return
        
        winning_red_balls, winning_blue_ball = self.generate_lottery_numbers()
        result = self.check_win(self.red_balls, self.blue_ball, winning_red_balls, winning_blue_ball)
        prize = self.prizes[result]

        # 显示中奖号码和结果
        self.display_results(result, prize, winning_red_balls, winning_blue_ball)

    def display_results(self, result, prize, winning_red_balls, winning_blue_ball):
        # 创建一个新的顶层窗口
        top = tk.Toplevel(self.master)
        top.title("抽奖结果")
        top.geometry("350x250")

        # 创建一个结果展示的标签
        result_message = (
            "{}！\n奖金为 {}\n\n"
            "中奖号码如下：\n"
            "红色球：{}\n"
            "蓝色球：{}".format(result, prize, sorted(winning_red_balls), winning_blue_ball)
        )
        label = tk.Label(top, text=result_message, font=("Helvetica", 12, "bold"), fg="red", justify=tk.LEFT)
        label.pack(pady=20)

        # 设置关闭按钮
        button_close = tk.Button(top, text="关闭", command=top.destroy)
        button_close.pack(pady=10)

        # 更新主界面的奖金标签
        self.label_prize.config(text="奖金：{}".format(prize))

    def clear_selection(self):
        self.red_balls = []
        self.blue_ball = None
        for button in self.red_buttons:
            button.config(state=tk.NORMAL, relief=tk.RAISED)
        for button in self.blue_buttons:
            button.config(state=tk.NORMAL, relief=tk.RAISED)
        self.update_selection()
        self.label_prize.config(text="")

    def generate_lottery_numbers(self):
        red_balls = random.sample(range(1, 34), 6)
        blue_ball = random.randint(1, 16)
        return red_balls, blue_ball

    def check_win(self, user_red_balls, user_blue_ball, winning_red_balls, winning_blue_ball):
        red_matches = set(user_red_balls).intersection(set(winning_red_balls))
        blue_match = (user_blue_ball == winning_blue_ball)
        
        if len(red_matches) == 6 and blue_match:
            return "一等奖"
        elif len(red_matches) == 6:
            return "二等奖"
        elif len(red_matches) == 5 and blue_match:
            return "三等奖"
        elif len(red_matches) == 5 or (len(red_matches) == 4 and blue_match):
            return "四等奖"
        elif len(red_matches) == 4 or (len(red_matches) == 3 and blue_match):
            return "五等奖"
        elif blue_match:
            return "六等奖"
        else:
            return "未中奖"

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryGUI(root)
    root.mainloop()

