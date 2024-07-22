import smtplib
import os
from email.mime.text import MIMEText
import random
from random import randint
from itertools import groupby
import datetime
import codecs
from datetime import date
import tkinter as tk
from tkinter import messagebox, Scrollbar, Text
from tkinter import ttk

def Get_time() -> int:
    dt_now = datetime.datetime.now()
    time = str(dt_now)[11:19]
    
    q1 = int(time[0])
    q2 = int(time[1])
    q3 = int(time[3])
    q4 = int(time[4])
    q5 = int(time[6])
    q6 = int(time[7])
    
    n = q1 * 36000 + q2 * 3600 + q3 * 600 + q4 * 60 + q5 * 10 + q6
    
    return n

def load_questions(file_path):
    questions = []
    with open(file_path, encoding='utf-8', mode='r') as file:
        A = [row.strip() for row in file]
        for i in range(len(A)):
            elem = A[i].split(",")
            questions.append(elem)
    return questions

class TestApp:
    def __init__(self, master):
        self.master = master
        master.title("Тест")

        self.name_label = tk.Label(master, text="Введите вашу фамилию и имя:")
        self.name_label.grid(row=0, column=0, sticky="w")

        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, sticky="w")

        self.class_label = tk.Label(master, text="Введите ваш класс обучения:")
        self.class_label.grid(row=1, column=0, sticky="w")

        self.class_entry = tk.Entry(master)
        self.class_entry.grid(row=1, column=1, sticky="w")

        self.start_button = tk.Button(master, text="Начать тест", command=self.start_test)
        self.start_button.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.question_label = tk.Label(master, text="")
        self.question_label.grid(row=3, column=0, columnspan=2, sticky="w")

        self.answer_entry = tk.Entry(master)
        self.answer_entry.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.submit_button = tk.Button(master, text="Отправить ответ", command=self.submit_answer)
        self.submit_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.results_label = tk.Label(master, text="")
        self.results_label.grid(row=6, column=0, columnspan=2, sticky="ew")

        self.sl = load_questions("test/b_slit.txt")
        random.shuffle(self.sl)
        self.ra = load_questions("test/c_razd.txt")
        random.shuffle(self.ra)
        
        self.score = 0
        self.current_question = 0
        self.start_time = 0
        self.finish_time = 0
        
        self.q = -1
        self.errors = []
        self.question = ""

    def start_test(self):
        self.name = self.name_entry.get()
        self.class_ = self.class_entry.get()

        self.start_time = Get_time()
        self.finish_time = self.start_time + 1
        
        self.display_question()

    def display_question(self):
        if self.current_question < 30:
            self.q = randint(0, 1)
            if self.q == 0:
                self.question = self.sl[0]
            else:
                self.question = self.ra[0]
            self.question_label.config(text=f"{self.current_question+1}) ({self.question[0]}) {self.question[1]} / {self.question[2]}")
        else:
            self.show_results()

    def submit_answer(self):
        answer = self.answer_entry.get().strip()
        
        if self.current_question < 30:
            if self.q == 0:
                correct_answer = self.sl[0][1].strip()
                del self.sl[0]
            else:
                correct_answer = self.ra[0][2].strip()
                del self.ra[0]
        else:
            return

        if answer == correct_answer:
            self.score += 1
        else:
            if self.q == 0:
                self.errors.append(f"{self.question[0]} ({self.question[1]} / {self.question[2]})  ---  {self.question[0]} {self.question[1]}")
            else:
                self.errors.append(f"{self.question[0]} ({self.question[1]} / {self.question[2]})  ---  {self.question[0]} {self.question[2]}")            

        self.current_question += 1
        self.finish_time = Get_time()
        if self.current_question < 30 and self.finish_time - self.start_time < 240:
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        if self.score < 25:
            result = "ВАША ОЦЕНКА 2:   " + str(self.score) + "/30"
        elif self.score >= 25 and self.score < 27:
            result = "ВАША ОЦЕНКА 3:   " + str(self.score) + "/30"
        elif self.score >= 27 and self.score < 29:
            result = "ВАША ОЦЕНКА 4:   " + str(self.score) + "/30"
        else:
            result = "ВАША ОЦЕНКА 5:   " + str(self.score) + "/30"

        self.results_label.config(text=result)

        error_msg = "Ошибки:\n" + "\n".join(self.errors)
        messagebox.showinfo("Результаты теста", error_msg)

        message = f"{self.name}:   {self.class_}   ОЦЕНКА: {result.split(':')[1].strip()}"
        print(self.send_email(message))

    def send_email(self, message):
        sender = ""  # почта отправителя
        password = ""  # пароль отправителя
        recipient = ""  # почта получателя
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        try:
            server.login(sender, password)
            msg = MIMEText(message, "plain", "utf-8")
            msg["Subject"] = "Тест"
            msg["From"] = sender
            msg["To"] = recipient
            server.sendmail(sender, recipient, msg.as_string())
            return "The message was sent successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"

root = tk.Tk()
app = TestApp(root)
root.mainloop()
