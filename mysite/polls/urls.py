from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all/", views.AllView.as_view(), name="all"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path("statistics/", views.statistics, name="statistics"),
    path("add/", views.get_question, name="add"),
    path("account/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("courses/", views.CourseView.as_view(), name="courses"),
    path("course_register/", views.LearnerRegister, name="course_register"),
    path("add-course-question/", views.add_course_question, name="add_course_question")
]
