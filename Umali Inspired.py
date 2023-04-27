from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import queue
import random
import time
import sqlite3

con = sqlite3.connect("Library.db")
cur = con.cursor()
try:
    cur.execute("INSERT INTO employees(first, last, fulltime, wage, FillIn) VALUES(?,?,?,?,?)", ('John', 'Doe', 'Full-time', '$20/hr', False))
    con.commit()
    print("Record inserted successfully into employees table")
except Exception as e:
    print(f"Error: {e}")



days_of_the_week = [
  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]

shift_day1 = {}
shift_name1 = {}
use = ""
for i in range(0, 7):
  shift_name1.update({
    1 + (3 * i): 'Librarian',
    2 + (3 * i): 'Technician',
    3 + (3 * i): 'Customer Assistant',
  })
  for j in range(1, 5):
    shift_day1.update({(j + (3 * i)): days_of_the_week[i]})

shift_day2 = {}
shift_name2 = {}
for i in range(0, 7):
  shift_name2.update({
    28 + 1 + (2 * i): 'Librarian',
    28 + 2 + (2 * i): 'Customer Assistant',
  })

for j in range(1, 3):
  shift_day2.update({28 + (j + (2 * i)): days_of_the_week[i]})

create_employees_table = (
  "CREATE TABLE IF NOT EXISTS employees(empID integer PRIMARY KEY, first text, last text, fulltime text, wage text, FillIn boolean);"
)
create_shifts_table = (
  """CREATE TABLE IF NOT EXISTS shifts(dutyID integer, empID integer,day text, role text);"""
)
create_timetable_table = (
  """CREATE TABLE IF NOT EXISTS timetable(dutyID integer PRIMARY KEY, assign_emp boolean);"""
)

cur.execute(create_employees_table)
cur.execute(create_shifts_table)
cur.execute(create_timetable_table)

for z in range(1, 43):
  cur.execute("SELECT * FROM timetable WHERE dutyID=?", (z, ))
  if not cur.fetchall():
    cur.execute("INSERT INTO timetable VALUES(?,?)", (z, False))
con.commit()

userList = []
SickDict = {}


class empCount():
  fulltime_emps = 0
  partime_emps = 0
  empIDindex = 1

  @classmethod
  def add_empIDindex(cls):
    cls.empIDindex += 1

  @classmethod
  def add_femp(cls):
    cls.fulltime_emps += 1

  @classmethod
  def add_pemp(cls):
    cls.partime_emps += 1

  @classmethod
  def rem_femp(cls):
    cls.fulltime_emps -= 1

  @classmethod
  def rem_pemp(cls):
    cls.partime_emps -= 1


class Login(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Employee Schedule System")
    self.geometry("500x300")

  def open_employee_window(self):
    empwindow = employeePage(self)
    empwindow.grab_set()

  def open_owner_window(self):
    ownerwindow = ownerPage(self)
    ownerwindow.grab_set()

  def checkmanager():
    if UsernameVal.get() == "manager234" and PasswordVal.get() == "General1":
      open_owner_window(self)
    else:
      messagebox.showinfo("", "Incorrect or empty credentials")

  def checkemployee():
    if UsernameVal.get() in userList and PasswordVal.get() == "employees2023":
      open_employee_window(self)
    else:
      messagebox.showinfo("", "Incorrect or empty credentials")
      Label(text="Login", font='ar 15 bold').grid(row=0, column=5)
      Username = Label(text="Username: ")
      Username.grid(row=1, column=2)
      Password = Label(text="Password: ")
      Password.grid(row=2, column=2)
      Username.grid(row=1, column=2)
      Password.grid(row=2, column=2)
      UsernameVal = StringVar()
      PasswordVal = StringVar()
      UsernameEntry = Entry(textvariable=UsernameVal)
      PasswordEntry = Entry(textvariable=PasswordVal)
      UsernameEntry.grid(row=1, column=3)
      PasswordEntry.grid(row=2, column=3)
      Button(text="Owner", command=checkmanager).grid(row=3, column=2)
      Button(text="Employee", command=checkemployee).grid(row=3, column=3)


class ownerPage(tk.Toplevel):
  use_day = ""
  use_shift = ""

  def __init__(self, parent):
    super().__init__(parent)
    self.title("Employee Schedule System")
    self.geometry("1350x750+0+0")
    self.config(bg="gray")
    self.SC1 = [1, 5, 9, 13, 17, 21, 25]
    self.CA1 = [2, 6, 10, 14, 18, 22, 26]
    self.SC2 = [3, 7, 11, 15, 19, 23, 27]
    self.CA2 = [4, 8, 12, 16, 20, 24, 28]
    self.assigncount = 0
    fulltime = StringVar()
    wage = StringVar()

  def Exit():
    CreateUserNames()  # found around line 221
    self.destroy()

  def CheckAdd():
    if fulltime.get().title() == "Yes":
      if empCount.fulltime_emps < 6:
        empCount.add_femp()
        addData()
      else:
        messagebox.showinfo("", "Maximum fulltime workers")
    else:
      if empCount.partime_emps < 6:
        empCount.add_pemp()
        addData()
      else:
        messagebox.showinfo("", "Maximum parttime workers")

  def addData():
    cur.execute("INSERT INTO employees VALUES (?,?,?,?,?,?)",
                (empCount.empIDindex, first.get().title(), last.get().title(),
                 fulltime.get().title(), wage.get(), False))
    con.commit()
    empCount.add_empIDindex()

  def OpenDelete(self):
    DeleteEmp = DeletePage(self)
    DeleteEmp.grab_set()

  def Delete():
    OpenDelete(self)

  def ViewRota():
    ViewRota = ShowEmployeeShifts(self)
    ViewRota.grab_set()

  def CreateUserNames():
    nameList = []
    part1List = []
    initialList = []
    firstList = []
    cur.execute("""SELECT last FROM employees""")
    for name in cur.fetchall():
      nameList.append(str(name))
    for x in range(len(nameList)):
      y = len(nameList[x])
      part1List.append("15" + nameList[x][2:(y - 3)].lower())
      cur.execute("""SELECT first FROM employees""")
    for firstname in cur.fetchall():
      firstList.append(str(firstname))
    for n in range(len(firstList)):
      initialList.append(firstList[n][2].lower())
    for part in range(len(part1List)):
      userList.append(part1List[part] + initialList[part])

  def check_free(use_day, use_shift, empID, dutyID):
    if self.assigncount > 0:
      self.temp_list = []
      self.return_val = ''
      check_same_day = ("""SELECT dutyID from shifts WHERE empID = ? """)
      cur.execute(check_same_day, (empID, ))
      for ids in cur.fetchall():
        self.temp_list.append(int(ids[0]))
      for ids in self.temp_list:
        if ids in self.SC1:
          if ids == (int(empID) + 1):
            self.return_val = 1
          else:
            self.return_val = 0
        elif ids in self.CA1:
          if ids == (int(empID) - 1):
            self.return_val = 1
          else:
            self.return_val = 0
        elif ids in self.SC2:
          if ids == (int(empID) + 1):
            self.return_val = 1
          else:
            self.return_val = 0
        else:
          if ids == (int(empID) - 1):
            self.return_val = 1
          else:
            self.return_val = 0
      if self.return_val == 0:
        y = SickDict.keys()
        if empID in y:
          day = self.use_day.get(dutyID)
          x = SickDict.setdefault(empID)
          if x == day:
            return 1
          else:
            return 0
        else:
          return 0
      else:
        return self.return_val
    else:
      y = SickDict.keys()
    if empID in y:
      day = self.use_day.get(dutyID)
      x = SickDict.setdefault(empID)
      if x == day:
        return 1
      else:
        return 0
    else:
      return 0

  def save_shift(use_day, use_shift, dutyID, empID):
    save_to = ("""INSERT INTO shifts VALUES (?,?,?,?)""")
    cur.execute(save_to,
                (dutyID, empID, use_day.get(dutyID), use_shift.get(dutyID)))
    con.commit()

  def CreateRota():
    CreateRotaFull()
    time.sleep(1)
    CreateRotaPart()
    time.sleep(1)
    CreateRotaPart()

  def CreateRotaFull():
    self.employees_full_Q = queue.Queue()
    cur.execute(""" SELECT empID FROM employees WHERE fulltime == 'Yes'""")
    for emp in cur.fetchall():
      self.employees_full_Q.put(int(emp[0]))
      self.vacant_jobs_full = []
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID < 21"""
      )
      for dutyID1 in cur.fetchall():
        self.vacant_jobs_full.append(int(dutyID1[0]))
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID < 39 AND dutyID > 28"""
      )
      for dutyID2 in cur.fetchall():
        self.vacant_jobs_full.append(int(dutyID2[0]))
        random.shuffle(self.vacant_jobs_full)
    for empID in self.employees_full_Q.queue:
      for dutyID in self.vacant_jobs_full:
        if self.assigncount >= 5:
          self.assigncount = 0
          break
        else:
          if dutyID < 29:
            use_shift = shift_day1
            use_day = shift_name1
          else:
            use_shift = shift_day2
            use_day = shift_name2
          check_if_taken = (
            """SELECT assign_emp from timetable WHERE dutyID = ? """)
          cur.execute(check_if_taken, (dutyID, ))
          TorF = cur.fetchall()
          if (str(TorF[0])[1]) == '0':
            free = check_free(use_day, use_shift, empID, dutyID)
            if free == 0:
              save_shift(use_day, use_shift, dutyID, empID)
              change_to_true = (
                """UPDATE timetable SET assign_emp = ? WHERE dutyID = ? """)
              con.commit()
              self.assigncount += 1
            else:
              pass
          else:
            pass

    def CreateRotaPart():
      self.employees_part_Q = queue.Queue()
      cur.execute(""" SELECT empID FROM employees WHERE fulltime == 'No'""")
      for emp in cur.fetchall():
        self.employees_part_Q.put(int(emp[0]))
        self.vacant_jobs_part = []
        cur.execute(
          """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID > 20 AND dutyID < 29"""
        )
        for dutyID3 in cur.fetchall():
          self.vacant_jobs_part.append(int(dutyID3[0]))
          cur.execute(
            """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID > 38"""
          )
        for dutyID4 in cur.fetchall():
          self.vacant_jobs_part.append(int(dutyID4[0]))
      for empID in self.employees_part_Q.queue:
        for dutyID in self.vacant_jobs_part:
          if self.assigncount > 1:
            self.assigncount = 0
            break
          else:
            if dutyID < 29:
              use_shift = shift_day1
              use_day = shift_name1
            else:
              use_shift = shift_day2
              use_day = shift_name2
            check_if_taken = (
              """SELECT assign_emp from timetable WHERE dutyID = ? """)
            cur.execute(check_if_taken, (dutyID, ))
            TorF = cur.fetchall()
            if (str(TorF[0])[1]) == '0':
              free = check_free(use_day, use_shift, empID, dutyID)
              if free == 0:
                save_shift(use_day, use_shift, dutyID, empID)
                change_to_true = (
                  """UPDATE timetable SET assign_emp = ? WHERE dutyID = ? """)
                cur.execute(change_to_true, (True, dutyID))
                con.commit()
                self.assigncount += 1
              else:
                pass
            else:
              pass

  def UpdateRotaFull():
    self.filler_empsD = queue.Queue()
    self.vacant_jobs_full = []
    try:
      cur.execute(
        """SELECT DISTINCT empID FROM employees WHERE FillIn = 1 AND fulltime == 'Yes'"""
      )
      for emp in cur.fetchall():
        self.filler_empsF.put(int(emp[0]))
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID < 21"""
      )
      for dutyID1 in cur.fetchall():
        self.vacant_jobs_full.append(int(dutyID1[0]))
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID < 39 AND dutyID > 28"""
      )
      for dutyID2 in cur.fetchall():
        self.vacant_jobs_full.append(int(dutyID2[0]))
      random.shuffle(self.vacant_jobs_full)
      for empID in self.filler_empsF.queue:
        for dutyID in self.vacant_jobs_full:
          if self.assigncount == 1:
            self.assigncount = 0
            break
          else:
            use_shift = shift_day2
            use_day = shift_name2
          check_if_taken = (
            """SELECT assign_emp from timetable WHERE dutyID = ? """)
          cur.execute(check_if_taken, (dutyID, ))
          TorF = cur.fetchall()
          if (str(TorF[0])[1]) == '0':
            free = check_free(use_day, use_shift, empID, dutyID)
            if free == 0:
              save_shift(use_day, use_shift, dutyID, empID)
              change_to_true = (
                """UPDATE timetable SET assign_emp = ? WHERE dutyID = ?""")
              cur.execute(change_to_true, (True, dutyID))
              con.commit()
              self.assigncount += 1
            else:
              pass
          else:
            pass
    except:  #if there are no full time employees that want to fill in then move on
      pass

  def UpdateRotaPart():
    self.filler_empsP = queue.Queue()
    self.vacant_jobs_part = []
    try:
      cur.execute(
        """SELECT DISTINCT empID FROM employees WHERE FillIn = 1 AND fulltime == 'No'"""
      )
      for emp in cur.fetchall():
        self.filler_empsF.put(int(emp[0]))
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID > 20 AND dutyID < 29"""
      )
      for dutyID3 in cur.fetchall():
        self.vacant_jobs_part.append(int(dutyID3[0]))
      cur.execute(
        """SELECT DISTINCT dutyID FROM timetable WHERE assign_emp = 0 AND dutyID > 38"""
      )
      for dutyID4 in cur.fetchall():
        self.vacant_jobs_part.append(int(dutyID4[0]))
      for empID in self.filler_empsP.queue:
        for dutyID in self.vacant_jobs_part:
          if self.assigncount == 1:
            self.assigncount = 0
            break
          else:
            if dutyID < 29:
              use_shift = shift_day1
              use_day = shift_name1
            else:
              use_shift = shift_day2
              use_day = shift_name2
            check_if_taken = (
              """SELECT assign_emp from timetable WHERE dutyID = ? """)
            cur.execute(check_if_taken, (dutyID, ))
            TorF = cur.fetchall()
            if (str(TorF[0])[1]) == '0':
              free = check_free(use_day, use_shift, empID, dutyID)
              if free == 0:
                save_shift(use_day, use_shift, dutyID, empID)
                change_to_true = (
                  """UPDATE timetable SET assign_emp = ? WHERE dutyID = ?""")
                cur.execute(change_to_true, (True, dutyID))
                con.commit()
                self.assigncount += 1
              else:
                pass
            else:
              pass
    except:
      pass

  def UpdateRota():
    UpdateRotaFull()
    time.sleep(1)
    UpdateRotaPart()

  def ClearRota():
    reset_shifts = ("""DELETE from shifts WHERE dutyID = ?""")
    reset_timetable = (
      """UPDATE timetable SET assign_emp = ? WHERE dutyID = ?""")
    for z in range(1, 43):
      cur.execute(reset_shifts, (z, ))
      cur.execute(reset_timetable, (False, z))
    con.commit()

  def ExportRota():
    cur.execute(
      """SELECT DISTINCT employees.empID,employees.first,employees.last,shifts.day,shifts.role FROM employeesm INNER JOIN shifts ON employees.empID=shifts.empID;"""
    )
    f = open('Rota.csv', 'w')  #Creates and opens a new csv file
    f.write("ID: | First name: | Surname: | Shift role: | Shift day: \n")
    for row in cur.fetchall():
      f.write(' '.join(str(x) for x in row) +
              '\n')  #Writes each shift to the csv file
    f.close()
    Mainframe = Frame(self, bg="gray")
    Mainframe.grid()
    Titleframe = Frame(Mainframe,
                       bd=2,
                       padx=54,
                       pady=8,
                       bg="azure",
                       relief=RIDGE)
    Titleframe.pack(side=TOP)
    self.lblTitle = Label(Titleframe,
                          font=('arial', 47),
                          text="Employee Schedule System",
                          bg="azure")
    self.lblTitle.grid()
    Buttonframe = Frame(Mainframe,
                        bd=2,
                        width=1350,
                        height=70,
                        padx=18,
                        pady=10,
                        bg="azure",
                        relief=RIDGE)
    Buttonframe.pack(side=BOTTOM)
    Dataframe = Frame(Mainframe,bd=1,width=1300,height=400,padx=20,pady=20,relief=RIDGE,bg="gray")
    Dataframe.pack(side=BOTTOM)
    DataframeLeft = LabelFrame(Dataframe,
                               bd=1,
                               width=1000,
                               height=600,
                               padx=20,
                               relief=RIDGE,
                               bg="azure",
                               font=('arial', 20),
                               text="Employee Information\n")
    DataframeLeft.pack(side=LEFT)
    self.lblfirst = Label(DataframeLeft,
                          font=('arial, 20'),
                          text="First Name",
                          padx=2,
                          pady=2,
                          bg="azure")
    self.lblfirst.grid(row=1, column=0, sticky=W)
    self.txtfirst = Entry(DataframeLeft,
                          font=('arial, 20'),
                          textvariable=first,
                          width=39)
    self.txtfirst.grid(row=1, column=1)
    self.lbllast = Label(DataframeLeft,
                         font=('arial, 20'),
                         text="Last Name",
                         padx=2,
                         pady=2,
                         bg="azure")
    self.lbllast.grid(row=2, column=0, sticky=W)
    self.txtlast = Entry(DataframeLeft,
                         font=('arial, 20'),
                         textvariable=last,
                         width=39)
    self.txtlast.grid(row=2, column=1)
    self.lblfulltime = Label(DataframeLeft,
                             font=('arial, 20'),
                             text="Full Time?",
                             padx=2,
                             pady=2,
                             bg="azure")
    self.lblfulltime.grid(row=3, column=0, sticky=W)
    self.txtfulltime = Entry(DataframeLeft,
                             font=('arial, 20'),
                             textvariable=fulltime,
                             width=39)
    self.txtfulltime.grid(row=3, column=1)
    self.lblwage = Label(DataframeLeft,
                         font=('arial,20'),
                         text="Wage",
                         padx=2,
                         pady=2,
                         bg="azure")
    self.lblwage.grid(row=4, column=0, sticky=W)
    self.txtwage = Entry(DataframeLeft,
                         font=('arial, 20'),
                         textvariable=wage,
                         width=39)
    self.txtwage.grid(row=4, column=1)

    self.btnAddData = Button(Buttonframe,
                             text="Add New",
                             font=('arial', 20),
                             height=1,
                             width=12,
                             bd=4,
                             command=CheckAdd)
    self.btnAddData.grid(row=0, column=0)
    self.btnViewSched = Button(Buttonframe,
                               text="View Rota",
                               font=('arial', 20),
                               height=1,
                               width=12,
                               bd=4,
                               command=ViewRota)
    self.btnViewSched.grid(row=0, column=1)
    self.btnExit = Button(Buttonframe,
                          text="Exit",
                          font=('arial', 20),
                          height=1,
                          width=12,
                          bd=4,
                          command=Exit)
    self.btnExit.grid(row=0, column=2)
    self.btnClear = Button(Buttonframe,
                           text="Clear",
                           font=('arial', 20),
                           height=1,
                           width=12,
                           bd=4,
                           command=ClearData)
    self.btnClear.grid(row=0, column=3)
    self.btnExportRota = Button(Buttonframe,
                                text="Export Rota",
                                font=('arial', 20),
                                height=1,
                                width=12,
                                bd=4,
                                command=ExportRota)
    self.btnExportRota.grid(row=0, column=4)
    self.btnDelete = Button(Buttonframe,
                            text="Delete",
                            font=('arial', 20),
                            height=1,
                            width=12,
                            bd=4,
                            command=Delete)
    self.btnDelete.grid(row=1, column=0)
    self.btnGenerate = Button(Buttonframe,
                              text="Create Rota",
                              font=('arial', 20),
                              height=1,
                              width=12,
                              bd=4,
                              command=CreateRota)
    self.btnGenerate.grid(row=1, column=1)
    self.btnViewEmps = Button(Buttonframe,
                              text="View Employees",
                              font=('arial', 20),
                              height=1,
                              width=12,
                              bd=4,
                              command=ViewEmps)
    self.btnViewEmps.grid(row=1, column=2)
    self.btnClearRota = Button(Buttonframe,
                               text="Clear Rota",
                               font=('arial', 20),
                               height=1,
                               width=12,
                               bd=4,
                               command=ClearRota)
    self.btnClearRota.grid(row=1, column=3)
    self.btnUpdateRota = Button(Buttonframe,
                                text="Update Rota",
                                font=('arial', 20),
                                height=1,
                                width=12,
                                bd=4,
                                command=UpdateRota)
    self.btnUpdateRota.grid(row=1, column=4)


class employeePage(tk.Toplevel):  #called from the login class

  def __init__(self, parent):
    super().__init__(parent)
    self.title("Employee Schedule System")
    self.geometry("1350x750+0+0")
    self.config(bg="gray")
    empID = StringVar()
    dayOff = StringVar()

    def Exit():
      self.destroy()

    def ClearData():
      self.txtempID.delete(0, END)
      self.txtfirst.delete(0, END)
      self.txtlast.delete(0, END)
      self.txtfulltime.delete(0, END)
      self.txtwage.delete(0, END)

    def AddPreference():
      id_list = []
      day = dayOff.get().title()  #Holds the day in a variable
      SickDict.update({empID.get(): day})
      update_timetable = """UPDATE timetable SET assign_emp = ? WHERE dutyID = ? """
      delete_shifts = """DELETE FROM shifts WHERE dutyID = ?"""
      get_Did = """SELECT dutyID FROM shifts WHERE empID = ? and role = ?"""
      cur.execute(get_Did, (empID.get(), day))
      for i in cur.fetchall():
        id_list.append(i[0])
        cur.execute(update_timetable, (False, i[0]))
        cur.execute(delete_shifts, (i[0], ))
      con.commit()

    def OpenIndividual(self, empID):
      Individual = ShowIndividualShifts(self)
      userList.clear()
      Individual.ShowIndEmpShifts(empID)

    def ViewIndividualRota():
      if len(empID.get()) == 0:
        ViewR = ShowEmployeeShifts(self)
        ViewR.grab_set()
      else:
        OpenIndividual(self, empID.get())

    def FillIn():
      update_fillin = ("""UPDATE employees SET FillIn = ? WHERE empID = ? """)
      cur.execute(update_fillin, (True, empID.get()))

    def ViewAllEmps():
      ViewEmp = ViewEmployeeData(self)
      ViewEmp.grab_set()

    Mainframe = Frame(self, bg="gray")
    Mainframe.grid()
    Titleframe = Frame(Mainframe,
                       bd=2,
                       padx=54,
                       pady=8,
                       bg="azure",
                       relief=RIDGE)
    Titleframe.pack(side=TOP)
    self.lblTitle = Label(Titleframe,
                          font=('arial', 47),
                          text="Employee Schedule System",
                          bg="azure")
    self.lblTitle.grid()
    Buttonframe = Frame(Mainframe,
                        bd=2,
                        width=1350,
                        height=70,
                        padx=18,
                        pady=10,
                        bg="azure",
                        relief=RIDGE)
    Buttonframe.pack(side=BOTTOM)
    Dataframe = Frame(Mainframe,
                      bd=1,
                      width=1300,
                      height=400,
                      padx=20,
                      pady=20,
                      relief=RIDGE,
                      bg="gray")
    Dataframe.pack(side=BOTTOM)
    DataframeLeft = LabelFrame(Dataframe,
                               bd=1,
                               width=1000,
                               height=600,
                               padx=20,
                               relief=RIDGE,
                               bg="azure",
                               font=('arial', 20),
                               text="Employee Information\n")
    DataframeLeft.pack(side=LEFT)
    self.lblempID = Label(DataframeLeft,
                          font=('arial, 20'),
                          text="Employee ID",
                          padx=2,
                          pady=2,
                          bg="azure")
    self.lblempID.grid(row=0, column=0, sticky=W)
    self.txtempID = Entry(DataframeLeft,
                          font=('arial, 20'),
                          textvariable=empID,
                          width=39)
    self.txtempID.grid(row=0, column=1)
    self.lblfirst = Label(DataframeLeft,
                          font=('arial, 20'),
                          text="Day Off",
                          padx=2,
                          pady=2,
                          bg="azure")
    self.lblfirst.grid(row=1, column=0, sticky=W)
    self.txtfirst = Entry(DataframeLeft,
                          font=('arial, 20'),
                          textvariable=dayOff,
                          width=39)
    self.txtfirst.grid(row=1, column=1)
    self.btnAddPref = Button(Buttonframe,
                             text="Sick day",
                             font=('arial', 20),
                             height=1,
                             width=12,
                             bd=4,
                             command=AddPreference)
    self.btnAddPref.grid(row=0, column=0)
    self.btnExit = Button(Buttonframe,
                          text="Exit",
                          font=('arial', 20),
                          height=1,
                          width=12,
                          bd=4,
                          command=Exit)
    self.btnExit.grid(row=0, column=1)
    self.btnClear = Button(Buttonframe,
                           text="Clear",
                           font=('arial', 20),
                           height=1,
                           width=12,
                           bd=4,
                           command=ClearData)
    self.btnClear.grid(row=0, column=2)
    self.btnViewRota = Button(Buttonframe,
                              text="View Rota",
                              font=('arial', 20),
                              height=1,
                              width=12,
                              bd=4,
                              command=ViewIndividualRota)
    self.btnViewRota.grid(row=1, column=0)
    self.btnSetFillIn = Button(Buttonframe,
                               text="Extra Hours",
                               font=('arial', 20),
                               height=1,
                               width=12,
                               bd=4,
                               command=FillIn)
    self.btnSetFillIn.grid(row=1, column=1)
    self.btnViewAllEmps = Button(Buttonframe,
                                 text="View Employees",
                                 font=('arial', 20),
                                 height=1,
                                 width=12,
                                 bd=4,
                                 command=ViewAllEmps)
    self.btnViewAllEmps.grid(row=1, column=2)




class ViewEmployeeData(tk.Toplevel):

  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent
    self.title("Employees")
    self.geometry("700x300")
    self.ShowEmpData()

  def ShowEmpData(self):
    tree = ttk.Treeview(self)
    tree['columns'] = ("col1", "col2", "col3", "col4", "col5")
    tree.column("col1", width=100)
    tree.column("col2", width=200)
    tree.column("col3", width=200)
    tree.column("col4", width=100)
    tree.column("col5", width=100)
    tree['show'] = 'headings'
    tree.heading("col1", text="Employee ID", anchor='center')
    tree.heading("col2", text="First Name", anchor='center')
    tree.heading("col3", text="Last Name", anchor='center')
    tree.heading("col4", text="Full time:", anchor='center')
    tree.heading("col5", text="Wage(£)", anchor='center')
    tree.grid(row=0, column=2, rowspan=3, columnspan=3)
    cur.execute("SELECT * FROM employees")
    records = cur.fetchall()
    for record in records:
      tree.insert('',
                  'end',
                  values=(record[0], record[1], record[2], record[3],
                          record[4]))


class ShowEmployeeShifts(tk.Toplevel):

  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent
    self.title("Employees")
    self.geometry("1000x300")
    self.ShowEmpShifts()

  def ShowEmpShifts(self):
    tree = ttk.Treeview(self)
    tree['columns'] = ("col1", "col2", "col3", "col4", "col5")
    tree.column("col1", width=100)
    tree.column("col2", width=200)
    tree.column("col3", width=200)
    tree.column("col4", width=300)
    tree.column("col5", width=200)
    tree['show'] = 'headings'
    tree.heading("col1", text="Employee ID", anchor='center')
    tree.heading("col2", text="First Name", anchor='center')
    tree.heading("col3", text="Last Name", anchor='center')
    tree.heading("col4", text="Role:", anchor='center')
    tree.heading("col5", text="Day:", anchor='center')
    tree.grid(row=0, column=2, rowspan=3, columnspan=3)
    cur.execute(
      """SELECT DISTINCT employees.empID,employees.first,employees.last,shifts.day,shifts.role FROM employees INNER JOIN shifts ON employees.empID=shifts.empID;"""
    )
    records = cur.fetchall()
    for record in records:
      tree.insert('',
                  'end',
                  values=(record[0], record[1], record[2], record[3],
                          record[4]))


class ShowIndividualShifts(tk.Toplevel):

  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent
    self.title("Employees")
    self.geometry("1000x300")

  def ShowIndEmpShifts(self, empIDS):
    tree = ttk.Treeview(self)
    tree['columns'] = ("col1", "col2", "col3", "col4", "col5")
    tree.column("col1", width=100)
    tree.column("col2", width=200)
    tree.column("col3", width=200)
    tree.column("col4", width=300)
    tree.column("col5", width=200)
    tree['show'] = 'headings'
    tree.heading("col1", text="Employee ID", anchor='center')
    tree.heading("col2", text="First Name", anchor='center')
    tree.heading("col3", text="Last Name", anchor='center')
    tree.heading("col4", text="Role:", anchor='center')
    tree.heading("col5", text="Day:", anchor='center')
    tree.grid(row=0, column=2, rowspan=3, columnspan=3)
    cur.execute(
      """SELECT DISTINCT employees.empID,employees.first,employees.last,shifts.day,shifts.role FROM employees INNER JOIN shifts ON employees.empID=shifts.empID WHERE employees.empID =?;""",
      (empIDS, ))
    records = cur.fetchall()
    for record in records:
      tree.insert('',
                  'end',
                  values=(record[0], record[1], record[2], record[3],
                          record[4]))


if __name__ == '__main__':
  app = Login()
  app.mainloop()
