import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Initialize FastAPI application
app = FastAPI()

# Setup Cross-Origin Resource Sharing (CORS) to allow frontend (e.g., Streamlit) access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# In-memory database for storing student data
students = {}  # Dictionary to store student details with ID as key
emails = set()  # Set to keep track of unique emails to prevent duplicates

# Ollama API Configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # URL for Ollama API
OLLAMA_MODEL = "llama3.2"  # Model version for Ollama API

# Student Pydantic model to validate input data
class Student(BaseModel):
    id: int  # Unique identifier for the student
    name: str  # Name of the student
    age: int  # Age of the student
    email: EmailStr  # Email of the student (validated as a valid email)

# Function to generate a student summary using Ollama's Llama model
def get_ollama_summary(student: Student) -> str:
    """
    This function sends a request to Ollama's API to generate a summary 
    of the student based on their name, age, and email.

    Args:
    - student: A Student object containing student details.

    Returns:
    - A string containing the generated summary.
    """
    # Define prompt for Ollama model to summarize the student's information
    prompt = f"Generate a summary for a student. Name: {student.name}, Age: {student.age}, Email: {student.email}. Provide a description of the student and any interesting traits."

    # Payload to be sent to Ollama's API
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # Use streaming to receive data progressively
    }

    # Headers for the request
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Sending POST request to Ollama API to generate summary
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for invalid responses

        output = ""  # To accumulate the response content

        # Iterate over the streamed response
        for line in response.iter_lines():
            if line:
                # Decode and parse the JSON response from Ollama
                body = json.loads(line.decode('utf-8'))

                # If there is an error in the response, raise an exception
                if "error" in body:
                    raise Exception(body["error"])

                # Append the content of the message to output
                if not body.get("done", False):
                    message = body.get("message", "")
                    content = message.get("content", "")
                    output += content

                # Return the output when the stream is complete
                if body.get("done", False):
                    return output

        return "Response still being processed."  # In case the response is still streaming

    except requests.exceptions.RequestException as e:
        # Catch any error that occurs during the request
        print(f"Error: {e}")
        return "Error generating summary"

    except ValueError as ve:
        # Handle potential JSON parsing errors
        print(f"JSON Parsing Error: {ve}")
        return "Error parsing response"

# CRUD Operations for managing students
@app.post("/students")
def create_student(student: Student):
    """
    Create a new student record. Ensures that the student ID and email are unique.

    Args:
    - student: A Student object with student details.

    Returns:
    - The newly created student record.
    """
    # Check if student ID already exists in the database
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    
    # Check if student email already exists in the system
    if student.email in emails:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")
    
    # Add student record to the in-memory database
    students[student.id] = student
    emails.add(student.email)  # Track email to ensure uniqueness
    return student

@app.get("/students")
def get_all_students():
    """
    Retrieve a list of all students.

    Returns:
    - List of all student records.
    """
    return list(students.values())

@app.get("/students/{student_id}")
def get_student(student_id: int):
    """
    Retrieve a specific student record by ID.

    Args:
    - student_id: The ID of the student to fetch.

    Returns:
    - The student record if found.
    """
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    """
    Update the details of an existing student. Ensures the email is unique if updated.

    Args:
    - student_id: The ID of the student to update.
    - updated_student: The updated student details.

    Returns:
    - The updated student record.
    """
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Check if the new email is unique, if it's being updated
    if updated_student.email != students[student_id].email:
        if updated_student.email in emails:
            raise HTTPException(status_code=400, detail="Email already in use.")
    
    # Update the student's record
    students[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    Delete a student record by ID.

    Args:
    - student_id: The ID of the student to delete.

    Returns:
    - Confirmation of deletion.
    """
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Remove email from the set before deleting the student
    emails.remove(students[student_id].email)
    
    # Delete the student record
    del students[student_id]
    return {"detail": "Student deleted successfully"}

# Endpoint to generate a summary for a specific student
@app.get("/students/{student_id}/summary")
def generate_summary(student_id: int):
    """
    Generate a summary of a student using the Ollama API.

    Args:
    - student_id: The ID of the student to generate a summary for.

    Returns:
    - The summary generated by Ollama.
    """
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    student = students[student_id]
    
    # Call Ollama to generate the student summary
    summary = get_ollama_summary(student)
    
    return {"summary": summary}
