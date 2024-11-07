import streamlit as st
import pandas as pd
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000"

# Display students in a table
def display_students():
    response = requests.get(f"{API_URL}/students")
    if response.status_code == 200:
        students = response.json()
        df = pd.DataFrame(students)
        if not df.empty:
            st.table(df)
        else:
            st.write("No students found.")
    else:
        st.error("Failed to fetch students.")

# Create a new student
def create_student(id, name, age, email):
    response = requests.post(
        f"{API_URL}/students",
        json={"id": id, "name": name, "age": age, "email": email},
    )
    if response.status_code == 200:
        st.success("Student created successfully!")
    else:
        st.error("Failed to create student.")

# Update a student
def update_student(id, name, age, email):
    response = requests.put(
        f"{API_URL}/students/{id}",
        json={"id": id, "name": name, "age": age, "email": email},
    )
    if response.status_code == 200:
        st.success("Student updated successfully!")
    else:
        st.error("Failed to update student.")

# Delete a student
def delete_student(id):
    response = requests.delete(f"{API_URL}/students/{id}")
    if response.status_code == 200:
        st.success("Student deleted successfully!")
    else:
        st.error("Failed to delete student.")

# Generate student summary
def generate_summary(id):
    response = requests.get(f"{API_URL}/students/{id}/summary")
    if response.status_code == 200:
        summary = response.json().get("summary", "No summary available.")
        st.info(f"Summary for Student {id}: {summary}")
    else:
        st.error("Failed to generate summary.")

# Streamlit app layout
st.title("Student Management System")

# Display Students
st.header("Student List")
if st.button("Refresh Student List"):
    display_students()

# Create Student
st.header("Create a New Student")
with st.form("create_form"):
    id = st.number_input("ID", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    email = st.text_input("Email")
    submitted = st.form_submit_button("Create Student")
    if submitted:
        create_student(id, name, age, email)
        display_students()

# Update Student
st.header("Update a Student")
with st.form("update_form"):
    update_id = st.number_input("Student ID to Update", min_value=1, step=1)
    update_name = st.text_input("New Name")
    update_age = st.number_input("New Age", min_value=1, step=1)
    update_email = st.text_input("New Email")
    update_submitted = st.form_submit_button("Update Student")
    if update_submitted:
        update_student(update_id, update_name, update_age, update_email)
        display_students()

# Delete Student
st.header("Delete a Student")
delete_id = st.number_input("Student ID to Delete", min_value=1, step=1)
if st.button("Delete Student"):
    delete_student(delete_id)
    display_students()

# Generate Summary
st.header("Generate Student Summary")
summary_id = st.number_input("Student ID for Summary", min_value=1, step=1)
if st.button("Generate Summary"):
    generate_summary(summary_id)