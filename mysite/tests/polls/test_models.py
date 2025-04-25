from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import make_aware

from polls import models
from polls.models import Learner, Teacher, Course, Question, Choice


@pytest.fixture
def user():
    user = User.objects.create(username='test', password='test2025')
    return user


@pytest.mark.django_db
def test_learner(user):
    learner = Learner.objects.create(user=user, address="5 rue des templiers 31000 Toulouse")

    assert learner.user.username == "test"
    assert learner.address == "5 rue des templiers 31000 Toulouse"


@pytest.mark.django_db
def test_teacher_str(user):
    teacher = Teacher.objects.create(user=user, hiring_date=make_aware(datetime(2000, 7, 2)))

    assert str(teacher) == "test"


@pytest.mark.django_db
def test_course_str(user):
    teacher = Teacher.objects.create(user=user, hiring_date=make_aware(datetime(2000, 7, 2)))
    leaner = Learner.objects.create(user=user, address="10 rue des fleurs toulouse")
    course = Course.objects.create(name="maths", start_date=make_aware(datetime(2000, 9, 3)),
                                   end_date=make_aware(datetime(2001, 6, 20)), teacher=teacher)
    course.learners.add(leaner)

    assert str(course) == "maths"


@pytest.mark.django_db
def test_question(user):
    teacher = Teacher.objects.create(user=user, hiring_date=make_aware(datetime(2000, 7, 2)))
    course = Course.objects.create(name="maths", start_date=make_aware(datetime(2000, 9, 3)),
                                   end_date=make_aware(datetime(2001, 6, 20)), teacher=teacher)
    question = Question(question_text="Quel est votre catcheur favori ?",
                        pub_date=make_aware(datetime(2025, 2, 24)), course=course)

    expected_age = timezone.now() - question.pub_date

    assert str(question) == f"{question.pub_date} - {models.text_excerpt(question.question_text, 20)}"
    assert abs(question.age().days - expected_age.days) < 1


@pytest.mark.django_db
def test_choice():
    question = Question.objects.create(question_text="Quel est votre catcheur favori ?",
                                       pub_date=make_aware(datetime(2025, 2, 24)))
    choice = Choice.objects.create(question=question, choice_text="John Cena", votes=2)

    assert str(choice) == "John Cena"
