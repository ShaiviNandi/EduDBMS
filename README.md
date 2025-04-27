# Computer Coaching Center Management System

## Project Overview
This project provides a comprehensive management system for computer coaching centers. It allows for the management of students, faculty, courses, and cohorts (batches) through a menu-driven interface connected to a MySQL database.

## Author
Shaivi Nandi, Class 12 A, Meridian School Madhapur

## Features
- **Student Management**: Register, update, delete, and search for student records
- **Faculty Management**: Add and delete faculty records
- **Course Management**: Add new courses and update course details
- **Cohort Management**: Create cohorts for courses, assign students to cohorts, search available cohorts, and mark cohorts as complete

## System Requirements
- Python 3.x
- MySQL database server
- mysql-connector-python package

## Database Structure
The system uses a MySQL database named `computerinstitute` with the following tables:
- `student`: Stores student information
- `faculty`: Stores faculty information
- `course`: Stores course details
- `cohort`: Stores batch/cohort information
- `studentcohort`: Junction table that connects students with cohorts

The database also includes the following views:
- `studentcoursecohortfaculty`: Combines data from student, cohort, course, and faculty tables
- `coursecohort`: Shows available course cohorts

## Installation and Setup

### 1. Database Setup
Run the SQL script `SQLTableCreate.sql` to create the database structure:
```bash
mysql -u root -p < SQLTableCreate.sql
```

### 2. Python Dependencies
Install the required Python package:
```bash
pip install mysql-connector-python
```

### 3. Configure Database Connection
Update the database connection details in `projectfunctions.py` if needed:
```python
def connecttodb():
  mydb = mysql.connector.connect(
    host="localhost",
    user="appuser",  # Update if needed
    password="appuser",  # Update if needed
    database="computerinstitute"
  )
  return mydb
```

## Usage
Run the main program file to start the application:
```bash
python startproject.py
```

### Navigation
The system provides a menu-driven interface. Use the numeric options to navigate:
1. Maintain student record
2. Maintain faculty record
3. Maintain courses
4. Maintain cohort
10. Exit

Each option leads to sub-menus with more specific operations.

## File Structure
- `startproject.py`: Main program file with the user interface and program flow
- `projectfunctions.py`: Contains all functions used by the main program
- `SQLTableCreate.sql`: SQL scripts to create the necessary database objects

## Function Reference

### Key Functions in projectfunctions.py:
- `prepmenu()`: Displays menu options and gets user choice
- `buildSQL()`: Builds SQL statements based on input parameters
- `connecttodb()`: Establishes database connection
- `registerstudent()`: Adds a new student to the database
- `unregisterstudent()`: Deletes a student record
- `searchanddisplayrecord()`: Searches and displays records
- `updaterecord()`: Updates database records
- `registercohort()`: Creates a new cohort/batch
- `assignstudentcohort()`: Assigns a student to a cohort

## Error Handling
The system includes error handling for:
- Type errors
- SQL programming errors
- Data integrity errors
- Data format errors
