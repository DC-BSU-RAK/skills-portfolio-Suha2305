import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import csv

# SECTION 1: CONFIGURATION AND CONSTANTS
BG_LIGHT_BLUE = "#DBF2FF" # background color 
BTN_DARK_BLUE = "#43728F" # sidebar buttons
TEXT_WHITE = "white" # text color for dark buttons
SIDEBAR_BG = "white" # sidebar background       
BTN_SAVE_NEW = "#00D91F" # green for Add and Save button
BTN_DELETE = "#D9002B"    # red 

# SECTION 2: STUDENT CLASS DATA MODEL AND CALCULATIONS
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        # data storage
        self.code = int(code)
        self.name = name
        self.c1 = int(c1) # coursework 1 mark (max 20)
        self.c2 = int(c2) # coursework 2 mark (max 20)
        self.c3 = int(c3) # coursework 3 mark (max 20)
        self.exam = int(exam) # exam mark (max 100)
        
        # calculated Metrics
        self.total_coursework = self.c1 + self.c2 + self.c3 # max 60
        self.total_possible = 160 # total possible marks (60 CW + 100 Exam)
        
        # calculate overall percentage
        self.overall_percent = round(((self.total_coursework + self.exam) / self.total_possible) * 100, 2)
        
        # to determine the final grade
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        p = self.overall_percent
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"

    def get_summary(self):
        return f"Name: {self.name}\n" \
               f"Code: {self.code}\n" \
               f"Coursework: {self.total_coursework} / 60\n" \
               f"Exam: {self.exam} / 100\n" \
               f"Overall %: {self.overall_percent}%\n" \
               f"Grade: {self.grade}\n"

    def get_row_data(self):
        return (
            self.code,
            self.name,
            self.total_coursework,
            self.exam,
            self.overall_percent,
            self.grade
        )

# SECTION 3: DATA HANDLING
def load_students(file_path="studentMarks.txt"):
    students = []
    try:
        with open(file_path, "r") as f:
            f.readline() # skip the student count line written by save_students()
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 6:
                        try:
                            students.append(Student(*parts))
                        except ValueError:
                            continue
    except FileNotFoundError: # If the file doesn't exist yet, start with an empty list
        pass
    return students

def save_students(file_path="studentMarks.txt"):
    with open(file_path, "w", newline="") as f:
        # write student count as the first line
        f.write(f"{len(students)}\n")
        # write the raw data for recreation upon next load
        for s in students:
            f.write(f"{s.code},{s.name},{s.c1},{s.c2},{s.c3},{s.exam}\n")

# initialize the master list of students 
students = load_students()

# SECTION 4: GUI SETUP
root = tk.Tk()
root.title("Student Manager")
root.geometry("900x600")
root.resizable(False, False) # stops window resizing

# sidebar frame 
sidebar = tk.Frame(root, width=220, bg=SIDEBAR_BG) 
sidebar.pack(side="left", fill="y")
title_label = tk.Label(sidebar, text="STUDENT MANAGER",
                       font=("Times New Roman", 16, "bold"), bg=SIDEBAR_BG) 
title_label.pack(pady=20)

def add_button(text, command):
    btn = tk.Button(sidebar, text=text, command=command,
                    font=("Times New Roman", 12), width=20, height=1,
                    bg=BTN_DARK_BLUE, fg=TEXT_WHITE)
    btn.pack(pady=8)
    return btn

# output frame container
output_container = tk.Frame(root, bg=BG_LIGHT_BLUE)
output_container.pack(side="right", fill="both", expand=True)

# output window components
output_label = tk.Label(output_container, font=("Times New Roman", 18, "bold"), bg=BG_LIGHT_BLUE)
output_label.pack(pady=10)

# scrollable Text widget for summaries, individual views, and errors
text_frame = tk.Frame(output_container)
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")
output_text = tk.Text(text_frame, wrap="word", font=("Times New Roman", 12))
output_text.pack(fill="both", expand=True)
output_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)

# treeview components (used for table mode)
treeview_frame = tk.Frame(output_container, padx=10, pady=10)
tree_cols = ("Code", "Name", "CW Total", "Exam", "Overall %", "Grade")
# the main table widget for displaying lists of students
student_table = ttk.Treeview(treeview_frame, columns=tree_cols, show='headings')

# configure treeview styling to use the custom font
style = ttk.Style()
style.configure("Treeview.Heading", font=("Times New Roman", 12, 'bold'))
style.configure("Treeview", font=("Times New Roman", 12))

# configure column names and widths
for col in tree_cols:
    student_table.heading(col, text=col)
    student_table.column(col, anchor='center', width=100 if col != "Name" else 150)
    
tree_scrollbar = tk.Scrollbar(treeview_frame, orient="vertical", command=student_table.yview)
student_table.configure(yscrollcommand=tree_scrollbar.set)
tree_scrollbar.pack(side="right", fill="y")
student_table.pack(fill="both", expand=True)

# Form Components
form_frame = tk.Frame(output_container, bg=BG_LIGHT_BLUE, padx=20, pady=20)
form_fields = {} # Dictionary to dynamically store references to Entry widgets (e.g., form_fields['name'])
dynamic_button_frame = tk.Frame(output_container, bg=BG_LIGHT_BLUE) # Used for multi-step input like Sort

# SECTION 5: MODE SWITCHING FUNCTIONS
def show_output_mode(title="Output Window"):
    # hide all competing dynamic frames
    form_frame.pack_forget()
    dynamic_button_frame.pack_forget()
    treeview_frame.pack_forget() 
    
    output_label.config(text=title)
    output_label.pack(pady=10)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)
    output_text.delete("1.0", "end") 

def show_table_mode(title="Student Records"):
    # hide all competing dynamic frames
    form_frame.pack_forget()
    dynamic_button_frame.pack_forget()
    text_frame.pack_forget() 

    output_label.config(text=title)
    output_label.pack(pady=10)
    treeview_frame.pack(fill="both", expand=True)
    
    # clear previous rows from the table
    for item in student_table.get_children():
        student_table.delete(item)
    
    # ensure any previous summary labels are removed
    if hasattr(root, 'summary_label'):
        root.summary_label.pack_forget()


def show_form_mode(title):
    # hide all competing dynamic frames
    text_frame.pack_forget()
    dynamic_button_frame.pack_forget()
    treeview_frame.pack_forget() 
    
    output_label.config(text=title)
    output_label.pack(pady=10)
    
    # destroy all widgets currently in the form_frame to prepare for a new form layout
    for widget in form_frame.winfo_children():
        widget.destroy()
        
    form_frame.pack(fill="both", expand=True)
    form_fields.clear() # Clears the dictionary that holds entry references

# SECTION 6: CORE DISPLAY LOGIC (VIEW ALL, MIN/MAX, SORT)
def view_all_students():
    show_table_mode(title="All Student Records (Overall Percentage)")
    
    if not students:
        show_output_mode(title="All Students")
        output_text.insert("end", "No student records found.")
        return

    total_percent_sum = 0
    for s in students:
        # insert each student's data into the table
        student_table.insert('', tk.END, values=s.get_row_data())
        total_percent_sum += s.overall_percent
        
    avg_percent = round(total_percent_sum / len(students), 2)
    
    summary_message = f"Number of students: {len(students)} | Average overall %: {avg_percent}%"
    
    # create or update the persistent summary label below the table view
    if not hasattr(root, 'summary_label'):
        # initial creation
        root.summary_label = tk.Label(treeview_frame, text=summary_message, font=("Times New Roman", 12), bg=BG_LIGHT_BLUE, anchor="w")
        root.summary_label.pack(fill="x", pady=(5, 0))
    else:
        # update existing label text and ensure it's visible
        root.summary_label.config(text=summary_message, font=("Times New Roman", 12), bg=BG_LIGHT_BLUE)
        root.summary_label.pack(fill="x", pady=(5, 0))


def highest_score():
    if not students:
        show_output_mode(title="Highest Score")
        output_text.insert("end", "No records to analyze.")
        return
        
    # use the max function with a lambda key to efficiently find the student object
    best = max(students, key=lambda x: x.overall_percent)
    
    show_table_mode(title="Student with Highest Overall Score")
    # insert the best record and apply a background tag for visual emphasis
    student_table.insert('', tk.END, values=best.get_row_data(), tags=('highlight',))
    student_table.tag_configure('highlight', background='#fff9e0', font=('Times New Roman', 11, 'bold'))


def lowest_score():
    if not students:
        show_output_mode(title="Lowest Score")
        output_text.insert("end", "No records to analyze.")
        return
        
    # use the min function with a lambda key
    worst = min(students, key=lambda x: x.overall_percent)
    
    show_table_mode(title="Student with Lowest Overall Score")
    # insert the worst record and apply a different background tag for visual emphasis
    student_table.insert('', tk.END, values=worst.get_row_data(), tags=('highlight',))
    student_table.tag_configure('highlight', background='#ffe0e0', font=('Times New Roman', 11, 'bold'))

# SORT FUNCTION LOGIC
def display_sorted_records(is_descending):
    
    if not students:
        show_output_mode(title="Sort Records")
        output_text.insert("end", "No records to sort.")
        return
        
    # python's built in sorted() function is used for sorting based on the key
    sorted_students = sorted(students, key=lambda x: x.overall_percent, reverse=is_descending)
    
    show_table_mode(title=f"Sorted Records ({'Descending' if is_descending else 'Ascending'})")
    
    # repopulate the table with the sorted list
    total_percent_sum = 0
    for s in sorted_students:
        student_table.insert('', tk.END, values=s.get_row_data())
        total_percent_sum += s.overall_percent
        
    avg_percent = round(total_percent_sum / len(students), 2)
    summary_message = f"Number of students: {len(students)} | Average overall %: {avg_percent}%"
    
    # update the summary label below the table
    if not hasattr(root, 'summary_label'):
        root.summary_label = tk.Label(treeview_frame, text=summary_message, font=("Times New Roman", 12), bg=BG_LIGHT_BLUE, anchor="w")
        root.summary_label.pack(fill="x", pady=(5, 0))
    else:
        root.summary_label.config(text=summary_message, font=("Times New Roman", 12), bg=BG_LIGHT_BLUE)
        root.summary_label.pack(fill="x", pady=(5, 0))


def sort_records():
    # switch to the dynamic button mode
    text_frame.pack_forget()
    form_frame.pack_forget() 
    treeview_frame.pack_forget() 
    output_label.config(text="Select Sort Order")
    output_label.pack(pady=10)
    
    # clear previous buttons from the dynamic frame
    for widget in dynamic_button_frame.winfo_children():
        widget.destroy()

    # create buttons, each calling display_sorted_records with the correct boolean flag
    desc_btn = tk.Button(dynamic_button_frame, text="Highest to Lowest (Descending)", 
                         command=lambda: display_sorted_records(True),
                         font=("Times New Roman", 12), bg=BTN_DARK_BLUE, fg=TEXT_WHITE, width=30, height=2)
    desc_btn.pack(pady=10)

    asc_btn = tk.Button(dynamic_button_frame, text="Lowest to Highest (Ascending)", 
                         command=lambda: display_sorted_records(False),
                         font=("Times New Roman", 12), bg=BTN_DARK_BLUE, fg=TEXT_WHITE, width=30, height=2)
    asc_btn.pack(pady=10)
    
    dynamic_button_frame.pack(fill="x", padx=150, pady=50)


# SECTION 7: DYNAMIC FORM LOGIC 
def create_input_fields(parent_frame, fields_list, initial_values=None):
    if initial_values is None: initial_values = {}
    row_num = 1
    for label_text, key, readonly in fields_list:
        # label setup
        label = tk.Label(parent_frame, text=label_text, anchor="w", 
                         font=("Times New Roman", 12), bg=BG_LIGHT_BLUE)
        label.grid(row=row_num, column=0, padx=10, pady=5, sticky="w")
        
        # entry field setup
        entry = tk.Entry(parent_frame, font=("Times New Roman", 12), width=30)
        entry.insert(0, initial_values.get(key, ""))
        entry.config(state="readonly" if readonly else "normal") # Set state for fields like student code
        entry.grid(row=row_num, column=1, padx=10, pady=5, sticky="ew")
        form_fields[key] = entry # Store reference
        row_num += 1

# logic for View One Student
def show_view_one_form():
    show_form_mode(title="View Individual Student")
    
    # code input widget setup
    code_entry = tk.Entry(form_frame, font=("Times New Roman", 12), width=20)
    code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def fetch_and_display():
        try:
            code = int(code_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid student code. Must be an integer.")
            return

        # linear search for the student object
        student_found = next((s for s in students if s.code == code), None)
        
        # cleanup: Remove previous displayed summary details 
        for widget in form_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) >= 2:
                widget.destroy()

        if student_found:
            # display detailed summary using labels
            tk.Label(form_frame, text="Student Details:", font=("Times New Roman", 14, "bold"), bg=BG_LIGHT_BLUE).grid(row=2, column=0, columnspan=2, pady=10)
            details = student_found.get_summary().split('\n')
            for i, line in enumerate(details):
                tk.Label(form_frame, text=line, anchor="w", justify="left", bg=BG_LIGHT_BLUE, font=("Times New Roman", 12)).grid(row=i + 3, column=0, columnspan=2, sticky="w", padx=10)
        else:
            tk.Label(form_frame, text=f"No student found with code {code}", fg="red", bg=BG_LIGHT_BLUE, font=("Times New Roman", 12)).grid(row=2, column=0, columnspan=2, pady=10)

    # label for code input
    code_label = tk.Label(form_frame, text="Enter Student Code:", font=("Times New Roman", 12), bg=BG_LIGHT_BLUE)
    code_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    # button to trigger the search logic
    fetch_btn = tk.Button(form_frame, text="Find Student", command=fetch_and_display, 
                          bg=BTN_DARK_BLUE, fg=TEXT_WHITE, font=("Times New Roman", 12))
    fetch_btn.grid(row=0, column=2, padx=10, pady=10)
    
# logic for Add Student
def add_student():
    show_form_mode(title="Add New Student Record")
    
    fields = [
        ("Student Code (1000-9999):", "code", False),
        ("Student Name:", "name", False),
        ("Coursework 1 (0-20):", "c1", False),
        ("Coursework 2 (0-20):", "c2", False),
        ("Coursework 3 (0-20):", "c3", False),
        ("Exam Mark (0-100):", "exam", False)
    ]
    create_input_fields(form_frame, fields)

    def submit_add():
        try:
            # retrieve data from entry fields
            code = int(form_fields["code"].get())
            name = form_fields["name"].get().strip()
            c1 = int(form_fields["c1"].get())
            c2 = int(form_fields["c2"].get())
            c3 = int(form_fields["c3"].get())
            exam = int(form_fields["exam"].get())
        except ValueError:
            messagebox.showerror("Error", "All code and marks must be valid integers.")
            return

        # comprehensive validation checks
        if any(s.code == code for s in students):
            messagebox.showerror("Error", f"Student code {code} already exists.")
            return
        if not (1000 <= code <= 9999) or not name or \
           not all(0 <= mark <= 20 for mark in [c1, c2, c3]) or \
           not 0 <= exam <= 100:
            messagebox.showerror("Error", "Invalid input: Check code range (1000-9999) or mark ranges (CW: 0-20, Exam: 0-100).")
            return

        # create new student object, append to list, and save to file
        students.append(Student(code, name, c1, c2, c3, exam))
        save_students()
        
        # clear form fields for next entry
        for entry in form_fields.values():
            entry.delete(0, tk.END)
            
        show_output_mode(title="Student Added")
        output_text.insert("end", f"Student {name} (Code: {code}) added and file saved!")

    # submit button
    submit_btn = tk.Button(form_frame, text=" Save New Student", 
                           command=submit_add,
                           font=("Times New Roman", 14, "bold"), bg=BTN_SAVE_NEW, fg="black")
    submit_btn.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

# logic for Delete Student
def delete_student():
    show_form_mode(title=" Delete Student Record")
    
    # input widget for the code to delete
    code_entry = tk.Entry(form_frame, font=("Times New Roman", 12), width=20)
    code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def submit_delete():
        try:
            code_to_delete = int(code_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid student code.")
            return

        # find the student object
        student_to_delete = next((s for s in students if s.code == code_to_delete), None)
        
        if student_to_delete:
            # use messagebox for critical confirmation step
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {student_to_delete.name} (Code: {code_to_delete})?"):
                students.remove(student_to_delete)
                save_students()
                show_output_mode(title="Deletion Successful")
                output_text.insert("end", f"Student {student_to_delete.name} deleted successfully!")
            else:
                show_output_mode(title="Deletion Cancelled")
                output_text.insert("end", "Deletion cancelled by user.")
        else:
            messagebox.showerror("Error", f"Student not found with code {code_to_delete}!")
            
    # delete button
    delete_btn = tk.Button(form_frame, text=" Delete Record", command=submit_delete, 
                           font=("Times New Roman", 12, "bold"), bg=BTN_DELETE, fg="white") 
    delete_btn.grid(row=0, column=2, padx=10, pady=10)

# logic for Update Student
current_student_to_update = None # global variable used to hold the student object between update steps

def show_update_form_step_2(student):
    global current_student_to_update
    current_student_to_update = student
    
    # clear step 1 widgets and title
    for widget in form_frame.winfo_children():
        widget.destroy()
        
    # title showing which record is being updated
    tk.Label(form_frame, text=f"Updating Record for: {student.name} (Code: {student.code})", 
             font=("Times New Roman", 14, "bold"), bg=BG_LIGHT_BLUE).grid(row=0, column=0, columnspan=2, pady=10)

    # configuration for editable fields (Code is excluded)
    fields = [
        ("Student Name:", "name", False),
        ("Coursework 1 (0-20):", "c1", False),
        ("Coursework 2 (0-20):", "c2", False),
        ("Coursework 3 (0-20):", "c3", False),
        ("Exam Mark (0-100):", "exam", False)
    ]
    
    # populate initial values for the form
    initial_values = {
        "name": student.name,
        "c1": str(student.c1),
        "c2": str(student.c2),
        "c3": str(student.c3),
        "exam": str(student.exam)
    }
    create_input_fields(form_frame, fields, initial_values)
    
    # final button
    update_btn = tk.Button(form_frame, text=" Apply Updates", command=submit_update, 
                           font=("Times New Roman", 14, "bold"), bg="#00b894", fg="black")
    update_btn.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)


def submit_update():
    global current_student_to_update
    s = current_student_to_update # reference to the object being modified
    
    try:
        # retrieve updated data
        new_name = form_fields["name"].get().strip()
        new_c1 = int(form_fields["c1"].get())
        new_c2 = int(form_fields["c2"].get())
        new_c3 = int(form_fields["c3"].get())
        new_exam = int(form_fields["exam"].get())
    except ValueError:
        messagebox.showerror("Error", "Marks must be valid integers.")
        return
        
    # Validation checks
    if not new_name:
        messagebox.showerror("Error", "Student name cannot be empty.")
        return
    if not all(0 <= mark <= 20 for mark in [new_c1, new_c2, new_c3]) or not 0 <= new_exam <= 100:
        messagebox.showerror("Error", "One or more entered marks are out of range.")
        return

    # apply changes to the object
    s.name = new_name
    s.c1 = new_c1
    s.c2 = new_c2
    s.c3 = new_c3
    s.exam = new_exam
    
    # crucially, recalculate derived properties
    s.total_coursework = s.c1 + s.c2 + s.c3
    s.overall_percent = round(((s.total_coursework + s.exam) / s.total_possible) * 100, 2)
    s.grade = s.calculate_grade()
    
    save_students()
    current_student_to_update = None # reset reference
    
    show_output_mode(title="Update Successful")
    output_text.insert("end", f"Student {s.name} updated and file saved!")


def update_student():
    show_form_mode(title=" Update Student Record (Step 1)")
    
    # input widget for the code to find
    code_entry = tk.Entry(form_frame, font=("Times New Roman", 12), width=20)
    code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def find_student_for_update():
        try:
            code_to_find = int(code_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid student code.")
            return

        student_found = next((s for s in students if s.code == code_to_find), None)
        
        if student_found:
            show_update_form_step_2(student_found) # Transition to the editing form
        else:
            messagebox.showerror("Error", f"Student not found with code {code_to_find}!")
            
    # button to find the student
    find_btn = tk.Button(form_frame, text="Find and Load", command=find_student_for_update, 
                         bg=BTN_DARK_BLUE, fg=TEXT_WHITE, font=("Times New Roman", 12))
    find_btn.grid(row=0, column=2, padx=10, pady=10)

# SECTION 8: BUTTON MAPPING AND EXECUTION
add_button("View ALL Students", view_all_students)
add_button("View ONE Student", show_view_one_form)
add_button("Highest Score", highest_score)
add_button("Lowest Score", lowest_score)
add_button("Sort Records", sort_records)
add_button("Add Student", add_student)
add_button("Delete Student", delete_student)
add_button("Update Student", update_student)

# set the initial view when the application loads
view_all_students()

# start the Tkinter event loop - this keeps the window open and listening for events
root.mainloop() 