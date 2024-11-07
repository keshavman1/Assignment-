import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Initialize FastAPI app
app = FastAPI()

# CORS middleware configuration to allow cross-origin requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# In-memory data structure to store student information
students = {}
emails = set()  # A set to track unique student emails

# Ollama API configurations
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ollama API endpoint URL
OLLAMA_MODEL = "llama3.2"  # Model name for Ollama's AI chatbot

# Pydantic model for student data validation
class Student(BaseModel):
    id: int  # Unique identifier for the student
    name: str  # Name of the student
    age: int  # Age of the student
    email: EmailStr  # Email of the student (validated as proper email format)

# Helper function to generate a student summary using Ollama's Llama model
def get_ollama_summary(student: Student) -> str:
    # Constructing a prompt to ask Ollama to generate a description of the student
    prompt = f"Generate a summary for a student. Name: {student.name}, Age: {student.age}, Email: {student.email}. Provide a description of the student and any interesting traits."

    # Setting up the payload for the API request to Ollama
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],  # Message content for Ollama
        "stream": True  # Enable streaming response for real-time results
    }

    headers = {
        'Content-Type': 'application/json',  # Content type for the API request
    }

    try:
        # Sending the POST request to Ollama API to get the summary
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error if the response code is not successful

        print(f"Response Status Code: {response.status_code}")  # Debugging output
        output = ""

        # Iterating through the response lines to process the streamed data
        for line in response.iter_lines():
            if line:
                body = json.loads(line.decode('utf-8'))  # Decode the JSON data from the line

                # Check for any errors in the response from Ollama
                if "error" in body:
                    raise Exception(body["error"])

                # Accumulate the content of the message (real-time data stream)
                if not body.get("done", False):
                    message = body.get("message", "")
                    content = message.get("content", "")
                    output += content

                # Once the response is finished, return the accumulated summary
                if body.get("done", False):
                    return output

        return "Response still being processed."  # If response is still being streamed

    except requests.exceptions.RequestException as e:
        # Handle errors in making the request (network issues, etc.)
        print(f"Error: {e}")
        return "Error generating summary"
    except ValueError as ve:
        # Handle any JSON parsing errors
        print(f"JSON Parsing Error: {ve}")
        return "Error parsing response"

# CRUD operations for student management (Create, Read, Update, Delete)

# Create a new student
@app.post("/students")
def create_student(student: Student):
    # Check if the student already exists using the unique student ID
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    
    # Check if the student's email already exists
    if student.email in emails:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")
    
    # Add student to the in-memory database
    students[student.id] = student
    emails.add(student.email)  # Add email to the set to ensure uniqueness
    return student

# Get details of all students
@app.get("/students")
def get_all_students():
    return list(students.values())  # Return all students as a list

# Get details of a specific student by their unique ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    # If the student does not exist, raise a 404 error
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students[student_id]

# Update a student's details (given their ID)
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    # If the student does not exist, raise a 404 error
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Check if the updated email is unique before changing
    if updated_student.email != students[student_id].email:
        if updated_student.email in emails:
            raise HTTPException(status_code=400, detail="Email already in use.")
    
    # Update the student's details in the database
    students[student_id] = updated_student
    return updated_student

# Delete a student by their unique ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    # If the student does not exist, raise a 404 error
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Remove the student's email from the email set
    emails.remove(students[student_id].email)
    
    # Remove the student from the database
    del students[student_id]
    return {"detail": "Student deleted successfully"}

# Generate a summary for a specific student using the Ollama model
@app.get("/students/{student_id}/summary")
def generate_summary(student_id: int):
    # If the student does not exist, raise a 404 error
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    student = students[student_id]  # Get the student from the database
    
    # Call the Ollama API to generate the summary
    summary = get_ollama_summary(student)
    
    return {"summary": summary}  # Return the generated summary
