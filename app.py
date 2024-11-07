import streamlit as st
import pandas as pd
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000"

# Function to show the list of students
def show_students():
    response = requests.get(f"{API_URL}/students")
    if response.status_code == 200:
        students_data = response.json()
        df = pd.DataFrame(students_data)
        if not df.empty:
            st.table(df)
        else:
            st.write("No students available.")
    else:
        st.error("Unable to fetch student data.")

# Function to add a new student
def add_student(id, name, age, email):
    response = requests.post(
        f"{API_URL}/students",
        json={"id": id, "name": name, "age": age, "email": email},
    )
    if response.status_code == 200:
        st.success("Student added successfully!")
    else:
        st.error("Error adding student.")

# Function to modify an existing student's details
def modify_student(id, name, age, email):
    response = requests.put(
        f"{API_URL}/students/{id}",
        json={"id": id, "name": name, "age": age, "email": email},
    )
    if response.status_code == 200:
        st.success("Student details updated successfully!")
    else:
        st.error("Error updating student details.")

# Function to remove a student
def remove_student(id):
    response = requests.delete(f"{API_URL}/students/{id}")
    if response.status_code == 200:
        st.success("Student deleted successfully!")
    else:
        st.error("Error deleting student.")

# Function to fetch the student's summary
def get_student_summary(id):
    response = requests.get(f"{API_URL}/students/{id}/summary")
    if response.status_code == 200:
        summary_data = response.json().get("summary", "No summary available.")
        st.info(f"Summary for Student {id}: {summary_data}")
    else:
        st.error("Unable to generate summary.")

# Streamlit app interface
st.title("Student Management System")

# Show Students Section
st.header("List of Students")
if st.button("Refresh List"):
    show_students()

# Add New Student Section
st.header("Add a New Student")
with st.form("add_student_form"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    student_name = st.text_input("Full Name")
    student_age = st.number_input("Age", min_value=1, step=1)
    student_email = st.text_input("Email Address")
    submitted = st.form_submit_button("Add Student")
    if submitted:
        add_student(student_id, student_name, student_age, student_email)
        show_students()

# Modify Student Details Section
st.header("Modify Student Details")
with st.form("modify_student_form"):
    modify_id = st.number_input("Student ID to Modify", min_value=1, step=1)
    modify_name = st.text_input("New Name")
    modify_age = st.number_input("New Age", min_value=1, step=1)
    modify_email = st.text_input("New Email")
    modify_submitted = st.form_submit_button("Update Student")
    if modify_submitted:
        modify_student(modify_id, modify_name, modify_age, modify_email)
        show_students()

# Remove Student Section
st.header("Remove a Student")
student_to_delete = st.number_input("Student ID to Remove", min_value=1, step=1)
if st.button("Remove Student"):
    remove_student(student_to_delete)
    show_students()

# Generate Student Summary Section
st.header("Student Summary")
summary_for_student = st.number_input("Enter Student ID for Summary", min_value=1, step=1)
if st.button("Get Summary"):
    get_student_summary(summary_for_student)
