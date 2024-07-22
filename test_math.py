from random import randint
import datetime
from datetime import date
import smtplib
import os
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

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

def send_email(message):
    sender = ""  # Введите свой адрес электронной почты
    password = ""  # Введите свой пароль
    recipient = ""  # Введите адрес получателя
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

def send(m):
    print(send_email(m))

class TestApp:
    def __init__(self, master):
        self.master = master
        master.title("Тест")

        self.start_button = tk.Button(master, text="Начать тест", command=self.start_test)
        self.start_button.pack()

        self.question_label = tk.Label(master, text="")
        self.question_label.pack()

        self.answer_entry = tk.Entry(master)
        self.answer_entry.pack()

        self.submit_button = tk.Button(master, text="Отправить ответ", command=self.submit_answer)
        self.submit_button.pack()

        self.results_label = tk.Label(master, text="")
        self.results_label.pack()

        self.score = 0
        self.current_question = 0
        self.start_time = 0
        self.finish_time = 0
        
        self.a = -1;
        self.b = -1;
        self.c = -1;
        self.d = -1;
        self.e = -1;

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)
        
        self.start_time = Get_time()
        self.finish_time = self.start_time + 1
        self.display_question()

    def display_question(self):
        self.a = randint(1, 1000)
        self.b = randint(1, 1000)
        
        if self.a < self.b: self.a, self.b = self.b, self.a
        
        self.c = randint(1, 20); 
        self.d = randint(1, 20); 
        self.e = self.c * self.d        
        
        if self.current_question < 20:
            self.O = randint(1, 12) - 1
            ANS = [self.a + self.b, self.a - self.b, self.c * self.d, self.e // self.c, self.a, self.b, self.a, self.b, self.c, self.d, self.e, self.c]
            SS = [str(self.a) + " + " + str(self.b) + " = " + "X",
                   str(self.a) + " - " + str(self.b) + " = " + "X",
                   str(self.c) + " * " + str(self.d) + " = " + "X",
                   str(self.e) + " : " + str(self.c) + " = " + "X",
                   "X" + " + " + str(self.b) + " = " + str(self.a + self.b),
                   str(self.a) + " + " + "X" + " = " + str(self.a + self.b),
                   "X" + " - " + str(self.b) + " = " + str(self.a - self.b),
                   str(self.a) + " - " + "X" + " = " + str(self.a - self.b),
                   "X" + " * " + str(self.d) + " = " + str(self.e),
                   str(self.c) + " * " + "X" + " = " + str(self.e),
                   "X" + " : " + str(self.c) + " = " + str(self.d),
                   str(self.e) + " : " + "X" + " = " + str(self.d)]
            self.question_label.config(text=str(self.current_question + 1) + ") " + SS[self.O])
        else:
            self.show_results()

    def submit_answer(self):
        answer = self.answer_entry.get().strip()

        if self.current_question < 20:
            ANS = [self.a + self.b, self.a - self.b, self.c * self.d, self.e // self.c, self.a, self.b, self.a, self.b, self.c, self.d, self.e, self.c]
            if answer == str(ANS[self.O]):
                self.score += 1
            self.current_question += 1
            self.finish_time = Get_time()
            if self.current_question < 20 and self.finish_time - self.start_time < 120:
                self.display_question()
            else:
                self.show_results()
        else:
            self.show_results()

    def show_results(self):
        if self.score < 10:
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/20"
        elif self.score >= 10 and self.score < 15:
            result = "ТВОЯ ОЦЕНКА 3: " + str(self.score) + "/20"
        elif self.score >= 15 and self.score < 19:
            result = "ТВОЯ ОЦЕНКА 4: " + str(self.score) + "/20"
        else:
            result = "ТВОЯ ОЦЕНКА 5: " + str(self.score) + "/20"

        self.results_label.config(text=result)

        current_date = date.today()
        s = str(current_date) + " "
        py = open('py.txt', 'a')
        py.write(s + " \n")
        py.write(result + "   " + str(self.score) + "/" + "20" + " \n")
        py.write(" \n")
        py.close()

        m = result + "   " + str(self.score) + "/" + "20" + " \n"
        send(m)
        
        self.submit_button.config(state=tk.DISABLED)

root = tk.Tk()
app = TestApp(root)
root.mainloop()
