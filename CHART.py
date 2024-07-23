from tkinter import *

global Gl, Gs

def close_window():
    tk.destroy()

def get_button_width(button):
    return button.winfo_reqwidth()

def Make_1():
    tk.attributes('-fullscreen', False)

def Make_2():
    tk.attributes('-fullscreen', True)
    
def Const_create(canvas):
    global Gl, Gs 
    
    size = int(min(screen_width, screen_height) * 6 / 7) // 20 * 20
    l = size // 20
    Gl = l
    Gs = size
    
    b0 = Button(canvas, text="Finish", command=close_window, bg='red')
    b0.place(x=screen_width-get_button_width(b0), y=0)
    
    b1 = Button(canvas, text="Window mode", command=Make_1, bg='red')
    b1.place(x=screen_width - get_button_width(b0) - l - get_button_width(b1), y=0)
    
    b2 = Button(canvas, text="Fullscrean", command=Make_2, bg='red')
    b2.place(x=screen_width - get_button_width(b0) - l - get_button_width(b1) - l - get_button_width(b2), y=0)
    
    canvas.create_line(2*Gl//2-0.5*Gl, Gs+2*Gl, 2*Gs+Gl*2, Gs+2*Gl, fill="#ffb3b3", width=2)
    canvas.create_line(2*Gs+Gl*2, Gs+2*Gl, 2*Gs+Gl+Gl*0.5, Gs+2*Gl+Gl*0.5, fill="#ffb3b3", width=2)
    canvas.create_line(2*Gs+Gl*2, Gs+2*Gl, 2*Gs+Gl+Gl*0.5, Gs+Gl*1.5, fill="#ffb3b3", width=2)
    canvas.create_text(2*Gs+Gl*1.7, Gs+Gl*1.9+Gl, text=str(X), font=('Courier', l), fill="black") 
    canvas.create_line(Gl, Gl, Gl, Gs+Gl*2.5, fill="#ffb3b3", width=2)
    canvas.create_line(Gl, Gl, Gl+0.5*Gl, Gl*1.5, fill="#ffb3b3", width=2)
    canvas.create_line(Gl, Gl, Gl-0.5*Gl, Gl*1.5, fill="#ffb3b3", width=2)
    canvas.create_text(Gl*1.8, Gl*1.2, text=str(Y), font=('Courier', l), fill="black")
    canvas.create_text(Gl*0.5, Gs+Gl*1.5+Gl, text=str(0), font=('Courier', l//3, 'bold'), fill="black") 
    
    for i in range(0, size * 2 + 1, size // 20):
        canvas.create_line(i + l, 0 + l * 2, i + l, size // 20 * 20 + l * 2, fill="#ffb3b3")
        
    for i in range(0, size + 1, size // 20):
        canvas.create_line(0 + l, i + l * 2, size // 20 * 40 + l, i + l * 2, fill="#ffb3b3")
    
    pp=20
    for i in range(2, 23):
        if pp != 0:
            canvas.create_text(Gl*0.5, i*l, text=str(pp), font=('Courier', l//3, 'bold'), fill="black") 
            pp-=1
            
    pp=1
    for i in range(2, 42):
        canvas.create_text(i*l, Gs+2.5*Gl, text=str(pp), font=('Courier', l//3, 'bold'), fill="black") 
        pp+=1    
    
def Online_Create(canvas):
    global Gl, Gs
    
    F = open('test/py.txt', 'r')
    
    L = F.readlines()
    GO = []
    for i in range(len(L)):
        L[i] = L[i].replace("\n", "")
        if (L[i]) != " ":
            GO += [L[i]]
            
    F.close()
        
    P = []
    for i in range(len(GO)-1, -1, -2):
        P += [GO[i]]
        if len(P) == 41:
            break
    P.reverse()
    
    Ch = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    Points = []
    for i in range(len(P)):
        s = str(P[i])
        N = 0
        for j in range(len(s)):
            if s[j] in Ch:
                N *= 10
                N += int(s[j])
            if s[j] == "/":
                N = int(str(N)[1::])
                Points += [N]            
                break
            
    Color = []
    for i in range(len(P)):
        s = str(P[i])
        if s[0] == "M":
            Color += [0]
        else:
            Color += [1]
            
    XY0 = []        
    XY1 = []
    for i in range(len(Points)):
        b = Points[i]
        a = i
        x = Gl + a * Gl
        y = Gs+Gl*1+Gl - b * Gl
        r = Gl//6
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="Black")
        if Color[i] == 0:
            XY0 += [[x, y]]
        else:
            XY1 += [[x, y]]
        
    for i in range(len(XY0) - 1):
        x1 = XY0[i][0]
        y1 = XY0[i][1]
        x2 = XY0[i + 1][0]
        y2 = XY0[i + 1][1]
        canvas.create_line(x1, y1, x2, y2, fill="#66b3ff", width = 2)   
        
    for i in range(len(XY1) - 1):
        x1 = XY1[i][0]
        y1 = XY1[i][1]
        x2 = XY1[i + 1][0]
        y2 = XY1[i + 1][1]
        canvas.create_line(x1, y1, x2, y2, fill="#ff4d4d", width = 2)    

tk = Tk()
tk.title('CHART')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.attributes('-fullscreen', True)

screen_width = tk.winfo_screenwidth() 
screen_height = tk.winfo_screenheight()    

canvas = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0, background='old lace')
canvas.pack()

def update_canvas():
    canvas.delete("all") 
    Const_create(canvas) 
    Online_Create(canvas)
    tk.after(1000, update_canvas)

Const_create(canvas)
    
update_canvas()
        
tk.mainloop()
