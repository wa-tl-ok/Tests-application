from random import randint
import datetime
from datetime import date
import smtplib
import os
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, ttk
import random

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

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Выбор Теста")

        style = ttk.Style()
        style.theme_use('vista') 
        style.configure('TButton', padding=10, font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 14))

        self.choice_frame = tk.Frame(self)
        self.choice_frame.pack(pady=20)

        self.choice_label = ttk.Label(self.choice_frame, text="Выберите тест:", wraplength=350)
        self.choice_label.pack()

        self.math_button = ttk.Button(self.choice_frame, text="Математика", command=lambda: self.start_test("math"), width=15)
        self.math_button.pack(pady=10)

        self.russian_button = ttk.Button(self.choice_frame, text="Русский язык", command=lambda: self.start_test("russian"), width=15)
        self.russian_button.pack(pady=10)

    def start_test(self, subject):
        self.destroy()
        
        if subject == "math":
            
            test_app = Math_app(subject)
            test_app.mainloop()
            
        else:
            
            test_app = Rus_app(subject)
            test_app.mainloop()            

class Math_app(tk.Tk):
    def __init__(self, subject):
        super().__init__()
        self.title("Тест")
        self.subject = subject

        style = ttk.Style()
        style.theme_use('vista')
        style.configure('TButton', padding=10, font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 14))
        style.configure('TEntry', font=('Arial', 12), padding=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)

        self.question_frame = tk.Frame(self.main_frame)
        self.question_frame.pack()

        self.question_label = ttk.Label(self.question_frame, text="", wraplength=350)
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self.question_frame, width=30)
        self.answer_entry.pack(pady=10)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Начать тест", command=self.start_test, width=15)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.submit_button = ttk.Button(self.button_frame, text="Отправить ответ", command=self.submit_answer, width=15)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=20)

        self.results_label = ttk.Label(self.result_frame, text="", wraplength=350)
        self.results_label.pack()

        self.score = 0
        self.current_question = 0
        self.start_time = 0
        self.finish_time = 0
        self.errors = []

        self.result_frame.pack_forget()

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
            self.SS = [str(self.a) + " + " + str(self.b) + " = " + "X",
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
            self.question_label.config(text=str(self.current_question + 1) + ") " + self.SS[self.O])
        else:
            self.show_results()

    def submit_answer(self):
        answer = self.answer_entry.get().strip()

        if self.current_question < 20:
            ANS = [self.a + self.b, self.a - self.b, self.c * self.d, self.e // self.c, self.a, self.b, self.a, self.b, self.c, self.d, self.e, self.c]
            if answer == str(ANS[self.O]):
                self.score += 1
            else:
                self.errors += [self.SS[self.O] + "  ---  " + "X = " + str(ANS[self.O])]
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
        
        error_msg = "Ошибки:\n" + "\n".join(self.errors)
        messagebox.showinfo("Результаты теста", error_msg)        

        current_date = date.today()
        s = str(current_date) + " "
        py = open('py.txt', 'a')
        py.write(s + " \n")
        py.write("MATH: " + result + "   " + str(self.score) + "/" + "20" + " \n")
        py.write(" \n")
        py.close()

        m = "Math" + "   " + str(self.score) + "/" + "20" + " \n"
        
        self.destroy() 
        
class Rus_app(tk.Tk):
    def __init__(self, subject):
        super().__init__()
        self.title("Тест")
        self.subject = subject

        style = ttk.Style()
        style.theme_use('vista')
        style.configure('TButton', padding=10, font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 14))
        style.configure('TEntry', font=('Arial', 12), padding=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)

        self.question_frame = tk.Frame(self.main_frame)
        self.question_frame.pack()

        self.question_label = ttk.Label(self.question_frame, text="", wraplength=350)
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self.question_frame, width=30)
        self.answer_entry.pack(pady=10)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Начать тест", command=self.start_test, width=15)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.submit_button = ttk.Button(self.button_frame, text="Отправить ответ", command=self.submit_answer, width=15)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=20)

        self.results_label = ttk.Label(self.result_frame, text="", wraplength=350)
        self.results_label.pack()

        self.score = 0
        self.current_question = 0
        self.start_time = 0
        self.finish_time = 0

        self.result_frame.pack_forget()

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
        self.start_button.config(state=tk.DISABLED)
        
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
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/30"
        elif self.score >= 25 and self.score < 27:
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/30"
        elif self.score >= 27 and self.score < 29:
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/30"
        else:
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/30"

        self.results_label.config(text=result)

        error_msg = "Ошибки:\n" + "\n".join(self.errors)
        messagebox.showinfo("Результаты теста", error_msg)
        
        current_date = date.today()
        s = str(current_date) + " "        
        py = open('py.txt', 'a')
        py.write(s + " \n")
        py.write("RUS: " + result + "   " + str(self.score) + "/" + "30" + " \n")
        py.write(" \n")
        py.close()        
        
        m = "Rus" + "   " + str(self.score) + "/" + "30" + " \n"

        self.destroy() 

main_app = MainApp()
main_app.mainloop()
