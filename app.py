import streamlit as st
import pandas as pd
import requests

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000"

# Function to display the list of students in a table format
def display_students():
    """
    Fetches student data from the FastAPI backend and displays it in a table.
    If no data is returned, shows a message indicating that no students were found.
    """
    # Sending GET request to fetch the list of students
    response = requests.get(f"{API_URL}/students")
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response JSON into a list of students
        students = response.json()
        
        # Convert the list of students into a pandas DataFrame for better readability
        df = pd.DataFrame(students)
        
        # Check if the DataFrame is empty and display the appropriate message
        if not df.empty:
            # Display the student data in a table format
            st.table(df)
        else:
            st.write("No students found.")
    else:
        # Handle the case when the API call fails
        st.error("Failed to fetch students.")

# Function to create a new student by sending data to the API
def create_student(id, name, age, email):
    """
    Sends a POST request to create a new student in the backend.
    Displays a success or error message based on the response.
    """
    # Prepare the student data in JSON format
    student_data = {"id": id, "name": name, "age": age, "email": email}
    
    # Sending POST request to create a new student
    response = requests.post(f"{API_URL}/students", json=student_data)
    
    # Check if the student was created successfully
    if response.status_code == 200:
        st.success("Student created successfully!")
    else:
        # Handle failure case
        st.error("Failed to create student.")

# Function to update an existing student's details
def update_student(id, name, age, email):
    """
    Sends a PUT request to update the details of an existing student.
    Displays a success or error message based on the response.
    """
    # Prepare the updated student data in JSON format
    updated_data = {"id": id, "name": name, "age": age, "email": email}
    
    # Sending PUT request to update the student information
    response = requests.put(f"{API_URL}/students/{id}", json=updated_data)
    
    # Check if the student information was updated successfully
    if response.status_code == 200:
        st.success("Student updated successfully!")
    else:
        # Handle failure case
        st.error("Failed to update student.")

# Function to delete a student based on the student ID
def delete_student(id):
    """
    Sends a DELETE request to remove a student from the backend.
    Displays a success or error message based on the response.
    """
    # Sending DELETE request to delete a student
    response = requests.delete(f"{API_URL}/students/{id}")
    
    # Check if the student was deleted successfully
    if response.status_code == 200:
        st.success("Student deleted successfully!")
    else:
        # Handle failure case
        st.error("Failed to delete student.")

# Function to generate a summary for a specific student
def generate_summary(id):
    """
    Sends a GET request to fetch a student's summary from the backend.
    Displays the summary or an error message based on the response.
    """
    # Sending GET request to fetch the student's summary
    response = requests.get(f"{API_URL}/students/{id}/summary")
    
    # Check if the summary was fetched successfully
    if response.status_code == 200:
        # Retrieve the summary from the response
        summary = response.json().get("summary", "No summary available.")
        st.info(f"Summary for Student {id}: {summary}")
    else:
        # Handle failure case
        st.error("Failed to generate summary.")

# Streamlit app layout and user interface design

# Title of the app
st.title("Student Management System")

# Display Students Section
st.header("Student List")
if st.button("Refresh Student List"):
    # Refresh the student list by calling the function to display students
    display_students()

# Create Student Section
st.header("Create a New Student")
with st.form("create_form"):
    # Form fields for creating a new student
    id = st.number_input("ID", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    email = st.text_input("Email")
    
    # Form submission button
    submitted = st.form_submit_button("Create Student")
    
    # If the form is submitted, call the function to create a student
    if submitted:
        create_student(id, name, age, email)
        # Refresh the student list after creation
        display_students()

# Update Student Section
st.header("Update a Student")
with st.form("update_form"):
    # Form fields for updating an existing student's details
    update_id = st.number_input("Student ID to Update", min_value=1, step=1)
    update_name = st.text_input("New Name")
    update_age = st.number_input("New Age", min_value=1, step=1)
    update_email = st.text_input("New Email")
    
    # Form submission button
    update_submitted = st.form_submit_button("Update Student")
    
    # If the form is submitted, call the function to update the student
    if update_submitted:
        update_student(update_id, update_name, update_age, update_email)
        # Refresh the student list after updating
        display_students()

# Delete Student Section
st.header("Delete a Student")
delete_id = st.number_input("Student ID to Delete", min_value=1, step=1)
if st.button("Delete Student"):
    # Call the function to delete a student
    delete_student(delete_id)
    # Refresh the student list after deletion
    display_students()

# Generate Summary Section
st.header("Generate Student Summary")
summary_id = st.number_input("Student ID for Summary", min_value=1, step=1)
if st.button("Generate Summary"):
    # Call the function to generate and display the student's summary
    generate_summary(summary_id)
