# Career Guidance System

A Django web application that helps students with career and education decisions.

Students can take tests, find suitable courses and colleges, apply for colleges and jobs, prepare for interviews, and communicate with mentors.

## Features

### Student

* Register and login
* Manage profile
* Search colleges and courses
* Filter courses by GPA and duration
* Take career tests
* Check eligible courses and colleges
* Apply to colleges
* Apply for jobs and upload resumes
* View interview preparation materials
* Chat with mentors

### College

* Register and manage profile
* Add and manage courses
* Manage mentors
* View students
* Manage applications

### Mentor

* Login
* Add interview preparation materials
* Upload PDF resources
* Communicate with students

### Admin

* Manage students and colleges
* Approve or reject colleges
* Manage test questions
* Manage job vacancies
* View applications and test results

## Main Workflow

```text
Student
   ↓
Career Test
   ↓
Test Result
   ↓
Eligible Courses
   ↓
Colleges
   ↓
College Application
   ↓
Job Applications
   ↓
Interview Preparation
   ↓
Mentor Communication
```

## Technology

* Python
* Django
* SQLite
* HTML
* CSS
* JavaScript
* Bootstrap

## Project Structure

```text
Career-Guidance/
├── manage.py
├── project/
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
├── media/
├── static/
└── README.md
```

## Installation

```bash
git clone <your-repository-url>
cd Career-Guidance

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`

## Database

The project uses Django ORM with SQLite.

Main models include:

* Student
* College
* Mentor
* Course
* Question
* Answer
* Jobs
* CollegeApplication
* JobApplication
* InterviewPreparation
* Chat

## Screenshots

Screenshots of the project can be added here.

## Future Improvements

* AI career recommendations
* AI resume analysis
* College and course comparison
* Better search and filtering
* Notifications
* REST API
* PostgreSQL
* Cloud deployment
* Mobile application

## Purpose

The main purpose of this project is to provide students with one platform for career testing, course selection, college applications, job opportunities, interview preparation, and mentor guidance.
