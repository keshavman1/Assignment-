import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware is added to the FastAPI app to allow cross-origin requests. 
# This is particularly useful when the backend and frontend are served from different domains or ports during development. 
# Here, it is configured to allow all origins, methods, headers, and credentials for development purposes. In production, 
# it's recommended to limit the allowed origins for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development purposes, modify in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers in requests
)

# In-memory database, represented by a dictionary `students` to store the student data, and a set `emails` 
# to track unique email addresses for students. This allows the app to perform CRUD operations on student records 
# while ensuring uniqueness of student IDs and emails.
students = {}
emails = set()

# Ollama API URL and model settings are defined to interface with the Ollama API, 
# which will be used to generate summaries for students. This is done by calling a helper function that interacts 
# with the API to get summaries based on student details.
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

# A Pydantic model `Student` is created to define the structure of the student data. 
# This model enforces validation rules for the incoming data, such as checking the type and format of fields like `id`, 
# `name`, `age`, and `email`.
class Student(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr

# A helper function `get_ollama_summary` is defined to interact with the Ollama API. 
# It sends a request with a dynamically constructed prompt containing the student's details to generate a summary.
# The function handles the response from the API, streaming it in chunks and accumulating the content to build the final summary.
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
                    return output

        return "Response still being processed."

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error generating summary"
    except ValueError as ve:
        print(f"JSON Parsing Error: {ve}")
        return "Error parsing response"

# The FastAPI app defines several CRUD (Create, Read, Update, Delete) routes for managing student records.

# The `create_student` route allows the creation of a new student by checking whether the student ID 
# and email already exist in the database. If they do, a 400 error is raised.
@app.post("/students")
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    
    if student.email in emails:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")
    
    students[student.id] = student
    emails.add(student.email)
    return student

# The `get_all_students` route retrieves all students stored in the database.
@app.get("/students")
def get_all_students():
    return list(students.values())

# The `get_student` route fetches a student by their ID. If the student doesn't exist, 
# a 404 error is raised.
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students[student_id]

# The `update_student` route updates an existing student's information. 
# It checks that the student exists, and if the email is updated, ensures it is unique.
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    if updated_student.email != students[student_id].email:
        if updated_student.email in emails:
            raise HTTPException(status_code=400, detail="Email already in use.")
    
    students[student_id] = updated_student
    return updated_student

# The `delete_student` route removes a student from the database. 
# It ensures the student exists, deletes their email from the set, 
# and removes their record from the `students` dictionary.
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    emails.remove(students[student_id].email)
    del students[student_id]
    return {"detail": "Student deleted successfully"}

# The `generate_summary` route generates a summary for a specific student using the Ollama API. 
# If the student is not found, a 404 error is raised. The summary is returned as part of the response.
@app.get("/students/{student_id}/summary")
def generate_summary(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    student = students[student_id]
    summary = get_ollama_summary(student)
    return {"summary": summary}
