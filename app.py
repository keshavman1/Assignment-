import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

# Initialize session state for created_students if not already initialized
if "created_students" not in st.session_state:
    st.session_state["created_students"] = {}

st.markdown("""
    <style>
        /* Set the background color to black for the entire app */
        body {
            background-color: #000000;
            color: white;
        }

        /* Header styling */
        h1, h2, h3 {
            color: #003366;  /* Dark blue for headings */
            text-align: center;  /* Center the headers */
        }

        /* Style the header of the app */
        .stApp {
            background-color: #000000;
        }

        /* Modern box-style for sections */
        .section-box {
            background-color: #262730;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        /* Style the select box with dark background */
        .stSelectbox select {
            background-color: #333333;
            color: white;
            border-radius: 5px;
            padding: 10px;
            border: none;
        }

        /* Style text input fields */
        .stTextInput input, .stNumberInput input {
            background-color: #333333;
            color: white;
            border-radius: 5px;
            padding: 10px;
            border: none;
        }

        /* Style the buttons */
        .stButton > button {
            background-color: #008CBA;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 12px 24px;
            border: none;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #005f75;  /* Darker cyan on hover */
        }

        /* Styling for the sidebar */
        .sidebar .sidebar-content {
            background-color: #000000;
            color: white;
        }

        /* Add padding to markdown components */
        .stMarkdown {
            padding: 10px;
        }

        /* Style for the table */
        .stTable {
            color: white;
            background-color: #2b2b2b;
            border-radius: 8px;
            border-collapse: collapse;
            width: 100%;
        }

        .stTable th, .stTable td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #444;
        }

        .stTable th {
            background-color: #333333;
            color: #ffffff;
            font-weight: bold;
        }

        .stTable tr:nth-child(even) {
            background-color: #3a3a3a;
        }

        /* Style for input labels */
        .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
            color: #ffffff;
            font-weight: bold;
        }

        /* Custom style for success messages to ensure text is visible */
        .stSuccess {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


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
        # Store the created student in session state
        st.session_state["created_students"][id] = {"id": id, "name": name, "age": age, "email": email}
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
st.title("Education Management System")

# Display Students
st.header("Data Of Students")
if st.button("Refresh Data"):
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

# Get User by ID
st.header("Get User by ID")
if st.session_state.get("created_students", {}):
    ids = list(st.session_state["created_students"].keys())
    selected_id = st.selectbox("Select Student ID", ids)
    if st.button("Fetch User"):
        student = st.session_state["created_students"].get(selected_id)
        if student:
            st.write("Student Information:")
            st.json(student)
else:
    st.write("No students created in this session.")

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
