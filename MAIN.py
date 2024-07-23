from random import randint
import datetime
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime
from datetime import date

global Type_class
Type_class = -1

def set_window_position(window, x, y):
    window.geometry(f"400x550+{x}+{y}")

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
    password = ""   # Введите свой пароль
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
        set_window_position(self, 50, 50)

        style = ttk.Style()
        style.theme_use('vista')
        style.configure('TButton', padding=20, font=('Arial', 15), width=15)
        style.configure('TLabel', font=('Arial', 20))
        
        style.configure('Math.TButton', background='#3498db', foreground='#e74c3c')
        style.map('Math.TButton', background=[('active', '#2980b9')])

        style.configure('Russian.TButton', background='#e74c3c', foreground='#3498db')
        style.map('Russian.TButton', background=[('active', '#c0392b')])
        
        style.configure('Finish.TButton', background='black', foreground='black', borderwidth=2, relief='solid')
        style.map('Finish.TButton', background=[('active', 'black')])        

        self.choice_frame = tk.Frame(self)
        self.choice_frame.pack(pady=20, anchor=tk.CENTER)

        self.choice_label = ttk.Label(self.choice_frame, text="  Test your knowledge  ", wraplength=350)
        self.choice_label.pack(pady=20, anchor=tk.CENTER)
        
        self.choice_label_2 = ttk.Label(self.choice_frame, text="Choose test", wraplength=350)
        self.choice_label_2.pack(pady=20, anchor=tk.CENTER)

        self.math_button = ttk.Button(self.choice_frame, text="Math", style='Math.TButton', command=lambda: self.start_test("math"))
        self.math_button.pack(pady=20, anchor=tk.CENTER)

        self.russian_button = ttk.Button(self.choice_frame, text="Russian language", style='Russian.TButton', command=lambda: self.start_test("russian"))
        self.russian_button.pack(pady=20, anchor=tk.CENTER)

        self.finish_button = ttk.Button(self.choice_frame, text="Finish", command=self.finish_app, style='Finish.TButton')
        self.finish_button.pack(pady=20, anchor=tk.CENTER)

    def start_test(self, subject):
        self.destroy()
        
        if subject == "math":
            test_app = MathApp(subject)
            test_app.mainloop()
        else:
            test_app = RusApp(subject)
            test_app.mainloop()

    def finish_app(self):
        self.destroy()

    def start_test(self, subject):
        self.destroy()
        
        if subject == "math":
            test_app = MathApp(subject)
            test_app.mainloop()
        else:
            test_app = RusApp(subject)
            test_app.mainloop()

class TestApp(tk.Tk):
    def __init__(self, subject, questions=None):
        super().__init__()
        self.title("Тест")
        set_window_position(self, 50, 50)
        self.subject = subject
        self.questions = questions
        self.current_question = 0
        self.score = 0
        self.errors = []
        self.start_time = 0
        self.finish_time = 0

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

        self.start_button = ttk.Button(self.button_frame, text="Начать тест", command=self.start_test, width=20)
        self.start_button.pack(pady=5)

        self.submit_button = ttk.Button(self.button_frame, text="Отправить ответ", command=self.submit_answer, width=20)
        self.submit_button.pack(pady=5)
        self.submit_button.config(state=tk.DISABLED)

        self.finish_button = ttk.Button(self.button_frame, text="Закончить тест", command=self.finish_test, width=20)
        self.finish_button.pack(pady=5)

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=20)

        self.results_label = ttk.Label(self.result_frame, text="", wraplength=350)
        self.results_label.pack()

        self.canvas = tk.Canvas(self.result_frame)
        self.scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        self.sl = load_questions("test/b_slit.txt")
        random.shuffle(self.sl)
        self.ra = load_questions("test/c_razd.txt")
        random.shuffle(self.ra)
        self.q = -1

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)
        self.finish_button.config(state=tk.NORMAL)
        self.start_time = Get_time()
        self.finish_time = self.start_time + 1
        self.display_question()

    def display_question(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def submit_answer(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def finish_test(self):
        self.show_results()

    def show_results(self):
        if self.score < 10:
            result = "ТВОЯ ОЦЕНКА 2: " + str(self.score) + "/20"
        elif self.score >= 10 and self.score < 15:
            result = "ТВОЯ ОЦЕНКА 3: " + str(self.score) + "/20"
        elif self.score >= 15 and self.score < 19:
            result = "ТВОЯ ОЦЕНКА 4: " + str(self.score) + "/20"
        elif self.score >= 19:
            result = "ТВОЯ ОЦЕНКА 5: " + str(self.score) + "/20"

        if self.finish_time - self.start_time >= 120:
            result += "\nВремя закончилось."
        
        result += "\n"
        self.results_label.config(text=result, justify=tk.CENTER)
        self.scrollable_frame.pack_forget() 
        
        error_label = tk.Label(self.scrollable_frame, text="Ваши ошибки:", wraplength=350, justify=tk.CENTER, anchor=tk.CENTER)
        error_label.grid(sticky='ew')       
        
        global Type_class
        
        current_date = date.today()
        s = str(current_date) + " "   
        m = ""
        
        if Type_class == 0:
            error = " " * 130
            error_label = tk.Label(self.scrollable_frame, text=error, wraplength=350, justify=tk.CENTER, anchor=tk.CENTER)
            error_label.grid(sticky='ew')             
            for i in range(len(self.errors)):
                error = self.errors[i]
                error_label = tk.Label(self.scrollable_frame, text=error, wraplength=350, justify=tk.CENTER, anchor=tk.CENTER)
                error_label.grid(sticky='ew') 
            py = open('test/py.txt', 'a')
            py.write(s + " \n")
            py.write("MATH: " + result)
            py.write(" \n")
            py.close()
            
            m = "MATH: " + result
        else:
            error = " " * 130
            error_label = tk.Label(self.scrollable_frame, text=error, wraplength=350, justify=tk.CENTER, anchor=tk.CENTER)
            error_label.grid(sticky='ew')              
            for i in range(0, len(self.errors)):
                error = self.errors[i]
                error_label = tk.Label(self.scrollable_frame, text=error, wraplength=350, justify=tk.CENTER, anchor=tk.CENTER)
                error_label.grid(sticky='ew')
            py = open('test/py.txt', 'a')
            py.write(s + " \n")
            py.write("RUS: " + result)
            py.write(" \n")
            py.close()
            
            m = "RUS: " + result
            
        send(m)

        self.finish_button.config(text="В главное меню", command=self.return_to_main_menu)
        self.submit_button.config(state=tk.DISABLED)

    def return_to_main_menu(self):
        self.destroy()
        main_app = MainApp()
        main_app.mainloop()

class MathApp(TestApp):
    def __init__(self, subject):
        super().__init__(subject)
        set_window_position(self, 50, 50)
            
    def display_question(self):
        global Type_class
        Type_class = 0
        if self.current_question < 20:
            self.a = randint(1, 1000)
            self.b = randint(1, 1000)
            
            if self.a < self.b: self.a, self.b = self.b, self.a
            
            self.c = randint(1, 20)
            self.d = randint(1, 20)
            self.e = self.c * self.d
            
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
                self.errors.append(f"{self.SS[self.O]} --- {ANS[self.O]}")
            self.current_question += 1
            self.finish_time = Get_time()
            if self.current_question < 20 and self.finish_time - self.start_time < 120:
                self.display_question()
            else:
                self.show_results()
        else:
            self.show_results()
            
class RusApp(TestApp):
    def __init__(self, subject):
        super().__init__(subject)
        set_window_position(self, 50, 50)
        
    def display_question(self):
        global Type_class
        Type_class = 1      
        if self.current_question < 20:
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

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
