# FealtyX - Student Management System with AI Summaries

FealtyX is an application built using FastAPI and Streamlit, integrated with Ollama’s AI technology to provide AI-based summaries of student information. The platform allows administrators to manage student data through a simple interface and generate detailed summaries using an AI model.

# Key-Features
Student Data Management: Easily add, view, update, and delete student records.

AI-Powered Summaries: Use Ollama’s Llama model to generate insightful, AI-based summaries from student information.

Streamlit Frontend: Interactive user interface for managing student data and viewing summaries.

Backend Utility Scripts: Includes Python scripts for handling data, server interaction, and AI processing.

## Installation
Clone the repository and install the following dependencies:


## Create a Virtual Environment
```bash
python -m venv env
```

## Activate the Virtual Environment:

```bash
.\env\Scripts\activate

```
## Install uvicorn and dependencies within the virtual environment:

```bash
pip install uvicorn fastapi requests pydantic pandas

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
If u get problem in launching uvicorn then 

```bash
pip install pydantic[email]

```

After that, try running your uvicorn command again:

```bash
uvicorn main:app --reload

```

Start the Streamlit Frontend: To launch the Streamlit UI, run:

```python
streamlit run app.py
```

## Run all three applications—Ollama, Streamlit, and Uvicorn—in three different CMD terminals.

## Application Features

Add a New Student: Complete the form by entering the student's details, including their unique ID, full name, age, and email address, to successfully register a new student in the system.

Edit an Existing Student's Information: Update the details of a student by providing their unique student ID and the new or corrected information, ensuring that the student's record is accurately reflected in the system.

Remove a Student from the System: To permanently delete a student's record, simply provide the student's ID, and the system will remove all associated information from the database.

Generate an AI-Powered Summary for Each Student: Utilize the power of Ollama’s AI technology to automatically generate insightful and personalized summaries for each student based on their records and history, offering valuable insights into their performance and background.