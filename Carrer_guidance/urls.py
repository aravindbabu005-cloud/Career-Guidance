from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),

    # ADMIN
    path('adminpg', views.adminpg),
    path('clgreject', views.clgreject),
    path('clgapprove', views.clgapprove),
    path('addquestions', views.addquestions, name="addquestions"),
    path('admin_clg_view', views.admin_clg_view),
    path('add_JobDetail', views.add_JobDetail, name='add_JobDetail'),
    path('admin_studview', views.admin_studview),
    path('stud_Dlt', views.stud_Dlt),

    path(
        'show_questions',
        views.show_questions,
        name='show_questions'
    ),

    path(
        'delete_question/<int:id>',
        views.delete_question,
        name='delete_question'
    ),

    path(
        'edit_question/<int:id>',
        views.edit_question,
        name='edit_question'
    ),

    path(
        'show_jobs',
        views.show_jobs,
        name='show_jobs'
    ),

    path(
        'delete_job/<int:id>',
        views.delete_job,
        name='delete_job'
    ),

    path(
        'edit_job/<int:id>',
        views.edit_job,
        name='edit_job'
    ),

    path(
        'admin_view_applications',
        views.admin_view_applications,
        name='admin_view_applications'
    ),

    path(
        'admin_view_college_applications',
        views.admin_view_college_applications,
        name='admin_view_college_applications'
    ),

    #STUDENT
    path('studreg', views.studreg),
    path('stdpg', views.stdpg),
    path('stud_clg_view', views.stud_clg_view),
    path('Stud_Course', views.Stud_Course),
    path('job_vacancy', views.job_vacancy),
    path('test', views.test),
    path('testresult', views.testresult),

    path(
        'eligible_colleges',
        views.eligible_college_course_view,
        name='eligible_colleges'
    ),

    path(
        'eligible_course',
        views.eligible_course
    ),

    path(
        'view_interviewnote_details',
        views.view_interviewnote_details
    ),

    path(
        'std_testresult',
        views.std_testresult
    ),

    path(
        'student_Profile',
        views.student_Profile
    ),

    path(
        'UpdateStud',
        views.UpdateStud
    ),

    path(
        'apply_to_college',
        views.apply_to_college,
        name='apply_to_college'
    ),

    path(
        'view_applied_colleges',
        views.view_applied_colleges,
        name='view_applied_colleges'
    ),

    path(
        'apply_job/<int:job_id>',
        views.apply_job,
        name='apply_job'
    ),

    path(
        'view_applied_jobs',
        views.view_applied_jobs,
        name='view_applied_jobs'
    ),

    path(
        'view_all_courses',
        views.view_all_courses,
        name='view_all_courses'
    ),

    # COLLEGE
    path('clgreg', views.clgreg),
    path('clgpg', views.clgpg),

    path(
        'addcourse',
        views.addcourse,
        name='addcourse'
    ),

    path(
        'clgview',
        views.clgview,
        name='clgview'
    ),

    path(
        'course_view',
        views.course_view,
        name='course_view'
    ),

    path(
        'update',
        views.update
    ),

    path(
        'addMentor',
        views.addMentor,
        name='addMentor'
    ),

    path(
        'delCourse',
        views.delCourse
    ),

    path(
        'InterviewNotes',
        views.InterviewNotes
    ),

    path(
        'download_interviewnotes',
        views.download_interviewnotes
    ),

    path(
        'collegeUpdate',
        views.collegeUpdate
    ),

    path(
        'std_results',
        views.std_results
    ),

    path(
        'viewMentors',
        views.viewMentors,
        name='viewMentors'
    ),

    path(
        'editMentor/<int:id>',
        views.editMentor,
        name='editMentor'
    ),

    path(
        'deleteMentor/<int:id>',
        views.deleteMentor,
        name='deleteMentor'
    ),

    path(
        'view_applications_college',
        views.view_applications_college,
        name='view_applications_college'
    ),

    path(
        'update_application_status/<int:app_id>/<str:status>',
        views.update_application_status,
        name='update_application_status'
    ),

    # MENTOR
    path(
        'mentorpg',
        views.mentorpg
    ),

    path(
        'view_Course',
        views.view_Course
    ),

    path(
        'InterviewPrepare',
        views.InterviewPrepare
    ),

    path(
        'reply',
        views.reply
    ),

    #  CHAT
    path(
        'chat/',
        views.chat,
        name='chat'
    ),

    #  OTHER 
    path(
        'dell/',
        views.dell
    ),
]