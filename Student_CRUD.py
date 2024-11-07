import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI()

# CORS setup for cross-origin access from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for students
students = {}
emails = set()  # To keep track of unique emails

# Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api/chat" 
OLLAMA_MODEL = "llama3.2" 

# Student model
class Student(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr

# Helper function to generate summary using Ollama Llama
def get_ollama_summary(student: Student) -> str:
    prompt = f"Generate a summary for a student. Name: {student.name}, Age: {student.age}, Email: {student.email}. Provide a description of the student and any interesting traits."

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, stream=True)
        response.raise_for_status() 
        
        print(f"Response Status Code: {response.status_code}")
        output = ""
        
        for line in response.iter_lines():
            if line:
                body = json.loads(line.decode('utf-8'))

                if "error" in body:
                    raise Exception(body["error"])

                if not body.get("done", False):
                    message = body.get("message", "")
                    content = message.get("content", "")
                    output += content

                if body.get("done", False):
                    return output  # Return the accumulated response

        return "Response still being processed."

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error generating summary"
    except ValueError as ve:
        print(f"JSON Parsing Error: {ve}")
        return "Error parsing response"

# CRUD Operations
@app.post("/students")
def create_student(student: Student):
    # Check if student ID already exists
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    
    # Check if student email already exists
    if student.email in emails:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")
    
    # Add student to the in-memory database
    students[student.id] = student
    emails.add(student.email)  # Add email to the set for unique check
    return student

@app.get("/students")
def get_all_students():
    return list(students.values())

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # If email is updated, check if it is unique
    if updated_student.email != students[student_id].email:
        if updated_student.email in emails:
            raise HTTPException(status_code=400, detail="Email already in use.")
    
    # Update the student information
    students[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Remove email from the set
    emails.remove(students[student_id].email)
    
    # Delete student
    del students[student_id]
    return {"detail": "Student deleted successfully"}

# Generate summary using Ollama's Llama model
@app.get("/students/{student_id}/summary")
def generate_summary(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    student = students[student_id]
    
    # Call Ollama to generate the summary
    summary = get_ollama_summary(student)
    
    return {"summary": summary}