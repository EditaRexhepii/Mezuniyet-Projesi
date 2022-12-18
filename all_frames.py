import tkinter as tk
from playsound import playsound
from tkinter import messagebox
from threading import Thread
from PIL import Image, ImageTk
import json
import sqlite3
from urllib.request import pathname2url
import os

class sign_in(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.check_database()
        self.controller=controller
        self.parent=parent
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        # **********************************************************************************
        welcome = tk.Label(self.container, text='Welcome to Turkish \n for Beginners (A1-Level)', font=("Helvetica", 35), bg='white')
        welcome.grid(row=0, column=1)
        # ************  LOG IN  *****************
        frame1=tk.Frame(self.container, bg='white')
        frame1.grid(row=1, column=1)

        lbl1=tk.Label(frame1, text='Username: ', font=("Helvetica", 15), bg='white')
        lbl1.grid(row=0, column=0, pady=50)

        self.entry_1=tk.Entry(frame1,width=15, font=("Helvetica", 15))
        self.entry_1.grid(row=0, column=1)

        lbl2=tk.Label(frame1, text='Password: ', font=("Helvetica", 15), bg='white')
        lbl2.grid(row=1, column=0)

        self.entry_2 = tk.Entry(frame1, width=15, font=("Helvetica", 15), show="*")
        self.entry_2.grid(row=1, column=1)

        btn1=tk.Button(frame1, text='Log In', font=("Helvetica", 15), bg='lawngreen', width=20, command=self.log_in)
        btn1.grid(row=2, column=0, columnspan=2, pady=25)
        # ************ SIGN UP  *********************
        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        lbl3=tk.Label(frame2, text='Click to open a new account', font=("Helvetica", 15), bg='white')
        lbl3.grid(row=0, column=0)

        btn2 = tk.Button(frame2, text='Create',font=("Helvetica", 15), bg='goldenrod', width=20, command=lambda: self.controller.show_frame(sign_up))
        btn2.grid(row=1, column=0, pady=15, columnspan=2)


        # ********* CREDITS ************************
        frame3 = tk.Frame(self.container, bg='white')
        frame3.grid(row=3, column=1)
        teachers = tk.Label(frame3, text='...We Are Your Teachers...', font=("Helvetica", 35),bg='white')
        teachers.grid(row=0, column=0)
        btn3 = tk.Button(frame3, text='Credits', font=("Helvetica", 15), bg='skyblue', width=20, command=self.credits)
        btn3.grid(row=1, column=0, pady=15, columnspan=2)
        # ******************* Teachers *********************
        self.tch1 = Image.open('Images/adam.png')
        self.tch1 = self.tch1.resize((150, 200))
        self.tch1 = ImageTk.PhotoImage(self.tch1)
        tch1=tk.Label(self.container, image=self.tch1, bg='white')
        tch1.grid(row=0, column=0)

        self.tch2 = Image.open('Images/afro_girl.png')
        self.tch2 = self.tch2.resize((150, 200))
        self.tch2 = ImageTk.PhotoImage(self.tch2)
        tch2 = tk.Label(self.container, image=self.tch2, bg='white')
        tch2.grid(row=1, column=0)

        self.tch3 = Image.open('Images/bear.png')
        self.tch3 = self.tch3.resize((150, 200))
        self.tch3 = ImageTk.PhotoImage(self.tch3)
        tch3 = tk.Label(self.container, image=self.tch3, bg='white')
        tch3.grid(row=2, column=0)

        self.tch4 = Image.open('Images/child.png')
        self.tch4 = self.tch4.resize((150, 200))
        self.tch4 = ImageTk.PhotoImage(self.tch4)
        tch4 = tk.Label(self.container, image=self.tch4, bg='white')
        tch4.grid(row=3, column=0)

        self.tch5 = Image.open('Images/hijabi_girl.png')
        self.tch5 = self.tch5.resize((150, 200))
        self.tch5 = ImageTk.PhotoImage(self.tch5)
        tch5 = tk.Label(self.container, image=self.tch5, bg='white')
        tch5.grid(row=0, column=2)

        self.tch6 = Image.open('Images/indian.png')
        self.tch6 = self.tch6.resize((150, 200))
        self.tch6 = ImageTk.PhotoImage(self.tch6)
        tch6 = tk.Label(self.container, image=self.tch6, bg='white')
        tch6.grid(row=1, column=2)

        self.tch7 = Image.open('Images/lady.png')
        self.tch7 = self.tch7.resize((150, 200))
        self.tch7 = ImageTk.PhotoImage(self.tch7)
        tch7 = tk.Label(self.container, image=self.tch7, bg='white')
        tch7.grid(row=2, column=2)

        self.tch8 = Image.open('Images/young_girl.png')
        self.tch8 = self.tch8.resize((150, 200))
        self.tch8 = ImageTk.PhotoImage(self.tch8)
        tch8 = tk.Label(self.container, image=self.tch8, bg='white')
        tch8.grid(row=3, column=2)

    def credits(self):
        tk.messagebox.showinfo(title="Credits", message="This work was done by Edita Rexhepi. If you need any help or whould like to contact her, free to to do so"
                                                        " via this addres editarexhepi@gmail.com")

    def log_in(self):
        if len(self.entry_1.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No username provided.")
            return
        elif len(self.entry_2.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No password provided")
            return
        else:
            connection_obj, cursor_obj = self.open_database()
            statement = """SELECT * FROM user_data WHERE name = ?"""
            cursor_obj.execute(statement, (self.entry_1.get(),))
            output = cursor_obj.fetchall()
            if len(output) == 0:
                tk.messagebox.showwarning(title="Warning", message="This username does not exist.")
                self.entry_1.delete(0, 'end')
                self.entry_2.delete(0, 'end')
            elif self.entry_2.get() != output[0][1]:
                tk.messagebox.showwarning(title="Warning", message="Wrong Password. Please try again.")
                self.entry_2.delete(0, 'end')
            elif self.entry_2.get() == output[0][1]:
                self.controller.shared_data["username"] = self.entry_1.get()
                self.entry_1.delete(0, 'end')
                self.entry_2.delete(0, 'end')
                self.controller.add_level_page()
                self.controller.show_frame(choose_level)

            self.close_database(connection_obj)

    def open_database(self):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        return connection_obj, cursor_obj

    def close_database(self, connection_obj):
        connection_obj.commit()
        connection_obj.close()

    def check_database(self):
        if os.path.exists('database')==True:
            try:
                dburi = 'file:{}?mode=rw'.format(pathname2url('database/users.db'))
                connection_obj = sqlite3.connect(dburi, uri=True)
                connection_obj.close()
            except sqlite3.OperationalError:
                conn = sqlite3.connect('database/users.db')
                c = conn.cursor()
                c.execute("""CREATE TABLE user_data (
                                                        name TEXT,
                                                        password TEXT,
                                                        beginner TEXT,
                                                        intermediate TEXT,
                                                        advanced TEXT
                                                )""")
        elif os.path.exists('database') == False:
            os.mkdir('database')
            try:
                dburi = 'file:{}?mode=rw'.format(pathname2url('database/users.db'))
                connection_obj = sqlite3.connect(dburi, uri=True)
                connection_obj.close()
            except sqlite3.OperationalError:
                conn = sqlite3.connect('database/users.db')
                c = conn.cursor()
                c.execute("""CREATE TABLE user_data (
                                                        name TEXT,
                                                        password TEXT,
                                                        beginner TEXT,
                                                        intermediate TEXT,
                                                        advanced TEXT
                                                )""")

class sign_up(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.parent=parent
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        # **********************************************************************************
        welcome = tk.Label(self.container, text='Create a New Account', font=("Helvetica", 35), bg='white')
        welcome.grid(row=0, column=1)
        # ************  LOG IN  *****************
        frame1=tk.Frame(self.container, bg='white')
        frame1.grid(row=1, column=1)

        lbl1=tk.Label(frame1, text='Username: ', font=("Helvetica", 15), bg='white')
        lbl1.grid(row=0, column=0, pady=50, sticky=tk.E)

        self.entry_1=tk.Entry(frame1,width=15, font=("Helvetica", 15))
        self.entry_1.grid(row=0, column=1)

        lbl2=tk.Label(frame1, text='Password: ', font=("Helvetica", 15), bg='white')
        lbl2.grid(row=1, column=0, sticky=tk.E)

        self.entry_2 = tk.Entry(frame1, width=15, font=("Helvetica", 15), show="*")
        self.entry_2.grid(row=1, column=1)

        lbl3 = tk.Label(frame1, text='Retype Password: ', font=("Helvetica", 15), bg='white')
        lbl3.grid(row=2, column=0, pady=50, sticky=tk.E)

        self.entry_3 = tk.Entry(frame1, width=15, font=("Helvetica", 15), show="*")
        self.entry_3.grid(row=2, column=1)

        btn1=tk.Button(frame1, text='Create', font=("Helvetica", 15), bg='goldenrod', width=20, command=self.create_user)
        btn1.grid(row=3, column=0, columnspan=2, pady=25)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((150, 150))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.container, image=self.home, bg='white', command=lambda: self.controller.show_frame(sign_in), bd=0)
        home.grid(row=2, column=1)

        # ********* CREDITS ************************
        frame3 = tk.Frame(self.container, bg='white')
        frame3.grid(row=3, column=1)
        teachers = tk.Label(frame3, text='...We Are Your Teachers...', font=("Helvetica", 35),bg='white')
        teachers.grid(row=0, column=0)
        # ******************* Teachers *********************
        self.tch1 = Image.open('Images/adam.png')
        self.tch1 = self.tch1.resize((150, 150))
        self.tch1 = ImageTk.PhotoImage(self.tch1)
        tch1=tk.Label(self.container, image=self.tch1, bg='white')
        tch1.grid(row=0, column=0)

        self.tch2 = Image.open('Images/afro_girl.png')
        self.tch2 = self.tch2.resize((150, 200))
        self.tch2 = ImageTk.PhotoImage(self.tch2)
        tch2 = tk.Label(self.container, image=self.tch2, bg='white')
        tch2.grid(row=1, column=0)

        self.tch3 = Image.open('Images/bear.png')
        self.tch3 = self.tch3.resize((150, 200))
        self.tch3 = ImageTk.PhotoImage(self.tch3)
        tch3 = tk.Label(self.container, image=self.tch3, bg='white')
        tch3.grid(row=2, column=0)

        self.tch4 = Image.open('Images/child.png')
        self.tch4 = self.tch4.resize((150, 200))
        self.tch4 = ImageTk.PhotoImage(self.tch4)
        tch4 = tk.Label(self.container, image=self.tch4, bg='white')
        tch4.grid(row=3, column=0)

        self.tch5 = Image.open('Images/hijabi_girl.png')
        self.tch5 = self.tch5.resize((150, 200))
        self.tch5 = ImageTk.PhotoImage(self.tch5)
        tch5 = tk.Label(self.container, image=self.tch5, bg='white')
        tch5.grid(row=0, column=2)

        self.tch6 = Image.open('Images/indian.png')
        self.tch6 = self.tch6.resize((150, 200))
        self.tch6 = ImageTk.PhotoImage(self.tch6)
        tch6 = tk.Label(self.container, image=self.tch6, bg='white')
        tch6.grid(row=1, column=2)

        self.tch7 = Image.open('Images/lady.png')
        self.tch7 = self.tch7.resize((150, 200))
        self.tch7 = ImageTk.PhotoImage(self.tch7)
        tch7 = tk.Label(self.container, image=self.tch7, bg='white')
        tch7.grid(row=2, column=2)

        self.tch8 = Image.open('Images/young_girl.png')
        self.tch8 = self.tch8.resize((150, 200))
        self.tch8 = ImageTk.PhotoImage(self.tch8)
        tch8 = tk.Label(self.container, image=self.tch8, bg='white')
        tch8.grid(row=3, column=2)

    def create_user(self):
        if len(self.entry_1.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No username provided.")
            return
        elif len(self.entry_2.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No password provided")
            return
        elif len(self.entry_3.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="Password needs to be retyped")
            return
        elif self.entry_2.get() != self.entry_3.get():
            tk.messagebox.showwarning(title="Warning", message="Passwords do not match")
            return
        else:
            connection_obj, cursor_obj = self.open_database()
            a = (self.entry_1.get(),)
            cursor_obj.execute('''SELECT name FROM user_data WHERE name=?''', a)
            output = cursor_obj.fetchall()
            if len(output) == 0:
                initial_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                sql_as_text = json.dumps(initial_level)
                records = (self.entry_1.get(), self.entry_2.get(), sql_as_text, sql_as_text, sql_as_text)
                cursor_obj.execute("INSERT INTO user_data VALUES (?,?,?,?,?)", records)
                self.close_database(connection_obj)
                tk.messagebox.showinfo(title="Notification", message="User created succesfully")
                self.entry_1.delete(0, 'end')
                self.entry_2.delete(0, 'end')
                self.entry_3.delete(0, 'end')
            else:
                tk.messagebox.showwarning(title="Warning", message="User already exists.")
                self.entry_1.delete(0, 'end')
                self.entry_2.delete(0, 'end')
                self.entry_3.delete(0, 'end')

    def open_database(self):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        return connection_obj, cursor_obj

    def close_database(self, connection_obj):
        connection_obj.commit()
        connection_obj.close()

class choose_level(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)

        self.log_out = Image.open('Images/log_out.png')
        self.log_out = self.log_out.resize((50, 50))
        self.log_out1 = ImageTk.PhotoImage(self.log_out)
        self.log_out = tk.Button(self.container, image=self.log_out1, bg='white', bd=0, command=self.log_out_to_main)
        self.log_out.grid(row=0, column=0)


        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close1 = ImageTk.PhotoImage(self.close)
        self.close = tk.Button(self.container, image=self.close1, command=self.close_app, bg='white', bd=0)
        self.close.grid(row=0, column=3)

        self.welcome = tk.Label(self.container, text='Welcome ' + str(
            self.controller.shared_data["username"]).capitalize() + '! \n Choose your level ', bg='white',
                                font=("Helvetica", 35))
        self.welcome.grid(row=0, column=1, columnspan=2)

        begginer = tk.Button(self.container, text='Beginner', font=("Helvetica", 35), bg='white',
                             command=self.lvL_beginner, width=15)
        begginer.grid(row=1, column=1)

        self.beginner = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.beginner.grid(row=1, column=2)

        intermediate = tk.Button(self.container, text='Intermediate', font=("Helvetica", 35), bg='white',
                                 command=self.lvl_intermediate, width=15)
        intermediate.grid(row=2, column=1)

        self.intermediate = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.intermediate.grid(row=2, column=2)

        advanced = tk.Button(self.container, text='Advanced', font=("Helvetica", 35), bg='white', command=self.lvl_advanced, width=15)
        advanced.grid(row=3, column=1)

        self.advanced = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.advanced.grid(row=3, column=2)

        self.read_level()

    def close_app(self):
        self.quit()

    def log_out_to_main(self):
        self.controller.show_frame(sign_in)

    def read_level(self):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT * FROM user_data WHERE name = ?"""
        cursor_obj.execute(statement, (self.controller.shared_data["username"],))
        output = cursor_obj.fetchall()
        beginner = json.loads(output[0][2])
        intermediate = json.loads(output[0][3])
        advanced = json.loads(output[0][4])
        self.beginner.config(text=str(sum(beginner)) + '/10')
        self.intermediate.config(text=str(sum(intermediate)) + '/10')
        self.advanced.config(text=str(sum(advanced)) + '/10')


    def lvl_advanced(self):
        self.controller.show_frame(advanced_lesson_1)

    def lvL_beginner(self):
        self.controller.show_frame(beginner_lesson_1)

    def lvl_intermediate(self):
        self.controller.show_frame(intermediate_lesson_1)
# ******************************************    Beginner Lessons ***************************************************
class beginner_lesson_1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 1', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=4, column=0, padx=15, pady=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip1)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous1)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4, padx=15, pady=15, sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Which one of these is "water"?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/water.png')
        self.image4 = self.image4.resize((150, 150))
        self.image4 = ImageTk.PhotoImage(self.image4)
        self.button_1 = tk.Radiobutton(self.container, image=self.image4, text="test", width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, command=self.sound_thread)
        self.button_1.grid(row=2, column=1)
        #
        self.tx1 = tk.Label(self.container, text='Su', bg='white', font=("Helvetica", 55))
        self.tx1.grid(row=3, column=1)
        #
        self.image5 = Image.open('Images/bread.png')
        self.image5 = self.image5.resize((150, 150))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Radiobutton(self.container, image=self.image5, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, command=self.sound_thread)
        self.button_2.grid(row=2, column=2)

        self.tx2 = tk.Label(self.container, text='Ekmek', bg='white', font=("Helvetica", 55))
        self.tx2.grid(row=3, column=2)
        #
        self.image6 = Image.open('Images/apple.png')
        self.image6 = self.image6.resize((150, 150))
        self.image6 = ImageTk.PhotoImage(self.image6)
        self.button_3 = tk.Radiobutton(self.container, image=self.image6, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, command=self.sound_thread)
        self.button_3.grid(row=2, column=3)

        self.tx3 = tk.Label(self.container, text='Elma', bg='white', font=("Helvetica", 55))
        self.tx3.grid(row=3, column=3)

    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        if self.var.get()==1:
            playsound('Audio\su.mp3')
        elif self.var.get() == 2:
            playsound('Audio\ekmek.mp3')
        elif self.var.get() == 3:
            playsound('Audio\elma.mp3')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def next_question(self):
        self.controller.show_frame(beginner_lesson_2)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 1:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self,val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[0]=val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip1(self):
        self.controller.show_frame(beginner_lesson_2)

    def previous1(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def close_app(self):
        self.quit()

class beginner_lesson_2(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 2', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the bear and write in English what he says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/bear.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Water', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Orange', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Orange ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio\su_bear.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Water \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[1] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_3)


    def previous2(self):
        self.controller.show_frame(beginner_lesson_1)

    def close_app(self):
        self.quit()

class beginner_lesson_3(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 3', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=4, column=0,padx=15, pady=15,sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4, padx=15, pady=15, sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Which one of these is "bread"?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/water.png')
        self.image4 = self.image4.resize((150, 150))
        self.image4 = ImageTk.PhotoImage(self.image4)
        self.button_1 = tk.Radiobutton(self.container, image=self.image4, text="test", width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, command=self.sound_thread)
        self.button_1.grid(row=2, column=1)
        #
        self.tx1 = tk.Label(self.container, text='Su', bg='white', font=("Helvetica", 55))
        self.tx1.grid(row=3, column=1)
        #
        self.image5 = Image.open('Images/bread.png')
        self.image5 = self.image5.resize((150, 150))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Radiobutton(self.container, image=self.image5, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, command=self.sound_thread)
        self.button_2.grid(row=2, column=2)

        self.tx2 = tk.Label(self.container, text='Ekmek', bg='white', font=("Helvetica", 55))
        self.tx2.grid(row=3, column=2)
        #
        self.image6 = Image.open('Images/apple.png')
        self.image6 = self.image6.resize((150, 150))
        self.image6 = ImageTk.PhotoImage(self.image6)
        self.button_3 = tk.Radiobutton(self.container, image=self.image6, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, command=self.sound_thread)
        self.button_3.grid(row=2, column=3)

        self.tx3 = tk.Label(self.container, text='Elma', bg='white', font=("Helvetica", 55))
        self.tx3.grid(row=3, column=3)

    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        if self.var.get()==3:
            playsound('Audio\su.mp3')
        elif self.var.get() == 1:
            playsound('Audio\ekmek.mp3')
        elif self.var.get() == 2:
            playsound('Audio\elma.mp3')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def next_question(self):
        self.controller.show_frame(beginner_lesson_2)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 1:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[2] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_4)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_2)

    def close_app(self):
        self.quit()

class beginner_lesson_4(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 4', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='How do you say "and" in Turkish?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="ekmek", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="ve", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1,  width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='veya', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)



    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def next_question(self):
        self.controller.show_frame(beginner_lesson_2)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 1:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[3] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_5)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_3)

    def close_app(self):
        self.quit()

class beginner_lesson_5(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 5', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the uncle and write in English what he says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/indian.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='We', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='A', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Or', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " A ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Or ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/bir.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' A \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[4] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_6)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_4)

    def close_app(self):
        self.quit()

class beginner_lesson_6(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 6', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='Eat', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='And', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Or', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Speak', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Also', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Eat ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " And ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Or ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Speak ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Also ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/ye_veya_ic.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Eat  Or  Drink \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[5] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_7)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_5)

    def close_app(self):
        self.quit()

class beginner_lesson_7(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 7', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Select the missing word: SU ______!', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Iç", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Ye", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='Izle', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 1:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[6] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_8)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_6)

    def close_app(self):
        self.quit()

class beginner_lesson_8(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 8', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='How do you say "OR"?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Ve", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Elma", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='Veya', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 3:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 3:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[7] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_9)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_7)

    def close_app(self):
        self.quit()

class beginner_lesson_9(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 9', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='Eat', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='An', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Or', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Speak', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Apple', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Eat ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " An ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Or ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Speak ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Apple ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/bir_elma_ye.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Eat  An  Apple \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[8] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(beginner_lesson_10)

    def previous2(self):
        self.controller.show_frame(beginner_lesson_8)

    def close_app(self):
        self.quit()

class beginner_lesson_10(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 10', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Well done you finished the Beginner Level \n How would you rate this level?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Very Easy", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Average", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='To advanced', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)


    def update_db(self,val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT beginner FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[9]=val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET beginner= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()


    def go_home(self):
        self.update_db(1)
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def previous2(self):
        self.update_db(1)
        self.controller.show_frame(beginner_lesson_9)

    def close_app(self):
        self.quit()

# ******************************************    Intermediate Lessons ***************************************************

class intermediate_lesson_1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 1', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Write this in English ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/child.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Water', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Child', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Child ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/cocuk.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Child \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[0] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_2)


    def previous2(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def close_app(self):
        self.quit()

class intermediate_lesson_2(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 2', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='How do you say "child" in Turkish?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="ekmek", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, command=self.sound_thread,  width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="çocuk", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, command=self.sound_thread,  width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='veya', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, command=self.sound_thread,  width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        if self.var.get()==3:
            playsound('Audio/ekmek.mp3')
        elif self.var.get() == 1:
            playsound('Audio/cocuk.mp3')
        elif self.var.get() == 2:
            playsound('Audio/veya.mp3')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)


    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 1:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 1:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[1] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_3)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_1)

    def close_app(self):
        self.quit()

class intermediate_lesson_3(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 3', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Write this in English... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/adam.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Ben', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='İçerim', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Yerim', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Ben ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İçerim ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Yerim ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/ben_yerim.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Ben  Yerim \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[2] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_4)


    def previous2(self):
        self.controller.show_frame(intermediate_lesson_2)

    def close_app(self):
        self.quit()

class intermediate_lesson_4(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 4', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Select the missing word: \n Ben Yerim ve Sen______!', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Yer", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Yersin", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='Yerim', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 2:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 2:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[3] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_5)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_3)

    def close_app(self):
        self.quit()

class intermediate_lesson_5(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 5', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Write this in English...', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='They', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='Woman', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='I', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='You', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Water', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " They ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Woman ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " I ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " You ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/ben_icerim.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' I  Drink \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[4] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_6)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_4)

    def close_app(self):
        self.quit()

class intermediate_lesson_6(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)


        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 6', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=3, column=2, sticky=tk.SE, padx=15, pady=15)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='How do you say "I drink"', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Kız", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="İçerim", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='Su', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 2:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 2:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[5] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_7)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_5)

    def close_app(self):
        self.quit()

class intermediate_lesson_7(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 7', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Write this in English ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/bear.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Water', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='I', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " I ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/ben_su_icerim.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' I  Drink  Water \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[6] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_8)


    def previous2(self):
        self.controller.show_frame(intermediate_lesson_6)

    def close_app(self):
        self.quit()

class intermediate_lesson_8(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 8', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='İçersin', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='Biz', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='O', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Onlar', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Sen', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Yeriz', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İçersin ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Biz ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Onlar ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " O ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Sen ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Yeriz ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/sen_icersin.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Sen  İçersin \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[7] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_9)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_7)

    def close_app(self):
        self.quit()

class intermediate_lesson_9(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 9', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the uncle and write in Turkish what he says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/indian.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Sen', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='İzlersin', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Yersin', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Sen ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İzlersin ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Yersin ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/sen_yersin.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Sen  Yersin \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[8] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(intermediate_lesson_10)

    def previous2(self):
        self.controller.show_frame(intermediate_lesson_8)

    def close_app(self):
        self.quit()

class intermediate_lesson_10(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 10', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Well done you finished the Intermediate Level \n How would you rate this level?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Very Easy", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Average", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='To advanced', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)


    def update_db(self,val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT intermediate FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[9]=val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET intermediate= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()


    def go_home(self):
        self.update_db(1)
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def previous2(self):
        self.update_db(1)
        self.controller.show_frame(intermediate_lesson_9)

    def close_app(self):
        self.quit()

# ******************************************  Advanced Lessons ***************************************************

class advanced_lesson_1(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 1', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=4, column=0, padx=15, pady=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip1)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous1)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4, padx=15, pady=15, sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Which one of these is "Sandwich"?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/bread.png')
        self.image4 = self.image4.resize((150, 150))
        self.image4 = ImageTk.PhotoImage(self.image4)
        self.button_1 = tk.Radiobutton(self.container, image=self.image4, text="test", width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, command=self.sound_thread)
        self.button_1.grid(row=2, column=1)
        #
        self.tx1 = tk.Label(self.container, text='Ekmek', bg='white', font=("Helvetica", 55))
        self.tx1.grid(row=3, column=1)
        #
        self.image5 = Image.open('Images/sandwich.png')
        self.image5 = self.image5.resize((150, 150))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Radiobutton(self.container, image=self.image5, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, command=self.sound_thread)
        self.button_2.grid(row=2, column=2)

        self.tx2 = tk.Label(self.container, text='Sandviç', bg='white', font=("Helvetica", 55))
        self.tx2.grid(row=3, column=2)
        #
        self.image6 = Image.open('Images/milk.png')
        self.image6 = self.image6.resize((150, 150))
        self.image6 = ImageTk.PhotoImage(self.image6)
        self.button_3 = tk.Radiobutton(self.container, image=self.image6, width=175, height=200, bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, command=self.sound_thread)
        self.button_3.grid(row=2, column=3)

        self.tx3 = tk.Label(self.container, text='Süt', bg='white', font=("Helvetica", 55))
        self.tx3.grid(row=3, column=3)

    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        if self.var.get()==1:
            playsound('Audio\ekmek.mp3')
        elif self.var.get() == 2:
            playsound('Audio\sandwich.mp3')
        elif self.var.get() == 3:
            playsound('Audio\sut.mp3')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.var.get() == 2:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        elif self.var.get() != 2:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self,val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[0]=val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip1(self):
        self.controller.show_frame(advanced_lesson_2)
        pass

    def previous1(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def close_app(self):
        self.quit()

class advanced_lesson_2(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 2', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the girl and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/young_girl.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.btn1=tk.Button(self.container, text='Water', bg='white', font=("Helvetica", 15), command=self.water)
        self.btn1.grid(row=3, column=1)
        self.btn2 = tk.Button(self.container, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink)
        self.btn2.grid(row=3, column=2, padx=(50,0))
        self.btn3 = tk.Button(self.container, text='Sandwich', bg='white', font=("Helvetica", 15), command=self.orange)
        self.btn3.grid(row=3, column=3)
        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def water(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def orange(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Sandwich ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio\sandwich.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Sandwich \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[1] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_3)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_1)

    def close_app(self):
        self.quit()

class advanced_lesson_3(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 3', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in Turkish what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='Biz', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='İçerim', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Kadın', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Yeriz', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='İçeriz', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Ve', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Biz ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İçerim ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Yeriz ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Kadın ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İçeriz ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Ve ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/we_eat_and_we_drink.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Biz  Yeriz  Ve  İçeriz \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[2] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_4)
    def previous2(self):
        self.controller.show_frame(advanced_lesson_2)

    def close_app(self):
        self.quit()

class advanced_lesson_4(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 4', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/hijabi_girl.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)
        #

        #
        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='You drink', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='They', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='We drink', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Drink', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Apple', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Home', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " You drink ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " They ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We drink ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Apple ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Home ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/onlar.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' They \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[3] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_5)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_3)

    def close_app(self):
        self.quit()

class advanced_lesson_5(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 5', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in Turkish what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/lady.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)

        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='Onlar', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='İçeriz', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Ben', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Elma', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Yer', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='Sandviç', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Onlar ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " İçeriz ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Elma ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Ben ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Yer ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Sandviç ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/onlar_elma_yer.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' Onlar  Elma  Yer \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[4] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_6)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_4)

    def close_app(self):
        self.quit()

class advanced_lesson_6(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 6', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/afro_girl.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)

        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='We', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='Water', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Girl', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='You Drink', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Drink', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='We Eat', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " You Drink ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Girl ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We Eat ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)


    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)


    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/biz_su_iceriz.mp3')


    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' We  Drink  Water \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[5] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_7)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_5)

    def close_app(self):
        self.quit()

class advanced_lesson_7(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 7', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=15,sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Listen to the lady and write in English what she says... ', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)
        #
        self.image4 = Image.open('Images/young_girl.png')
        self.image4 = self.image4.resize((150, 200))
        self.image4 = ImageTk.PhotoImage(self.image4)
        bear_img=tk.Label(self.container,image=self.image4, bg='white')
        bear_img.grid(row=2, column=1, sticky=tk.E)

        self.image5 = Image.open('Images/audio.png')
        self.image5 = self.image5.resize((50, 50))
        self.image5 = ImageTk.PhotoImage(self.image5)
        self.button_2 = tk.Button(self.container, image=self.image5, width=50, height=50, bg='white',command=self.sound_thread, bd=1)
        self.button_2.grid(row=2, column=2, sticky=tk.W)

        self.txt=tk.Text(self.container, width=25, height=3,font=("Helvetica", 15), bg='white', state=tk.DISABLED)
        self.txt.grid(row=2, column=3, sticky=tk.W)

        self.frame1=tk.Frame(self.container, bg='white')
        self.frame1.grid(row=3, column=1)

        self.btn1=tk.Button(self.frame1, text='We', bg='white', font=("Helvetica", 15), command=self.eat,width=10)
        self.btn1.grid(row=0, column=0, pady=(0,15))

        self.btn2 = tk.Button(self.frame1, text='Water', bg='white', font=("Helvetica", 15), command=self.and_1,width=10)
        self.btn2.grid(row=1, column=0)

        self.frame2 = tk.Frame(self.container, bg='white')
        self.frame2.grid(row=3, column=2)

        self.btn3 = tk.Button(self.frame2, text='Girl', bg='white', font=("Helvetica", 15), command=self.or_1,width=10)
        self.btn3.grid(row=0, column=0, pady=(0,15))

        self.btn4 = tk.Button(self.frame2, text='Milk', bg='white', font=("Helvetica", 15), command=self.drink,width=10)
        self.btn4.grid(row=1, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=3, column=3)

        self.btn5 = tk.Button(self.frame3, text='Drink', bg='white', font=("Helvetica", 15), command=self.speak,width=10)
        self.btn5.grid(row=0, column=0, pady=(0,15))

        self.btn6 = tk.Button(self.frame3, text='We Eat', bg='white', font=("Helvetica", 15), command=self.also,width=10)
        self.btn6.grid(row=1, column=0)

        self.clear = tk.Button(self.container, text='Clear', bg='lavender', font=("Helvetica", 15), command=self.clear, width=15)
        self.clear.grid(row=4, column=2)

    def eat(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We ")
        self.btn1.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def and_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Water ")
        self.btn2.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def drink(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Milk ")
        self.btn4.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def or_1(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Girl ")
        self.btn3.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def speak(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " Drink ")
        self.btn5.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def also(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, " We Eat ")
        self.btn6.config(state=tk.DISABLED)
        self.txt.config(state=tk.DISABLED)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.btn1.config(state=tk.NORMAL)
        self.btn2.config(state=tk.NORMAL)
        self.btn3.config(state=tk.NORMAL)
        self.btn4.config(state=tk.NORMAL)
        self.btn5.config(state=tk.NORMAL)
        self.btn6.config(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.config(state=tk.DISABLED)

    def sound_thread(self):
        thr2=Thread(target=self.play_sound)
        thr2.start()

    def play_sound(self):
        playsound('Audio/biz_sut_iceriz.mp3')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def response(self):
        thr1=Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.txt.get("1.0",tk.END)==' We  Drink  Milk \n':
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[6] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_8)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_6)

    def close_app(self):
        self.quit()

class advanced_lesson_8(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.check1 = 0
        self.check2 = 0
        self.count_click = 0
        self.total_correct = 0

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15,0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 8', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15,0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=(15,0),sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Match the Turkish words with the English ones', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)

        self.frame2=tk.Frame(self.container, bg='white')
        self.frame2.grid(row=2, column=1, rowspan=3)

        self.word_1_e=tk.Button(self.frame2, text='Apple', font=("Helvetica", 25), bg='white', command=lambda: self.change_check1(1), width=15)
        self.word_1_e.grid(row=0, column=0, pady=(0,15))

        self.word_2_e = tk.Button(self.frame2, text='Girl', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(2), width=15)
        self.word_2_e.grid(row=1, column=0, pady=(0,15))

        self.word_3_e = tk.Button(self.frame2, text='Bread', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(3), width=15)
        self.word_3_e.grid(row=2, column=0, pady=(0,15))

        self.word_4_e = tk.Button(self.frame2, text='I Drink', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(4), width=15)
        self.word_4_e.grid(row=3, column=0, pady=(0,15))

        self.word_5_e = tk.Button(self.frame2, text='Milk', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(5), width=15)
        self.word_5_e.grid(row=4, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=2, column=3, rowspan=3)

        self.word_1_t = tk.Button(self.frame3, text='İçerim', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(4), width=15)
        self.word_1_t.grid(row=0, column=0, pady=(0,15))

        self.word_2_t = tk.Button(self.frame3, text='Kız', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(2), width=15)
        self.word_2_t.grid(row=1, column=0, pady=(0,15))

        self.word_3_t = tk.Button(self.frame3, text='Süt', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(5), width=15)
        self.word_3_t.grid(row=2, column=0, pady=(0,15))

        self.word_4_t = tk.Button(self.frame3, text='Ekmek', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(3), width=15)
        self.word_4_t.grid(row=3, column=0, pady=(0,15))

        self.word_5_t = tk.Button(self.frame3, text='Elma', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(1), width=15)
        self.word_5_t.grid(row=4, column=0)

    def change_check1(self, variable):
        self.check1=variable
        self.check_values_thr1()

    def change_check2(self, variable):
        self.check2=variable
        self.check_values_thr2()

    def check_values_thr1(self):
        thr3=Thread(target=self.check_values_th())
        thr3.start()

    def check_values_thr2(self):
        thr3=Thread(target=self.check_values_th())
        thr3.start()

    def check_values_th(self):
        self.count_click +=1
        if self.count_click==2:
            if self.check1 == 1 and self.check2 == 1:
                self.word_1_e.config(state=tk.DISABLED, bg='chartreuse', disabledforeground='white')
                self.word_5_t.config(state=tk.DISABLED, bg='chartreuse', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct+=1
            elif self.check1 == 2 and self.check2 == 2:
                self.word_2_e.config(state=tk.DISABLED, bg='gold', disabledforeground='white')
                self.word_2_t.config(state=tk.DISABLED, bg='gold', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 3 and self.check2 == 3:
                self.word_3_e.config(state=tk.DISABLED, bg='magenta', disabledforeground='white')
                self.word_4_t.config(state=tk.DISABLED, bg='magenta', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 4 and self.check2 == 4:
                self.word_4_e.config(state=tk.DISABLED, bg='orange', disabledforeground='white')
                self.word_1_t.config(state=tk.DISABLED, bg='orange', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 5 and self.check2 == 5:
                self.word_5_e.config(state=tk.DISABLED, bg='lightgrey', disabledforeground='white')
                self.word_3_t.config(state=tk.DISABLED, bg='lightgrey', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 != self.check2:
                self.check1 = 0
                self.check2 = 0
                self.count_click = 0
        else:
            pass

    def response(self):
        thr1 = Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.total_correct == 5:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[7] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_9)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_7)

    def close_app(self):
        self.quit()

class advanced_lesson_9(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_rowconfigure(4, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.grid_columnconfigure(3, weight=1)
        self.container.grid_columnconfigure(4, weight=1)

        self.check1 = 0
        self.check2 = 0
        self.count_click = 0
        self.total_correct = 0

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15,0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 9', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15,0))

        frame1=tk.Frame(self.container)
        frame1.grid(row=4, column=0, pady=15, padx=15, sticky=tk.SW)
        self.skip = Image.open('Images/skip.png')
        self.skip = self.skip.resize((100, 100))
        self.skip = ImageTk.PhotoImage(self.skip)
        skip = tk.Button(frame1, image=self.skip, border=0, bg='white', command=self.skip2)
        skip.grid(row=0, column=1)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.check = Image.open('Images/check.png')
        self.check = self.check.resize((100, 100))
        self.check = ImageTk.PhotoImage(self.check)
        self.check_bt = tk.Button(self.container, image=self.check, border=0, bg='white', command=self.response)
        self.check_bt.grid(row=4, column=4, padx=15, pady=15, sticky=tk.SE)
        #
        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=4,padx=15, pady=(15,0),sticky=tk.NE)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Match the Turkish words with the English ones', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1, columnspan=3)

        self.frame2=tk.Frame(self.container, bg='white')
        self.frame2.grid(row=2, column=1, rowspan=3)

        self.word_1_e=tk.Button(self.frame2, text='A', font=("Helvetica", 25), bg='white', command=lambda: self.change_check1(1), width=15)
        self.word_1_e.grid(row=0, column=0, pady=(0,15))

        self.word_2_e = tk.Button(self.frame2, text='They', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(2), width=15)
        self.word_2_e.grid(row=1, column=0, pady=(0,15))

        self.word_3_e = tk.Button(self.frame2, text='Or', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(3), width=15)
        self.word_3_e.grid(row=2, column=0, pady=(0,15))

        self.word_4_e = tk.Button(self.frame2, text='Sandwich', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(4), width=15)
        self.word_4_e.grid(row=3, column=0, pady=(0,15))

        self.word_5_e = tk.Button(self.frame2, text='You Eat', font=("Helvetica", 25), bg='white',command=lambda: self.change_check1(5), width=15)
        self.word_5_e.grid(row=4, column=0)

        self.frame3 = tk.Frame(self.container, bg='white')
        self.frame3.grid(row=2, column=3, rowspan=3)

        self.word_1_t = tk.Button(self.frame3, text='Bir', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(1), width=15)
        self.word_1_t.grid(row=0, column=0, pady=(0,15))

        self.word_2_t = tk.Button(self.frame3, text='Onlar', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(2), width=15)
        self.word_2_t.grid(row=1, column=0, pady=(0,15))

        self.word_3_t = tk.Button(self.frame3, text='Sandvix', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(4), width=15)
        self.word_3_t.grid(row=2, column=0, pady=(0,15))

        self.word_4_t = tk.Button(self.frame3, text='Veya', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(3), width=15)
        self.word_4_t.grid(row=3, column=0, pady=(0,15))

        self.word_5_t = tk.Button(self.frame3, text='Yersin', font=("Helvetica", 25), bg='white', command=lambda: self.change_check2(5), width=15)
        self.word_5_t.grid(row=4, column=0)

    def change_check1(self, variable):
        self.check1=variable
        self.check_values_thr1()

    def change_check2(self, variable):
        self.check2=variable
        self.check_values_thr2()

    def check_values_thr1(self):
        thr3=Thread(target=self.check_values_th())
        thr3.start()

    def check_values_thr2(self):
        thr3=Thread(target=self.check_values_th())
        thr3.start()

    def check_values_th(self):
        self.count_click +=1
        if self.count_click==2:
            if self.check1 == 1 and self.check2 == 1:
                self.word_1_e.config(state=tk.DISABLED, bg='chartreuse', disabledforeground='white')
                self.word_1_t.config(state=tk.DISABLED, bg='chartreuse', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct+=1
            elif self.check1 == 2 and self.check2 == 2:
                self.word_2_e.config(state=tk.DISABLED, bg='gold', disabledforeground='white')
                self.word_2_t.config(state=tk.DISABLED, bg='gold', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 3 and self.check2 == 3:
                self.word_3_e.config(state=tk.DISABLED, bg='magenta', disabledforeground='white')
                self.word_4_t.config(state=tk.DISABLED, bg='magenta', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 4 and self.check2 == 4:
                self.word_4_e.config(state=tk.DISABLED, bg='orange', disabledforeground='white')
                self.word_3_t.config(state=tk.DISABLED, bg='orange', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 == 5 and self.check2 == 5:
                self.word_5_e.config(state=tk.DISABLED, bg='lightgrey', disabledforeground='white')
                self.word_5_t.config(state=tk.DISABLED, bg='lightgrey', disabledforeground='white')
                self.check1=0
                self.check2=0
                self.count_click = 0
                self.total_correct += 1
            elif self.check1 != self.check2:
                self.check1 = 0
                self.check2 = 0
                self.count_click = 0
        else:
            pass

    def response(self):
        thr1 = Thread(target=self.response_1)
        thr1.start()

    def response_1(self):
        if self.total_correct == 5:
            self.check_bt.config(bg='green', fg='green')
            self.update_db(1)
            playsound('Audio\correct.wav')
        else:
            self.check_bt.config(bg='red')
            self.update_db(0)
            playsound('Audio\wrong.wav')

    def go_home(self):
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def update_db(self, val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[8] = val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()

    def skip2(self):
        self.controller.show_frame(advanced_lesson_10)

    def previous2(self):
        self.controller.show_frame(advanced_lesson_8)

    def close_app(self):
        self.quit()

class advanced_lesson_10(tk.Frame):
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.container = tk.Frame(self, height=400, width=600, bg='white')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.var = tk.IntVar()

        self.frame_0 = tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=(15, 0), sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 10', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=(15, 0))

        frame1 = tk.Frame(self.container)
        frame1.grid(row=3, column=0, sticky=tk.SW, padx=15, pady=15)

        self.previous = Image.open('Images/return.png')
        self.previous = self.previous.resize((100, 100))
        self.previous = ImageTk.PhotoImage(self.previous)
        previous = tk.Button(frame1, image=self.previous, border=0, bg='white', command=self.previous2)
        previous.grid(row=0, column=0)

        self.close = Image.open('Images/close.png')
        self.close = self.close.resize((50, 50))
        self.close = ImageTk.PhotoImage(self.close)
        check = tk.Button(self.container, image=self.close, border=0, bg='white', command=self.close_app)
        check.grid(row=0, column=2, sticky=tk.NE, padx=15, pady=15)

#         *********************     Question Section ****************************

        self.label = tk.Label(self.container, text='Well done you finished the Advanced Level \n How would you rate this level?', bg='white', font=("Helvetica", 25))
        self.label.grid(row=1, column=1)

        frame2 = tk.Frame(self.container, bg='white')
        frame2.grid(row=2, column=1)

        self.button_1 = tk.Radiobutton(frame2, text="Very Easy", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=1, width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="Average", bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=2, width=45, height=3, font=("Helvetica", 15))
        self.button_2.grid(row=1, column=0, pady=15)

        self.button_3 = tk.Radiobutton(frame2, text='To advanced', bg='white',
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, width=45, height=3, font=("Helvetica", 15))
        self.button_3.grid(row=2, column=0, pady=15)


    def update_db(self,val):
        connection_obj = sqlite3.connect('database/users.db')
        cursor_obj = connection_obj.cursor()
        statement = """SELECT advanced FROM user_data WHERE name = ? """
        cursor_obj.execute(statement, (self.controller.shared_data['username'],))
        output = cursor_obj.fetchall()
        to_dump = json.loads(output[0][0])
        to_dump[9]=val
        sql_as_text = json.dumps(to_dump)
        statement = '''UPDATE user_data SET advanced= ? WHERE name= ?'''
        cursor_obj.execute(statement, (sql_as_text, self.controller.shared_data['username'],))
        connection_obj.commit()
        connection_obj.close()


    def go_home(self):
        self.update_db(1)
        self.controller.add_level_page()
        self.controller.show_frame(choose_level)

    def previous2(self):
        self.update_db(1)
        self.controller.show_frame(advanced_lesson_9)

    def close_app(self):
        self.quit()

