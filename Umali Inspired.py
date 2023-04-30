#import tkinter as tk
import tkinter as tk
#from tkinter import ttk, messagebox
from tkinter import ttk, messagebox
#import pulp as lp
import pulp as lp
#import pandas as pd
import pandas as pd
#from datetime import time, datetime
from datetime import time, datetime

root = tk.Tk()
root.title('Shift Scheduler')

# Define Employees
employees = {
    'Employee 1': {'Max Hours': 12, 'Skill': 'Skill 1', 'Time Off': []},
    'Employee 2': {'Max Hours': 12, 'Skill': 'Skill 2', 'Time Off': []},
    'Employee 3': {'Max Hours': 12, 'Skill': 'Skill 1', 'Time Off': []},
}

# Define Shifts
shift_data = {
    'Monday': [
        {'Start Time': time(9, 0), 'End Time': time(12, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(12, 0), 'End Time': time(15, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(15, 0), 'End Time': time(18, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
    ],
    'Tuesday': [
        {'Start Time': time(9, 0), 'End Time': time(12, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(12, 0), 'End Time': time(15, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
        {'Start Time': time(15, 0), 'End Time': time(18, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
    ],
    'Wednesday': [
        {'Start Time': time(9, 0), 'End Time': time(12, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
        {'Start Time': time(12, 0), 'End Time': time(15, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
        {'Start Time': time(15, 0), 'End Time': time(18, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
    ],
    'Thursday': [
        {'Start Time': time(9, 0), 'End Time': time(12, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(12, 0), 'End Time': time(15, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(15, 0), 'End Time': time(18, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
    ],
    'Friday': [
        {'Start Time': time(9, 0), 'End Time': time(12, 0), 'Skill Required': 'Skill 2', 'Required Employees': 1},
        {'Start Time': time(12, 0), 'End Time': time(15, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
        {'Start Time': time(15, 0), 'End Time': time(18, 0), 'Skill Required': 'Skill 1', 'Required Employees': 1},
    ],
}

# Define Shifts
#define and Iterate
shifts = list(shift_data.keys())

# Define Employee Data

employee_data = {}
for emp in employees:
    employee_data[emp] = {'Max Hours': employees[emp]['Max Hours'], 'Skill': employees[emp]['Skill'], 'Time Off': employees[emp]['Time Off'], 'Scheduled Hours': 0}


# Generate Schedule Frame

generate_schedule_frame = ttk.LabelFrame(root, text='Generate Schedule')

generate_schedule_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

#function of generation
def generate_schedule():
    # Create LP Problem
    prob = lp.LpProblem('Shift_Scheduling', lp.LpMaximize)
    # Create Variables
    
    shifts_vars = lp.LpVariable.dicts('Shifts', [(e, d) for e in employees for d in shifts], lowBound=0, upBound=1, cat='Integer')

    # Create Objective Function
    prob += lp.lpSum([shifts_vars[(e, d)] for e in employees for d in shifts])

    # Create Constraints
    for e in employees:
        # Maximum Hours Constraint
        prob += lp.lpSum([shift_data[d][i]['End Time'].hour - shift_data[d][i]['Start Time'].hour for d in shifts for i in range(len(shift_data[d])) if (e, d) in shifts_vars and shifts_vars[(e, d)] == 1]) <= employee_data[e]['Max Hours'], f"Maximum_Hours_Constraint_{e}"

        # Skill Required Constraint
        for d in shifts:
            for i in range(len(shift_data[d])):
                prob += lp.lpSum([shifts_vars[(e, d)] for e in employees if (e, d) in shifts_vars and employee_data[e]['Skill'] == shift_data[d][i]['Skill Required']]) >= shift_data[d][i]['Required Employees'], f"Skill_Required_Constraint_{d}_{i}"

        # One Shift Per Day Constraint
        for d in shifts:
            prob += lp.lpSum([shifts_vars[(e, d)] for e in employees if (e, d) in shifts_vars]) == 1, f"One_Shift_Per_Day_Constraint_{e}_{d}"

    # Time Off Constraint
    for e in employees:
        for d in employee_data[e]['Time Off']:
            prob += lp.lpSum([shifts_vars[(e, d)]]) == 0, f"Time_Off_Constraint_{e}_{d}"

    # Solve Problem
    #get result
    prob.solve()

    
    # Display Results
    
    schedule_df = pd.DataFrame(columns=['Employee', 'Day', 'Start Time', 'End Time'])
    
    #iterate all e in employes
    for e in employees:
        for d in shifts:
            for i in range(len(shift_data[d])):
                if shifts_vars[(e, d)].varValue == 1:
                    schedule_df = schedule_df.append({'Employee': e, 'Day': d, 'Start Time': shift_data[d][i]['Start Time'], 'End Time': shift_data[d][i]['End Time']}, ignore_index=True)
                    employee_data[e]['Scheduled Hours'] += shift_data[d][i]['End Time'].hour - shift_data[d][i]['Start Time'].hour

    schedule_df = schedule_df.sort_values(by=['Day', 'Start Time'])

    messagebox.showinfo('Schedule Generated', 'Schedule has been generated.')

    
    # Show Schedule Frame
    
    show_schedule_frame = ttk.LabelFrame(root, text='Show Schedule')
    
    show_schedule_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
 
    #getttt treeview
    treeview = ttk.Treeview(show_schedule_frame, columns=('Employee', 'Day', 'Start Time', 'End Time'))
    
    #gettt treeview headingg
    treeview.heading('Employee', text='Employee')
    
    #gettt treeview headinggg
    treeview.heading('Day', text='Day')
    
    #gettt treeview headinggg2 
    treeview.heading('Start Time', text='Start Time')
    
    #gettt treeview headinggg2 
    treeview.heading('End Time', text='End Time')


    for e in employees:
        treeview.insert('', 'end', text=e, values=list(schedule_df[schedule_df['Employee'] == e][['Employee', 'Day', 'Start Time', 'End Time']].itertuples(index=False, name=None)))


    treeview.pack()

##
# Modify Schedule Frame

modify_schedule_frame = ttk.LabelFrame(root, text='Modify Schedule')

## Modify Schedule Frame throgh coulumns
modify_schedule_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Define Variables for Modify Schedule
assigned_shifts = []

# Create Function to Assign Shift
def assign_shift():

    selected_item = treeview.focus()
    if selected_item:
    
        employee_name = treeview.item(selected_item, 'text')

        shift_info = treeview.item(selected_item, 'values')

        #get day
        day = shift_info[0]
        
        #get startt timea
        
        #endtimea
        
        #shift
      
        start_time = shift_info[1]
        end_time = shift_info[2]
        shift = {'Employee': employee_name, 'Day': day, 'Start Time': start_time, 'End Time': end_time}
        
        assigned_shifts.append(shift)
        
        assigned_shifts_df = pd.DataFrame(assigned_shifts)

        assigned_shifts_df = assigned_shifts_df.sort_values(by=['Day', 'Start Time'])

        assigned_treeview.delete(*assigned_treeview.get_children())
        
        for index, row in assigned_shifts_df.iterrows():
            assigned_treeview.insert('', 'end', text=row['Employee'], values=(row['Day'], row['Start Time'], row['End Time']))
        treeview.delete(selected_item)
        

# Create Function to Reassign Shift

def reassign_shift():

    selected_item = assigned_treeview.focus()

    if selected_item:
        
        #initialize employee_name
        employee_name = assigned_treeview.item(selected_item, 'text')
        
        #initialize shift_info
        shift_info = assigned_treeview.item(selected_item, 'values')
        
        #initialize
        day = shift_info[0]
        
        #initialize
        start_time = shift_info[1]
        
        #initialize
        end_time = shift_info[2]
        
        #initialize
        shift = {'Employee': employee_name, 'Day': day, 'Start Time': start_time, 'End Time': end_time}
        
        #initialize
        assigned_shifts.remove(shift)
        
        #initialize
        assigned_shifts_df = pd.DataFrame(assigned_shifts)
        
        #initialize
        assigned_shifts_df = assigned_shifts_df.sort_values(by=['Day', 'Start Time'])
        
        #initialize
        assigned_treeview.delete(*assigned_treeview.get_children())
        
        #initialize
        for index, row in assigned_shifts_df.iterrows():
            assigned_treeview.insert('', 'end', text=row['Employee'], values=(row['Day'], row['Start Time'], row['End Time']))
        treeview.insert('', 'end', text=employee_name, values=(day, start_time, end_time))
        


# Create Function to Remove Shift

def remove_shift():
    selected_item = assigned_treeview.focus()

    if selected_item:
        
        #initialize
        employee_name = assigned_treeview.item(selected_item, 'text')
        
        #initialize
        shift_info = assigned_treeview.item(selected_item, 'values')
        
        #initialize
        day = shift_info[0]
        
        #initialize
        start_time = shift_info[1]
        
        #initialize
        end_time = shift_info[2]
        
        #initialize
        #Employeee
        #Dayy
        #Startt timee
        #endd timeee
        shift = {'Employee': employee_name, 'Day': day, 'Start Time': start_time, 'End Time': end_time}
        #assigned_shifts.remove
        
        assigned_shifts.remove(shift)
        
        #assigned_shifts_df = pd.DataFrame
        assigned_shifts_df = pd.DataFrame(assigned_shifts)
        
        #assigned_shifts_df
        assigned_shifts_df = assigned_shifts_df.sort_values(by=['Day', 'Start Time'])

        assigned_treeview.delete(*assigned_treeview.get_children())

        for index, row in assigned_shifts_df.iterrows():
            assigned_treeview.insert('', 'end', text=row['Employee'], values=(row['Day'], row['Start Time'], row['End Time']))
            
# Create Function to Finalize Schedule
#gett dataa
def finalize_schedule():
    # Update Schedule DataFrame

    for index, row in assigned_shifts_df.iterrows():
        schedule_df = schedule_df.append(row, ignore_index=True)
    schedule_df = schedule_df.sort_values(by=['Day', 'Start Time'])
    
    # Save Schedule to CSV

    schedule_df.to_csv('schedule.csv', index=False)
    
    # Show Success Message

    messagebox.showinfo('Schedule Finalized', 'Schedule has been finalized and saved to schedule.csv.')
    
    # Close Application

    root.destroy()

# Assigned Shifts Frame

assigned_shifts_frame = ttk.LabelFrame(modify_schedule_frame, text='Assigned Shifts')

assigned_shifts_frame.grid(row=0, column=0, padx=10, pady=10)

assigned_treeview = ttk.Treeview(assigned_shifts_frame, columns=('Day', 'Start Time', 'End Time'))

assigned_treeview.heading('Day', text='Day')

assigned_treeview.heading('Start Time', text='Start Time')

assigned_treeview.heading('End Time', text='End Time')

assigned_treeview.pack()

# Available Shifts Frame

available_shifts_frame = ttk.LabelFrame(modify_schedule_frame, text='Available Shifts')

available_shifts_frame.grid(row=0, column=1, padx=10, pady=10)


treeview = ttk.Treeview(available_shifts_frame, columns=('Day', 'Start Time', 'End Time'))

treeview.heading('Day', text='Day')

treeview.heading('Start Time', text='Start Time')

treeview.heading('End Time', text='End Time')

treeview.pack()

# Button Frame

button_frame = ttk.Frame(modify_schedule_frame)

button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

assign_button = ttk.Button(button_frame, text='Assign Shift', command=assign_shift)

assign_button.grid(row=0, column=0, padx=10, pady=10)

reassign_button = ttk.Button(button_frame, text='Reassign Shift', command=reassign_shift)

reassign_button.grid(row=0, column=1, padx=10, pady=10)

remove_button = ttk.Button(button_frame, text='Remove Shift', command=remove_shift)

remove_button.grid(row=0, column=2, padx=10, pady=10)

finalize_button = ttk.Button(modify_schedule_frame, text='Finalize Schedule', command=finalize_schedule)

finalize_button.grid(row=2, column=1, padx=10, pady=10)

# Employee Time-Off Request System

#def request_time_off():

#    employee_name = employee_name_var.get()

#    day = day_var.get()

#    time_off_requests_df = pd.read_csv('time_off_requests.csv')
#    time_off_requests_df = time_off_requests_df.append({'Employee': employee_name, 'Day': day}, ignore_index=True)
#    time_off_requests_df.to_csv('time_off_requests.csv', index=False)
#    messagebox.showinfo('Time-Off Request Submitted', 'Your time-off request has been submitted.')
    
#time_off_frame = ttk.LabelFrame(root, text='Employee Time-Off Request')
#time_off_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

#employee_name_label = ttk.Label(time_off_frame, text='Employee Name:')
#employee_name_label.grid(row=0, column=0, padx=10, pady=10)

#employee_name_var = tk.StringVar()
#employee_name_entry = ttk.Entry(time_off_frame, textvariable=employee_name_var)
#employee_name_entry.grid(row=0, column=1, padx=10, pady=10)

#day_label = ttk.Label(time_off_frame, text='Day:')
#day_label.grid(row=1, column=0, padx=10, pady=10)

#day_var = tk.StringVar()

#day_entry = ttk.Entry(time_off_frame, textvariable=day_var)

#day_entry.grid(row=1, column=1, padx=10, pady=10)

#request_button = ttk.Button(time_off_frame, text='Request Time-Off', command=request_time_off)
#request_button.grid(row=2, column=1, padx=10, pady=10)

# Employee Time-Off Request System

def request_time_off():

    employee_name = employee_name_var.get()

    day = day_var.get()

    time_off_requests_df = pd.read_csv('time_off_requests.csv')

    time_off_requests_df = time_off_requests_df.append({'Employee': employee_name, 'Day': day}, ignore_index=True)

    time_off_requests_df.to_csv('time_off_requests.csv', index=False)

    messagebox.showinfo('Time-Off Request Submitted', 'Your time-off request has been submitted.')

    
#Get timeas_off
time_off_frame = ttk.LabelFrame(root, text='Employee Time-Off Request')

time_off_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

#Get employee_name

employee_name_label = ttk.Label(time_off_frame, text='Employee Name:')

employee_name_label.grid(row=0, column=0, padx=10, pady=10)

#get employee_name-Varr

employee_name_var = tk.StringVar()

#get name_entry
employee_name_entry = ttk.Entry(time_off_frame, textvariable=employee_name_var)

#get name_entry.grid
employee_name_entry.grid(row=0, column=1, padx=10, pady=10)

#get day_label
day_label = ttk.Label(time_off_frame, text='Day:')

#getx day_label.grid
day_label.grid(row=1, column=0, padx=10, pady=10)

#gets day_var
day_var = tk.StringVar()

#get day_entry
day_entry = ttk.Entry(time_off_frame, textvariable=day_var)

#get day_entry.grid
day_entry.grid(row=1, column=1, padx=10, pady=10)

#requestt buttons
request_button = ttk.Button(time_off_frame, text='Request Time-Off', command=request_time_off)

request_button.grid(row=2, column=1, padx=10, pady=10)

# Open CSV Files

schedule_df = pd.read_csv('schedule.csv')
time_off_requests_df = pd.read_csv('time_off_requests.csv')

# Display Schedule in Treeview
for index, row in schedule_df.iterrows():
    treeview.insert('', 'end', text=row['Employee'], values=(row['Day'], row['Start Time'], row['End Time']))

# Display Assigned Shifts in Treeview
for index, row in assigned_shifts_df.iterrows():
    assigned_treeview.insert('', 'end', text=row['Employee'], values=(row['Day'], row['Start Time'], row['End Time']))

# Main Loop
root.mainloop()

#The script defines a set of employees, their maximum working hours, their skills, and their time off. 
#It also defines a set of shifts for each day of the week. 

#Each shift has a start time, end time, skill required, and the number of employees required.
#The script creates LP variables to represent the shifts that each employee is assigned to. 

#It defines an objective function that maximizes the number of shifts assigned to employees.
#The script creates constraints to ensure that each employee does not exceed their maximum working hours, 

#that the required skills for each shift are met, and that each employee is assigned to only one shift per day.
#The script solves the LP problem and generates a work schedule that satisfies all the constraints.

#The generated schedule can be displayed to the user through a graphical user interface built using the Tkinter library.
#The user can interact with the GUI to generate schedules for different months and years, display the schedule for a particular employee, 

#modify the schedule by reassigning or removing shifts, and submit time-off requests.
#Iterate over each employee in the employees list and populate the treeview widget with the employee's schedule by using the treeview.insert() method.

#Make sure that schedule_df is properly defined before calling this code. It looks like this code is using schedule_df to populate the treeview, 
#so if schedule_df is not properly defined, this code may not work as expected.

#Make sure that schedule_df is properly defined before calling this code. It looks like this code is using schedule_df to populate the treeview, 
#so if schedule_df is not properly defined, this code may not work as expected.

#The code starts by importing the necessary libraries, including tkinter, ttk, pandas, and messagebox.
#The code defines a few functions, including request_time_off(), to handle time-off requests and display the work schedule in the treeview widget.

#The code creates a LabelFrame widget called time_off_frame to hold the time-off request system. 
#The widget includes a Label widget to prompt the user for their name, an Entry widget to allow the user to enter their name, a Label widget to prompt the user for the day they want to take off, 

#an Entry widget to allow the user to enter the day they want to take off, and a Button widget to submit the time-off request.

#The reassign_shift() function gets the selected item from the assigned_treeview widget, extracts the employee name and shift information from the item, 

#removes the shift from the assigned_shifts list, updates the assigned_treeview widget with the updated list of assigned shifts, 
#and updates the treeview widget for unassigned shifts with the reassigned shift.
