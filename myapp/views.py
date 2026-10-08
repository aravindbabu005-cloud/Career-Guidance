from django.shortcuts import render, redirect, get_object_or_404
from .models import *

from django.contrib.auth import authenticate
from django.contrib import messages

import random
import os
import re

from datetime import date as date, datetime as dt

from django.db.models import Q, F, Value, Sum
from django.db.models.functions import Coalesce

from django.http import FileResponse, Http404
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# =========================================================
# HOME
# =========================================================

def index(request):
    return render(request, "index.html")
def login(request):

    if request.method == "POST":

        name = request.POST.get("email")
        password = request.POST.get("password")

        if not name or not password:
            messages.error(
                request,
                "Please enter username and password."
            )
            return render(request, "login.html")

        user = authenticate(
            request,
            username=name,
            password=password
        )

        if user is not None:

            if user.usertype == "admin":

                messages.info(
                    request,
                    "Welcome to admin page"
                )

                return redirect("/adminpg")

            elif user.usertype == "college":

                messages.info(
                    request,
                    "Welcome to college page"
                )

                request.session["Uid"] = user.id

                return redirect("/clgpg")

            elif user.usertype == "student":

                messages.info(
                    request,
                    "Welcome to student page"
                )

                request.session["Uid"] = user.id

                return redirect("/stdpg")

            elif user.usertype == "Financer":

                messages.info(
                    request,
                    "Welcome to Financer page"
                )

                request.session["Uid"] = user.id

                return redirect("/finpg")

            elif user.usertype == "Mentor":

                messages.info(
                    request,
                    "Welcome to Mentor page"
                )

                request.session["Uid"] = user.id

                return redirect("/mentorpg")

            else:

                messages.error(
                    request,
                    "Invalid user type."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")

# =========================================================
# VALIDATION
# =========================================================

def validate_password(password):

    if len(password) < 8:

        return False, "Password must be at least 8 characters long."

    if not re.search(r"[a-z]", password):

        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"[A-Z]", password):

        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"\d", password):

        return False, "Password must contain at least one number."

    if not re.search(
        r'[!@#$%^&*(),.?":{}|<>]',
        password
    ):

        return False, "Password must contain at least one special character."

    return True, "Password is valid."


def check_email(email):

    if not re.match(
        r"^[^@]+@[^@]+\.[^@]+$",
        email
    ):

        return False, "Invalid email format."

    return True, "Email is valid."


# =========================================================
# COLLEGE REGISTRATION
# =========================================================

def clgreg(request):

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        location = request.POST["location"]
        phone = request.POST["phone"]
        image = request.FILES.get("image")

        # Email validation
        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                "Invalid email format."
            )

            return redirect("/clgreg")

        # Password validation
        is_valid, message = validate_password(password)

        if not is_valid:

            messages.error(
                request,
                message
            )

            return redirect("/clgreg")

        # Check duplicate email
        if Login.objects.filter(email=email).exists():

            messages.info(
                request,
                "Email already registered."
            )

        # Check duplicate phone
        elif College.objects.filter(phone=phone).exists():

            messages.info(
                request,
                "Phone number already registered."
            )

        else:

            clg = Login.objects.create_user(
                username=email,
                view_password=password,
                password=password,
                usertype="college",
                is_active=0
            )

            clg.save()

            reg = College.objects.create(
                name=name,
                email=email,
                password=password,
                image=image,
                phone=phone,
                location=location,
                user=clg
            )

            reg.save()

            messages.success(
                request,
                "Registration Successful. Wait For Approval."
            )

            return redirect("/login")

    return render(
        request,
        "college/clgreg.html"
    )


# =========================================================
# STUDENT REGISTRATION
# =========================================================

def studreg(request):

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        location = request.POST["location"]
        phone = request.POST["phone"]
        qualification = request.POST["qualification"]
        image = request.FILES.get("image")

        # Email validation
        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                "Invalid email format."
            )

            return redirect("/studreg")

        # Password validation
        is_valid, message = validate_password(password)

        if not is_valid:

            messages.error(
                request,
                message
            )

            return redirect("/studreg")

        # Check email
        if Login.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect("/studreg")

        # Check phone
        if Student.objects.filter(phone=phone).exists():

            messages.error(
                request,
                "Phone number already registered."
            )

            return redirect("/studreg")

        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=1,
            usertype="student"
        )

        log.save()

        reguser = Student.objects.create(
            user=log,
            name=name,
            qualification=qualification,
            email=email,
            phone=phone,
            location=location,
            image=image
        )

        reguser.save()

        messages.success(
            request,
            "Registration Successful. Wait For Approval."
        )

        return redirect("/login")

    return render(
        request,
        "student/studreg.html"
    )


# =========================================================
# FINANCER REGISTRATION
# =========================================================

def finReg(request):

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        location = request.POST["location"]
        phone = request.POST["phone"]

        if Login.objects.filter(email=email).exists():

            messages.info(
                request,
                "Already registered"
            )

        else:

            fin = Login.objects.create_user(
                username=email,
                view_password=password,
                password=password,
                usertype="Financer",
                is_active=1
            )

            fin.save()

            reg = Financer.objects.create(
                name=name,
                email=email,
                password=password,
                phone=phone,
                location=location,
                user=fin
            )

            reg.save()

            return redirect("/login")

    return render(
        request,
        "financer/finReg.html"
    )


# =========================================================
# ADMIN
# =========================================================

def adminpg(request):

    return render(
        request,
        "admin/adminpg.html"
    )


def admin_clg_view(request):

    data = College.objects.all()

    return render(
        request,
        "admin/admin_clg_view.html",
        {"data": data}
    )


def admin_studview(request):

    data = Student.objects.all()

    return render(
        request,
        "admin/admin_studview.html",
        {"data": data}
    )


def stud_Dlt(request):

    id = request.GET["id"]

    Login.objects.filter(
        id=id
    ).delete()

    return redirect("/admin_studview")


# =========================================================
# COLLEGE APPROVAL / REJECTION
# =========================================================

def clgapprove(request):

    id = request.GET["id"]

    clg_user = Login.objects.get(
        id=id
    )

    clg_user.is_active = True
    clg_user.save()

    college = College.objects.get(
        user=clg_user
    )

    send_mail(
        "College Registration Approved",
        f"""Hello {college.name},

Your college registration has been approved.
You can now log in and access the platform.

Thank you.""",
        "jissjoshy3@gmail.com",
        [college.email],
        fail_silently=False,
    )

    return redirect(
        "/admin_clg_view"
    )


def clgreject(request):

    id = request.GET["id"]

    college = College.objects.get(
        id=id
    )

    send_mail(
        "College Registration Rejected",
        f"""Dear {college.name},

We regret to inform you that your college registration has been rejected.

Thank you.""",
        "jissjoshy3@gmail.com",
        [college.email],
        fail_silently=False,
    )

    Login.objects.filter(
        id=college.user.id
    ).delete()

    college.delete()

    return redirect(
        "/admin_clg_view"
    )


# =========================================================
# QUESTIONS
# =========================================================

def addquestions(request):

    global qlist, o1, o2, o3, o4, ansl

    msgcount = int(
        request.POST.get(
            "msgcount",
            1
        )
    )

    if request.method == "POST":

        qstn = request.POST["qstn"]
        op1 = request.POST["op1"]
        op2 = request.POST["op2"]
        op3 = request.POST["op3"]
        op4 = request.POST["op4"]
        ans = request.POST["ans"]

        qnaadd = Question.objects.create(
            question=qstn,
            option1=op1,
            option2=op2,
            option3=op3,
            option4=op4,
            answer=ans
        )

        qnaadd.save()

        messages.success(
            request,
            "Added successfully"
        )

    return render(
        request,
        "Admin/addquestions.html",
        {"msgcount": msgcount}
    )


def show_questions(request):

    questions = Question.objects.all()

    return render(
        request,
        "admin/show_questions.html",
        {"questions": questions}
    )


def delete_question(request, id):

    Question.objects.get(
        id=id
    ).delete()

    messages.info(
        request,
        "Question Deleted Successfully"
    )

    return redirect(
        "show_questions"
    )


def edit_question(request, id):

    question = get_object_or_404(
        Question,
        id=id
    )

    if request.method == "POST":

        question.question = request.POST["question"]
        question.option1 = request.POST["option1"]
        question.option2 = request.POST["option2"]
        question.option3 = request.POST["option3"]
        question.option4 = request.POST["option4"]
        question.answer = request.POST["answer"]

        question.save()

        messages.success(
            request,
            "Question Edited Successfully"
        )

        return redirect(
            "show_questions"
        )

    return render(
        request,
        "admin/edit_question.html",
        {"question": question}
    )


# =========================================================
# JOBS - ADMIN
# =========================================================

def add_JobDetail(request):

    if request.method == "POST":

        name = request.POST["name"]
        description = request.POST["description"]

        # Removed accidental space from company_name
        company_name = request.POST["company_name"]

        location = request.POST["location"]
        salary = request.POST["salary"]
        eligibility_criteria = request.POST["eligibility_criteria"]
        created_at = request.POST["created_at"]
        application_deadline = request.POST["application_deadline"]

        job = Jobs.objects.create(
            name=name,
            description=description,
            company_name=company_name,
            location=location,
            salary=salary,
            eligibility_criteria=eligibility_criteria,
            created_at=created_at,
            application_deadline=application_deadline
        )

        job.save()

    return render(
        request,
        "admin/add_JobDetail.html"
    )


def std_testresult(request):

    data = Answer.objects.all()

    return render(
        request,
        "admin/std_testresult.html",
        {"data": data}
    )


def show_jobs(request):

    jobs = Jobs.objects.all()

    return render(
        request,
        "admin/show_jobs.html",
        {"jobs": jobs}
    )


def edit_job(request, id):

    job = get_object_or_404(
        Jobs,
        id=id
    )

    courses = Course.objects.all()

    if request.method == "POST":

        job.name = request.POST["name"]
        job.description = request.POST["description"]
        job.company_name = request.POST["company_name"]
        job.location = request.POST["location"]
        job.salary = request.POST["salary"]
        job.eligibility_criteria = request.POST["eligibility"]
        job.application_deadline = request.POST["deadline"]

        job.save()

        return redirect(
            "show_jobs"
        )

    return render(
        request,
        "admin/edit_job.html",
        {
            "job": job,
            "courses": courses
        }
    )


def delete_job(request, id):

    job = get_object_or_404(
        Jobs,
        id=id
    )

    job.delete()

    return redirect(
        "show_jobs"
    )


# =========================================================
# COLLEGE
# =========================================================

def clgpg(request):

    return render(
        request,
        "college/clgpg.html"
    )


def clgview(request):

    id = request.session["Uid"]

    data = College.objects.filter(
        user_id=id
    )

    return render(
        request,
        "college/clgview.html",
        {"data": data}
    )


def studentView(request):

    return render(
        request,
        "admin/studentview.html"
    )


def addMentor(request):

    uid = request.session["Uid"]

    uid = College.objects.get(
        user_id=uid
    )

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        location = request.POST["location"]
        qualification = request.POST["qualification"]
        password = request.POST["password"]

        # Email check
        if Login.objects.filter(
            username=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return redirect(
                "/addMentor"
            )

        # Phone check
        if Mentor.objects.filter(
            phone=phone
        ).exists():

            messages.error(
                request,
                "Phone number is already registered."
            )

            return redirect(
                "/addMentor"
            )

        # Validate email
        email_valid, email_message = check_email(
            email
        )

        if not email_valid:

            messages.error(
                request,
                email_message
            )

            return redirect(
                "/addMentor"
            )

        # Validate password
        password_valid, password_message = validate_password(
            password
        )

        if not password_valid:

            messages.error(
                request,
                password_message
            )

            return redirect(
                "/addMentor"
            )

        # Create login
        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=1,
            usertype="Mentor"
        )

        log.save()

        # Create mentor
        Mentor.objects.create(
            user=log,
            clg=uid,
            name=name,
            email=email,
            phone=phone,
            location=location,
            qualification=qualification
        )

        messages.success(
            request,
            "Mentor added successfully"
        )

        return redirect(
            "/clgpg"
        )

    return render(
        request,
        "college/addMentor.html"
    )


def addcourse(request):

    uid = request.session["Uid"]

    clg = College.objects.get(
        user_id=uid
    )

    mentors = Mentor.objects.filter(
        clg=clg
    )

    if request.method == "POST":

        name = request.POST["name"]
        duration = request.POST["duration"]
        fees = request.POST["fees"]
        details = request.POST["details"]
        gpa = request.POST["gpa"]

        mentor_id = request.POST["mentor"]

        mentor = Mentor.objects.get(
            id=mentor_id
        )

        course = Course.objects.create(
            name=name,
            duration=duration,
            fees=fees,
            details=details,
            gpa=gpa,
            clg=clg,
            mentor=mentor
        )

        course.save()

    return render(
        request,
        "college/addcourse.html",
        {"mentors": mentors}
    )


def delCourse(request):

    id = request.GET["id"]

    Course.objects.filter(
        id=id
    ).delete()

    return redirect(
        "/course_view"
    )


def course_view(request):

    data = Course.objects.all()

    return render(
        request,
        "college/course_view.html",
        {"data": data}
    )


def update(request):

    id = request.GET["id"]

    clg = Course.objects.get(
        id=id
    )

    if request.method == "POST":

        name = request.POST["name"]
        duration = request.POST["duration"]
        fees = request.POST["fees"]
        details = request.POST["details"]
        gpa = float(
            request.POST["gpa"]
        )

        clg.name = name
        clg.duration = duration
        clg.fees = fees
        clg.details = details
        clg.gpa = gpa

        clg.save()

        return redirect(
            "/course_view"
        )

    return render(
        request,
        "college/update.html",
        {"ups": [clg]}
    )


def collegeUpdate(request):

    uid = request.GET.get("uid")

    datas = College.objects.filter(
        user=uid
    )

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        location = request.POST.get("location")

        image = request.FILES.get("image")

        data = College.objects.get(
            user=uid
        )

        data.name = name
        data.phone = phone
        data.location = location

        if image:
            data.image = image

        data.save()

        messages.success(
            request,
            "Updated successfully"
        )

        return redirect(
            "/clgview"
        )

    return render(
        request,
        "college/collegeUpdate.html",
        {"datas": datas}
    )


def std_results(request):

    data = Answer.objects.all()

    return render(
        request,
        "college/std_results.html",
        {"data": data}
    )


# =========================================================
# COLLEGE MENTORS
# =========================================================

def viewMentors(request):

    uid = request.session["Uid"]

    clg = College.objects.get(
        user_id=uid
    )

    mentors = Mentor.objects.filter(
        clg=clg
    )

    return render(
        request,
        "college/viewMentors.html",
        {"mentors": mentors}
    )


def editMentor(request, id):

    mentor = Mentor.objects.get(
        id=id
    )

    if request.method == "POST":

        mentor.name = request.POST["name"]
        mentor.email = request.POST["email"]
        mentor.phone = request.POST["phone"]
        mentor.location = request.POST["location"]
        mentor.qualification = request.POST["qualification"]

        mentor.save()

        login_user = Login.objects.get(
            id=mentor.user.id
        )

        login_user.username = request.POST["email"]

        login_user.save()

        messages.success(
            request,
            "Mentor details updated successfully"
        )

        return redirect(
            "viewMentors"
        )

    return render(
        request,
        "college/editMentor.html",
        {"mentor": mentor}
    )


def deleteMentor(request, id):

    mentor = Mentor.objects.get(
        id=id
    )

    login_user = Login.objects.get(
        id=mentor.user.id
    )

    mentor.delete()
    login_user.delete()

    messages.success(
        request,
        "Mentor deleted successfully"
    )

    return redirect(
        "viewMentors"
    )


# =========================================================
# STUDENT
# =========================================================

def stdpg(request):

    return render(
        request,
        "student/stdpg.html"
    )


def stud_clg_view(request):

    data = College.objects.all()

    return render(
        request,
        "student/stud_clg_view.html",
        {"data": data}
    )


def student_Profile(request):

    uid = request.session["Uid"]

    data = Student.objects.filter(
        user=uid
    )

    return render(
        request,
        "student/student_Profile.html",
        {"data": data}
    )


def UpdateStud(request):

    uid = request.GET.get("uid")

    datas = Student.objects.filter(
        user=uid
    )

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")

        image = request.FILES.get("image")

        data = Student.objects.get(
            user=uid
        )

        data.name = name
        data.phone = phone
        data.location = location
        data.qualification = qualification

        if image:
            data.image = image

        data.save()

        messages.success(
            request,
            "Profile updated successfully"
        )

        return redirect(
            "/student_Profile"
        )

    return render(
        request,
        "student/UpdateStud.html",
        {"datas": datas}
    )


# =========================================================
# STUDENT COURSES
# =========================================================

def Stud_Course(request):

    search_term = (
        request.POST.get(
            "search_term",
            ""
        ).strip()
        if request.method == "POST"
        else ""
    )

    if search_term:

        data = Course.objects.filter(

            Q(name__icontains=search_term)
            |
            Q(gpa__icontains=search_term)
            |
            Q(duration__icontains=search_term)

        )

    else:

        data = Course.objects.all()

    return render(
        request,
        "student/Stud_Course.html",
        {
            "data": data,
            "search_term": search_term
        }
    )


def join_Course(request):

    student_id = request.session["Uid"]

    id = request.GET["id"]

    student = Student.objects.get(
        user=student_id
    )

    course = Course.objects.get(
        id=id
    )

    total_sum = Answer.objects.filter(
        std=student
    ).aggregate(
        total_sum=Coalesce(
            Sum("one"),
            Value(0)
        )
    )["total_sum"]

    if total_sum >= int(course.gpa):

        messages.success(
            request,
            "You have successfully joined the course."
        )

    else:

        messages.error(
            request,
            "Your GPA is too low to join this course."
        )

    return redirect(
        "/Stud_Course"
    )


# =========================================================
# TEST QUESTIONS
# =========================================================

def generate_final_qna(questions):

    final_qna = []

    random.shuffle(questions)

    for q in questions:

        final_qna.append(q)

    return final_qna


def assign_questions_to_candidate(
    request,
    questions
):

    final_qna = generate_final_qna(
        questions
    )

    qna_primary_keys = [
        q.pk
        for q in final_qna
    ]

    request.session[
        "assigned_questions"
    ] = qna_primary_keys

    request.session[
        "obj_index"
    ] = 0

    request.session[
        "qcount"
    ] = 1


def dell(request):

    Answer.objects.all().delete()

    return redirect("/adminpg")


# =========================================================
# STUDENT TEST
# =========================================================

def test(request):

    student_id = request.session.get(
        "Uid"
    )

    if not student_id:

        return redirect(
            "/login"
        )

    try:

        user = Student.objects.get(
            user=student_id
        )

    except Student.DoesNotExist:

        return redirect(
            "/error"
        )

    # Assign 10 random questions
    if "assigned_questions" not in request.session:

        questions = list(
            Question.objects.order_by("?")[:10]
        )

        assigned_qna_primary_keys = [
            q.id
            for q in questions
        ]

        request.session[
            "assigned_questions"
        ] = assigned_qna_primary_keys

        request.session[
            "obj_index"
        ] = 0

        request.session[
            "qcount"
        ] = 1

    else:

        assigned_qna_primary_keys = request.session[
            "assigned_questions"
        ]

    curr_obj_index = request.session.get(
        "obj_index",
        0
    )

    qcount = request.session.get(
        "qcount",
        1
    )

    if request.method == "POST":

        selected = request.POST.get(
            "opt"
        )

        qid = request.POST.get(
            "qid"
        )

        try:

            question = Question.objects.get(
                id=qid
            )

        except Question.DoesNotExist:

            return redirect(
                "/error"
            )

        if question.answer == selected:

            user_answer, created = Answer.objects.get_or_create(
                std=user,
                defaults={
                    "one": 0
                }
            )

            user_answer.one = F("one") + 1

            user_answer.save()

        curr_obj_index += 1
        qcount += 1

        request.session[
            "obj_index"
        ] = curr_obj_index

        request.session[
            "qcount"
        ] = qcount

        if curr_obj_index < len(
            assigned_qna_primary_keys
        ):

            curr_obj = Question.objects.get(
                pk=assigned_qna_primary_keys[
                    curr_obj_index
                ]
            )

        else:

            request.session.pop(
                "assigned_questions",
                None
            )

            request.session.pop(
                "obj_index",
                None
            )

            request.session.pop(
                "qcount",
                None
            )

            return redirect(
                "/testresult"
            )

    else:

        if curr_obj_index < len(
            assigned_qna_primary_keys
        ):

            curr_obj = Question.objects.get(
                pk=assigned_qna_primary_keys[
                    curr_obj_index
                ]
            )

        else:

            request.session.pop(
                "assigned_questions",
                None
            )

            request.session.pop(
                "obj_index",
                None
            )

            request.session.pop(
                "qcount",
                None
            )

            return redirect(
                "/userhome"
            )

    return render(
        request,
        "student/test.html",
        {
            "obj": curr_obj,
            "qcount": qcount
        }
    )


# =========================================================
# TEST RESULT
# =========================================================

def testresult(request):

    user_id = request.session.get(
        "Uid"
    )

    if not user_id:

        return redirect(
            "/login"
        )

    user = Student.objects.get(
        user=user_id
    )

    answers = Answer.objects.filter(
        std=user
    )

    total_sum = answers.aggregate(
        total_sum=Coalesce(
            Sum("one"),
            Value(0)
        )
    )["total_sum"]

    try:

        answer = Answer.objects.get(
            std=user
        )

        answer.total_sum = total_sum
        answer.one = total_sum

        answer.save()

    except Answer.DoesNotExist:

        Answer.objects.create(
            std=user,
            one=total_sum,
            total_sum=total_sum
        )

    return render(
        request,
        "student/testresult.html",
        {
            "total_sum": total_sum
        }
    )


# =========================================================
# ELIGIBLE COURSES
# =========================================================

def eligible_course(student_id):

    student = Student.objects.filter(
        user=student_id
    ).first()

    if not student:

        return None

    total_sum = Answer.objects.filter(
        std=student
    ).aggregate(
        total_sum=Coalesce(
            Sum("one"),
            Value(0)
        )
    )["total_sum"]

    eligible_courses = Course.objects.filter(
        gpa__lte=total_sum
    )

    eligible_colleges = College.objects.filter(
        course__in=eligible_courses
    ).distinct()

    return {
        "total_sum": total_sum,
        "eligible_colleges": eligible_colleges,
        "eligible_courses": eligible_courses
    }


def eligible_college_course_view(request):

    student_id = request.session[
        "Uid"
    ]

    result = eligible_course(
        student_id
    )

    if result:

        return render(
            request,
            "student/eligible_colleges.html",
            {
                "data": result[
                    "eligible_colleges"
                ],
                "cou": result[
                    "eligible_courses"
                ],
                "total_sum": result[
                    "total_sum"
                ]
            }
        )

    else:

        messages.error(
            request,
            "You are not eligible."
        )

        return redirect(
            "/test"
        )


# =========================================================
# COLLEGE APPLICATION
# =========================================================

def apply_to_college(request):

    if request.method == "POST":

        student_id = request.session.get(
            "Uid"
        )

        student = Student.objects.get(
            user__id=student_id
        )

        college_id = request.POST.get(
            "college_id"
        )

        course_id = request.POST.get(
            "course_id"
        )

        college = College.objects.get(
            id=college_id
        )

        course = Course.objects.get(
            id=course_id
        )

        already_applied = CollegeApplication.objects.filter(
            student=student,
            college=college,
            course=course
        ).exists()

        if already_applied:

            messages.warning(
                request,
                "You have already applied to this course."
            )

        else:

            CollegeApplication.objects.create(
                student=student,
                college=college,
                course=course
            )

            messages.success(
                request,
                "Application submitted successfully."
            )

        return redirect(
            "eligible_colleges"
        )

    return redirect(
        "eligible_colleges"
    )


# =========================================================
# FINANCIAL AID
# =========================================================

def financial_aid(request):

    student_id = request.session.get(
        "Uid"
    )

    if not student_id:

        messages.error(
            request,
            "You need to log in first."
        )

        return redirect(
            "/login"
        )

    student = Student.objects.filter(
        user=student_id
    ).first()

    if not student:

        messages.error(
            request,
            "Student record not found."
        )

        return redirect(
            "/userhome"
        )

    total_score = Answer.objects.filter(
        std=student
    ).aggregate(
        total_sum=Coalesce(
            Sum("one"),
            Value(0)
        )
    )["total_sum"]

    if total_score == 0:

        messages.error(
            request,
            "Please attend the test to view financial aid options."
        )

        return redirect(
            "/test"
        )

    eligible_loans = Loan.objects.filter(
        eligibile_gpa__lte=total_score
    ).distinct()

    return render(
        request,
        "student/financial_aid.html",
        {
            "loans": eligible_loans,
            "score": total_score
        }
    )


# =========================================================
# TEST RESULT - ALTERNATIVE VIEW
# =========================================================

def test_result(request):

    student_id = request.session.get(
        "Uid"
    )

    if not student_id:

        messages.error(
            request,
            "Please log in to access your test results."
        )

        return redirect(
            "/login"
        )

    student = Student.objects.filter(
        user=student_id
    ).first()

    if not student:

        messages.error(
            request,
            "Student record not found."
        )

        return redirect(
            "/userhome"
        )

    total_score = Answer.objects.filter(
        std=student
    ).aggregate(
        total_sum=Coalesce(
            Sum("one"),
            Value(0)
        )
    )["total_sum"]

    eligible_courses = Course.objects.filter(
        gpa__lte=total_score
    )

    return render(
        request,
        "student/test_result.html",
        {
            "score": total_score,
            "courses": eligible_courses
        }
    )


# =========================================================
# INTERVIEW NOTES - STUDENT
# =========================================================

def InterviewNotes(request):

    data = InterviewPreparation.objects.all()

    return render(
        request,
        "student/InterviewNotes.html",
        {"data": data}
    )


def view_interviewnote_details(request):

    note_id = request.GET.get(
        "id"
    )

    try:

        note = InterviewPreparation.objects.get(
            id=note_id
        )

        return render(
            request,
            "student/view_interviewnote_details.html",
            {"note": note}
        )

    except InterviewPreparation.DoesNotExist:

        raise Http404(
            "Note not found"
        )


def download_interviewnotes(request):

    note_id = request.GET.get(
        "id"
    )

    if not note_id:

        raise Http404(
            "Note ID not provided"
        )

    try:

        interview = InterviewPreparation.objects.get(
            id=note_id
        )

        if not interview.pdf:

            raise Http404(
                "Study material not found"
            )

        file_path = interview.pdf.path

        response = FileResponse(
            open(file_path, "rb"),
            as_attachment=True
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; filename="{os.path.basename(file_path)}"'
        )

        return response

    except InterviewPreparation.DoesNotExist:

        raise Http404(
            "Interview preparation note not found"
        )

    except FileNotFoundError:

        raise Http404(
            "Study material file not found"
        )


# =========================================================
# JOB VACANCY - STUDENT
# =========================================================

def job_vacancy(request):

    data = Jobs.objects.all()

    return render(
        request,
        "student/job_vacancy.html",
        {"data": data}
    )


# =========================================================
# FINANCER
# =========================================================

def finpg(request):

    return render(
        request,
        "financer/finpg.html"
    )


def addLoan(request):

    uid = request.session["Uid"]

    fin = Financer.objects.get(
        user_id=uid
    )

    if request.method == "POST":

        name = request.POST["name"]
        provider = request.POST["provider"]

        interest_rate = request.POST[
            "interest_rate"
        ]

        max_amount = request.POST[
            "max_amount"
        ]

        tenure_years = request.POST[
            "tenure_years"
        ]

        eligibile_gpa = request.POST[
            "eligibile_gpa"
        ]

        details = request.POST[
            "details"
        ]

        loan = Loan.objects.create(
            name=name,
            provider=provider,
            interest_rate=interest_rate,
            max_amount=max_amount,
            tenure_years=tenure_years,
            eligibile_gpa=eligibile_gpa,
            details=details,
            fin=fin
        )

        loan.save()

    return render(
        request,
        "financer/addLoan.html"
    )


def viewLoan(request):

    data = Loan.objects.all()

    return render(
        request,
        "financer/viewLoan.html",
        {"data": data}
    )


def delLoan(request):

    id = request.GET["id"]

    Loan.objects.filter(
        id=id
    ).delete()

    return redirect(
        "/viewLoan"
    )


# =========================================================
# MENTOR
# =========================================================

def mentorpg(request):

    return render(
        request,
        "Mentor/mentorpg.html"
    )


def view_Course(request):

    data = Course.objects.all()

    return render(
        request,
        "Mentor/view_Course.html",
        {"data": data}
    )


def InterviewPrepare(request):

    uid = request.session["Uid"]

    mentor = Mentor.objects.get(
        user_id=uid
    )

    if request.method == "POST":

        title = request.POST["title"]
        content = request.POST["content"]

        pdf = request.FILES.get(
            "pdf"
        )

        note = InterviewPreparation.objects.create(
            mentor=mentor,
            title=title,
            content=content,
            pdf=pdf
        )

        note.save()

    return render(
        request,
        "Mentor/InterviewPrepare.html"
    )


def viewnotes(request):

    data = InterviewPreparation.objects.all()

    return render(
        request,
        "Mentor/viewnotes.html",
        {"data": data}
    )


# =========================================================
# NORMAL CHAT
# =========================================================
# NOTE:
# Chatbot has been completely removed.
# These functions are only for Student <-> Mentor chat.

def chat(request):

    uid = request.session["Uid"]

    name = ""

    artistData = Mentor.objects.all()

    id = request.GET.get(
        "id"
    )

    getChatData = Chat.objects.filter(
        Q(sellerid__user=uid)
        &
        Q(customerid=id)
    )

    current_time = dt.now().time()

    formatted_time = current_time.strftime(
        "%H:%M"
    )

    userid = Student.objects.get(
        user=uid
    )

    customerid = None

    if id:

        customerid = Mentor.objects.get(
            id=id
        )

        name = customerid.name

    if request.method == "POST":

        message = request.POST["message"]

        sendMsg = Chat.objects.create(
            sellerid=userid,
            message=message,
            customerid=customerid,
            time=formatted_time,
            utype="STUDENT"
        )

        sendMsg.save()

    return render(
        request,
        "Student/reciever.html",
        {
            "artistData": artistData,
            "getChatData": getChatData,
            "customerid": name,
            "id": id
        }
    )


def reply(request):

    uid = request.session["Uid"]

    name = ""

    userData = Student.objects.all()

    id = request.GET.get(
        "id"
    )

    getChatData = Chat.objects.filter(
        Q(customerid__user=uid)
        &
        Q(sellerid=id)
    )

    current_time = dt.now().time()

    formatted_time = current_time.strftime(
        "%H:%M"
    )

    customerid = Mentor.objects.get(
        user=uid
    )

    userid = None

    if id:

        userid = Student.objects.get(
            id=id
        )

        name = userid.name

    if request.method == "POST":

        message = request.POST["message"]

        sendMsg = Chat.objects.create(
            sellerid=userid,
            message=message,
            customerid=customerid,
            time=formatted_time,
            utype="MENTOR"
        )

        sendMsg.save()

    return render(
        request,
        "Mentor/sender.html",
        {
            "userData": userData,
            "getChatData": getChatData,
            "userid": name,
            "id": id
        }
    )


# =========================================================
# COLLEGE APPLICATIONS
# =========================================================

def view_applied_colleges(request):

    uid = request.session.get(
        "Uid"
    )

    student = Student.objects.get(
        user_id=uid
    )

    applications = CollegeApplication.objects.filter(
        student=student
    )

    return render(
        request,
        "student/view_applied_colleges.html",
        {
            "applications": applications
        }
    )


def view_applications_college(request):

    uid = request.session.get(
        "Uid"
    )

    college = College.objects.get(
        user_id=uid
    )

    applications = CollegeApplication.objects.filter(
        college=college
    )

    return render(
        request,
        "college/view_applications_college.html",
        {
            "applications": applications
        }
    )


def update_application_status(
    request,
    app_id,
    status
):

    CollegeApplication.objects.filter(
        id=app_id
    ).update(
        status=status
    )

    return redirect(
        "view_applications_college"
    )


# =========================================================
# JOB APPLICATION
# =========================================================

def apply_job(request, job_id):

    if "Uid" not in request.session:

        return redirect(
            "/login"
        )

    login_id = request.session[
        "Uid"
    ]

    user = Login.objects.get(
        id=login_id
    )

    student = Student.objects.get(
        user=user
    )

    job = Jobs.objects.get(
        id=job_id
    )

    # Check duplicate application
    if JobApplication.objects.filter(
        student=student,
        job=job
    ).exists():

        messages.info(
            request,
            "You have already applied for this job."
        )

        return redirect(
            "/job_vacancy"
        )

    if request.method == "POST":

        qualification = request.POST.get(
            "qualification"
        )

        marks = request.POST.get(
            "marks"
        )

        resume = request.FILES.get(
            "resume"
        )

        JobApplication.objects.create(
            student=student,
            job=job,
            highest_qualification=qualification,
            marks=marks,
            resume=resume
        )

        messages.success(
            request,
            "Your application has been submitted successfully!"
        )

        return redirect(
            "/job_vacancy"
        )

    return render(
        request,
        "student/apply_job.html",
        {
            "job": job,
            "student": student
        }
    )


def view_applied_jobs(request):

    uid = request.session["Uid"]

    login_obj = Login.objects.get(
        id=uid
    )

    student = Student.objects.get(
        user=login_obj
    )

    applications = JobApplication.objects.filter(
        student=student
    )

    return render(
        request,
        "student/view_applied_jobs.html",
        {
            "applications": applications
        }
    )


# =========================================================
# ADMIN APPLICATION VIEWS
# =========================================================

def admin_view_applications(request):

    applications = JobApplication.objects.select_related(
        "student",
        "job"
    )

    return render(
        request,
        "admin/admin_view_applications.html",
        {
            "applications": applications
        }
    )


def admin_view_college_applications(request):

    applications = CollegeApplication.objects.select_related(
        "student",
        "college",
        "course"
    )

    return render(
        request,
        "admin/admin_view_college_applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# ALL COURSES
# =========================================================

def view_all_courses(request):

    data = Course.objects.all()

    return render(
        request,
        "college/view_all_courses.html",
        {
            "data": data
        }
    )