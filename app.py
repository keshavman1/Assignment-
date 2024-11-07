import streamlit as st
import pandas as pd
import requests

# Define the FastAPI base URL for API requests
API_URL = "http://127.0.0.1:8000"

# Function to display the list of students in a table
def display_students():
    try:
        # Fetch all students from the FastAPI endpoint
        response = requests.get(f"{API_URL}/students")
        
        # If the request is successful, display the students in a table
        if response.status_code == 200:
            students = response.json()
            df = pd.DataFrame(students)  # Convert the list of students to a DataFrame
            
            # Check if the DataFrame is not empty
            if not df.empty:
                st.table(df)  # Display students in a table format
            else:
                st.write("No students found.")  # If no students, show a message
        else:
            st.error("Failed to fetch students. Status Code: {}".format(response.status_code))
    
    except requests.exceptions.RequestException as e:
        # Catch any request-related errors
        st.error(f"Error fetching data: {e}")

# Function to create a new student
def create_student(id, name, age, email):
    try:
        # Send a POST request to the FastAPI endpoint to create a new student
        response = requests.post(
            f"{API_URL}/students",
            json={"id": id, "name": name, "age": age, "email": email},
        )
        
        # Check if the student was created successfully
        if response.status_code == 200:
            st.success("Student created successfully!")
        else:
            st.error("Failed to create student. Status Code: {}".format(response.status_code))
    
    except requests.exceptions.RequestException as e:
        # Catch any request-related errors
        st.error(f"Error creating student: {e}")

# Function to update an existing student's details
def update_student(id, name, age, email):
    try:
        # Send a PUT request to the FastAPI endpoint to update the student information
        response = requests.put(
            f"{API_URL}/students/{id}",
            json={"id": id, "name": name, "age": age, "email": email},
        )
        
        # Check if the student was updated successfully
        if response.status_code == 200:
            st.success("Student updated successfully!")
        else:
            st.error("Failed to update student. Status Code: {}".format(response.status_code))
    
    except requests.exceptions.RequestException as e:
        # Catch any request-related errors
        st.error(f"Error updating student: {e}")

# Function to delete a student
def delete_student(id):
    try:
        # Send a DELETE request to the FastAPI endpoint to remove a student
        response = requests.delete(f"{API_URL}/students/{id}")
        
        # Check if the student was deleted successfully
        if response.status_code == 200:
            st.success("Student deleted successfully!")
        else:
            st.error("Failed to delete student. Status Code: {}".format(response.status_code))
    
    except requests.exceptions.RequestException as e:
        # Catch any request-related errors
        st.error(f"Error deleting student: {e}")

# Function to generate a summary for a student
def generate_summary(id):
    try:
        # Send a GET request to fetch the student summary
        response = requests.get(f"{API_URL}/students/{id}/summary")
        
        # Check if the summary was successfully generated
        if response.status_code == 200:
            summary = response.json().get("summary", "No summary available.")
            st.info(f"Summary for Student {id}: {summary}")
        else:
            st.error("Failed to generate summary. Status Code: {}".format(response.status_code))
    
    except requests.exceptions.RequestException as e:
        # Catch any request-related errors
        st.error(f"Error generating summary: {e}")

# Streamlit app layout setup
st.title("Student Management System")

# Display the list of students
st.header("Student List")
if st.button("Refresh Student List"):
    display_students()

# Create a new student
st.header("Create a New Student")
with st.form("create_form"):
    id = st.number_input("ID", min_value=1, step=1)  # Input for student ID
    name = st.text_input("Name")  # Input for student name
    age = st.number_input("Age", min_value=1, step=1)  # Input for student age
    email = st.text_input("Email")  # Input for student email
    submitted = st.form_submit_button("Create Student")
    if submitted:
        create_student(id, name, age, email)
        display_students()  # Refresh the list after creating a student

# Update an existing student's information
st.header("Update a Student")
with st.form("update_form"):
    update_id = st.number_input("Student ID to Update", min_value=1, step=1)  # Student ID to update
    update_name = st.text_input("New Name")  # New student name
    update_age = st.number_input("New Age", min_value=1, step=1)  # New student age
    update_email = st.text_input("New Email")  # New student email
    update_submitted = st.form_submit_button("Update Student")
    if update_submitted:
        update_student(update_id, update_name, update_age, update_email)
        display_students()  # Refresh the list after updating a student

# Delete a student
st.header("Delete a Student")
delete_id = st.number_input("Student ID to Delete", min_value=1, step=1)  # ID of the student to delete
if st.button("Delete Student"):
    delete_student(delete_id)
    display_students()  # Refresh the list after deleting a student

# Generate a summary for a student
st.header("Generate Student Summary")
summary_id = st.number_input("Student ID for Summary", min_value=1, step=1)  # ID of the student for summary
if st.button("Generate Summary"):
    generate_summary(summary_id)
