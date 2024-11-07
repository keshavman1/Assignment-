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

## Install Streamlit
```bash
pip install streamlit
```
## Running the project

Start the Ollama Llama Model: First, launch the Ollama AI model by running:
```bash
ollama run llama3.2
```

Launch the FastAPI Backend: Start the FastAPI backend with this command:
```python
uvicorn main:app --reload
```
Start the Streamlit Frontend: To launch the Streamlit UI, run:
```python
streamlit run app.py
```
Open the Streamlit app in your browser (typically available at http://localhost:8501).

## Usage
Application Features
Create a New Student: Add a student by entering their unique details (ID, Name, Age, Email).

Update Existing Student: Modify an existing student's information by providing their ID and the updated details.

Delete Student: Remove a student's record by their unique student ID.



