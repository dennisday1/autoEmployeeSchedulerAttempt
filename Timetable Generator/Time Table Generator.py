import tkinter, os, time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import sqlite3
import hashlib

class Database():
    def __init__(this, name:str = 'assets/databases/.db_1') -> None:    
        this.database = sqlite3.connect(name)

    def create_table(this) -> None:
        this.database.execute('''CREATE TABLE IF NOT EXISTS users
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USERNAME TEXT NOT NULL,
             PASSWORD_HASH TEXT NOT NULL,
             MONDAY TEXT DEFAULT 'Present,07:00 AM,05:00 PM',
             TUESDAY TEXT DEFAULT 'Present,07:00 AM,05:00 PM',
             WEDNESDAY TEXT DEFAULT 'Present,07:00 AM,05:00 PM',
             THURSDAY TEXT DEFAULT 'Present,07:00 AM,05:00 PM',
             FRIDAY TEXT DEFAULT 'Present,07:00 AM,05:00 PM');''')

    def user_existence(this, username:str = None) -> bool:
        result = this.database.execute("SELECT * FROM users WHERE USERNAME=?", (username,)).fetchone()
        return True if result else False

    def register(this, username:str = None, password:str = None) -> None:
        if this.user_existence(username = username):
            return None
        else:
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            try:
                this.database.execute(f"INSERT INTO users (USERNAME, PASSWORD_HASH) VALUES ('{username}', '{password_hash}')")
                this.database.commit()
                this.update_shifts(username = username)
                return True
            except:
                return False
        
    def login(this, username:str = None, password:str = None) -> bool:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return True if this.database.execute("SELECT * FROM users WHERE USERNAME=? AND PASSWORD_HASH=?", (username, password_hash)).fetchone() else False

    def get_users(this) -> list:
        result = this.database.execute("SELECT USERNAME FROM users").fetchall()
        return [row[0] for row in result]
    
    def get_shifts(this, username:str) -> dict:
        try:
            result = this.database.execute("SELECT MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY FROM users WHERE USERNAME=?", (username,)).fetchone()
            shift = {}
            shift['Monday'] = result[0]
            shift['Tuesday'] = result[1]
            shift['Wednesday'] = result[2]
            shift['Thursday'] = result[3]
            shift['Friday'] = result[4]
            return shift
        except:return False
    
    def update_shifts(this, username:str = None, monday:str = None, tuesday:str = None, wednesday:str = None, thursday:str = None, friday:str = None) -> bool:
        if not this.user_existence(username):
            return False
        else:
            query = "UPDATE users SET "
            values = []
            if monday is not None:
                query += "MONDAY=?, "
                values.append(monday)
            if tuesday is not None:
                query += "TUESDAY=?, "
                values.append(tuesday)
            if wednesday is not None:
                query += "WEDNESDAY=?, "
                values.append(wednesday)
            if thursday is not None:
                query += "THURSDAY=?, "
                values.append(thursday)
            if friday is not None:
                query += "FRIDAY=?, "
                values.append(friday)

            query = query[:-2]
            query += " WHERE USERNAME=?"
            values.append(username)
            try:
                this.database.execute(query, tuple(values))
                this.database.commit()
                return True
            except:
                return False


class App():
    def __init__(this) -> None:
        this.window = tkinter.Tk()
        this.pioneer = not os.path.exists('assets/databases/.db_1')
        
        this.window.resizable(False, False)
        this.window.protocol("WM_DELETE_WINDOW", False)

        this.window_height = 391
        this.window_width = 500

        screen_width = this.window.winfo_screenwidth()
        screen_height = this.window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (this.window_width/2))
        y_cordinate = int((screen_height/2) - (this.window_height/2))

        this.window.geometry("{}x{}+{}+{}".format(this.window_width, this.window_height, x_cordinate, y_cordinate))
        this.window.attributes('-topmost', True)
        this.window.overrideredirect(1)
        this.window.configure(bg='white')

        
        this.canvas= Canvas(this.window, width= this.window_width, height= this.window_height,  bd = 0, highlightbackground = 'white', highlightthickness = 0, highlightcolor='white')
        this.canvas.configure(bg='white')
        this.canvas.pack()

        this.title_bar= Canvas(this.canvas, width= this.window_width, height= 30,  bd = 0, highlightbackground = 'white', highlightthickness = 0, highlightcolor='white')
        this.title_bar.configure(bg='#ECEDEE')
        this.icon= ImageTk.PhotoImage(Image.open("assets/icons/icon.png"))
        this.title_bar.create_image(16, 16,image=this.icon)
        this.title_bar.place(x = 0, y = 0)
        this.title_2 = tkinter.Label(this.title_bar, text = "Employee Timetable Generator", font=("Arial Rounded MT Bold", 9), justify = 'center', foreground = 'gray')
        this.title_2.place(x = 154, y = 4)

        this.display= ImageTk.PhotoImage(Image.open("assets/icons/user_l.jpg"))
        this.display_image = this.canvas.create_image(this.window_width/2, this.window_height/2-60, anchor=tkinter.CENTER,image=this.display)

        this.user_img= ImageTk.PhotoImage(Image.open("assets/icons/user_s.png"))
        this.user_image = this.canvas.create_image(158, 210, anchor=tkinter.CENTER,image=this.user_img)
        this.lock_img= ImageTk.PhotoImage(Image.open("assets/icons/lock.png"))
        this.lock_image = this.canvas.create_image(158, 240, anchor=tkinter.CENTER,image=this.lock_img)
        
        this.exit_btn= ImageTk.PhotoImage(Image.open("assets/icons/exit.png"))
        this.exit_button = this.canvas.create_image(486, 378, anchor=tkinter.CENTER,image=this.exit_btn)
        this.canvas.tag_bind(this.exit_button, "<Button-1>", lambda event: this.window.destroy())
        
        this.username_entry = ttk.Entry(this.canvas, width=19, font=("Arial", 11, 'bold'), justify = 'center', foreground = '#113C83')
        this.username_entry.focus_set()
        this.username_entry.place(x=250, y=210, anchor=CENTER)
        
        this.password_entry = ttk.Entry(this.canvas, width=19, show="●", font=("Helvetica", 11, 'bold'), justify = 'center', foreground = '#333F43')
        this.password_entry.place(x=250, y=240, anchor=CENTER)

        this.database = Database('assets/databases/.db_1')
        if this.pioneer == False:
            this.database.user_existence('admin')


        this.register_btn= ImageTk.PhotoImage(Image.open("assets/icons/register.png"))
        if this.pioneer == True:
            this.register_button = this.canvas.create_image(254, 275, anchor=tkinter.CENTER,image=this.register_btn)
        else:
            this.register_button = this.canvas.create_image(297, 275, anchor=tkinter.CENTER,image=this.register_btn)
        this.canvas.tag_bind(this.register_button, "<Button-1>", this.__register_user)

        this.register_lable = ttk.Label(this.canvas, text = 'Register', font=("Helvetica", 10), justify = 'center', foreground = '#636466', background = '#B9BABB', cursor = 'hand2')
        if this.pioneer == True:
            this.register_lable.place(x = 226, y = 265)
        else:
            this.register_lable.place(x = 269, y = 265)
        this.register_lable.bind("<Button-1>", this.__register_user)

        if not this.pioneer:
            this.login_btn= ImageTk.PhotoImage(Image.open("assets/icons/login.png"))
            this.login_button = this.canvas.create_image(205, 275, anchor=tkinter.CENTER,image=this.login_btn)
            this.canvas.tag_bind(this.login_button, "<Button-1>", this.__login_user)

            this.login_lable = ttk.Label(this.canvas, text = 'Login', font=("Helvetica", 10), justify = 'center', foreground = 'white', background = '#419FD9', cursor = 'hand2')
            this.login_lable.place(x = 187, y = 265)
            this.login_lable.bind("<Button-1>", this.__login_user)

        
        if this.pioneer:
            this.database.create_table()
            messagebox.showinfo('New comer!', 'You need to register as admin first.')



    def __login_user(this, event) -> None:
        username = this.username_entry.get().strip()
        password = this.password_entry.get().strip()
        if len(username) != 0 or len(password) != 0:
            if this.database.login(username = username, password = password):
                this.canvas.destroy()
            
                this.canvas= Canvas(this.window, width= this.window_width, height= this.window_height,  bd = 0, highlightbackground = 'white', highlightthickness = 0, highlightcolor='white')
                this.canvas.configure(bg='white')
                this.canvas.pack()

                this.title_bar= Canvas(this.canvas, width= this.window_width, height= 30,  bd = 0, highlightbackground = 'white', highlightthickness = 0, highlightcolor='white')
                this.title_bar.configure(bg='#ECEDEE')
                this.icon= ImageTk.PhotoImage(Image.open("assets/icons/icon.png"))
                this.title_bar.create_image(16, 16,image=this.icon)
                this.title_bar.place(x = 0, y = 0)
                this.title_2 = tkinter.Label(this.title_bar, text = "Employee Timetable Generator", font=("Arial Rounded MT Bold", 9), justify = 'center', foreground = 'gray')
                this.title_2.place(x = 154, y = 4)

                this.exit_btn= ImageTk.PhotoImage(Image.open("assets/icons/exit.png"))
                this.exit_button = this.canvas.create_image(486, 378, anchor=tkinter.CENTER,image=this.exit_btn)
                this.canvas.tag_bind(this.exit_button, "<Button-1>", lambda event: this.window.destroy())

                if username == 'admin':
                    this.users_icon= ImageTk.PhotoImage(Image.open("assets/icons/users.png"))
                    this.canvas.create_image(17, 40, anchor=tkinter.CENTER, image=this.users_icon)
                    
                    list_heading = ttk.Label(this.canvas, text = 'Employees', font=("Arial Rounded MT Bold", 9), justify = 'center', foreground = '#396CD1', background = 'white')
                    list_heading.place(x = 30, y = 30)

                    info_lbl = tkinter.Label(this.canvas, text = 'Select employee from left pane to see details', background = 'white', foreground = '#DADADA', font = ('monopace', 12, 'bold'))
                    info_lbl.place(x = 140, y = 200)

                    scrollbar = tkinter.Scrollbar(this.canvas)
                    listbox = tkinter.Listbox(this.canvas, width = 17, height = 21, font = ("Arial", 9), yscrollcommand=scrollbar.set, border = 1, relief = 'flat', highlightthickness = 1, highlightcolor = 'white', background = '#D8F0FC', selectbackground = "#4BAFE1", activestyle = 'none')
                    users = this.database.get_users()
                    users.remove('admin')
                    for user in users:listbox.insert("end", f"  {user}")
                    listbox.place(x = 0, y = 51)
                    scrollbar.config(command=listbox.yview)
                    def on_select(event):
                        try:
                            selected_user = event.widget.get(event.widget.curselection()).strip()

                            monday_frame = ttk.LabelFrame(this.canvas, text = 'Monday', width = 370, height = 57)
                            monday_frame.place(x = 126, y = 70)
                            tuesday_frame = ttk.LabelFrame(this.canvas, text = 'Tuesday', width = 370, height = 57)
                            tuesday_frame.place(x = 126, y = 130)
                            wednesday_frame = ttk.LabelFrame(this.canvas, text = 'Wednesday', width = 370, height = 57)
                            wednesday_frame.place(x = 126, y = 190)
                            thursday_frame = ttk.LabelFrame(this.canvas, text = 'Thursday', width = 370, height = 57)
                            thursday_frame.place(x = 126, y = 250)
                            friday_frame = ttk.LabelFrame(this.canvas, text = 'Friday', width = 370, height = 57)
                            friday_frame.place(x = 126, y = 310)

                            frames = [monday_frame, tuesday_frame, wednesday_frame, thursday_frame, friday_frame]
                            raw_data = this.database.get_shifts(username = selected_user)
                            
                            attendaces = [value.split(',')[0] for key, value in raw_data.items()]
                            shifts = [f"{value.split(',')[1]} - {value.split(',')[2]}" for key, value in raw_data.items()]
                            
                            for frame, attendance, shift in zip(frames, attendaces, shifts):
                                attendance_lbl = ttk.Label(frame, text = 'Attendance ●', font = ("Arial", 9))
                                attendance_lbl.place(x = 40, y = 3)
                                attendance_vale = ttk.Label(frame, text = attendance, font = ("Arial", 9), foreground = 'red' if attendance.lower() == 'absent' else 'green' if attendance.lower() == 'present' else '#CD7702')
                                attendance_vale.place(x = 115, y = 3)

                                shift_lbl = ttk.Label(frame, text = 'Shift ●', font = ("Arial", 9))
                                shift_lbl.place(x = 195, y = 3)
                                shift_etr = ttk.Label(frame, text = '00:00 AM - 00:00 PM' if attendance.lower() == 'absent' else shift if attendance.lower() == 'present' else '00:00 AM - 00:00 AM', font = ("Arial", 9), foreground = 'blue' if attendance.lower() == 'present' else 'grey')
                                shift_etr.place(x = 233, y = 3)
                        except:pass
                    listbox.bind("<<ListboxSelect>>", on_select)
                else:                
                    x_lblfrm = 25
                    width_lblfrm = 450
                    monday_frame = ttk.LabelFrame(this.canvas, text = 'Monday', width = width_lblfrm, height = 57)
                    monday_frame.place(x = x_lblfrm, y = 35)
                    tuesday_frame = ttk.LabelFrame(this.canvas, text = 'Tuesday', width = width_lblfrm, height = 57)
                    tuesday_frame.place(x = x_lblfrm, y = 95)
                    wednesday_frame = ttk.LabelFrame(this.canvas, text = 'Wednesday', width = width_lblfrm, height = 57)
                    wednesday_frame.place(x = x_lblfrm, y = 155)
                    thursday_frame = ttk.LabelFrame(this.canvas, text = 'Thursday', width = width_lblfrm, height = 57)
                    thursday_frame.place(x = x_lblfrm, y = 215)
                    friday_frame = ttk.LabelFrame(this.canvas, text = 'Friday', width = width_lblfrm, height = 57)
                    friday_frame.place(x = x_lblfrm, y = 275)

                    frames = [monday_frame, tuesday_frame, wednesday_frame, thursday_frame, friday_frame]
                    raw_data = this.database.get_shifts(username = username)
                    
                    attendaces = [value.split(',')[0] for key, value in raw_data.items()]
                    shifts = [f"{value.split(',')[1]} - {value.split(',')[2]}" for key, value in raw_data.items()]
                    shifts = list(map(lambda x: tuple(sub.split()[0] for sub in x.split(' - ')), shifts))

                    for frame in frames:
                        attendance_lbl = ttk.Label(frame, text = 'Attendance ●', font = ("Arial", 9))
                        attendance_lbl.place(x = 67, y = 3)
                        shift_lbl = ttk.Label(frame, text = 'Shift ●', font = ("Arial", 9))
                        shift_lbl.place(x = 260, y = 3)
                        am_lbl = ttk.Label(frame, text = 'AM  to', font = ("Arial", 9))
                        am_lbl.place(x = 337, y = 3)
                        am_lbl = ttk.Label(frame, text = 'PM', font = ("Arial", 9))
                        am_lbl.place(x = 412, y = 3)

                    monday_attendance_options = ["Present   ", "Absent    ", "Sick Leave"]
                    monday_attendance = tkinter.StringVar()
                    monday_dropdown = ttk.OptionMenu(monday_frame, monday_attendance, monday_attendance_options[0], *monday_attendance_options)
                    monday_dropdown.place(x = 140, y = 1)
                    monday_attendance.set(attendaces[0])
                    monday_shift_start = ttk.Entry(monday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    monday_shift_start.place(x = 300, y = 3)
                    monday_shift_start.insert(0, shifts[0][0].lstrip('0'))
                    monday_shift_end = ttk.Entry(monday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    monday_shift_end.insert(0, shifts[0][1].lstrip('0'))
                    monday_shift_end.place(x = 376, y = 3)

                    tuesday_attendance_options = ["Present   ", "Absent    ", "Sick Leave"]
                    tuesday_attendance = tkinter.StringVar()
                    tuesday_dropdown = ttk.OptionMenu(tuesday_frame, tuesday_attendance, tuesday_attendance_options[0], *tuesday_attendance_options)
                    tuesday_dropdown.place(x = 140, y = 2)
                    tuesday_attendance.set(attendaces[1])
                    tuesday_shift_start = ttk.Entry(tuesday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    tuesday_shift_start.place(x = 300, y = 3)
                    tuesday_shift_start.insert(0, shifts[1][0].lstrip('0'))
                    tuesday_shift_end = ttk.Entry(tuesday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    tuesday_shift_end.insert(0, shifts[1][1].lstrip('0'))
                    tuesday_shift_end.place(x = 376, y = 3)

                    wednesday_attendance_options = ["Present   ", "Absent    ", "Sick Leave"]
                    wednesday_attendance = tkinter.StringVar()
                    wednesday_dropdown = ttk.OptionMenu(wednesday_frame, wednesday_attendance, wednesday_attendance_options[0], *wednesday_attendance_options)
                    wednesday_dropdown.place(x = 140, y = 2)
                    wednesday_attendance.set(attendaces[2])
                    wednesday_shift_start = ttk.Entry(wednesday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    wednesday_shift_start.place(x = 300, y = 3)
                    wednesday_shift_start.insert(0, shifts[2][0].lstrip('0'))
                    wednesday_shift_end = ttk.Entry(wednesday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    wednesday_shift_end.insert(0, shifts[2][1].lstrip('0'))
                    wednesday_shift_end.place(x = 376, y = 3)

                    thursday_attendance_options = ["Present   ", "Absent    ", "Sick Leave"]
                    thursday_attendance = tkinter.StringVar()
                    thursday_dropdown = ttk.OptionMenu(thursday_frame, thursday_attendance, thursday_attendance_options[0], *thursday_attendance_options)
                    thursday_dropdown.place(x = 140, y = 2)
                    thursday_attendance.set(attendaces[3])
                    thursday_shift_start = ttk.Entry(thursday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    thursday_shift_start.place(x = 300, y = 3)
                    thursday_shift_start.insert(0, shifts[3][0].lstrip('0'))
                    thursday_shift_end = ttk.Entry(thursday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    thursday_shift_end.insert(0, shifts[3][1].lstrip('0'))
                    thursday_shift_end.place(x = 376, y = 3)

                    friday_attendance_options = ["Present   ", "Absent    ", "Sick Leave"]
                    friday_attendance = tkinter.StringVar()
                    friday_dropdown = ttk.OptionMenu(friday_frame, friday_attendance, friday_attendance_options[0], *friday_attendance_options)
                    friday_dropdown.place(x = 140, y = 2)
                    friday_attendance.set(attendaces[4])
                    friday_shift_start = ttk.Entry(friday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    friday_shift_start.place(x = 300, y = 3)
                    friday_shift_start.insert(0, shifts[4][0].lstrip('0'))
                    friday_shift_end = ttk.Entry(friday_frame, font = ("Arial", 9), foreground = 'blue', width = 4, justify = 'center')
                    friday_shift_end.insert(0, shifts[4][1].lstrip('0'))
                    friday_shift_end.place(x = 376, y = 3)

                    def save_schedule():
                        monday_scehdule = f"{monday_attendance.get().strip()},{monday_shift_start.get()} AM,{monday_shift_end.get()} PM"
                        tuesday_scehdule = f"{tuesday_attendance.get().strip()},{tuesday_shift_start.get()} AM,{tuesday_shift_end.get()} PM"
                        wednesday_scehdule = f"{wednesday_attendance.get().strip()},{wednesday_shift_start.get()} AM,{wednesday_shift_end.get()} PM"
                        thursday_scehdule = f"{thursday_attendance.get().strip()},{thursday_shift_start.get()} AM,{thursday_shift_end.get()} PM"
                        friday_scehdule = f"{friday_attendance.get().strip()},{friday_shift_start.get()} AM,{friday_shift_end.get()} PM"
                        this.database.update_shifts(username = username, monday = monday_scehdule, tuesday = tuesday_scehdule, wednesday = wednesday_scehdule, thursday = thursday_scehdule, friday = friday_scehdule)
                        messagebox.showinfo('Success!', 'Your schedule saved successfully!')

                    save_btn = ttk.Button(this.canvas, text = 'Save', command = save_schedule)
                    save_btn.place(x = 215, y = 345)
            else:
                messagebox.showerror ('Error', 'Invalid credentials!')
        else:
            messagebox.showerror('Invalid Credentials!', 'Username or password must not be empty!')

    def __register_user(this, event) -> None:
        username = this.username_entry.get().strip()
        password = this.password_entry.get().strip()
        if len(username) < 5 or len(password) < 5:
            messagebox.showerror('Invalid Credentials!', 'Username or password must be atleat of length 5!')
        elif len(username) >= 5 or len(password) >= 5:
            if this.database.user_existence(username = username) == True:
                messagebox.showwarning(username, f'User "{username}" already registered!')
            else:
                this.database.register(username, password)
                messagebox.showinfo(username, f'User "{username}" has been registered succesfully!')

            this.canvas.delete(this.register_btn)
            this.canvas.delete(this.register_button)
            this.register_lable.place(x = 269, y = 265)
            this.register_button = this.canvas.create_image(297, 275, anchor=tkinter.CENTER,image=this.register_btn)

            this.username_entry.delete(0, tkinter.END)
            this.password_entry.delete(0, tkinter.END)
            this.username_entry.focus_set()
            
            this.login_btn= ImageTk.PhotoImage(Image.open("assets/icons/login.png"))
            this.login_button = this.canvas.create_image(205, 275, anchor=tkinter.CENTER,image=this.login_btn)
            this.canvas.tag_bind(this.login_button, "<Button-1>", this.__login_user)

            this.login_lable = ttk.Label(this.canvas, text = 'Login', font=("Helvetica", 10), justify = 'center', foreground = 'white', background = '#419FD9', cursor = 'hand2')
            this.login_lable.place(x = 187, y = 265)
            this.login_lable.bind("<Button-1>", this.__login_user)
        else:
            messagebox.showerror('Invalid Credentials!', 'Username or password must not be empty!')


    def run(this) -> None:
        this.window.mainloop()


if __name__ == "__main__":
    App().run()