import tkinter as tk
from tkinter import messagebox
import cx_Oracle

# Replace with your Oracle connection details
connection = cx_Oracle.connect("system/Admin123#@localhost/XE")

# Function to insert a new student record
def insert_student():
    try:
        cursor = connection.cursor()
        query = "INSERT INTO student (S_NO, S_NAME, S_CLASS, S_CONTACT, S_ADD) VALUES (:id, :name, :class, :contact, :address)"
        values = {
            'id': int(id_entry.get()),  # Add the student ID from the input field
            'name': name_entry.get(),
            'class': class_entry.get(),
            'contact': contact_entry.get(),
            'address': address_entry.get()
        }
        cursor.execute(query, values)
        connection.commit()
        clear_entries()
        messagebox.showinfo("Insert", "Student record inserted successfully!")
    except cx_Oracle.Error as e:
        messagebox.showerror("Error", str(e))

# Function to retrieve and display all student records
def display_students():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")
        records = cursor.fetchall()
        display_text.config(state=tk.NORMAL)
        display_text.delete(1.0, tk.END)
        for record in records:
            display_text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Class: {record[2]}, Contact: {record[3]}, Address: {record[4]}\n")
        display_text.config(state=tk.DISABLED)
    except cx_Oracle.Error as e:
        messagebox.showerror("Error", str(e))

# Function to delete a student record
def delete_student():
    try:
        cursor = connection.cursor()
        student_id = int(delete_id_entry.get())
        query = "DELETE FROM student WHERE S_NO = :id"
        cursor.execute(query, {'id': student_id})
        connection.commit()
        messagebox.showinfo("Delete", "Student record deleted successfully!")
        display_students()  # Refresh the displayed records
    except cx_Oracle.Error as e:
        messagebox.showerror("Error", str(e))




# Function to update a student record
def update_student():
    try:
        cursor = connection.cursor()
        student_id = int(update_id_entry.get())
        query = "UPDATE student SET S_NAME = :name, S_CLASS = :class, S_CONTACT = :contact, S_ADD = :address WHERE S_NO = :id"
        values = {
            'name': update_name_entry.get(),
            'class': update_class_entry.get(),
            'contact': update_contact_entry.get(),
            'address': update_address_entry.get(),
            'id': student_id
        }
        cursor.execute(query, values)
        connection.commit()
        clear_entries()
        messagebox.showinfo("Update", "Student record updated successfully!")
        display_students()  # Refresh the displayed records
    except cx_Oracle.DatabaseError as e:
        if e.args[0].code == -20001:
            messagebox.showerror("Update", e.args[0].message)
        else:
            messagebox.showerror("Error", str(e))




# Function to search for a student record by ID
def search_student():
    try:
        cursor = connection.cursor()
        student_id = int(search_id_entry.get())
        query = "SELECT * FROM student WHERE S_NO = :id"
        cursor.execute(query, {'id': student_id})
        record = cursor.fetchone()
        display_text.config(state=tk.NORMAL)
        display_text.delete(1.0, tk.END)
        if record:
            display_text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Class: {record[2]}, Contact: {record[3]}, Address: {record[4]}\n")
        else:
            messagebox.showinfo("Search", "Student record not found.")
        display_text.config(state=tk.DISABLED)
    except cx_Oracle.Error as e:
        messagebox.showerror("Error", str(e))

# Function to calculate pending fees for a student
def calculate_pending_fees():
    try:
        cursor = connection.cursor()

     
        student_id = int(procedure_student_id_entry.get())

        # Create an OUT parameter to capture the pending fees
        pending_fees = cursor.var(cx_Oracle.NUMBER)

        # Call the procedure to calculate pending fees
        cursor.callproc("CALCULATE_PENDING_FEES", [student_id, pending_fees])

        # Fetch the result from the OUT parameter
        pending_fees_value = pending_fees.getvalue()

        if pending_fees_value is not None:
            messagebox.showinfo("Pending Fees", f"Pending Fees: {pending_fees_value}")
        else:
            messagebox.showinfo("Pending Fees", "No pending fees found.")

    except cx_Oracle.Error as e:
        messagebox.showerror("Error", str(e))

# Function to check staff schedule and display the day
def get_staff_schedule():
    staff_id = int(function_staff_id_entry.get())
    try:
        cursor = connection.cursor()

        # Call the PL/SQL function
        result = cursor.callfunc("GET_STAFF_SCHEDULE", cx_Oracle.STRING, [staff_id])

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Staff with ID {staff_id} has the following schedule: {result}\n")
        result_text.config(state=tk.DISABLED)

        cursor.close()
    except cx_Oracle.Error as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Database Error: {e}\n")
        result_text.config(state=tk.DISABLED)

# Function to clear input entries
def clear_entries():
    name_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Coaching Institute Database")

# Styling
root.configure(bg="black")  # Set the main background color

# Add a heading label
heading_label = tk.Label(root, text="Coaching Institute Database", font=("Arial", 16, "bold"), bg="black", fg="yellow")
heading_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create and grid labels and input entries for student details
id_label = tk.Label(root, text="Id:", bg="black", fg="yellow")
id_label.grid(row=1, column=0, padx=10, pady=5)
id_entry = tk.Entry(root)
id_entry.grid(row=1, column=1, padx=10, pady=5)

name_label = tk.Label(root, text="Name:", bg="black", fg="yellow")
name_label.grid(row=2, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=2, column=1, padx=10, pady=5)

class_label = tk.Label(root, text="Class:", bg="black", fg="yellow")
class_label.grid(row=3, column=0, padx=10, pady=5)
class_entry = tk.Entry(root)
class_entry.grid(row=3, column=1, padx=10, pady=5)

contact_label = tk.Label(root, text="Contact:", bg="black", fg="yellow")
contact_label.grid(row=4, column=0, padx=10, pady=5)
contact_entry = tk.Entry(root)
contact_entry.grid(row=4, column=1, padx=10, pady=5)

address_label = tk.Label(root, text="Address:", bg="black", fg="yellow")
address_label.grid(row=5, column=0, padx=10, pady=5)
address_entry = tk.Entry(root)
address_entry.grid(row=5, column=1, padx=10, pady=5)

# Create and grid a text box to display records
display_text = tk.Text(root, height=9, width=52, state=tk.DISABLED)
display_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Buttons for student management
insert_button = tk.Button(root, text="Insert Student Record", command=insert_student, bg="white", fg="black")
insert_button.grid(row=7, column=0, padx=10, pady=5)

display_button = tk.Button(root, text="Display Student Records", command=display_students, bg="white", fg="black")
display_button.grid(row=7, column=1, padx=10, pady=5)

delete_label = tk.Label(root, text="Enter Student ID to Delete:", bg="black", fg="yellow")
delete_label.grid(row=8, column=0, padx=10, pady=5)
delete_id_entry = tk.Entry(root)
delete_id_entry.grid(row=8, column=1, padx=10, pady=5)

delete_button = tk.Button(root, text="Delete Student Record", command=delete_student, bg="white", fg="black")
delete_button.grid(row=9, column=0, padx=10, pady=5)

# Right side: Update Student Record Section
update_label = tk.Label(root, text="Update Student Record", font=("Arial", 14, "bold"), bg="black", fg="yellow")
update_label.grid(row=1, column=2, padx=10, pady=5, columnspan=2)

update_id_label = tk.Label(root, text="Enter Student ID:", bg="black", fg="yellow")
update_id_label.grid(row=2, column=2, padx=10, pady=5)
update_id_entry = tk.Entry(root)
update_id_entry.grid(row=2, column=3, padx=10, pady=5)

update_name_label = tk.Label(root, text="Name:", bg="black", fg="yellow")
update_name_label.grid(row=3, column=2, padx=10, pady=5)
update_name_entry = tk.Entry(root)
update_name_entry.grid(row=3, column=3, padx=10, pady=5)

update_class_label = tk.Label(root, text="Class:", bg="black", fg="yellow")
update_class_label.grid(row=4, column=2, padx=10, pady=5)
update_class_entry = tk.Entry(root)
update_class_entry.grid(row=4, column=3, padx=10, pady=5)

update_contact_label = tk.Label(root, text="Contact:", bg="black", fg="yellow")
update_contact_label.grid(row=5, column=2, padx=10, pady=5)
update_contact_entry = tk.Entry(root)
update_contact_entry.grid(row=5, column=3, padx=10, pady=5)

update_address_label = tk.Label(root, text="Address:", bg="black", fg="yellow")
update_address_label.grid(row=6, column=2, padx=10, pady=5)
update_address_entry = tk.Entry(root)
update_address_entry.grid(row=6, column=3, padx=10, pady=5)

update_button = tk.Button(root, text="Update Student Record", command=update_student, bg="white", fg="black")
update_button.grid(row=7, column=2, padx=10, pady=5, columnspan=2)

# Create and grid a label and entry for searching by Student ID
search_label = tk.Label(root, text="Enter Student ID to Search:", bg="black", fg="yellow")
search_label.grid(row=10, column=0, padx=10, pady=5)
search_id_entry = tk.Entry(root)
search_id_entry.grid(row=10, column=1, padx=10, pady=5)

# Create a button to trigger the student search operation
search_button = tk.Button(root, text="Search Student by ID", command=search_student, bg="white", fg="black")
search_button.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

# Procedure: Calculate Total Pending Fees
procedure_label = tk.Label(root, text="Calculate Total Pending Fees:", font=("Arial", 12, "bold"), bg="black", fg="yellow")
procedure_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

procedure_student_id_label = tk.Label(root, text="Enter Student ID:", bg="black", fg="yellow")
procedure_student_id_label.grid(row=13, column=0, padx=10, pady=5)
procedure_student_id_entry = tk.Entry(root)
procedure_student_id_entry.grid(row=13, column=1, padx=10, pady=5)
calculate_procedure_button = tk.Button(root, text="Calculate Pending Fees", command=calculate_pending_fees, bg="white", fg="black")
calculate_procedure_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

# Function: Check Staff Schedule
function_label = tk.Label(root, text="Check Staff Schedule:", font=("Arial", 12, "bold"), bg="black", fg="yellow")
function_label.grid(row=15, column=0, columnspan=2, padx=10, pady=10)

function_staff_id_label = tk.Label(root, text="Enter Staff ID:", bg="black", fg="yellow")
function_staff_id_label.grid(row=16, column=0, padx=10, pady=5)
function_staff_id_entry = tk.Entry(root)
function_staff_id_entry.grid(row=16, column=1, padx=10, pady=5)

# Create a button to check staff schedule
check_button = tk.Button(root, text="Check Schedule", command=get_staff_schedule, bg="white", fg="black")
check_button.grid(row=17, column=0, columnspan=2, padx=10, pady=5)

result_text = tk.Text(root, height=5, width=52, state=tk.DISABLED)
result_text.grid(row=18, column=0, columnspan=2, padx=10, pady=10)

# Close the database connection when the GUI is closed
def on_closing():
    connection.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI application
root.mainloop()
