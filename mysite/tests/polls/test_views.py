from datetime import datetime

import pytest
from django.contrib.auth.models import User

from django.test import Client
from django.urls import reverse
from django.utils.timezone import make_aware
from pytest_django.asserts import assertTemplateUsed

from polls.models import Question, Choice, Teacher, Course


@pytest.fixture
def client():
    """
    fixture de l'objet fourni par django test pour simuler un utilisateur
    :return: client instancié
    """
    client = Client()
    return client


@pytest.fixture
def credentials():
    """
    fixture fournissant des paramètres d'enregistrement
    :return: credentials
    """
    credentials = {
        'username': 'test',
        'email': 'user@gmail.com',
        'password1': 'user1234',
        'password2': 'user1234',
        'address': '5 rue des chalets Toulouse',
        'course': 'maths',
        'teacher': 'teacher'
    }
    return credentials


@pytest.fixture
def login_user(client, credentials):
    """
    fixture pour simuler l'enregistrement et la connexion d'un utilisateur
    :param client: fixture client
    :param credentials: fixture credentials
    :return: l'utilisateur enregistré
    """
    temp_user = client.post('/user/signup/', credentials)
    client.post('/user/login/', {'username': 'test', 'password': 'user1234'})
    return temp_user


def test_index_view(client):
    response = client.get(reverse('polls:index'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'polls/index.html')


@pytest.mark.django_db
def test_all_view(client):
    response = client.get(reverse('polls:all'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'polls/all.html')


@pytest.mark.django_db
def test_detail_view(client):
    Question.objects.create(question_text="Quel est votre couleur favorite?",
                            pub_date=make_aware(datetime(2025, 2, 12)))
    path = reverse('polls:detail', kwargs={'pk': 1})
    response = client.get(path)

    assert response.status_code == 200
    assertTemplateUsed(response, 'polls/detail.html')


@pytest.mark.django_db
def test_result_view(client):
    Question.objects.create(question_text="Quel est votre couleur favorite?",
                            pub_date=make_aware(datetime(2025, 2, 12)))
    path = reverse('polls:results', kwargs={'pk': 1})
    response = client.get(path)

    assert response.status_code == 200
    assertTemplateUsed(response, 'polls/results.html')


@pytest.mark.django_db
def test_frequency_view(client):
    Question.objects.create(question_text="Quel est votre couleur favorite?",
                            pub_date=make_aware(datetime(2025, 2, 12)))
    path = reverse('polls:frequency', kwargs={'pk': 1})
    response = client.get(path)

    assert response.status_code == 200
    assertTemplateUsed(response, 'polls/frequency.html')


@pytest.mark.django_db
def test_course_view(client, login_user):
    response = client.get(reverse('polls:courses'))

    assert response.status_code == 302


@pytest.mark.django_db
def test_vote(client):
    question = Question.objects.create(question_text="Quel est votre prochain voyage ?",
                                       pub_date=make_aware(datetime(2025, 3, 17)))
    second_choice = Choice.objects.create(choice_text="Japon", votes=3, question=question)

    response = client.post(reverse('polls:vote', args=[question.id]), {'choice': second_choice.id})

    second_choice.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse('polls:results', args=[question.id])
    assert second_choice.votes == 4


@pytest.mark.django_db
def test_get_question_when_user_not_logged(client):
    response = client.get(reverse('polls:add'))

    assert response.status_code == 302
    assert response.url == reverse('polls:login')


@pytest.mark.django_db
def test_get_question_when_teacher_logged(client):
    user = User.objects.create_user(username='teacher1', password='testprof')
    Teacher.objects.create(user=user, hiring_date=make_aware(datetime(2005, 9, 20)))

    client.login(username='teacher1', password='testprof')

    data = {
        'question_text': "Quel est votre couleur préférée ?",
        'choice_text[]': ['bleu', 'vert', 'jaune']
    }
    response = client.post(reverse('polls:add'), data)

    assert response.status_code == 302
    assert response.url == reverse('polls:all')

    question = Question.objects.get(question_text="Quel est votre couleur préférée ?")
    choices = question.choice_set.all()

    assert choices.count() == 3
    assert set(choice.choice_text for choice in choices) == {'bleu', 'vert', 'jaune'}


@pytest.mark.django_db
def test_add_new_question_with_course(client):
    user = User.objects.create_user(username='teacher1', password='testprof')
    teacher = Teacher.objects.create(user=user, hiring_date=make_aware(datetime(2005, 9, 20)))

    client.login(username='teacher1', password='testprof')

    course = Course.objects.create(name="Géographie", start_date=make_aware(datetime(2006, 9, 5)),
                                   end_date=make_aware(datetime(2007, 6, 30)), teacher=teacher)

    data = {
        'question_text': 'Quel est la capitale la plus visitée ?',
        'choice_text[]': ['Paris', 'New York', 'Tokyo', 'Rio de Janeiro'],
        'course': course.id
    }

    response = client.post(reverse('polls:add_course_question'), data)

    assert response.status_code == 302
    assert response.url == reverse('polls:courses')

    question = Question.objects.get(question_text="Quel est la capitale la plus visitée ?")
    choices = question.choice_set.all()

    assert choices.count() == 4
    assert set(choice.choice_text for choice in choices) == {'Paris', 'New York', 'Tokyo', 'Rio de Janeiro'}
    assert question.course == course
