# FealtyX - Student Management System with AI Summaries

FealtyX is an application built using FastAPI and Streamlit, integrated with Ollama’s AI technology to provide AI-based summaries of student information. The platform allows administrators to manage student data through a simple interface and generate detailed summaries using an AI model.

# Key-Features
Student Data Management: Easily add, view, update, and delete student records.

AI-Powered Summaries: Use Ollama’s Llama model to generate insightful, AI-based summaries from student information.

Streamlit Frontend: Interactive user interface for managing student data and viewing summaries.

Backend Utility Scripts: Includes Python scripts for handling data, server interaction, and AI processing.


## Create a Virtual Environment
```bash
python -m venv env
```

## Activate the Virtual Environment:

```bash
.\env\Scripts\activate

```


## Installation
Clone the repository and install the following dependencies:

```bash
pip install fastapi uvicorn requests pydantic pandas
```

##INSTALL Streamlit
```bash
pip install streamlit
```
## Running the project

Start the Ollama Llama Model: First, launch the Ollama AI model by running:
```bash
ollama run llama3.2
```

Start the FastAPI backend:
```python
uvicorn main:app --reload
```
Run the Streamlit frontend:
```python
streamlit run app.py
```
Open the Streamlit app in your browser (typically available at http://localhost:8501).

## Usage
Create a New Student: Fill out the form with student details (ID, Name, Age, Email) to create a new student.

Update a Student: Modify the details of an existing student by providing the student ID and the new details.

Delete a Student: Provide the student ID to remove a student from the system.

Generate Summary: For each student, generate an AI-powered summary using Ollama.


## Images front end
