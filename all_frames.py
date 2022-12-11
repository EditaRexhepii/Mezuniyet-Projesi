import tkinter as tk
from tkinter import ttk
from playsound import playsound
from tkinter import messagebox
from threading import Thread
from PIL import Image, ImageTk
import json
import sqlite3
from urllib.request import pathname2url
import sys
import os


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.check_database()
        self.controller=controller
        self.parent=parent
        self.container = tk.Frame(self, height=400, width=600)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=2)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # **********************************************************************************
        welcome = tk.Label(self.container, text='Welcome', font=("Helvetica", 55))
        welcome.grid(row=0, column=0, columnspan=4)

        sign_in_labelframe = tk.LabelFrame(self.container, text='If you already have an account',
                                           font=("Helvetica", 15))
        sign_in_labelframe.grid(row=1, column=0, rowspan=2)

        sign_up_labelframe = tk.LabelFrame(self.container, text='If you do not have an account', font=("Helvetica", 15))
        sign_up_labelframe.grid(row=1, column=1, rowspan=2)

        sign_in = tk.Label(sign_in_labelframe, text='Sign In', font=("Helvetica", 35))
        sign_in.grid(row=0, column=0, columnspan=2, pady=(15, 0))

        name_1 = tk.Label(sign_in_labelframe, text='Name:', font=("Helvetica", 35))
        name_1.grid(row=1, column=0, sticky=tk.E)

        password_1 = tk.Label(sign_in_labelframe, text='Password:', font=("Helvetica", 35))
        password_1.grid(row=2, column=0, sticky=tk.E)

        self.entry_1 = tk.Entry(sign_in_labelframe, width=15, font=("Helvetica", 17))
        self.entry_1.grid(row=1, column=1, sticky=tk.W, padx=10)

        self.entry_2 = tk.Entry(sign_in_labelframe, width=15, font=("Helvetica", 17), show="*")
        self.entry_2.grid(row=2, column=1, sticky=tk.W, padx=10)

        enter_1 = tk.Button(sign_in_labelframe, text='Enter', font=("Helvetica", 35), command=self.log_in)
        # enter_1 = tk.Button(sign_in_labelframe, text='Enter', font=("Helvetica", 35), command=lambda: self.controller.show_frame(beginner_lesson_1))

        enter_1.grid(row=3, column=0, columnspan=2, sticky=tk.N, pady=15)

        sign_up = tk.Label(sign_up_labelframe, text='Sign Up', font=("Helvetica", 35))
        sign_up.grid(row=0, column=0, columnspan=2, pady=(15, 0))

        name_2 = tk.Label(sign_up_labelframe, text='Name:', font=("Helvetica", 35))
        name_2.grid(row=1, column=0, sticky=tk.E)

        password_2 = tk.Label(sign_up_labelframe, text='Password:', font=("Helvetica", 35))
        password_2.grid(row=2, column=0, sticky=tk.E)

        self.entry_3 = tk.Entry(sign_up_labelframe, width=15, font=("Helvetica", 17))
        self.entry_3.grid(row=1, column=1, sticky=tk.W, padx=10)

        self.entry_4 = tk.Entry(sign_up_labelframe, width=15, font=("Helvetica", 17), show="*")
        self.entry_4.grid(row=2, column=1, sticky=tk.W, padx=10)

        enter_2 = tk.Button(sign_up_labelframe, text='Create User', font=("Helvetica", 35), command=self.create_user)
        enter_2.grid(row=3, column=0, columnspan=2, sticky=tk.N, pady=15)

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
                # Call function from "choose_level" class
                # self.controller.frames[self.shared_data['choose_level']].read_level()
                # choose_level.read_level(choose_level)
                # self.controller.read_userData()

            self.close_database(connection_obj)

    def create_user(self):
        if len(self.entry_3.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No username provided.")
            return
        elif len(self.entry_4.get()) == 0:
            tk.messagebox.showwarning(title="Warning", message="No password provided")
            return
        else:
            connection_obj, cursor_obj = self.open_database()
            a = (self.entry_3.get(),)
            cursor_obj.execute('''SELECT name FROM user_data WHERE name=?''', a)
            output = cursor_obj.fetchall()
            if len(output) == 0:
                initial_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                sql_as_text = json.dumps(initial_level)
                records = (self.entry_3.get(), self.entry_4.get(), sql_as_text, sql_as_text, sql_as_text)
                cursor_obj.execute("INSERT INTO user_data VALUES (?,?,?,?,?)", records)
                self.close_database(connection_obj)
                tk.messagebox.showinfo(title="Notification", message="User created succesfully")
                self.entry_3.delete(0, 'end')
                self.entry_4.delete(0, 'end')
            else:
                tk.messagebox.showwarning(title="Warning", message="User already exists.")
                self.entry_3.delete(0, 'end')
                self.entry_4.delete(0, 'end')

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
                             command=self.lvl_start)
        begginer.grid(row=1, column=1)

        self.beginner = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.beginner.grid(row=1, column=2)

        intermediate = tk.Button(self.container, text='Intermediate', font=("Helvetica", 35), bg='white',
                                 command=self.test)
        intermediate.grid(row=2, column=1)

        self.intermediate = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.intermediate.grid(row=2, column=2)

        advanced = tk.Button(self.container, text='Advanced', font=("Helvetica", 35), bg='white', command=self.test)
        advanced.grid(row=3, column=1)

        self.advanced = tk.Label(self.container, font=("Helvetica", 35), bg='white')
        self.advanced.grid(row=3, column=2)

        self.read_level()

    def close_app(self):
        self.quit()

    def log_out_to_main(self):
        self.controller.show_frame(MainPage)

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


    def test(self):
        tk.messagebox.showwarning(title="Warning", message="Levels not available yet")

    def lvl_start(self):
        self.controller.show_frame(beginner_lesson_1)

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

        self.frame_0=tk.Frame(self.container, bg='white')
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 1', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 2', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 3', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 4', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
                                  indicatoron=0, selectcolor='azure2', variable=self.var, value=3, command=self.sound_thread,  width=45, height=3, font=("Helvetica", 15))
        self.button_1.grid(row=0, column=0, pady=15)

        self.button_2 = tk.Radiobutton(frame2,text="ve", bg='white',
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
            playsound('Audio/ve.mp3')
        elif self.var.get() == 2:
            playsound('Audio/veya.mp3')

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 5', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 6', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 7', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 8', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 9', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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
        self.frame_0.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        self.home = Image.open('Images/home.png')
        self.home = self.home.resize((50, 50))
        self.home = ImageTk.PhotoImage(self.home)
        home = tk.Button(self.frame_0, image=self.home, border=0, bg='white', command=self.go_home)
        home.grid(row=0, column=0, padx=15, pady=15, sticky=tk.NW)

        lesson_name = tk.Label(self.frame_0, text='Lesson 10', font=("Helvetica", 25), bg='white')
        lesson_name.grid(row=1, column=0, sticky=tk.N, pady=15)

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