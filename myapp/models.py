from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50,null=True)
    view_password=models.CharField(max_length=50,null=True)

class College(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True) 
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    location=models.CharField(max_length=30,null=True)
    image=models.FileField(upload_to='file' ,null=True)
    # department=models.CharField(max_length=30,null=True)

class Student(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True) 
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    location=models.CharField(max_length=30,null=True)
    qualification=models.CharField(max_length=30,null=True)
    image=models.FileField(upload_to='file' ,null=True)


class Mentor(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    clg=models.ForeignKey(College,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True) 
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    qualification=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    location=models.CharField(max_length=30,null=True)

class Course(models.Model):
    mentor=models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True)
    clg=models.ForeignKey(College,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    duration=models.CharField(max_length=50,null=True)
    fees=models.CharField(max_length=50,null=True)
    details=models.CharField(max_length=100,null=True)
    gpa=models.FloatField(null=True)


class Question(models.Model):
    question=models.CharField(max_length=50,null=True)
    option1=models.CharField(max_length=10,null=True)
    option2=models.CharField(max_length=10,null=True)
    option3=models.CharField(max_length=10,null=True)
    option4=models.CharField(max_length=10,null=True)
    answer=models.CharField(max_length=10,null=True)



class Answer(models.Model):
    std=models.ForeignKey(Student,on_delete=models.CASCADE)
    one=models.IntegerField()
    two=models.IntegerField(blank=True,null=True)
    total_sum=models.IntegerField(default=0)



class Jobs(models.Model):
    # course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)  
    name= models.CharField(max_length=100, null=True)  
    description = models.CharField( max_length=100,null=True )  
    company_name = models.CharField(max_length=100, null=True)  
    location = models.CharField(max_length=100, null=True)  
    salary = models.CharField(max_length=50, null=True)  
    eligibility_criteria = models.CharField(max_length=100,null=True)  
    created_at = models.DateField(auto_now_add=True) 
    application_deadline = models.DateField(null=True, blank=True) 


class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    highest_qualification = models.CharField(max_length=100, null=True)
    marks = models.CharField(max_length=20, null=True)
    resume = models.FileField(upload_to='resumes/', null=True)
    applied_at = models.DateTimeField(auto_now_add=True)



class Financer(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True) 
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    location=models.CharField(max_length=30,null=True)


class Loan(models.Model):
    fin=models.ForeignKey(Financer,on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True)  
    provider = models.CharField(max_length=100,null=True)  
    interest_rate = models.CharField(max_length=100,null=True) 
    max_amount = models.CharField(max_length=100,null=True) 
    tenure_years = models.CharField(max_length=100,null=True)
    eligibile_gpa = models.CharField(max_length=100,null=True) 
    details = models.CharField(max_length=100,null=True)
    
class Chat(models.Model):
    sellerid = models.ForeignKey(Student, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
    
class InterviewPreparation(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    pdf = models.FileField(upload_to='file' ,null=True)
   


class CollegeApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
