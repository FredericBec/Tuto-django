from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from polls.form import PollForm, LearnerRegisterForm, CourseQuestionForm
from polls.models import Course, Teacher


@pytest.fixture
def course():
    """
    fixture de l'objet course permettant sa réusabilité
    :return: l'objet course
    """
    user = User.objects.create(username='prof', password='profmdp')
    teacher = Teacher.objects.create(user=user, hiring_date=datetime(2000, 9, 1))
    course = Course.objects.create(name='maths', start_date=datetime(2000, 9, 1), end_date=datetime(2001, 6, 20),
                                   teacher=teacher)
    return course


def test_poll_form_valid():
    poll_form = {
        'question_text': 'Quelle est votre ville préférée?',
        'pub_date': timezone.now()
    }

    form = PollForm(data=poll_form)

    assert form.is_valid()


@pytest.mark.django_db
def test_learner_form_valid(course):
    leaner_form = {
        'username': 'gigi24',
        'email': 'gigi24@gmail.com',
        'password1': 'test2025',
        'password2': 'test2025',
        'address': '5 rue des fleurs toulouse',
        'course': [course.id]
    }

    form = LearnerRegisterForm(leaner_form)

    assert form.is_valid()


@pytest.mark.django_db
def test_question_with_course_form_valid(course):
    question_form = {
        'question_text': 'Quelle est votre ville préférée ?',
        'course': course
    }

    form = CourseQuestionForm(question_form)

    assert form.is_valid()
