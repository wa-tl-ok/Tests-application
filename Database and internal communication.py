import smtplib
import os
from email.mime.text import MIMEText
from random import randint
from itertools import groupby
import datetime
import codecs
from datetime import date

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

Qwe=[]; Qwer=[]; sl=[]; ra=[]; n=""; P=0; K=0

B = input("Введите вашу фамилию и имя:   ")
KL = input("Введите ваш класс обучения:   ")

B = B + ":   "
B += KL + "   "

print()

with open("test/b_slit.txt", encoding='utf-8', mode='r') as file:
    A = [row.strip() for row in file]
    
for i in range(len(A)):
    elem = A[i].split(",")
    sl += [elem]

with open("test/c_razd.txt", encoding='utf-8', mode='r') as file:
    A = [row.strip() for row in file]
    
for i in range(len(A)):
    elem = A[i].split(",")
    ra += [elem]

while n != "start":
    n = input("Введите start, чтобы начать: ")

Start_time = Get_time()
Finish_time = Start_time + 1
    
current_date = date.today()
st = str(current_date)

while K < 30 and Finish_time - Start_time < 240:
    q = randint(0, 1)
    if q == 0:
        a = randint(0, len(sl) - 1)
        print(K + 1, ")", " (", sl[a][0], ") ", sl[a][1], " /", sl[a][2], sep="")
        ans = input() + "    "
        
        while ans[-1] == " " and len(ans) > 2:
            ans = ans[:-2]  
            
        if " " + ans == sl[a][1]:
            P += 1
            del sl[a]
        else:
            P += 0
            Qwer += [sl[a]]
            Qwe += [sl[a][1]]
            del sl[a]
            
        print()
        Finish_time = Get_time()
    elif q == 1:
        a = randint(0, len(ra)-1)
        print(K + 1, ")", " (", ra[a][0], ") ", ra[a][1], " /", ra[a][2], sep="")
        ans = input() + "    "
        
        while ans[-1] == " " and len(ans) > 2:
            ans=ans[:-2]
            
        if " " + ans == ra[a][2]:
            P += 1
            del ra[a]
        else:
            P += 0
            Qwer += [ra[a]]
            Qwe += [ra[a][2]]
            del ra[a]
            
        print()
        Finish_time = Get_time() 
    K += 1
        
        
if P < 25:
    print("ВАША ОЦЕНКА 2:   ", P, "/30", sep="")
    B += "ОЦЕНКА: 2" + " --- " + str(P) + "/" + "30"
elif P >= 25 and P < 27:
    print("ВАША ОЦЕНКА 3:   ", P, "/30", sep="")
    B += "ОЦЕНКА: 3" + " --- " + str(P) + "/" + "30"
elif P >= 27 and P < 29:
    print("ВАША ОЦЕНКА 4:   ", P, "/30", sep="")
    B += "ОЦЕНКА: 4" + " --- " + str(P) + "/" + "30"
else:
    print("ВАША ОЦЕНКА 5:   ", P, "/30", sep="")
    B += "ОЦЕНКА: 5" + " --- " + str(P) + "/"+"30"
    
    
print("Ошибки:")
for i in range(len(Qwer)):
    print(Qwer[i][0], " (" + Qwer[i][1], " /" + Qwer[i][2], " )",  "  ---  ",  Qwer[i][0], Qwe[i], sep="")
print()
    
def send_email(message):
    sender = "" # почта отправителя
    password = "" # пароль отправителя
    recipient = "" # почта получателя
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

def go():
    print(send_email(B))
    
go()
